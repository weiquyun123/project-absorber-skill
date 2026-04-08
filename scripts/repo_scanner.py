#!/usr/bin/env python3
"""
repo_scanner.py - 快速扫描仓库目录结构

用法：
  python repo_scanner.py [目录路径] [--depth N] [--format text|json]

输出：
  - 目录树（默认深度3层）
  - 识别的项目类型
  - 关键文件列表

在 project-absorber Phase 1 和 Phase 3 中使用，避免每次手动列目录。
"""

import os
import sys
import json
import argparse
from pathlib import Path

# 项目类型识别规则（文件/目录 → 类型）
PROJECT_SIGNALS = {
    "cli": ["bin/", "cli.py", "cli.ts", "cli.js", "cmd/", "__main__.py"],
    "web_app": ["app.py", "app.ts", "app.js", "server.py", "server.ts",
                "routes/", "controllers/", "views/", "templates/"],
    "library": ["src/lib/", "src/index.ts", "src/index.js", "lib/", "index.py"],
    "agent_tool": [".claude/", "SKILL.md", "skills/", "hooks/"],
    "api_service": ["api/", "swagger.yaml", "openapi.yaml", "routes/api/"],
}

# 忽略的目录（噪声）
IGNORE_DIRS = {
    ".git", "node_modules", "__pycache__", ".venv", "venv", "env",
    "dist", "build", ".next", ".nuxt", "target", "vendor",
    ".idea", ".vscode", "coverage", ".pytest_cache", ".mypy_cache",
}

# 忽略的文件扩展名
IGNORE_EXTENSIONS = {
    ".pyc", ".pyo", ".class", ".o", ".so", ".dylib",
    ".jpg", ".jpeg", ".png", ".gif", ".ico", ".svg",
    ".mp4", ".mp3", ".zip", ".tar", ".gz",
}

# 关键文件（优先显示）
KEY_FILES = {
    "readme": ["README.md", "README.rst", "README.txt", "README"],
    "config": ["package.json", "pyproject.toml", "setup.py", "Cargo.toml",
               "go.mod", "pom.xml", "build.gradle", "Makefile"],
    "claude": ["CLAUDE.md", ".claude/"],
    "ci": [".github/workflows/", ".gitlab-ci.yml", ".circleci/"],
    "docker": ["Dockerfile", "docker-compose.yml", "docker-compose.yaml"],
    "entry": ["main.py", "main.ts", "main.js", "main.go", "main.rs",
              "index.py", "index.ts", "index.js", "app.py", "app.ts"],
}


def should_ignore(path: Path) -> bool:
    """判断是否应该跳过这个路径"""
    if path.name in IGNORE_DIRS:
        return True
    if path.suffix in IGNORE_EXTENSIONS:
        return True
    if path.name.startswith(".") and path.name not in {".github", ".claude", ".env.example"}:
        return True
    return False


def scan_tree(root: Path, depth: int, max_depth: int, prefix: str = "") -> list[str]:
    """递归扫描目录树"""
    if depth > max_depth:
        return []

    lines = []
    try:
        entries = sorted(root.iterdir(), key=lambda x: (x.is_file(), x.name.lower()))
    except PermissionError:
        return [f"{prefix}[权限不足]"]

    visible = [e for e in entries if not should_ignore(e)]

    for i, entry in enumerate(visible):
        is_last = i == len(visible) - 1
        connector = "└── " if is_last else "├── "
        ext = "/ " if entry.is_dir() else ""
        lines.append(f"{prefix}{connector}{entry.name}{ext}")

        if entry.is_dir() and depth < max_depth:
            child_prefix = prefix + ("    " if is_last else "│   ")
            lines.extend(scan_tree(entry, depth + 1, max_depth, child_prefix))

    return lines


