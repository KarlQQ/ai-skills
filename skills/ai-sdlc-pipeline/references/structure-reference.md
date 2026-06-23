# 結構參考 (Structure Reference)

啟動腳本 `scripts/bootstrap.py` 會生成下列結構。本檔供需要向使用者詳細解釋各檔用途時參考。

## 治理層 00-governance/

| 檔案 | 誰用 | 用途 |
| --- | --- | --- |
| `pipeline.md` | PM / 所有 Agent | 流水線定義：7 個階段的進入條件、產出、退出閘門、審查點、觸發方式 |
| `numbering-convention.md` | 所有 Agent | 文件編號格式、類型碼總表、追溯鏈規則 |
| `traceability-matrix.md` | 所有 Agent + 人類 | 全專案真相來源；REQ → 規格 → 架構 → 設計 → 開發 → 測試 的對照總表 |
| `review-checklists.md` | REV | 各階段審查清單（通用 + 階段專屬） |
| `roles/ROLE-*.md` | 編排器 | 10 個 Agent 的系統提示（定位、必讀、產出、步驟、閘門、鐵則） |
| `status/project-status.md` | PM + 人類 | 狀態看板；改 gate=ready 觸發 Agent；人類追蹤入口 |
| `status/open-questions.md` | 所有 Agent | 上游矛盾/缺漏登記處；blocked 解除依據 |

## 階段層 01–07

每階段資料夾都有 `_templates/` 放對應文件範本。文件型別與負責角色：

| 階段 | 資料夾 | 文件型別 | 主辦 |
| --- | --- | --- | --- |
| 01 discovery | meeting-records, scope | MOM, SCOPE | 人工 / BA |
| 02 requirements | （根目錄） | REQ, SRS, UC | BA, SA |
| 03 architecture | system, infrastructure, integration, data | ARCH, INFRA, INT, DM | ARCH |
| 04 design | ux, ui, design-system | UX, UI, DS | UX |
| 05 development | frontend, backend, database | FE, BE, DB | FE, BE |
| 06 quality | test-plans, test-cases, defects | TP, TC, BUG | QA |
| 07 delivery | deployment, runbooks | DEP, RB | DEVOPS |

## 一個需求的生命週期（範例追溯）

```
MOM-001（客戶說「想知道店家願意付多少」）
  └─ REQ-003 店家付費意願調查（BA 拆出，驗收條件可測）
       ├─ UC-002 調查員記錄付費區間（SA）
       ├─ SRS-001 調查模組功能規格（SA）
       ├─ ARCH-001 系統架構含調查服務（ARCH）
       │    └─ INT-004 POST /surveys API 合約（ARCH）
       │         └─ DM-002 survey 資料表（ARCH）
       ├─ UI-005 付費區間輸入畫面（UX）
       ├─ FE-003 前端表單實作（FE，串 INT-004）
       ├─ BE-004 後端調查 API（BE，實作 INT-004）
       │    └─ DB-002 survey migration（BE）
       └─ TC-007 付費區間記錄測試（QA，覆蓋 REQ-003）
            └─ DEP-001 部署（DEVOPS）
```

每一步的 frontmatter `traces_from` 都往上指,REV 在每個閘門抽查這條鏈是否完整。

## 自訂與擴充

- 要加新文件型別：在 `numbering-convention.md` 加一列類型碼,並在對應階段 `_templates/`
  放範本即可。
- 要拆角色（例如把 UX 拆成 UX + UI、或新增 Security 角色）：在 `roles/` 加 `ROLE-*.md`,
  並在 `pipeline.md` 安排其階段與閘門。
- 要改觸發機制：`pipeline.md` 末段「觸發方式」可換成你的編排框架（半自動 / 全自動）。
