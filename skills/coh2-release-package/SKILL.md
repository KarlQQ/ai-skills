---
name: coh2-release-package
description: >-
  Run the coh2 release packaging workflow: update production branch, rebase
  the issue branch onto production, force-push, then collect changed files
  with rsync and package them into a zip with a diff list. Use when the user
  mentions 包版, 出版, 打包版本, release packaging, or asks to package an
  issue branch (e.g. issue/7510) for delivery.
---

# coh2 出版包版流程

輸入：要包版的 branch（例如 `issue/7510`）。以下以 `{N}` 代表 issue 編號（`7510`）、`{BRANCH}` 代表完整 branch 名（`issue/7510`）。

開始前先和使用者確認 `{BRANCH}`，並用 `git status` 確認工作區乾淨（有未 commit 的變更先停下來詢問）。

## Step 1：更新 production

```bash
git checkout production
git pull
```

**注意**：`git pull` 會遇到 Ericsson 的認證，需要使用者人工介入。執行時放背景並提醒使用者完成認證，等 pull 成功後再繼續；若長時間卡住，通知使用者處理認證，不要自行中斷重試。

## Step 2：rebase 並更新 remote

```bash
git checkout {BRANCH}
git rebase production
git push -u origin {BRANCH} --force
```

- rebase 發生衝突時**立即停止**，列出衝突檔案請使用者決定如何處理，不要自行解衝突或 `--abort`。
- force push 是此流程的既定作法（rebase 後必須），但僅限 `issue/*` branch，**絕不可對 production 執行**。

## Step 3：包版

在 repo 根目錄執行：

```bash
mkdir {N}
rsync -R $(git diff --name-only production --diff-filter=d) {N}
git diff --name-status production > "{N}_diff.txt"
zip -r {N}.zip {N}
```

- `--diff-filter=d` 排除「已刪除」的檔案（已不存在於工作區，rsync 會報錯）；若 `{N}_diff.txt` 中有 `D` 開頭的項目，在總結時特別提醒使用者該版本包含刪檔。
- `{N}/`、`{N}.zip`、`{N}_diff.txt` 是包版產物，**不要 commit 進 repo**。
- 若 `{N}` 目錄或 zip 已存在（重新包版），先刪除舊的再重做。

## 完成後回報

- 異動檔案數（依 `{N}_diff.txt` 統計 A/M/D 各幾筆）
- zip 檔絕對路徑
- 是否有刪除檔案需特別注意
- **本次修改內容總結**：閱讀 `git log production..{BRANCH} --oneline` 的 commit 訊息與 `git diff production` 的實際變更，用條列說明此版本「改了什麼、為什麼改」（以功能行為描述，不要逐行翻譯程式碼），讓使用者可直接取用於版本說明或通知信
