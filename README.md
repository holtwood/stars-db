# ⭐ Stars Index

> 📚 我的 GitHub Star 项目分类索引 · 共 **1317** 个项目 · 已分类 **1317** 个
> 
> 由脚本从 GitHub API 自动生成，与我的 [Star Lists](https://github.com/LessUp?tab=stars) 保持同步

## 📑 分类导航

| 分类 | 文档 | 项目数 |
|------|------|--------|
| 🤖 AI 与 LLM | [链接](./ai.md) | 308 |
| ☁️ DevOps 与云原生 | [链接](./devops.md) | 26 |
| 🧩 语言生态 | [链接](./lang.md) | 259 |
| 🎨 前端与 Web | [链接](./frontend.md) | 86 |
| ⌨️ CLI 与终端 | [链接](./cli.md) | 129 |
| 🗄️ 数据库与存储 | [链接](./storage.md) | 13 |
| 🔐 安全与逆向 | [链接](./security.md) | 3 |
| 🌐 网络与代理 | [链接](./net.md) | 40 |
| 🎬 图形与音视频 | [链接](./multimedia.md) | 20 |
| 🧩 浏览器扩展 | [链接](./browser.md) | 11 |
| 📱 移动开发 | [链接](./mobile.md) | 12 |
| 📝 编辑器与文档笔记 | [链接](./docs.md) | 34 |
| 🧮 算法与面试 | [链接](./algo.md) | 80 |
| ⚡ 高性能计算 | [链接](./hpc.md) | 5 |
| 🗜️ 压缩与编码 | [链接](./compression.md) | 3 |
| 🧬 生物信息 | [链接](./bio.md) | 51 |
| 📚 学习资源与清单 | [链接](./learning.md) | 225 |
| 🎯 面试资料 | [链接](./interview.md) | 15 |
| 📦 其他与杂项 | [链接](./misc.md) | 15 |

## 📌 关于

这个仓库是我在 GitHub 上 star 过的所有项目的分类索引，目的是：

- 🧭 快速导航：按领域找到我收藏过的项目
- 📖 学习路径：按分类浏览，了解技术全景
- 🔄 持续同步：新增 star 后可运行脚本重新生成

## 🔄 如何更新

```bash
gh api --paginate 'user/starred?per_page=100' --jq '.[] | {id, node_id, full_name, description, language, topics, stargazers_count, fork, archived, html_url}' > starred_full.json
python3 gen_index.py
```
