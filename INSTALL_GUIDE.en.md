# Step-by-Step Installation Guide — Claude Usage Monitor

**Language / 語言：** English | [繁體中文](INSTALL_GUIDE.md)

> No programming knowledge required. Just follow each step.

---

## ⚠️ Security Notice — Please Read First

Before using this tool, make sure you understand the following:

1. **Your Cookie is equivalent to your password.**
   The `sessionKey` cookie you copy fully identifies your Claude account. Anyone who obtains this string can log in as you. Never share it via messages, email, screenshots, or with anyone claiming to be technical support.

2. **Only download from the official source.**
   Make sure you are installing from `https://github.com/Shishimaruko/claude-usage-monitor`. Modified versions from other sources may contain malicious code designed to steal your cookie.

3. **This tool does not upload your data.**
   Your cookie is stored only on your computer at `~/.claude_monitor.json`. The app only sends requests to `claude.ai`. You can read `app.py` yourself to verify, or ask a developer friend to review it.

4. **If you suspect a leak, act immediately.**
   Go to [claude.ai](https://claude.ai) → Account Settings → Sign out of all devices. This immediately invalidates the cookie.

5. **This tool is not affiliated with Anthropic.**
   This is an unofficial, open-source personal project. Anthropic provides no support or warranty.

---

## What Does This Do?

After installation, your Mac's menu bar will always show your Claude usage — for example, **Claude 45%** — without needing to open a browser.

**It does not consume your Claude quota.** It only reads a number that claude.ai has already calculated.

---

## Step 1 — Install Homebrew

Open **Terminal** (press `⌘ Space`, type "Terminal", press Enter).

Paste the following line and press Enter. Follow any on-screen prompts (press Enter or type your Mac password when asked):

```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

> If the installer tells you to run two lines starting with `echo` and `eval` at the end, run those too.

---

## Step 2 — Install Python

In Terminal, paste:

```
brew install python
```

---

## Step 3 — Download This Tool

```
git clone https://github.com/Shishimaruko/claude-usage-monitor.git
cd claude-usage-monitor
pip3 install rumps requests --break-system-packages
```

---

## Step 4 — Get Your Claude Cookie

The cookie lets the tool verify your account identity. It is stored only on your own computer.

1. Open **Chrome** and log in to [claude.ai](https://claude.ai)

2. Press `F12` to open DevTools (on Mac: `⌘ Option I`)

3. Click the **Application** tab at the top of DevTools

4. In the left sidebar, expand **Cookies → https://claude.ai**

5. Find the row named `sessionKey`, then double-click the **Value** column

6. Select all (`⌘A`) and copy (`⌘C`)

---

## Step 5 — Launch and Paste Your Cookie

In Terminal, type:

```
python3 app.py
```

Once you see **Claude …** appear in the top-right menu bar:

1. Click on it
2. Select **Update Cookie…**
3. Paste your copied cookie (`⌘V`)
4. Click **Save**

Within a few seconds you'll see something like **Claude 45%**.

---

## Launching the App in the Future

Open Terminal and paste:

```
cd claude-usage-monitor && python3 app.py
```

---

## Troubleshooting

**Claude ! appears in the menu bar**
→ Your cookie has expired. Repeat Step 4 to copy a fresh one, then update it via **Update Cookie…**

**Nothing appears in the menu bar**
→ Your macOS menu bar may be too full. Try hiding or removing other menu bar icons to make room.

**Is this safe to use?**
→ Your cookie is stored only on your machine (`~/.claude_monitor.json`) and is never sent anywhere other than `claude.ai`. The behavior is identical to you opening a browser tab to check your account.

---

## Auto-Start on Login (Optional)

Run the following in Terminal. Replace `YOUR_USERNAME` with the result of running `whoami`:

```bash
mkdir -p ~/Library/LaunchAgents
cat > ~/Library/LaunchAgents/com.user.claude-monitor.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>com.user.claude-monitor</string>
  <key>ProgramArguments</key>
  <array>
    <string>/opt/homebrew/bin/python3</string>
    <string>/Users/YOUR_USERNAME/claude-usage-monitor/app.py</string>
  </array>
  <key>RunAtLoad</key><true/>
  <key>KeepAlive</key><true/>
</dict>
</plist>
EOF
launchctl load ~/Library/LaunchAgents/com.user.claude-monitor.plist
```
