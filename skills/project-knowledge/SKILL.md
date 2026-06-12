---
name: project-knowledge
description: >-
  Builds and maintains project-knowledge/ in each project: codebase analysis,
  feature docs, client requirements (REQ-*), and issues (ISSUE-*/P*). Use when
  onboarding, analyzing a codebase, archiving requirements or bugs, or when the
  user mentions project-knowledge, 專案知識庫, 需求歸檔, or issue 歸檔.
---

# Project Knowledge

在專案根目錄維護 `project-knowledge/`（不參與編譯）。

## 目錄結構

```
project-knowledge/
├── README.md
├── _templates/          # feature.md, requirement.md, issue.md
├── 00-overview/         # architecture.md, feature-index.md
├── 01-features/         # 每個主功能一份 md
├── 02-requirements/     # REQ-001-*.md
├── 03-issues/           # ISSUE-001-*.md 或 P0-*.md
└── 04-reference/        # 開發參考文件（API spec、javadoc、vendor docs），每主題一個子目錄
```

## 四步驟

**一、分析專案**（初次或架構大改）
- 寫 `00-overview/architecture.md`（目錄樹、技術棧、入口）
- 每個主功能寫 `01-features/{名稱}.md`
- 更新 `feature-index.md`

**二、客戶需求** → `02-requirements/REQ-{編號}-{slug}.md`

**三、系統問題** → `03-issues/ISSUE-{編號}-{slug}.md` 或 `P0-{slug}.md`

`REQ-001-xxx` 與 `ISSUE-001-xxx` 共用編號與 slug。

**四、參考文件** → `04-reference/{主題}/`
- 存放開發時應查閱的原始文件（API spec、javadoc、協定文件等），文件本體只放這裡，不放別處
- 對大型或開發時常查的參考文件，另建專案 skill `.cursor/skills/{主題}/SKILL.md` 作為薄指引層：
  - frontmatter description 寫清楚觸發時機（相關 class／檔案／關鍵字）
  - 內文只放查詢指引（檔案位置、驗證過的 grep 模式、常用條目索引、注意事項），指向 `project-knowledge/04-reference/{主題}/`，不複製文件內容

## 原則

- 先讀 code 再寫；不記錄機密設定
- 改 code 後同步更新對應文件與 issue 狀態
