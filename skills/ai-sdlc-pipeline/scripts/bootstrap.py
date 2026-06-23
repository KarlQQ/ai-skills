#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI SDLC Pipeline — 專案啟動器 (Project Bootstrapper)

用法：
    python3 bootstrap.py \
        --name "乡村市场调研系统" \
        --code "RMR" \
        --overview "為品牌曝光服務建立鄉村市場調研與媒合平台" \
        --client "客戶名稱" \
        --date "2026-06-23" \
        --output-dir "/mnt/user-data/outputs"

必填：--name, --overview
選填：--code（文件 ID 前綴，預設 PRJ）、--client、--date（預設今日）、--output-dir（預設當前目錄）

執行後會在 output-dir 下建立 `{slug}/` 完整專案,內含治理框架、10 個 Agent 角色定義、
各階段範本與追溯矩陣,可立即開始一條龍自動化開發。
"""
import argparse
import datetime
import os
import re
import sys
import textwrap

# ╔══════════════════════════════════════════════════════════════╗
# ║ 變數 → 在 main() 注入                                          ║
# ╚══════════════════════════════════════════════════════════════╝
V = {}  # 由 main 填入: NAME, CODE, OVERVIEW, CLIENT, DATE

FILES = {}

def add(path, content):
    FILES[path] = textwrap.dedent(content).lstrip("\n")

def slugify(name):
    s = re.sub(r"[^\w\u4e00-\u9fff]+", "-", name.strip().lower())
    s = re.sub(r"-+", "-", s).strip("-")
    return s or "project"


def build_files():
    NAME = V["NAME"]; CODE = V["CODE"]; OVERVIEW = V["OVERVIEW"]
    CLIENT = V["CLIENT"]; DATE = V["DATE"]

    # ──────────────────────────────────────────────────────────
    # 根層
    # ──────────────────────────────────────────────────────────
    add("README.md", f"""
    # {NAME} — AI Agent 軟體開發生產線

    > 專案代碼：`{CODE}`　｜　啟動日：{DATE}　｜　客戶：{CLIENT or "（待填）"}
    >
    > **{OVERVIEW}**

    一條龍自動化開發流程：人工只負責「與客戶開會、定義 scope 與需求」,把結果放進
    `01-discovery/`,其餘各角色 Agent 依序接力,直到可部署上線。

    ## 運作方式

    ```
    人工：開會 → 寫會議記錄(MOM) + 範圍(SCOPE)   ← 唯一的人工輸入點
       │
       ▼
    [BA]   需求拆解   → 02-requirements/
    [SA]   功能規格   → 02-requirements/ (SRS/UC)
    [ARCH] 系統架構   → 03-architecture/ (含基礎建設、系統介接、資料模型)
    [UX]   畫面設計   → 04-design/      (UI/UX 同一位)
    [FE/BE] 前後端開發 → 05-development/
    [QA]   測試驗證   → 06-quality/
    [DEVOPS] 部署維運 → 07-delivery/

    [PM]  全程編排調度        [REV] 每個閘門前審查把關
    ```

    每階段都是：**讀上游文件 → 產出本階段文件 → 更新追溯矩陣 → Reviewer 審查 → 通過閘門 → 交棒**。

    ## 你每天會用到的三個檔案

    | 檔案 | 用途 |
    | --- | --- |
    | `00-governance/status/project-status.md` | **人類追蹤入口**：現在做到哪、誰在做、卡在哪 |
    | `00-governance/traceability-matrix.md` | **追溯總表**：需求 → 程式碼 → 測試的完整鏈路 |
    | `00-governance/pipeline.md` | 流水線定義：每階段進入/退出條件與審查點 |

    ## 目錄總覽

    ```
    {slugify(NAME)}/
    ├── README.md
    ├── PROJECT.md                  專案後設資料（客戶、技術棧、里程碑）
    ├── 00-governance/              治理：流程、編號規則、10 個角色、追溯矩陣、審查清單、狀態
    ├── 01-discovery/              【人工輸入起點】會議記錄、範圍定義
    ├── 02-requirements/            REQ 需求 / SRS 規格 / UC 使用案例
    ├── 03-architecture/            ARCH 架構 / INFRA 基礎建設 / INT 系統介接 / DM 資料模型
    ├── 04-design/                  UX 流程 / UI 畫面 / DS 設計系統（同一位設計師）
    ├── 05-development/             FE 前端 / BE 後端 / DB 資料庫
    ├── 06-quality/                 TP 測試計畫 / TC 測試案例 / BUG 缺陷
    ├── 07-delivery/                DEP 部署 / RB 維運手冊
    └── 99-assets/                  共用圖檔附件
    ```

    編號規則一句話：`{{類型碼}}-{{三位數}}-{{slug}}`,例 `REQ-003-store-exposure`。詳見
    `00-governance/numbering-convention.md`。
    """)

    add("PROJECT.md", f"""
    ---
    project_code: {CODE}
    project_name: "{NAME}"
    client: "{CLIENT}"
    status: discovery
    created: "{DATE}"
    updated: "{DATE}"
    ---

    # 專案後設資料

    ## 一、Scope 摘要（北極星）
    > {OVERVIEW}

    ## 二、基本資訊
    - **客戶 / 委託方**：{CLIENT or "（待填）"}
    - **專案負責人（人工）**：（待填）
    - **預計交付日**：（待填）

    ## 三、技術棧（由 ARCH 於 03 階段填寫並回填此處）
    - 前端：
    - 後端：
    - 資料庫：
    - 基礎建設 / 部署：

    ## 四、里程碑
    | 里程碑 | 對應階段 | 目標日 | 狀態 |
    | --- | --- | --- | --- |
    | 需求凍結 | 02 | | |
    | 架構定案 | 03 | | |
    | 設計定稿 | 04 | | |
    | 開發完成 | 05 | | |
    | 驗收通過 | 06 | | |
    | 上線 | 07 | | |
    """)

    _governance()
    _roles()
    _phase_templates(NAME, DATE)
    _gitkeeps()


# ──────────────────────────────────────────────────────────────
# 00-governance
# ──────────────────────────────────────────────────────────────
def _governance():
    add("00-governance/pipeline.md", """
    # 自動化流水線定義 (Pipeline)

    每個階段是一道「工序」。Agent 啟動時讀本檔,確認**進入條件**已滿足,完成後交給 Reviewer
    審查,通過**退出閘門**才可交棒。

    ## 階段總表

    | # | 階段 | 主辦 Agent | 進入條件 | 產出 | 退出閘門（REV 審查 + 條件） |
    | --- | --- | --- | --- | --- | --- |
    | 01 | Discovery 探索 | 人工 + BA | 有客戶會議 | MOM、SCOPE | 🧑 Scope 經客戶確認 |
    | 02 | Requirements 需求 | BA → SA | 01 done | REQ、SRS、UC | 每條 REQ 可測試、無 TBD、REV 通過 |
    | 03 | Architecture 架構 | ARCH | 02 done | ARCH、INFRA、INT、DM | 🧑 每條 REQ 有對應元件、介接點明確、REV 通過 |
    | 04 | Design 設計 | UX | 03 done | UX、UI、DS | 每個 UC 有對應畫面、REV 通過 |
    | 05 | Development 開發 | FE + BE | 04 done(FE)/03 done(BE) | FE、BE、DB | 可建置、自檢清單過、REV 通過 |
    | 06 | Quality 品質 | QA | 05 done | TP、TC、BUG | 需求覆蓋率 100%、無 P0/P1、REV 通過 |
    | 07 | Delivery 交付 | DEVOPS | 06 done | DEP、RB | 🧑 部署成功、health check 綠燈 |

    （🧑 = 該閘門需人工核准才放行,是刻意留的安全帶。）

    ## 每階段的標準循環
    ```
    1. PM 在 status 看到 gate=ready → 啟動主辦 Agent
    2. 主辦 Agent 讀上游資料夾 → 產出本階段文件 → 回填 traceability-matrix
    3. 主辦 Agent 跑自我檢查清單 → 標 status=in-review
    4. REV 依 review-checklists.md 審查 → pass / 退回
    5. pass → PM 標本階段 done、下游 gate=ready；fail → 退回主辦 Agent 修正
    6. 遇上游矛盾/缺漏 → 寫 open-questions.md、標 blocked,不自行假設
    ```

    ## 閘門通用規則
    1. **不可跳階**：下游啟動前,上游必須在 `project-status.md` 標記 `done`。
    2. **追溯必填**：任何產出 frontmatter 的 `traces_from` 必含上游 ID,並同步更新追溯矩陣。
    3. **缺口回拋**：上游有矛盾/缺漏 → 寫 `open-questions.md`、退回上一階段,**不腦補**。
    4. **Reviewer 把關**：每個非人工閘門都要 REV 簽核（在審查清單打勾）才能 done。
    5. **人工閘門**：🧑 標記的閘門需人工核准。

    ## 觸發方式（建議）
    - **半自動**：人工把某階段 gate 標 `ready`,編排器啟動對應 Agent。
    - **全自動**：每個 Agent 通過 REV 後,自動把下游 gate 標 `ready` 觸發下游。
    - 編排器（orchestrator）只做四件事：選 Agent → 餵 `ROLE-*.md` + 對應資料夾 → 跑主辦 →
      跑 REV → 檢查閘門。
    """)

    add("00-governance/numbering-convention.md", """
    # 文件編號規則

    ## 格式
    ```
    {類型碼}-{三位數編號}-{slug}.md
    ```
    - **類型碼**：見下表,對應階段。
    - **編號**：同類型內遞增三位數（001, 002, …）,不重用、不補位。
    - **slug**：小寫英文 + 連字號短描述,例 `store-exposure-need`。
    - 需全域唯一時加專案前綴：`{專案代碼}-REQ-003-...`。

    ## 類型碼總表

    | 階段 | 資料夾 | 類型碼 | 中文 | 負責角色 |
    | --- | --- | --- | --- | --- |
    | 01 | 01-discovery/meeting-records | `MOM` | 會議記錄 | 人工/BA |
    | 01 | 01-discovery/scope | `SCOPE` | 範圍定義 | 人工/BA |
    | 02 | 02-requirements | `REQ` | 需求項 | BA |
    | 02 | 02-requirements | `SRS` | 軟體需求規格 | SA |
    | 02 | 02-requirements | `UC` | 使用案例 | SA |
    | 03 | 03-architecture/system | `ARCH` | 系統架構 | ARCH |
    | 03 | 03-architecture/infrastructure | `INFRA` | 基礎建設 | ARCH/DEVOPS |
    | 03 | 03-architecture/integration | `INT` | 系統介接 / API 合約 | ARCH |
    | 03 | 03-architecture/data | `DM` | 資料模型 | ARCH |
    | 04 | 04-design/ux | `UX` | UX 流程 / 線框 | UX |
    | 04 | 04-design/ui | `UI` | UI 畫面設計 | UX |
    | 04 | 04-design/design-system | `DS` | 設計系統 / 元件 | UX |
    | 05 | 05-development/frontend | `FE` | 前端開發文件 | FE |
    | 05 | 05-development/backend | `BE` | 後端開發文件 | BE |
    | 05 | 05-development/database | `DB` | 資料庫 schema / migration | BE |
    | 06 | 06-quality/test-plans | `TP` | 測試計畫 | QA |
    | 06 | 06-quality/test-cases | `TC` | 測試案例 | QA |
    | 06 | 06-quality/defects | `BUG` | 缺陷單 | QA |
    | 07 | 07-delivery/deployment | `DEP` | 部署文件 | DEVOPS |
    | 07 | 07-delivery/runbooks | `RB` | 維運手冊 | DEVOPS |

    ## 追溯鏈（誰生自誰）
    ```
    MOM ─► SCOPE ─► REQ ─┬─► UC ──► UX ──► UI ─┬─► FE ─► TC
                         │                      │
                         ├─► SRS ───────────────┤
                         │                      │
                         └─► ARCH ─► INT ─► DM ─┴─► BE ─► DB ─► TC ─► DEP
    ```
    鐵則：**下游文件 frontmatter 的 `traces_from` 必含至少一個上游 ID。沒有來源的需求不存在。**
    """)

    add("00-governance/traceability-matrix.md", """
    # 需求追溯矩陣 (Traceability Matrix)

    > 全專案的真相來源。每新增一條需求就加一列；任何 Agent 產出文件都要回填對應欄。
    > 人類只要看這張表,就能從「客戶在哪次會議講的」追到「哪段程式碼、哪個測試」。

    | REQ ID | 需求摘要 | 來源 (MOM/SCOPE) | 規格 (SRS/UC) | 架構 (ARCH/INT) | 設計 (UI) | 開發 (FE/BE/DB) | 測試 (TC) | 狀態 |
    | --- | --- | --- | --- | --- | --- | --- | --- | --- |
    | REQ-001 | （範例）店家曝光需求調查 | MOM-001 | UC-001 | ARCH-001 | UI-002 | BE-001 | TC-001 | dev |
    | | | | | | | | | |

    ## 狀態值
    `todo` → `spec` → `design` → `dev` → `test` → `done` ／ `blocked`

    ## 覆蓋率自檢（QA 於 06 階段執行,REV 複核）
    - [ ] 每條 REQ 都有對應 TC（需求覆蓋率 = 100%）
    - [ ] 每個 UC 都有對應 UI
    - [ ] 每個 INT 介接點都有對應 BE 與 TC
    - [ ] 無孤兒文件：任何 FE/BE/UI 都能往上追到某條 REQ
    """)

    add("00-governance/review-checklists.md", """
    # 各階段審查清單 (Reviewer 用)

    Reviewer (REV) 在每個閘門前依此清單逐項檢查,全過才簽核放行。任何一項不過 → 退回主辦
    Agent,並在 `open-questions.md` 記錄原因。

    ## 通用檢查（每階段都查）
    - [ ] 所有新文件命名符合編號規則,編號無重複
    - [ ] 每份文件 frontmatter `traces_from` 都有有效上游 ID
    - [ ] `traceability-matrix.md` 已同步更新
    - [ ] 無 `TBD` / 空白必填欄
    - [ ] 無孤兒文件（都能往上追到 REQ）

    ## 02 需求
    - [ ] 每條 REQ 原子化（一條只講一件事）、可測試、有驗收條件
    - [ ] 每條 REQ 可追到某 MOM / SCOPE
    - [ ] 範圍外項目已明確標示,未混入

    ## 03 架構
    - [ ] 每條 REQ 對應到至少一個架構元件
    - [ ] 每個外部/內部介接點都有 INT 合約（含 endpoint、欄位、錯誤碼）
    - [ ] 資料模型涵蓋所有 SRS 提及的實體
    - [ ] 技術棧已回填 PROJECT.md

    ## 04 設計
    - [ ] 每個 UC 都有對應 UI 畫面
    - [ ] 每個畫面定義了載入 / 空 / 錯誤 / 成功態
    - [ ] 共用元件已抽進 DS

    ## 05 開發
    - [ ] FE 的 API 呼叫與對應 INT 合約完全一致
    - [ ] BE 已實作每一個 INT 合約,回應格式吻合
    - [ ] DB migration 可執行、對應 DM
    - [ ] 主辦 Agent 自檢清單全勾

    ## 06 品質
    - [ ] 需求覆蓋率 100%（每條 REQ ≥1 TC）
    - [ ] 無未解 P0 / P1 缺陷
    - [ ] 失敗項都有對應 BUG 並指派

    ## 07 交付
    - [ ] 部署流程含回滾程序
    - [ ] runbook 含監控、告警、常見故障處理
    - [ ] health check 通過
    """)

    add("00-governance/status/project-status.md", f"""
    # 專案狀態看板（人類追蹤入口）

    > 編排器與人工都讀寫這張看板。改 `gate` 為 `ready` 即可觸發對應 Agent。

    ## 當前階段
    **current_phase:** `01-discovery`

    ## 階段狀態
    | 階段 | gate | 負責 | 備註 |
    | --- | --- | --- | --- |
    | 01 discovery | `ready` | 人工/BA | 等待會議記錄輸入 |
    | 02 requirements | `waiting` | BA/SA | |
    | 03 architecture | `waiting` | ARCH | |
    | 04 design | `waiting` | UX | |
    | 05 development | `waiting` | FE/BE | |
    | 06 quality | `waiting` | QA | |
    | 07 delivery | `waiting` | DEVOPS | |

    `gate` 值：`waiting`（上游未完成）｜`ready`（可開工）｜`in-progress`｜`in-review`（待 REV）｜`done`｜`blocked`

    ## 進行中工作
    | 文件 ID | Agent | 開始 | 狀態 |
    | --- | --- | --- | --- |
    | | | | |
    """)

    add("00-governance/status/open-questions.md", """
    # 待釐清問題 (Open Questions)

    > Agent 遇到上游矛盾或缺漏時寫在這裡,**不要自行假設**。由人工或上游角色回覆後才解除 blocked。

    | QID | 提問 Agent | 相關文件 | 問題 | 指派給 | 狀態 | 回覆 |
    | --- | --- | --- | --- | --- | --- | --- |
    | Q-001 | | | | 人工 | open | |
    """)


# ──────────────────────────────────────────────────────────────
# 角色定義（Agent system prompt）— 10 個角色
# ──────────────────────────────────────────────────────────────
ROLE_TMPL = """
---
role_id: {rid}
role_name: {rname}
phase: "{phase}"
reads: {reads}
writes: {writes}
---

