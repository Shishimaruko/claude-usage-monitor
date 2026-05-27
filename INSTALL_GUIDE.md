# 傻瓜安裝教學 — Claude 用量顯示器

> 完全不需要懂程式。跟著步驟做就好。

---

## ⚠️ 資安警語（請先閱讀）

使用本工具前，請確認你了解以下幾點：

1. **Cookie 等同密碼**
   你複製的 `sessionKey` Cookie 可以完整代表你的 Claude 帳號身份。任何拿到這串文字的人都能以你的身份登入。請勿透過 LINE、Email、截圖等方式傳給任何人，包含聲稱是技術支援的人員。

2. **只從官方來源下載**
   請確認你安裝的是來自 `https://github.com/Shishimaruko/claude-usage-monitor` 的版本。從其他來源下載的「修改版」可能暗藏竊取 Cookie 的惡意程式碼。

3. **本工具不會上傳你的資料**
   Cookie 只儲存在你的電腦 `~/.claude_monitor.json`，程式只會對 `claude.ai` 發送請求。你可以自行閱讀 `app.py` 的原始碼確認，或請懂程式的朋友協助審查。

4. **懷疑外洩時立即處理**
   如果你不確定 Cookie 是否已洩漏，請登入 [claude.ai](https://claude.ai) → 帳號設定 → 登出所有裝置，Cookie 會立即失效。

5. **此工具與 Anthropic 官方無關**
   這是非官方的個人開源工具，Anthropic 不提供任何支援或擔保。

---

## 這是什麼？

裝好之後，你的 Mac 右上角會一直顯示你的 Claude 用量，例如 **Claude 45%**，不用一直開瀏覽器查。

不會消耗你的 Claude 用量，只是讀取數字而已。

---

## 第一步：安裝 Homebrew（電腦的套件管理工具）

打開 **Terminal**（按 `⌘ 空白鍵` 搜尋「Terminal」）

貼上以下這行，按 Enter，然後一路按 Enter / 輸入電腦密碼：

```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

> 裝完後如果畫面提示你執行兩行 `echo` 和 `eval` 的指令，照做。

---

## 第二步：安裝 Python

在 Terminal 貼上：

```
brew install python
```

---

## 第三步：下載這個工具

```
git clone https://github.com/Shishimaruko/claude-usage-monitor.git
cd claude-usage-monitor
pip3 install rumps requests --break-system-packages
```

---

## 第四步：取得你的 Claude Cookie

Cookie 是讓工具確認「這是我的帳號」的通行證，只存在你自己的電腦上。

1. 打開 **Chrome**，登入 [claude.ai](https://claude.ai)

2. 按鍵盤 `F12`（沒有 F12 的 Mac 按 `⌘ Option I`）

3. 點上方的 **Application** 分頁

   ![DevTools Application tab](https://placehold.co/500x30/f0f0f0/333?text=Application+分頁在+DevTools+上方)

4. 左側展開 **Cookies → https://claude.ai**

5. 找到名稱是 `sessionKey` 的那一列，雙擊右邊的 **Value** 欄位

6. 全選（`⌘A`）→ 複製（`⌘C`）

---

## 第五步：啟動工具並貼上 Cookie

在 Terminal 輸入：

```
python3 app.py
```

右上角出現 **Claude …** 後：

1. 點一下它
2. 選 **Update Cookie…**
3. 貼上剛才複製的內容（`⌘V`）
4. 按 **Save**

幾秒後就會顯示 **Claude 45%** 這樣的數字。

---

## 之後每次要啟動

打開 Terminal，貼上：

```
cd claude-usage-monitor && python3 app.py
```

---

## 常見問題

**Q：顯示 Claude !**
→ Cookie 過期了。重複「第四步」複製新的 Cookie，再用 **Update Cookie…** 更新。

**Q：完全沒出現在右上角**
→ macOS 右上角可能太滿，試著把其他圖示縮小或移除。

**Q：會不會有資安問題？**
→ Cookie 只存在你的電腦（`~/.claude_monitor.json`），不會上傳到任何地方。工具只對 claude.ai 發送請求，行為跟你打開瀏覽器查帳號一樣。

---

## 讓它開機自動啟動（選用）

在 Terminal 貼上（把 `你的帳號名稱` 換成 `whoami` 指令的結果）：

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
    <string>/Users/你的帳號名稱/claude-usage-monitor/app.py</string>
  </array>
  <key>RunAtLoad</key><true/>
  <key>KeepAlive</key><true/>
</dict>
</plist>
EOF
launchctl load ~/Library/LaunchAgents/com.user.claude-monitor.plist
```
