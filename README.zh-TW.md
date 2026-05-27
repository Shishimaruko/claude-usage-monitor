# Claude 用量顯示器

**Language / 語言：** [English](README.md) | 繁體中文

在 macOS 右上角即時顯示你的 [claude.ai](https://claude.ai) session 使用量，不用開瀏覽器查。

![Menu bar 顯示 "Claude 73%"](https://placehold.co/300x40/1a1a1a/ffffff?text=Claude+73%25)

## 功能

- 常駐 macOS menu bar，顯示目前用量（5 小時視窗）
- 下拉選單另外顯示 7 天累積用量
- 每隔 N 分鐘自動刷新（可設定，預設 30 分鐘）
- 支援手動立即刷新
- Cookie 與設定儲存在本機 `~/.claude_monitor.json`（權限 600）
- **不消耗 Claude 算力**，只是讀取伺服器上已計算好的數字

---

## ⚠️ 資安警語

- **`sessionKey` Cookie 等同你的帳號密碼。** 請勿傳給任何人。
- 本工具將 Cookie 儲存在本機 `~/.claude_monitor.json`（權限 600），只會向 `claude.ai` 發送請求，不經過任何第三方伺服器。
- 若懷疑 Cookie 外洩，請至 claude.ai → 帳號設定 → 登出所有裝置。
- 本工具為非官方開源專案，與 Anthropic 無關，Anthropic 不提供任何支援或擔保。

---

## 系統需求

| | |
|---|---|
| macOS | 12 Monterey 或更新版本 |
| Python | 3.10+（執行 `python3 --version` 確認）|
| pip | Python 內建附帶 |

---

## 快速安裝

```bash
# 1. 下載
git clone https://github.com/Shishimaruko/claude-usage-monitor.git
cd claude-usage-monitor

# 2. 安裝依賴套件
pip3 install rumps requests
# 如果出現 "externally managed environment" 錯誤（Python 3.11+）：
pip3 install rumps requests --break-system-packages

# 3. 啟動
python3 app.py
```

載入中會顯示 **Claude …**，設定完 Cookie 後即更新為實際數字。

> 不熟悉指令列操作？請參閱 [傻瓜安裝教學](INSTALL_GUIDE.md)。

---

## 第一次設定 Cookie

Claude 的用量 API 需要登入後的 session cookie。以下是從 Chrome 複製的方式：

### 步驟一：登入 claude.ai

用 Chrome 開啟 [https://claude.ai](https://claude.ai) 並確認已登入。

### 步驟二：開啟 DevTools

按 `F12` 或 `⌘ Option I`。

### 步驟三：複製 Cookie（二選一）

**方法 A — 只複製 sessionKey 值（推薦）**

1. 點上方 **Application** 分頁
2. 左側展開 **Cookies → https://claude.ai**
3. 找到名稱為 `sessionKey` 的列
4. 雙擊 **Value** 欄位 → `⌘A` → `⌘C`

**方法 B — 複製完整 cookie 標頭（新手較簡單）**

1. 點上方 **Network** 分頁
2. 前往 [https://claude.ai/settings/limits](https://claude.ai/settings/limits)
3. 點清單中的 `limits` 請求 → **Headers** 分頁
4. 在 **Request Headers** 裡，右鍵 `cookie:` 那行 → **Copy value**

### 步驟四：貼到 app

點 menu bar 的 **Claude …** → **Update Cookie…** → 貼上 → **Save**。

幾秒後數字即更新。

> Cookie 只存在你的電腦，不會傳到其他地方。

---

## Menu bar 顯示說明

| 顯示 | 意思 |
|------|------|
| `Claude …` | 抓取中 |
| `Claude 62%` | 5 小時視窗已用 62%（範例數字）|
| `Claude !` | 網路錯誤或 Cookie 過期 |

下拉選單另顯示 **7-day: X%**（7 天滾動用量）。

---

## 選單功能

| 項目 | 功能 |
|------|------|
| **Refresh now** | 立即抓取 |
| **7-day: X%** | 資訊顯示（不可點擊）|
| **Interval: N min** | 點擊後可更改刷新間隔 |
| **Update Cookie…** | 更新 session cookie |
| **Open claude.ai/settings/limits** | 在瀏覽器開啟用量頁面 |

---

## 開機自動啟動（選用）

```bash
# 將 YOUR_USERNAME 換成你的 macOS 帳號名稱（執行 whoami 可查）
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

## Cookie 過期處理

Session cookie 通常有效數週。若 menu bar 顯示 **Claude !**：

1. 重複步驟三，從 Chrome 複製新的 Cookie
2. 用 **Update Cookie…** 更新

---

## 運作原理

本工具呼叫兩個 claude.ai 內部 JSON API：

1. `/api/bootstrap` — 取得你的 organization UUID（不儲存個人資料）
2. `/api/organizations/{uuid}/usage` — 回傳 `five_hour.utilization` 與 `seven_day.utilization`

無 HTML 爬蟲，無 Selenium，無瀏覽器自動化。

---

## 授權

MIT
