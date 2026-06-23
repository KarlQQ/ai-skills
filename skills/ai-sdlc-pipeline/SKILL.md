---
name: ai-sdlc-pipeline
description: >-
  啟動一個全自動化「AI Agent 軟體開發生產線」專案：一個命令就建好從需求到部署的完整目錄結構、
  治理框架、10 個 Agent 角色定義（PM / BA / SA / 架構 ARCH / UX-UI / 前端 FE / 後端 BE /
  QA / DevOps / Reviewer）、文件編號規則與需求追溯矩陣。當使用者要「開新案子 / 啟動新專案 /
  建專案骨架 / 設定 agent 開發團隊 / 建立需求到部署的一條龍流程 / 軟體開發生產線」,或提到
  SDLC pipeline、專案啟動、scaffold、需求訪談到開發的目錄結構時,務必使用本 skill。
  Use this whenever the user wants to bootstrap or scaffold a new software project workspace,
  set up a multi-agent development team, or create a requirements-to-deployment pipeline —
  even if they don't say the exact word "pipeline". 啟動前會先向使用者蒐集專案名稱、概述等變數。
---

# AI SDLC Pipeline — 全自動化 Agent 開發生產線啟動器

這個 skill 用一個啟動腳本,把一個新軟體專案需要的整套結構一次建好：治理框架、10 個 Agent
角色的系統提示、各階段文件範本、文件編號規則、需求追溯矩陣。建完後,人工只要把客戶會議結果
放進 `01-discovery/`,各角色 Agent 就能依序接力,一路做到可部署。

## 核心理念

整條流程只有**一個人工輸入點**：與客戶開會,寫下會議記錄(MOM)與確認過的範圍(SCOPE)。
之後每個階段都是「讀上游文件 → 產出本階段文件 → 更新追溯矩陣 → Reviewer 審查 → 過閘門 → 交棒」。

```
人工：開會 → MOM + SCOPE          ← 唯一人工輸入點
  ▼
BA 需求 → SA 規格 → ARCH 架構 → UX 設計 → FE/BE 開發 → QA 測試 → DevOps 部署
                （PM 全程編排調度 · REV 每個閘門前審查把關）
```

## 啟動步驟

### 步驟 1：蒐集啟動變數

啟動前**必須**先取得這些變數。若使用者尚未提供,先詢問（建議用互動選項或直接列出問清楚）：

| 變數 | 必填 | 說明 |
| --- | --- | --- |
| `--name` | ✅ | 專案名稱（會用於標題與資料夾名） |
| `--overview` | ✅ | 專案概述 / 一句話目標（會作為全專案北極星寫進 PROJECT.md） |
| `--code` | 選填 | 文件 ID 前綴 / 專案代碼,例 `RMR`；預設 `PRJ` |
| `--client` | 選填 | 客戶 / 委託方名稱 |
| `--date` | 選填 | 啟動日期 YYYY-MM-DD；預設今天 |
| `--output-dir` | 選填 | 建立位置；預設當前目錄,Claude.ai 環境建議用 `/mnt/user-data/outputs` |

至少要問到 `name` 與 `overview` 才能啟動。其餘可給合理預設並在啟動後告知使用者可調整。

### 步驟 2：執行啟動腳本

```bash
python3 scripts/bootstrap.py \
  --name "專案名稱" \
  --overview "專案概述" \
  --code "PRJ" \
  --client "客戶名稱" \
  --output-dir "/mnt/user-data/outputs"
```

腳本是自包含的（所有範本與角色定義都在腳本內）,會在 `output-dir` 下建立 `{專案 slug}/`
完整結構並注入變數。若目標資料夾已存在會中止,提醒使用者改名。

### 步驟 3：確認與交付

- 用 `present_files`（若可用）把整包專案夾或其 zip 交給使用者。
- 簡述建好的結構,並指出下一步：**把客戶會議記錄放進 `01-discovery/meeting-records/`,
  確認 `01-discovery/scope/` 的 SCOPE 後,即可在 `00-governance/status/project-status.md`
  把 02 階段 gate 標為 `ready` 啟動流水線。**

## 建出來的結構（速查）

