# Skill Vet — AI Agent 技能安全审查协议

> **偏执是一种特质。** 🔒🦀

一套结构化、可重复执行的 AI Agent 技能安全审查协议 —— 专为 Hermes Agent 生态系统设计，同时适用于任何基于技能（skill-based）的 AI Agent 系统。

## 功能说明

Skill Vet 不是扫描器 —— 它是一个**人工介入的审查协议**。它提供逐步检查清单，让你在安装任何技能前进行手动审查，能发现：

- 凭证/访问令牌泄露模式
- 向未知端点的恶意网络请求
- 混淆或动态执行的代码
- 过度授权的文件或系统访问
- 可疑的依赖安装

## 快速开始

### Agent 使用方式（Hermes）

作为技能加载到 Hermes Agent：

```
skills/
└── software-development/
    └── skill-vetter/
        ├── SKILL.md           ← 主要协议文档
        └── references/
            └── red-flags.md   ← 红旗模式参考
```

告诉 agent 在安装任何技能前进行审查即可激活。

### CLI 使用方式

```bash
# 审查来自 GitHub 的技能
curl -s "https://raw.githubusercontent.com/YOURREPO/main/skills/SKILL_NAME/SKILL.md"

# 检查仓库元数据
curl -s "https://api.github.com/repos/OWNER/REPO" | jq '{stars: .stargazers_count, updated: .updated_at}'
```

## 审查协议（5 步）

```
第 1 步：来源检查        — 这个技能从哪里来的？
第 2 步：阅读所有文件     — SKILL.md + 脚本 + 参考文档
第 3 步：红旗清单检查     — 即时拒绝模式
第 4 步：权限审计        — 它实际需要什么权限？
第 5 步：风险分类        — LOW / MEDIUM / HIGH / EXTREME
```

完整协议请参阅 [SKILL.md](SKILL.md)。

## 信任层级

| 来源 | 审查级别 |
|------|---------|
| Hermes 仓库内技能 | 最小审查 |
| 高星标官方仓库（1000+） | 轻度审查 |
| 知名/实名作者 | 中度审查 |
| 新/未知来源 | 最高审查 |
| 任何请求凭证的技能 | **必须人工审批** |

## 核心原则

> **没有任何技能值得牺牲安全。当有疑问时，不要安装 —— 询问你的主人。**

## 文件结构

```
skill-vetter/
├── SKILL.md                    # 主要审查协议
├── references/
│   └── red-flags.md           # 红旗模式参考
├── scripts/
│   └── vet_report_template.py # （可选）报告生成器
├── .github/
│   └── workflows/
│       └── ci.yml             # 基本验证
├── LICENSE
└── README.md / README_zh.md    # 中英文说明文档
```

## 参与贡献

发现新的攻击模式？提交 issue 或 PR。这是一个活文档 —— 威胁模式在不断演变。

## 许可证

MIT
