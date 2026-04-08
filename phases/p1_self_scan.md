# Phase 1：项目自扫描详细指令

## 目标
建立当前项目的完整「自我画像」，为后续竞品对比提供精确基准。

## 扫描顺序

### 1. 项目元信息
按优先级读取（找到即止）：
- `README.md` / `README.rst` / `README.txt`
- `package.json`（Node.js）→ 关注 name/description/scripts/dependencies
- `pyproject.toml` / `setup.py` / `setup.cfg`（Python）
- `Cargo.toml`（Rust）
- `go.mod`（Go）
- `pom.xml` / `build.gradle`（Java/Kotlin）
- `CLAUDE.md`（如有，了解项目约定）

### 2. 目录结构扫描
用 `ls -la` 或 Glob 扫描根目录及主要子目录（深度3层）。
识别：
- 源码目录（src/、lib/、pkg/ 等）
- 测试目录（test/、tests/、__tests__/ 等）
- 文档目录（docs/、doc/）
- 配置文件（.env.example、config/ 等）
- CI/CD（.github/workflows/、.gitlab-ci.yml 等）

### 3. 入口文件分析
找到并读取主入口：
- `src/main.*`、`src/index.*`、`src/app.*`
- `cmd/main.go`（Go）
- `__main__.py`（Python）
- CLI工具：找 `bin/`、`cli.*`

### 4. 核心模块识别
根据目录结构推断核心模块，读取每个模块的入口文件（不需要读全部代码，只看结构和接口）。

## 项目类型识别规则

| 特征 | 类型 |
|------|------|
| `bin/` + CLI框架依赖 | CLI工具 |
| Express/FastAPI/Gin等 | Web应用/API |
| 无main入口，主要export | 库/框架 |
| `.claude/`目录 + skill | Claude Agent工具 |
| Dockerfile + k8s配置 | 服务/平台 |

## 弱项识别清单

主动检查以下是否存在/完善：
- [ ] 单元测试覆盖
- [ ] 集成测试
- [ ] 文档（API文档、使用指南）
- [ ] 错误处理机制
- [ ] 日志系统
- [ ] 配置管理
- [ ] 插件/扩展机制
- [ ] CLI补全
- [ ] 性能监控/指标
- [ ] 国际化
- [ ] 贡献者指南/CONTRIBUTING.md

## 搜索关键词生成规则

生成3-5组关键词，格式：
- 功能描述词（如 `code review tool`）
- 技术栈词（如 `python cli tool`）
- 领域词（如 `ai agent framework`）

用于Phase 2的GitHub搜索。