```
{專案}/
├── README.md                  專案總覽與流程
├── PROJECT.md                 後設資料（客戶、技術棧、里程碑、Scope 北極星）
├── 00-governance/             治理核心
│   ├── pipeline.md            流水線：各階段進入/退出條件與審查點
│   ├── numbering-convention.md 文件編號規則與類型碼總表
│   ├── traceability-matrix.md  需求追溯矩陣（全專案真相來源）
│   ├── review-checklists.md    Reviewer 各階段審查清單
│   ├── roles/ROLE-*.md         10 個 Agent 角色的系統提示
│   └── status/                 project-status.md（看板）、open-questions.md
├── 01-discovery/             【人工輸入起點】MOM 會議記錄、SCOPE 範圍
├── 02-requirements/           REQ 需求 / SRS 規格 / UC 使用案例
├── 03-architecture/           ARCH 架構 / INFRA 基建 / INT 介接 / DM 資料模型
├── 04-design/                 UX 流程 / UI 畫面 / DS 設計系統（同一位設計師）
├── 05-development/            FE 前端 / BE 後端 / DB 資料庫
├── 06-quality/                TP 測試計畫 / TC 測試案例 / BUG 缺陷
├── 07-delivery/               DEP 部署 / RB 維運手冊
└── 99-assets/                 共用圖檔附件
```

每個階段資料夾內都有 `_templates/`,各文件型別都有對應範本（含 frontmatter 與 `traces_from`）。

## 10 個 Agent 角色

| 代碼 | 角色 | 階段 | 一句話 |
| --- | --- | --- | --- |
| PM | Project Manager | 全程 | 編排調度、檢查閘門、維護狀態看板（不寫技術文件） |
| BA | Business Analyst | 02 | 把會議「人話」拆成可驗證的需求項 |
| SA | System Analyst | 02 | 把需求深化成規格與使用案例（定義 what） |
| ARCH | Solution Architect | 03 | 系統架構、基礎建設、系統介接、資料模型（定義 how） |
| UX | UX/UI Designer | 04 | 一人包辦 UX 流程與 UI 畫面 + 設計系統 |
| FE | Frontend Engineer | 05 | 依 UI 與 API 合約實作前端 |
| BE | Backend Engineer | 05 | 依架構與資料模型實作後端與資料庫 |
| QA | QA Engineer | 06 | 依需求寫測試、驗證實作、確保覆蓋率 |
| DEVOPS | DevOps / Infra | 07 | 部署、回滾、維運手冊 |
| REV | Reviewer | 全程閘門 | 每個閘門前依清單審查內容品質與追溯一致性,簽核才放行 |

每個角色的 `ROLE-*.md` 就是餵給該 Agent 的系統提示,明確寫了它該讀哪些資料夾、產出什麼、
退出閘門是什麼。編排器（orchestrator）的工作就是：選 Agent → 餵 `ROLE-*.md` + 對應資料夾 →
跑主辦 → 跑 REV → 檢查閘門 → 觸發下游。

## 文件編號與追溯（重點）

- 格式：`{類型碼}-{三位數}-{slug}`,例 `REQ-003-store-exposure`。
- 每份文件 frontmatter 的 `traces_from` 必含上游 ID,串成完整追溯鏈：
  `MOM → SCOPE → REQ → {UC, SRS, ARCH} → INT/DM → UI → FE/BE/DB → TC → DEP`。
- 全部匯總到 `traceability-matrix.md`：人類看一張表就能從「客戶哪次會議講的」追到
  「哪段程式碼、哪個測試」。鐵則：**沒有來源的需求不存在。**

## 安全帶（人工閘門）

三個閘門標 🧑,需人工核准才放行：**Scope 確認、架構定案、上線部署**。這是刻意設計,
避免自動化在錯誤前提上一路狂奔。Agent 遇到上游矛盾或缺漏時,寫進 `open-questions.md`
並標 `blocked`,不自行腦補。

## 進一步參考

- `references/structure-reference.md`：完整結構與各檔用途說明（使用者問細節時可讀）。
- 啟動後,專案內 `00-governance/pipeline.md` 與 `roles/` 是運轉這條生產線的操作手冊。
