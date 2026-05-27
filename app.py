#!/usr/bin/env python3
"""Claude Usage Monitor - macOS menu bar app."""

import json
import os
import stat
import subprocess
import threading
import time

import requests
import rumps

CONFIG_PATH = os.path.expanduser("~/.claude_monitor.json")
DEFAULT_CONFIG = {
    "interval_minutes": 30,
    "cookie": "",
}

BASE_URL = "https://claude.ai"
LIMITS_PAGE = f"{BASE_URL}/settings/limits"
BOOTSTRAP_URL = f"{BASE_URL}/api/bootstrap"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": LIMITS_PAGE,
}


def load_config():
    if not os.path.exists(CONFIG_PATH):
        return DEFAULT_CONFIG.copy()
    with open(CONFIG_PATH) as f:
        data = json.load(f)
    return {**DEFAULT_CONFIG, **data}


def save_config(config):
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2)
    os.chmod(CONFIG_PATH, stat.S_IRUSR | stat.S_IWUSR)  # 600


def _cookie_header(raw: str) -> str:
    """Ensure cookie has the sessionKey= prefix."""
    raw = raw.strip()
    if raw.startswith("sessionKey=") or "=" in raw.split(";")[0]:
        return raw
    return f"sessionKey={raw}"


def fetch_org_uuid(cookie_header: str) -> str | None:
    """Fetch org UUID from /api/bootstrap. Returns None on failure."""
    try:
        r = requests.get(
            BOOTSTRAP_URL,
            headers={**HEADERS, "Cookie": cookie_header},
            timeout=15,
        )
        r.raise_for_status()
        data = r.json()
        memberships = (data.get("account") or {}).get("memberships") or []
        if memberships:
            return memberships[0]["organization"]["uuid"]
    except Exception:
        pass
    return None


def fetch_usage(cookie: str) -> tuple[str, str] | None:
    """Return (five_hour_pct, seven_day_pct) strings, or None on failure."""
    if not cookie:
        return None
    cookie_header = _cookie_header(cookie)
    try:
        org_uuid = fetch_org_uuid(cookie_header)
        if not org_uuid:
            return None

        usage_url = f"{BASE_URL}/api/organizations/{org_uuid}/usage"
        r = requests.get(
            usage_url,
            headers={**HEADERS, "Cookie": cookie_header},
            timeout=15,
        )
        r.raise_for_status()
        data = r.json()

        five_h = (data.get("five_hour") or {}).get("utilization")
        seven_d = (data.get("seven_day") or {}).get("utilization")

        five_str = f"{five_h:.0f}%" if five_h is not None else "?%"
        seven_str = f"{seven_d:.0f}%" if seven_d is not None else "?%"
        return five_str, seven_str
    except requests.exceptions.RequestException:
        return None


class ClaudeMonitorApp(rumps.App):
    def __init__(self):
        super().__init__("Claude", title="Claude …")
        self.config = load_config()
        self._timer_thread = None
        self._stop_event = threading.Event()
        self._last_seven_day = "?%"

        self._interval_item = rumps.MenuItem(
            f"Interval: {self.config['interval_minutes']} min",
            callback=self.set_interval,
        )
        self._seven_day_item = rumps.MenuItem("7-day: …")
        self._seven_day_item.set_callback(None)  # display-only

        self.menu = [
            rumps.MenuItem("Refresh now", callback=self.manual_refresh),
            None,
            self._seven_day_item,
            None,
            self._interval_item,
            rumps.MenuItem("Update Cookie…", callback=self.update_cookie),
            None,
            rumps.MenuItem("Open claude.ai/settings/limits", callback=self.open_limits),
        ]

        self._start_timer()
        threading.Thread(target=self._fetch_and_update, daemon=True).start()

    # ------------------------------------------------------------------ #
    #  Timer                                                               #
    # ------------------------------------------------------------------ #

    def _start_timer(self):
        self._stop_event.clear()
        self._timer_thread = threading.Thread(target=self._timer_loop, daemon=True)
        self._timer_thread.start()

    def _restart_timer(self):
        self._stop_event.set()
        self._start_timer()

    def _timer_loop(self):
        interval = self.config["interval_minutes"] * 60
        elapsed = 0
        while not self._stop_event.is_set():
            time.sleep(1)
            elapsed += 1
            if elapsed >= interval:
                elapsed = 0
                self._fetch_and_update()

    # ------------------------------------------------------------------ #
    #  Core fetch                                                          #
    # ------------------------------------------------------------------ #

    def _fetch_and_update(self):
        self.title = "Claude …"
        result = fetch_usage(self.config["cookie"])
        if result is None:
            self.title = "Claude !"
            self._seven_day_item.title = "7-day: —"
            rumps.notification(
                "Claude Monitor",
                "Fetch failed",
                "Check your cookie or network connection.",
                sound=False,
            )
        else:
            five_h, seven_d = result
            self.title = f"Claude {five_h}"            # 5-hour window in menu bar
            self._seven_day_item.title = f"7-day: {seven_d}"

    # ------------------------------------------------------------------ #
    #  Menu callbacks                                                      #
    # ------------------------------------------------------------------ #

    def manual_refresh(self, _):
        threading.Thread(target=self._fetch_and_update, daemon=True).start()

    def set_interval(self, _):
        response = rumps.Window(
            message="Enter refresh interval in minutes:",
            title="Set Interval",
            default_text=str(self.config["interval_minutes"]),
            ok="Save",
            cancel="Cancel",
            dimensions=(200, 24),
        ).run()
        if response.clicked and response.text.strip().isdigit():
            minutes = max(1, int(response.text.strip()))
            self.config["interval_minutes"] = minutes
            save_config(self.config)
            self._interval_item.title = f"Interval: {minutes} min"
            self._restart_timer()

    def update_cookie(self, _):
        response = rumps.Window(
            message=(
                "Paste your claude.ai sessionKey cookie value below.\n"
                "(DevTools → Application → Cookies → sessionKey → Value)"
            ),
            title="Update Cookie",
            default_text=self.config.get("cookie", ""),
            ok="Save",
            cancel="Cancel",
            dimensions=(400, 60),
        ).run()
        if response.clicked and response.text.strip():
            self.config["cookie"] = response.text.strip()
            save_config(self.config)
            threading.Thread(target=self._fetch_and_update, daemon=True).start()

    def open_limits(self, _):
        subprocess.call(["open", LIMITS_PAGE])


if __name__ == "__main__":
    ClaudeMonitorApp().run()
