# Claude Usage Monitor

**Language / 語言：** English | [繁體中文](README.zh-TW.md)

A lightweight macOS menu bar app that shows your [claude.ai](https://claude.ai) session usage percentage in real time — without needing to open a browser.

![Menu bar screenshot showing "Claude 73%"](https://placehold.co/300x40/1a1a1a/ffffff?text=Claude+73%25)

## Features

- Sits in the macOS menu bar and displays current usage (5-hour window)
- Shows 7-day cumulative usage in the dropdown
- Auto-refreshes every N minutes (configurable, default 30 min)
- Manual refresh on demand
- Cookie and settings stored locally at `~/.claude_monitor.json` (permissions: 600)

---

## Security Notice

- **Your `sessionKey` cookie is equivalent to your password.** Never share it with anyone.
- This tool stores the cookie locally at `~/.claude_monitor.json` (mode 600) and sends it only to `claude.ai`. No third-party servers are involved.
- If you suspect your cookie has been compromised, go to claude.ai → Account Settings → Sign out all devices.
- This is an unofficial open-source tool. It is not affiliated with or endorsed by Anthropic.

## Requirements

| | |
|---|---|
| macOS | 12 Monterey or later |
| Python | 3.10+ (`python3 --version` to check) |
| pip | bundled with Python |

---

## Quick Install

```bash
# 1. Clone
git clone https://github.com/YOUR_USERNAME/claude-usage-monitor.git
cd claude-usage-monitor

# 2. Install dependencies
pip3 install rumps requests
# If you get an "externally managed environment" error (Python 3.11+):
pip3 install rumps requests --break-system-packages

# 3. Launch
python3 app.py
```

The menu bar will show **Claude …** while loading.

---

## First-Time Cookie Setup

Claude's usage API requires a valid session cookie. Here's how to copy it from Chrome:

### Step 1 — Log in to claude.ai

Open [https://claude.ai](https://claude.ai) in Chrome and make sure you're logged in.

### Step 2 — Open DevTools

Press `F12` or `⌘ Option I`.

### Step 3 — Copy the cookie (two options)

**Option A — Copy just the sessionKey value (recommended)**

1. Go to the **Application** tab
2. In the left sidebar: **Cookies → https://claude.ai**
3. Find the row named `sessionKey`
4. Double-click the **Value** column → `⌘A` → `⌘C`

**Option B — Copy the full cookie header (easier for beginners)**

1. Go to the **Network** tab
2. Navigate to [https://claude.ai/settings/limits](https://claude.ai/settings/limits)
3. Click the `limits` request in the list → **Headers** tab
4. Under **Request Headers**, right-click the `cookie:` line → **Copy value**

### Step 4 — Paste into the app

In the menu bar, click **Claude …** → **Update Cookie…** → paste → **Save**.

The display will update within a few seconds.

> **Note:** The cookie is stored only on your machine at `~/.claude_monitor.json` (mode 600). It is never sent anywhere except back to `claude.ai`.

---

## Menu Bar Indicators

| Display | Meaning |
|---------|---------|
| `Claude …` | Fetching data |
| `Claude 62%` | 5-hour window is 62% used (example) |
| `Claude !` | Network error or expired cookie |

The dropdown also shows **7-day: X%** (rolling 7-day usage).

---

## Menu Options

| Item | Action |
|------|--------|
| **Refresh now** | Fetch immediately |
| **7-day: X%** | Info display (not clickable) |
| **Interval: N min** | Click to change refresh interval |
| **Update Cookie…** | Paste a new session cookie |
| **Open claude.ai/settings/limits** | Open the limits page in browser |

---

## Auto-start on Login (optional)

```bash
# Replace YOUR_USERNAME with your macOS username (run: whoami)
mkdir -p ~/Library/LaunchAgents

cat > ~/Library/LaunchAgents/com.user.claude-monitor.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>com.user.claude-monitor</string>
  <key>ProgramArguments</key>
  <array>
    <string>/opt/homebrew/bin/python3</string>
    <string>/Users/YOUR_USERNAME/claude-usage-monitor/app.py</string>
  </array>
  <key>RunAtLoad</key>
  <true/>
  <key>KeepAlive</key>
  <true/>
</dict>
</plist>
EOF

launchctl load ~/Library/LaunchAgents/com.user.claude-monitor.plist
```

---

## Cookie Expiry

Session cookies typically last several weeks. If the menu bar shows **Claude !**:

1. Go back to [Step 3](#step-3--copy-the-cookie-two-options) above
2. Copy a fresh cookie from Chrome
3. Use **Update Cookie…** in the app

---

## How It Works

The app calls two internal claude.ai JSON endpoints:

1. `/api/bootstrap` — to get your organization UUID (no personal data is stored)
2. `/api/organizations/{uuid}/usage` — returns `five_hour.utilization` and `seven_day.utilization`

No scraping, no Selenium, no browser automation.

---

## License

MIT
