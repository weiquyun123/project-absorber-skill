# project-absorber · 大吞噬器

一个 Claude ​Code skill，自动把同类开源竞品的优点吸收进你的项目——让它成为整个赛道的「融合怪」。

## 它做什么

对任意项目运行大吞噬器，它会：

1. **读懂自己** — 扫描项目结构、技术栈、核心特性，识别已知弱项
2. **发现竞品** — 在 GitHub 搜索同类开源项目，按 Stars 排序筛选
3. **深度分析** — 浅层克隆竞品仓库，从 8 个维度逐项比对
4. **PM统筹计划** — 去重合并所有发现，全局重排优先级，生成可执行计划书
5. **逐项吸收** — 每项实施前征得你确认，完成后更新进度，再进入下一项

直到你的项目把所有竞品的优点都吸收完——再开始下一个竞品。

## Demo

真实运行案例：对 [quant-os](https://github.com/weiquyun123/quant-os)（一个 Claude ​Code 量化投研工作流 skill）跑了一遍。

**Phase 1 — 自我画像：**
```
✅ 自我画像完成
项目类型：AI agent 工具（Claude ​Code skill）
技术栈：Markdown + YAML（prompt 工程）
核心特性：5段路由（framing / 研报翻译 / A股审查 / 执行 / 复盘）
已知弱项：无会话状态 · 无任务追踪 · 无引导式启动 · 跨 worker 传递不规范
```

**Phase 2 — 竞品发现（11个候选 → 4个确认）：**
```
🔍 发现 4 个相关竞品：
1. Microsoft RD-Agent   (⭐ 12.4k) — 最成熟的 LLM 量化研究 orchestrator，有持久化机制
2. TradingAgents        (⭐ 48.5k) — 多 Agent 工作流，有会话状态和引导式启动
3. FinRobot             (⭐  6.6k) — Smart Scheduler 路由 + Synthesis 质控环节
4. QuantaAlpha          (⭐   623) — 自然语言→因子→验证闭环，最接近核心主张

确认此顺序？
```

**Phase 3 — 深度分析（3个竞品，每个8个维度）：**
```
📊 RD-Agent 发现：
  P0：KnowledgeBase 持久化 → 启发 state.json 会话协议
  P0：Trace 研究日志       → 启发 RESEARCH_BACKLOG.md（三态追踪）
  P1：失败记录结构化       → 启发执行合同里的结构化失败日志
  不吸收：dill/Docker（属于基础设施层，不该写进 Markdown skill）

📊 TradingAgents 发现：
  P0：AgentState 命名字段  → 启发交付物合约表
  P0：8步引导式启动        → 启发 first-run 检测 + 4问引导问卷
  P1：条件回流路由         → 启发路由回流条件声明
  ...
```

**Phase 4 — PM 计划书（13项，去重后）：**
```
📋 吸收计划书已生成

已分析 3 个竞品 · 发现 13 项可吸收特性：
  P0（立即做）：4 项
  P1（下轮迭代）：5 项
  P2（可选）：3 项
  不吸收：5 项（含原因）

P0 预览：
  PA-001  会话状态持久化（state.json）   | 来自：RD-Agent + TradingAgents | 难度：低
  PA-002  研究任务看板（三态追踪）       | 来自：RD-Agent                 | 难度：低
  PA-003  引导式启动问卷                | 来自：TradingAgents             | 难度：低
  PA-004  交付物合约表（类型化传递）     | 来自：TradingAgents             | 难度：低

开始执行？
```

**Phase 5 — 执行 PA-001（~30行加入 SKILL.md）：**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
准备实施 PA-001：会话状态协议
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
参考来源：RD-Agent KnowledgeBase + TradingAgents AgentState
效果：controller 启动时读取 .quant-os/state.json → 自动恢复上次会话
涉及文件：quant-os/SKILL.md（末尾追加约30行）

继续？✓

✅ PA-001 完成。进度：1/13 项（P0 剩余：3项）
下一项：PA-002 研究任务看板 | 难度：低
继续？
```

完整 demo 产物：[`quant-os/absorber-workspace/`](https://github.com/weiquyun123/quant-os/tree/main/absorber-workspace)

---

## 安装

**方式一：`.skill` 文件（推荐）**

从 [Releases](../../releases) 下载 `project-absorber.skill`，在 Claude ​Code 中安装。

**方式二：手动克隆**

```bash
git clone https://github.com/weiquyun123/project-absorber-skill \
  ~/.claude/skills/project-absorber
```

## 环境要求

- [Claude ​Code](https://claude.ai/code)（CLI 或 IDE 插件）
- Git（用于浅层克隆竞品仓库）
- Python 3.8+（用于 `repo_scanner.py`）

## 使用方法

进入你的项目目录，对 Claude ​Code 说：

```
开始吸收          # 从 Phase 1 开始
继续吸收          # 从上次中断处继续
大吞噬器          # 同上
帮我吸收竞品      # 触发词
absorb competitors  # 英文触发词也支持
```

也可以更具体：

```
分析这几个竞品：[GitHub URL1] [URL2]   # 直接指定竞品，跳过搜索
从 PA-003 开始执行                      # 从计划书某项开始
只做 P0 的项目                          # 只执行高优先级项目
```

## 工作原理

```
project-absorber/
├── SKILL.md                  # 主入口 — 5阶段完整工作流
├── phases/
│   ├── p1_self_scan.md       # 项目自扫描
│   ├── p2_discover.md        # 竞品发现策略
│   ├── p3_analyze.md         # 8维度分析框架
│   ├── p4_pm_plan.md         # PM去重 + 全局优先级排序
│   └── p5_execute.md         # 执行循环与确认机制
├── templates/
│   └── absorption_plan.md    # 计划书模板
└── scripts/
    └── repo_scanner.py       # 仓库结构快速扫描器
```

所有中间产物保存到项目根目录的 `absorber-workspace/`：

```
absorber-workspace/
├── self_profile.md           # 项目自我画像
├── competitor_list.md        # 确认后的竞品队列
├── [竞品名]/
│   └── analysis.md           # 逐项分析结果
└── ABSORPTION_PLAN.md        # 总计划书（实时更新进度）
```

克隆的竞品仓库存入 `/tmp/absorber/`，不会进入你的项目。

## 8个分析维度

对每个竞品，skill 从以下维度评估：

| # | 维度 | 关注点 |
|---|------|--------|
| 1 | 用户体验与接口 | CLI帮助质量、API一致性、onboarding 体验 |
| 2 | 配置与扩展性 | 配置文件格式、插件/钩子系统 |
| 3 | 错误处理与可观测性 | 错误提示质量、日志系统、指标监控 |
| 4 | 测试架构 | 覆盖策略、测试工具选型、数据管理 |
| 5 | 文档与开发者体验 | README结构、API文档、CONTRIBUTING |
| 6 | 性能与工程质量 | 缓存策略、并发处理、依赖精简 |
| 7 | 社区与生态 | Issue模板、Badge、社区集成 |
| 8 | 安全性 | 输入验证、敏感信息处理、权限控制 |

## 吸收原则

- **借鉴思路，不照抄代码** — 用你项目的代码风格重新实现
- **只采纳明确加分项** — 不是清晰优势的，进入「不吸收」清单并说明原因
- **特性级 + 模式级两种粒度** — 「加个插件系统」和「他们的错误提示会给修复建议」都算
- **诚实的 PM** — 风险或不兼容的项目如实标注，不强行塞入

## 安全机制

- 每项代码改动前都需要你明确确认
- 「高难度」项目无论模式如何，执行前必须确认
- 实施遇到阻碍时，停下来说明，不强行推进
- 竞品代码在 `/tmp/` 分析，不会混入你的项目

## License

MIT
