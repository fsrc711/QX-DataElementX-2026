# Project Memory — 多AI协同记忆方案

## 定位

独立于任何AI之外的"项目记忆中心"，所有AI（星期五/WorkBuddy、ChatGPT/GPT、Claude 等）共享同一套 Markdown 文件。
工作前先读，工作后更新。**不依赖聊天记录。**

## 目录结构

```
project-memory/
├── README.md              ← 协议说明（本文件）
├── CURRENT_STATE.md       ← 项目唯一状态入口
├── TASKS.md               ← 任务看板
├── DECISIONS.md           ← 决策日志（append-only）
├── HANDOFF.md             ← AI交接记录（append-only）
└── CONTEXT_SUMMARY.md     ← 长期上下文压缩
```

## 协同规则

### 工作前（任何AI）
读取顺序：
1. CURRENT_STATE.md — 了解项目当前状态和焦点
2. CONTEXT_SUMMARY.md — 快速获取历史上下文（如果存在）
3. 最近若干条 HANDOFF.md — 了解最近发生了什么
4. 最近若干条 DECISIONS.md — 了解关键决策及其原因

### 工作中
重要决策立即写入 DECISIONS.md（append-only）

### 工作后
- 更新 CURRENT_STATE.md（当前焦点、进度、风险）
- 更新 TASKS.md（任务状态变更）
- 追加 HANDOFF.md（本次完成、发现问题、建议下一步、注意事项）

## 设计原则

1. **Single Source of Truth** — 项目真实状态只存在于 Memory 文件中
2. **Append-only History** — HANDOFF 与 DECISIONS 不覆盖历史，只追加
3. **Context Compression** — 通过 CONTEXT_SUMMARY 持续压缩历史，减少新AI的阅读负担
4. **AI-Agnostic** — 适用于 ChatGPT、WorkBuddy、Claude、Gemini 等任何AI

## Git 仓库

- GitHub: （待创建）
- 路径：project-memory/
- 更新方式：星期五通过 git 自动推送，ChatGPT/GPT 通过 Raw 链接读取