def detect_project_type(root: Path) -> list[str]:
    """识别项目类型"""
    detected = []
    all_files = set()

    for item in root.rglob("*"):
        if not should_ignore(item):
            rel = str(item.relative_to(root))
            all_files.add(rel)
            all_files.add(item.name)

    for proj_type, signals in PROJECT_SIGNALS.items():
        for signal in signals:
            if any(signal in f for f in all_files):
                detected.append(proj_type)
                break

    return detected if detected else ["unknown"]


def find_key_files(root: Path) -> dict:
    """找出关键文件"""
    found = {}
    for category, candidates in KEY_FILES.items():
        for candidate in candidates:
            target = root / candidate
            if target.exists():
                found[category] = str(target.relative_to(root))
                break
    return found


def detect_tech_stack(root: Path) -> list[str]:
    """从配置文件推断技术栈"""
    stack = []
    checks = {
        "Node.js/TypeScript": ["package.json", "tsconfig.json"],
        "Python": ["pyproject.toml", "setup.py", "requirements.txt"],
        "Rust": ["Cargo.toml"],
        "Go": ["go.mod"],
        "Java": ["pom.xml", "build.gradle"],
        "Ruby": ["Gemfile"],
        "PHP": ["composer.json"],
    }
    for tech, files in checks.items():
        if any((root / f).exists() for f in files):
            stack.append(tech)
    return stack if stack else ["未知"]


def suggest_search_keywords(project_types: list[str], tech_stack: list[str], root: Path) -> list[str]:
    """生成竞品搜索关键词建议"""
    keywords = []

    # 读取README摘要
    for readme_name in ["README.md", "README.rst", "README.txt"]:
        readme = root / readme_name
        if readme.exists():
            try:
                content = readme.read_text(errors="ignore")[:500]
                first_line = content.split("\n")[0].strip("# ").strip()
                if first_line:
                    keywords.append(first_line)
            except Exception:
                pass
            break

    # 基于项目类型
    type_keywords = {
        "cli": "command line tool",
        "web_app": "web application framework",
        "library": "library",
        "agent_tool": "AI agent tool claude",
        "api_service": "API service",
    }
    for pt in project_types:
        if pt in type_keywords:
            keywords.append(type_keywords[pt])

    # 基于技术栈
    for tech in tech_stack:
        lang = tech.split("/")[0]
        keywords.append(f"{lang} {project_types[0] if project_types else 'tool'}")

    return keywords[:5]  # 最多5组


def main():
    parser = argparse.ArgumentParser(description="仓库结构快速扫描器")
    parser.add_argument("path", nargs="?", default=".", help="要扫描的目录（默认当前目录）")
    parser.add_argument("--depth", type=int, default=3, help="扫描深度（默认3）")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="输出格式")
    args = parser.parse_args()

    root = Path(args.path).resolve()
    if not root.exists():
        print(f"错误：路径不存在 {root}", file=sys.stderr)
        sys.exit(1)

    project_types = detect_project_type(root)
    tech_stack = detect_tech_stack(root)
    key_files = find_key_files(root)
    keywords = suggest_search_keywords(project_types, tech_stack, root)
    tree_lines = scan_tree(root, 1, args.depth)

    if args.format == "json":
        result = {
            "root": str(root),
            "project_types": project_types,
            "tech_stack": tech_stack,
            "key_files": key_files,
            "search_keywords": keywords,
            "tree": tree_lines,
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"\n{'='*50}")
        print(f"📁 项目扫描报告：{root.name}")
        print(f"{'='*50}")
        print(f"\n🏷️  项目类型：{', '.join(project_types)}")
        print(f"🔧 技术栈：{', '.join(tech_stack)}")

        if key_files:
            print(f"\n📌 关键文件：")
            for category, path in key_files.items():
                print(f"   {category}: {path}")

        print(f"\n📂 目录结构（深度 {args.depth}）：")
        print(f"{root.name}/")
        for line in tree_lines:
            print(line)

        print(f"\n🔍 搜索关键词建议（用于竞品发现）：")
        for kw in keywords:
            print(f"   - {kw}")
        print()


if __name__ == "__main__":
    main()