# 角色：{rname} ({rid})

## 定位
{positioning}

## 進入條件
{entry}

## 必讀文件
{readlist}

## 產出文件
{writelist}

## 工作步驟
{steps}

## 退出閘門（做完才能交棒）
{gate}

## 鐵則
{rules}
"""

COMMON_RULES = """- 任何產出 frontmatter 的 `traces_from` 必含上游 ID；同步更新 `traceability-matrix.md`。
- 遇上游矛盾/缺漏：寫入 `open-questions.md`,把該需求標 `blocked`,**不自行腦補**。
- 不修改不屬於你階段的文件（回填追溯欄除外）。
- 完成自檢後把狀態標 `in-review`,交 Reviewer；REV 通過後 PM 才標 `done`。"""


def _role(rid, rname, phase, reads, writes, positioning, entry, readlist, writelist, steps, gate, rules=None):
    add("00-governance/roles/ROLE-%s.md" % rid, ROLE_TMPL.format(
        rid=rid, rname=rname, phase=phase, reads=reads, writes=writes,
        positioning=positioning.strip(), entry=entry.strip(), readlist=readlist.strip(),
        writelist=writelist.strip(), steps=steps.strip(), gate=gate.strip(),
        rules=(rules or COMMON_RULES).strip()))


def _roles():
    _role("PM", "Project Manager（編排者）", "全程",
        "[全部]", "[project-status.md, PROJECT.md, open-questions.md]",
        "你是流水線的編排者與調度者。不產出技術文件,負責調度各角色、檢查閘門、維護狀態看板與里程碑,並把 open-questions 指派給正確的人/Agent。",
        "- 任何階段狀態變更時被觸發。",
        "- `pipeline.md`、`project-status.md`、`traceability-matrix.md`、`open-questions.md`",
        "- 更新 `project-status.md`（誰在做、做到哪）\n- 維護 `PROJECT.md` 里程碑\n- 指派 open-questions",
        "1. 讀 status,找出 gate=`ready` 的階段。\n2. 確認進入條件（上游 `done`、無未解 blocking 問題）。\n3. 啟動對應主辦 Agent,餵入其 `ROLE-*.md` 與該階段資料夾。\n4. 主辦回報 `in-review` → 啟動 REV 審查。\n5. REV 通過 → 標該階段 `done`,把下游設 `ready`；未通過 → 退回主辦並記錄。",
        "- 每階段閘門都經 REV 與（必要時）人工核准,狀態看板與真實進度一致。",
        "- 不替代各角色做專業判斷,只負責流程與閘門。\n- 🧑 人工閘門（Scope/架構/上線）務必停下等待人工核准。")

    _role("BA", "Business Analyst", "02 需求（承接 01）",
        "[01-discovery/]", "[02-requirements/REQ-*]",
        "你把『人話』翻成『可開發的需求』。輸入是會議記錄與範圍,輸出是一條條獨立、可驗證的需求項。",
        "- `project-status.md` 中 01 階段 gate=`done`,且 SCOPE 已客戶確認。",
        "- 全部 `01-discovery/meeting-records/MOM-*`\n- `01-discovery/scope/SCOPE-*`",
        "- `02-requirements/REQ-{NNN}-{slug}.md`（每條一檔,用 `_templates/requirement.md`）",
        "1. 通讀所有 MOM 與 SCOPE。\n2. 把口語需求拆成原子化、可測試的 REQ（一條只講一件事）。\n3. 每條標：來源 MOM ID、優先級（P0/P1/P2）、驗收條件。\n4. 範圍外需求寫進該 REQ 的 `out-of-scope` 或記入 open-questions。\n5. 為每條 REQ 在追溯矩陣開一列。",
        "- 每條 REQ 都可追到某 MOM/SCOPE、都有驗收條件、無 `TBD`。")

    _role("SA", "System Analyst（系統分析）", "02 需求",
        "[02-requirements/REQ-*]", "[02-requirements/SRS-*, UC-*]",
        "你把『需求』深化成『規格與使用案例』,定義系統該有的行為（what）,不碰技術選型（那是 ARCH）。",
        "- BA 已完成 REQ 清單。",
        "- 全部 `02-requirements/REQ-*`",
        "- `02-requirements/SRS-{NNN}-{slug}.md`（功能/非功能需求）\n- `02-requirements/UC-{NNN}-{slug}.md`（使用案例：角色、前置、主流程、例外流程）",
        "1. 把相關 REQ 群組成功能模組,寫 SRS。\n2. 為每個關鍵互動寫 UC（含正常與例外流程）。\n3. 補非功能需求（效能、安全、相容）。\n4. 回填追溯矩陣 `規格` 欄。",
        "- 每條 REQ 都被至少一份 SRS 或 UC 覆蓋。")

    _role("ARCH", "Solution Architect（系統架構）", "03 架構",
        "[02-requirements/]", "[03-architecture/*]",
        "你決定系統『怎麼蓋』：整體架構、基礎建設、外部系統介接、資料模型。你的 INT 文件是後端開發的 API 合約來源。",
        "- 02 需求階段 `done`。",
        "- 全部 `02-requirements/SRS-*`、`UC-*`、`REQ-*`",
        "- `03-architecture/system/ARCH-{NNN}-*.md`（元件圖、技術棧、分層）\n- `03-architecture/infrastructure/INFRA-{NNN}-*.md`（部署拓樸、環境、雲資源）\n- `03-architecture/integration/INT-{NNN}-*.md`（API 合約、第三方介接）\n- `03-architecture/data/DM-{NNN}-*.md`（實體關係、資料字典）",
        "1. 由 SRS/UC 推導需要哪些元件與服務。\n2. 定技術棧並回填 `PROJECT.md`。\n3. 畫部署拓樸（INFRA）與每個介接點合約（INT,含 endpoint、欄位、錯誤碼）。\n4. 建資料模型（DM）。\n5. 確認每條 REQ 對應到至少一個元件,回填追溯矩陣 `架構` 欄。",
        "- 每條 REQ 有對應元件；所有外部介接點都有明確 INT 合約；技術棧已定。（🧑 架構定案需人工核准）")

    _role("UX", "UX/UI Designer（設計,UI與UX同一位）", "04 設計",
        "[02-requirements/UC-*, 03-architecture/]", "[04-design/*]",
        "你一人包辦 UX 與 UI：先做 UX（流程、線框、資訊架構）,再做 UI（視覺、畫面、狀態）,並維護設計系統供前端 1:1 對齊。",
        "- 03 架構 `done`。",
        "- `02-requirements/UC-*`\n- `03-architecture/system/ARCH-*`（了解技術限制）",
        "- `04-design/ux/UX-{NNN}-*.md`（流程圖、線框、互動說明）\n- `04-design/ui/UI-{NNN}-*.md`（畫面規格：版面、元件、所有狀態）\n- `04-design/design-system/DS-{NNN}-*.md`（色彩、字級、間距、共用元件）",
        "1. 為每個 UC 設計畫面流程（UX）。\n2. 細化每個畫面的 UI 規格與所有狀態（預設/載入/空/錯誤/成功）。\n3. 抽出共用元件進 DS。\n4. 回填追溯矩陣 `設計` 欄。",
        "- 每個 UC 都有對應 UI；每個畫面都定義了載入/空/錯誤態。")

    _role("FE", "Frontend Engineer", "05 開發",
        "[04-design/, 03-architecture/integration/]", "[05-development/frontend/FE-*]",
        "你依 UI 規格與 DS 實作前端,依 INT 合約串接後端 API,產出開發文件（元件樹、路由、狀態管理、API 對應）。",
        "- 04 設計 `done`,且對應 INT 合約已定。",
        "- `04-design/ui/UI-*`、`design-system/DS-*`\n- `03-architecture/integration/INT-*`（API 合約）",
        "- `05-development/frontend/FE-{NNN}-*.md`（元件樹、路由、狀態、API 對接、實作筆記）",
        "1. 由 UI/DS 規劃元件與路由。\n2. 依 INT 合約定義 API 呼叫層與型別。\n3. 實作並對照 UI 的每個狀態。\n4. 跑自我檢查清單。\n5. 回填追溯矩陣 `開發` 欄。",
        "- 可建置、所有畫面狀態實作完成、API 呼叫與 INT 合約一致。")

    _role("BE", "Backend Engineer", "05 開發",
        "[03-architecture/, 02-requirements/]", "[05-development/backend/BE-*, database/DB-*]",
        "你依架構與資料模型實作後端服務與 API（須符合 INT 合約）,並建立資料庫 schema/migration。",
        "- 03 架構 `done`（可與 FE 平行,不需等 04）。",
        "- `03-architecture/integration/INT-*`（API 合約,須一致）\n- `03-architecture/data/DM-*`、`02-requirements/SRS-*`",
        "- `05-development/backend/BE-{NNN}-*.md`（服務、endpoint、商業邏輯、錯誤處理）\n- `05-development/database/DB-{NNN}-*.md`（schema、migration、索引）",
        "1. 依 DM 建資料表與 migration。\n2. 依 INT 合約逐一實作 endpoint（請求/回應/錯誤碼須完全吻合）。\n3. 實作 SRS 的商業邏輯與非功能需求。\n4. 自檢：每個 INT 合約都有對應實作。\n5. 回填追溯矩陣 `開發` 欄。",
        "- 所有 INT 合約皆已實作且回應格式吻合；migration 可執行。")

    _role("QA", "QA Engineer", "06 品質",
        "[02-requirements/, 05-development/]", "[06-quality/*]",
        "你是執行品質閘門。依需求與使用案例寫測試計畫與案例,驗證實作,登記缺陷,確保需求覆蓋率達標。",
        "- 05 開發 `done`。",
        "- `02-requirements/REQ-*`、`UC-*`\n- `05-development/`（FE/BE/DB）",
        "- `06-quality/test-plans/TP-{NNN}-*.md`\n- `06-quality/test-cases/TC-{NNN}-*.md`（對應 REQ/UC）\n- `06-quality/defects/BUG-{NNN}-*.md`（含嚴重度 P0~P3）",
        "1. 由 REQ/UC 推導測試案例,每條 REQ ≥1 TC。\n2. 執行並記錄結果。\n3. 失敗項開 BUG（標嚴重度、退回對應開發角色）。\n4. 計算需求覆蓋率,回填追溯矩陣 `測試` 欄。",
        "- 需求覆蓋率 100%、無未解 P0/P1 缺陷。")

    _role("DEVOPS", "DevOps / Infra Engineer", "07 交付",
        "[03-architecture/infrastructure/, 05-development/]", "[07-delivery/*]",
        "你依 INFRA 規劃建置環境並部署,撰寫部署文件與維運手冊,確保上線後可維運、可回滾。",
        "- 06 品質 `done`。",
        "- `03-architecture/infrastructure/INFRA-*`\n- `05-development/`（建置產物）",
        "- `07-delivery/deployment/DEP-{NNN}-*.md`（環境、流程、CI/CD、回滾）\n- `07-delivery/runbooks/RB-{NNN}-*.md`（監控、告警、故障處理）",
        "1. 依 INFRA 備妥環境。\n2. 設定部署/回滾流程。\n3. 部署並跑 health check。\n4. 寫 runbook 交維運。\n5. 通知 PM 標記專案 `done`。",
        "- 部署成功、health check 綠燈、runbook 完成。（🧑 上線需人工核准）")

    _role("REV", "Reviewer（跨階段審查把關）", "全程閘門",
        "[當前審查階段的產出 + 其上游]", "[review 簽核, open-questions.md, BUG-*（文件層級）]",
        "你是每個閘門前的守門員,與 PM 互補：PM 管流程進度,你管**內容品質與一致性**。你不產出技術文件,負責依 `review-checklists.md` 逐項審查當階段產出,確認它忠實對應上游、追溯完整、無缺漏,才簽核放行。",
        "- 某階段主辦 Agent 把狀態標為 `in-review`。",
        "- `00-governance/review-checklists.md`\n- 當前階段全部產出 + 其上游文件\n- `traceability-matrix.md`",
        "- 在 `review-checklists.md` 對應段落打勾並簽註結論\n- 不通過項目寫入 `open-questions.md`\n- 文件層級缺陷可開 `BUG-*`（type=DOC）",
        "1. 取出當前階段產出與其上游。\n2. 逐項跑通用清單 + 該階段專屬清單。\n3. 抽查追溯鏈：隨機挑幾條 REQ,確認能一路追到本階段產出。\n4. 全過 → 簽核 `REV-PASS`,通知 PM 可標 `done`；任一項不過 → 標 `REV-REJECT`,列出具體問題退回主辦 Agent。\n5. 不臆測修正內容,只指出問題,由主辦 Agent 修。",
        "- 清單全勾、追溯抽查通過、無未解 blocking 問題,才簽 `REV-PASS`。",
        "- 你**只審查不代寫**：發現問題退回主辦,不自己改文件。\n- 寧可退回也不放水；閘門失守會讓錯誤一路流到下游放大。\n- 審查意見要具體可執行（指出哪份文件、哪一條、缺什麼）。")


# ──────────────────────────────────────────────────────────────
# 各階段範本與種子檔
# ──────────────────────────────────────────────────────────────
def _phase_templates(NAME, DATE):
    # 01 discovery
    add("01-discovery/_templates/MOM-template.md", """
    ---
    id: MOM-{NNN}
    type: MOM
    date: ""
    attendees: []
    traces_from: []
    ---
    # 會議記錄 MOM-{NNN}：{會議主題}

    ## 與會者
    -

    ## 客戶原話 / 重點（盡量保留原始語境）
    -

    ## 已確認事項
    -

    ## 待確認 / 開放問題
    -

    ## BA 註記（哪些可拆成 REQ）
    -
    """)
    add("01-discovery/scope/_templates/SCOPE-template.md", """
    ---
    id: SCOPE-{NNN}
    type: SCOPE
    traces_from: [MOM-{NNN}]
    confirmed_by_client: false
    ---
    # 範圍定義 SCOPE-{NNN}

    ## 一句話目標
    >

    ## 本期要做（In Scope）
    -

    ## 本期不做（Out of Scope）
    -

    ## 假設與限制
    -

    ## 客戶確認
    - [ ] 客戶已確認本範圍（confirmed_by_client: true 後方可進入 02）
    """)
    add("01-discovery/meeting-records/MOM-001-kickoff.md", f"""
    ---
    id: MOM-001
    type: MOM
    date: "{DATE}"
    attendees: ["客戶", "PM(人工)"]
    traces_from: []
    ---
    # 會議記錄 MOM-001：{NAME} 啟動會議

    ## 與會者
    - 客戶、人工 PM

    ## 客戶原話 / 重點
    - （把客戶說的話放這裡,這是整條生產線唯一的源頭）

    ## 已確認事項
    -

    ## 待確認
    -
    """)

    # 02 requirements
    add("02-requirements/_templates/requirement.md", """
    ---
    id: REQ-{NNN}
    type: REQ
    priority: P1
    traces_from: [MOM-{NNN}]
    status: todo
    ---
    # REQ-{NNN}：{需求標題}

    ## 需求敘述（使用者故事）
    > 身為 {角色},我想要 {功能},以便 {價值}。

    ## 驗收條件（可測試）
    - [ ]
    - [ ]

    ## 範圍外
    -

    ## 備註
    -
    """)
    add("02-requirements/_templates/SRS-template.md", """
    ---
    id: SRS-{NNN}
    type: SRS
    traces_from: [REQ-{NNN}]
    ---
    # SRS-{NNN}：{模組名稱}

    ## 功能需求
    | FR | 說明 | 對應 REQ |
    | --- | --- | --- |

    ## 非功能需求
    | NFR | 類型 | 指標 |
    | --- | --- | --- |
    | | 效能/安全/可用性 | |
    """)
    add("02-requirements/_templates/UC-template.md", """
    ---
    id: UC-{NNN}
    type: UC
    traces_from: [REQ-{NNN}]
    ---
    # UC-{NNN}：{使用案例名稱}

    - **主要角色**：
    - **前置條件**：
    - **後置條件**：

    ## 主流程
    1.

    ## 例外流程
    - E1：
    """)

    # 03 architecture
    add("03-architecture/_templates/ARCH-template.md", """
    ---
    id: ARCH-{NNN}
    type: ARCH
    traces_from: [SRS-{NNN}]
    ---
    # ARCH-{NNN}：系統架構

    ## 架構概觀（元件圖）
    ```
    [Client] -> [API Gateway] -> [Service] -> [DB]
    ```
    ## 技術棧
    | 層 | 選型 | 理由 |
    | --- | --- | --- |

    ## 元件對需求對應
    | 元件 | 對應 REQ |
    | --- | --- |
    """)
    add("03-architecture/integration/_templates/INT-template.md", """
    ---
    id: INT-{NNN}
    type: INT
    traces_from: [ARCH-{NNN}]
    ---
    # INT-{NNN}：API / 介接合約

    ## Endpoint
    `{METHOD} /path`

    ## 請求
    | 欄位 | 型別 | 必填 | 說明 |
    | --- | --- | --- | --- |

    ## 回應（200）
    ```json
    {}
    ```
    ## 錯誤碼
    | code | 意義 |
    | --- | --- |

    > 此合約同時是 FE 串接與 BE 實作的唯一依據,兩邊必須與此一致。
    """)
    add("03-architecture/infrastructure/_templates/INFRA-template.md", """
    ---
    id: INFRA-{NNN}
    type: INFRA
    traces_from: [ARCH-{NNN}]
    ---
    # INFRA-{NNN}：基礎建設

    ## 部署拓樸
    ## 環境（dev / staging / prod）
    ## 雲資源清單
    ## CI/CD 流程
    """)
    add("03-architecture/data/_templates/DM-template.md", """
    ---
    id: DM-{NNN}
    type: DM
    traces_from: [SRS-{NNN}]
    ---
    # DM-{NNN}：資料模型

    ## 實體關係
    ## 資料字典
    | 表 | 欄位 | 型別 | 說明 |
    | --- | --- | --- | --- |
    """)

    # 04 design
    add("04-design/ux/_templates/UX-template.md", """
    ---
    id: UX-{NNN}
    type: UX
    traces_from: [UC-{NNN}]
    ---
    # UX-{NNN}：{流程名稱}

    ## 使用者流程
    ## 線框（描述或附圖於 99-assets）
    ## 資訊架構
    """)
    add("04-design/ui/_templates/UI-template.md", """
    ---
    id: UI-{NNN}
    type: UI
    traces_from: [UX-{NNN}, UC-{NNN}]
    ---
    # UI-{NNN}：{畫面名稱}

    ## 版面
    ## 元件清單（對應 DS）
    ## 狀態
    - 預設 / 載入中 / 空資料 / 錯誤 / 成功
    """)
    add("04-design/design-system/_templates/DS-template.md", """
    ---
    id: DS-{NNN}
    type: DS
    traces_from: []
    ---
    # DS-{NNN}：設計系統

    ## 色彩 / 字級 / 間距
    ## 共用元件規格
    """)

    # 05 development
    add("05-development/frontend/_templates/FE-template.md", """
    ---
    id: FE-{NNN}
    type: FE
    traces_from: [UI-{NNN}, INT-{NNN}]
    ---
    # FE-{NNN}：{功能/頁面}

    ## 元件樹 / 路由
    ## 狀態管理
    ## API 對接（對應 INT）
    ## 自我檢查
    - [ ] 可建置
    - [ ] 所有 UI 狀態已實作
    - [ ] API 呼叫與 INT 合約一致
    """)
    add("05-development/backend/_templates/BE-template.md", """
    ---
    id: BE-{NNN}
    type: BE
    traces_from: [INT-{NNN}, DM-{NNN}, SRS-{NNN}]
    ---
    # BE-{NNN}：{服務名稱}

    ## 實作的 Endpoints（對應 INT）
    ## 商業邏輯
    ## 錯誤處理
    ## 自我檢查
    - [ ] 每個 INT 合約都已實作且回應吻合
    """)
    add("05-development/database/_templates/DB-template.md", """
    ---
    id: DB-{NNN}
    type: DB
    traces_from: [DM-{NNN}]
    ---
    # DB-{NNN}：Schema / Migration

    ## 資料表
    ## Migration 腳本說明
    ## 索引
    """)

    # 06 quality
    add("06-quality/test-plans/_templates/TP-template.md", """
    ---
    id: TP-{NNN}
    type: TP
    traces_from: [SRS-{NNN}]
    ---
    # TP-{NNN}：測試計畫
    ## 範圍 / 策略 / 環境 / 需求覆蓋對照
    """)
    add("06-quality/test-cases/_templates/TC-template.md", """
    ---
    id: TC-{NNN}
    type: TC
    traces_from: [REQ-{NNN}, UC-{NNN}]
    ---
    # TC-{NNN}：{測試項}

    | 步驟 | 操作 | 預期 |
    | --- | --- | --- |

    - **結果**：pass / fail
    - **關聯 BUG**：
    """)
    add("06-quality/defects/_templates/BUG-template.md", """
    ---
    id: BUG-{NNN}
    type: BUG
    severity: P2
    traces_from: [TC-{NNN}]
    assigned_to: ""
    status: open
    ---
    # BUG-{NNN}：{標題}
    ## 重現步驟 / 預期 / 實際
    """)

    # 07 delivery
    add("07-delivery/deployment/_templates/DEP-template.md", """
    ---
    id: DEP-{NNN}
    type: DEP
    traces_from: [INFRA-{NNN}]
    ---
    # DEP-{NNN}：部署文件
    ## 環境 / 步驟 / CI-CD / 回滾程序 / health check
    """)
    add("07-delivery/runbooks/_templates/RB-template.md", """
    ---
    id: RB-{NNN}
    type: RB
    traces_from: [DEP-{NNN}]
    ---
    # RB-{NNN}：維運手冊
    ## 監控指標 / 告警 / 常見故障處理 / 聯絡人
    """)

    add("99-assets/README.md", "# 共用資源\n圖檔、附件、匯出檔放這裡,於文件中以相對路徑引用。\n")


def _gitkeeps():
    for d in [
        "02-requirements", "03-architecture/system", "04-design/ux", "04-design/ui",
        "04-design/design-system", "05-development/frontend", "05-development/backend",
        "05-development/database", "06-quality/test-plans", "06-quality/test-cases",
        "06-quality/defects", "07-delivery/deployment", "07-delivery/runbooks",
    ]:
        FILES["%s/.gitkeep" % d] = ""


# ──────────────────────────────────────────────────────────────
# main
# ──────────────────────────────────────────────────────────────
def main():
    p = argparse.ArgumentParser(description="AI SDLC Pipeline 專案啟動器")
    p.add_argument("--name", required=True, help="專案名稱（必填）")
    p.add_argument("--overview", required=True, help="專案概述（必填）")
    p.add_argument("--code", default="PRJ", help="文件 ID 前綴 / 專案代碼，預設 PRJ")
    p.add_argument("--client", default="", help="客戶 / 委託方")
    p.add_argument("--date", default=datetime.date.today().isoformat(), help="啟動日期 YYYY-MM-DD")
    p.add_argument("--output-dir", default=".", help="專案建立位置，預設當前目錄")
    args = p.parse_args()

    V.update(NAME=args.name, CODE=args.code, OVERVIEW=args.overview,
             CLIENT=args.client, DATE=args.date)

    build_files()

    root = os.path.join(os.path.abspath(args.output_dir), slugify(args.name))
    if os.path.exists(root):
        print("⚠ 目標已存在：%s（請改名或刪除後重試）" % root)
        sys.exit(1)

    for rel, content in FILES.items():
        full = os.path.join(root, rel)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w", encoding="utf-8") as f:
            f.write(content)

    print("✓ 已建立專案：%s" % root)
    print("  檔案數：%d" % len(FILES))
    print("  下一步：把客戶會議記錄放進 01-discovery/meeting-records/，把 SCOPE 確認後即可啟動 02。")


if __name__ == "__main__":
    main()
