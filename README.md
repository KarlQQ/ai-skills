# ai-skills

公開的 AI Agent Skills 集合。每個 skill 一個子目錄，內含 `SKILL.md`。

## 目錄

```
ai-skills/
├── README.md
└── skills/
    ├── _template/              # 新增 skill 時複製此目錄
    └── {skill-name}/
        └── SKILL.md            # 必要
```

## 給 AI Agent

1. 讀取 `skills/` 下各子目錄的 `SKILL.md`
2. 依各平台慣例安裝到本機（例如 Cursor：`~/.cursor/skills/`；Claude Code：`~/.claude/skills/`）
3. 執行 skill 內的工作流

## Skill 清單

| Skill | 說明 |
|-------|------|
| [project-knowledge](./skills/project-knowledge/) | 專案工程知識庫：代碼分析、需求與 issue 歸檔 |

## 新增 Skill

複製 `skills/_template/` 為 `skills/新名稱/`，編輯 `SKILL.md`（`name` 須與目錄名相同）。
