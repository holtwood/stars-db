# ⭐ Stars Index

> 我的 GitHub Star 分类索引 · 由脚本自动生成 · 与 [Star Lists](https://github.com/LessUp?tab=stars) 同步

![项目数](https://img.shields.io/badge/Star_项目-1317-8A2BE2) ![最后同步](https://img.shields.io/badge/最后同步-2026--08--21-2ea44f) ![自动更新](https://img.shields.io/badge/自动更新-GitHub_Actions-007ec6)

> 📈 **1317** 个项目 · **19** 个分类 · **28** 个 Star Lists · 每日自动同步

## 📑 分类导航

| 分类 | 项目数 | 占比 | 文档 |
|------|--------|------|------|
| 🤖 AI 与 LLM | 308 | `████░░░░░░░░░░░░` (23%) | [docs/ai.md](docs/ai.md) |
| ☁️ DevOps 与云原生 | 26 | `█░░░░░░░░░░░░░░░` (2%) | [docs/devops.md](docs/devops.md) |
| 🧩 语言生态 | 259 | `███░░░░░░░░░░░░░` (20%) | [docs/lang.md](docs/lang.md) |
| 🎨 前端与 Web | 86 | `█░░░░░░░░░░░░░░░` (7%) | [docs/frontend.md](docs/frontend.md) |
| ⌨️ CLI 与终端 | 129 | `██░░░░░░░░░░░░░░` (10%) | [docs/cli.md](docs/cli.md) |
| 🗄️ 数据库与存储 | 13 | `█░░░░░░░░░░░░░░░` (1%) | [docs/storage.md](docs/storage.md) |
| 🔐 安全与逆向 | 3 | `█░░░░░░░░░░░░░░░` (0%) | [docs/security.md](docs/security.md) |
| 🌐 网络与代理 | 40 | `█░░░░░░░░░░░░░░░` (3%) | [docs/net.md](docs/net.md) |
| 🎬 图形与音视频 | 20 | `█░░░░░░░░░░░░░░░` (2%) | [docs/multimedia.md](docs/multimedia.md) |
| 🧩 浏览器扩展 | 11 | `█░░░░░░░░░░░░░░░` (1%) | [docs/browser.md](docs/browser.md) |
| 📱 移动开发 | 12 | `█░░░░░░░░░░░░░░░` (1%) | [docs/mobile.md](docs/mobile.md) |
| 📝 编辑器与文档笔记 | 34 | `█░░░░░░░░░░░░░░░` (3%) | [docs/notes.md](docs/notes.md) |
| 🧮 算法与面试 | 80 | `█░░░░░░░░░░░░░░░` (6%) | [docs/algo.md](docs/algo.md) |
| ⚡ 高性能计算 | 5 | `█░░░░░░░░░░░░░░░` (0%) | [docs/hpc.md](docs/hpc.md) |
| 🗜️ 压缩与编码 | 3 | `█░░░░░░░░░░░░░░░` (0%) | [docs/compression.md](docs/compression.md) |
| 🧬 生物信息 | 51 | `█░░░░░░░░░░░░░░░` (4%) | [docs/bio.md](docs/bio.md) |
| 📚 学习资源与清单 | 225 | `███░░░░░░░░░░░░░` (17%) | [docs/learning.md](docs/learning.md) |
| 🎯 面试资料 | 15 | `█░░░░░░░░░░░░░░░` (1%) | [docs/interview.md](docs/interview.md) |
| 📦 其他与杂项 | 20 | `█░░░░░░░░░░░░░░░` (2%) | [docs/misc.md](docs/misc.md) |

## 📊 快速入口

- 📦 [全量索引(1317)](docs/all.md) — 所有项目按 ⭐ 排序
- 🗣️ [按语言浏览](docs/by-language.md) — 语言分布一览

## 🔄 自动同步

本仓库由 [GitHub Actions](.github/workflows/sync.yml) 每日自动拉取最新的 Star 数据并重新生成,也可在 Actions 页面手动触发 `workflow_dispatch`。

### 本地手动更新

```bash
# 1. 拉取 stars 数据(需要 GitHub 认证)
bash scripts/fetch_stars.sh
# 2. 拉取 Star Lists 归属(需要认证)
python3 scripts/fetch_lists.py
# 3. 重新生成 README 与 docs/
python3 scripts/gen_index.py
```

