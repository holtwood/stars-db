#!/usr/bin/env python3
"""生成 stars-index 索引仓库内容（从 GitHub API 拉取的 star 数据）"""
import json, re

# ---------- 加载数据 ----------
repos = []
with open('starred_full.json') as f:
    for line in f:
        line = line.strip()
        if line:
            repos.append(json.loads(line))

# ---------- 加载 lists 归属 ----------
list_items = json.load(open('list_items.json'))
lists_meta = {l['id']: l for l in json.load(open('lists_meta.json'))}
name2id = {l['name']: l['id'] for l in lists_meta.values()}
# repo -> [list名]
repo_lists = {}
for lid, items in list_items.items():
    for item in items:
        repo_lists.setdefault(item, []).append(lists_meta[lid]['name'])

repo_by_name = {r['full_name']: r for r in repos}

# ---------- 分类配置（对齐 28 个 list，按领域分组） ----------
CATEGORIES = [
    {
        'key': 'ai', 'title': 'AI 与 LLM', 'emoji': '🤖',
        'desc': '大模型、训练/推理框架、Agent、MCP 生态',
        'lists': ['AI与LLM', 'AI-Agent与MCP', 'AI-Infra'],
    },
    {
        'key': 'devops', 'title': 'DevOps 与云原生', 'emoji': '☁️',
        'desc': '容器、编排、CI/CD、自托管',
        'lists': ['DevOps与云原生'],
    },
    {
        'key': 'lang', 'title': '语言生态', 'emoji': '🧩',
        'desc': 'Python / Go / Rust / C++ / JVM 等语言库与工具',
        'lists': ['Python生态', 'Go生态', 'Rust生态', 'Modern-C++', 'JVM与其他语言'],
    },
    {
        'key': 'frontend', 'title': '前端与 Web', 'emoji': '🎨',
        'desc': '前端框架、Web 应用与资源',
        'lists': ['前端与Web'],
    },
    {
        'key': 'cli', 'title': 'CLI 与终端', 'emoji': '⌨️',
        'desc': '命令行工具、终端效率、系统与桌面工具',
        'lists': ['CLI与终端工具', '系统与桌面工具', '主题与字体'],
    },
    {
        'key': 'storage', 'title': '数据库与存储', 'emoji': '🗄️',
        'desc': '数据库、缓存与存储系统',
        'lists': ['数据库与存储'],
    },
    {
        'key': 'security', 'title': '安全与逆向', 'emoji': '🔐',
        'desc': '安全工具、逆向工程、隐私',
        'lists': ['安全与逆向'],
    },
    {
        'key': 'net', 'title': '网络与代理', 'emoji': '🌐',
        'desc': '代理客户端、规则集与网络工具',
        'lists': ['网络与代理'],
    },
    {
        'key': 'multimedia', 'title': '图形与音视频', 'emoji': '🎬',
        'desc': '图形、图像、音频、视频处理',
        'lists': ['图形与音视频'],
    },
    {
        'key': 'browser', 'title': '浏览器扩展', 'emoji': '🧩',
        'desc': '浏览器扩展与用户脚本',
        'lists': ['浏览器扩展'],
    },
    {
        'key': 'mobile', 'title': '移动开发', 'emoji': '📱',
        'desc': 'Android / iOS / 跨平台移动开发',
        'lists': ['移动开发'],
    },
    {
        'key': 'docs', 'title': '编辑器与文档笔记', 'emoji': '📝',
        'desc': '编辑器、Markdown、笔记与知识管理',
        'lists': ['编辑器与文档笔记'],
    },
    {
        'key': 'algo', 'title': '算法与面试', 'emoji': '🧮',
        'desc': '算法题、面试准备、竞赛编程',
        'lists': ['算法与面试'],
    },
    {
        'key': 'hpc', 'title': '高性能计算', 'emoji': '⚡',
        'desc': 'HPC、CUDA/GPU 计算、性能优化',
        'lists': ['高性能计算'],
    },
    {
        'key': 'compression', 'title': '压缩与编码', 'emoji': '🗜️',
        'desc': '压缩算法与编码库',
        'lists': ['压缩与编码'],
    },
    {
        'key': 'bio', 'title': '生物信息', 'emoji': '🧬',
        'desc': '生物信息学算法与工具',
        'lists': ['BioInfoAlgo'],
    },
    {
        'key': 'learning', 'title': '学习资源与清单', 'emoji': '📚',
        'desc': '教程、书籍、awesome 清单、学习路线',
        'lists': ['学习资源与清单'],
    },
    {
        'key': 'interview', 'title': '面试资料', 'emoji': '🎯',
        'desc': '面试资料专项',
        'lists': ['面试资料'],
    },
    {
        'key': 'misc', 'title': '其他与杂项', 'emoji': '📦',
        'desc': '未归类与杂项',
        'lists': ['其他与杂项'],
    },
]

def star(n):
    if n >= 1000:
        return f"{n/1000:.1f}k"
    return str(n)

def esc(text):
    if not text:
        return ''
    # 清理 markdown 表格特殊字符
    return text.replace('|', '\\|').replace('\n', ' ').strip()

def repo_md(r):
    desc = esc(r.get('description') or '')
    lang = r.get('language') or ''
    return f"| [{r['full_name']}]({r['html_url']}) | ⭐ {star(r['stargazers_count'])} | {lang} | {desc} |"

# ---------- 生成各分类 md 文件 ----------
files = {}
all_counts = {}
for cat in CATEGORIES:
    items = []
    seen = set()
    for lst in cat['lists']:
        for name in repo_lists:
            if lst in repo_lists[name] and name not in seen:
                seen.add(name)
                r = repo_by_name.get(name)
                if r:
                    items.append(r)
    items.sort(key=lambda x: -x['stargazers_count'])
    all_counts[cat['key']] = len(items)

    lines = [f"# {cat['emoji']} {cat['title']}", "",
             f"> {cat['desc']}", "",
             f"共 **{len(items)}** 个项目，按 ⭐ 数排序", "",
             "| 项目 | 星数 | 语言 | 描述 |",
             "|------|------|------|------|"]
    for r in items:
        lines.append(repo_md(r))
    files[cat['key']] = '\n'.join(lines) + '\n'

# ---------- 生成 README ----------
total = len(repos)
categorized = len(repo_lists)

readme = []
readme.append("# ⭐ Stars Index")
readme.append("")
readme.append(f"> 📚 我的 GitHub Star 项目分类索引 · 共 **{total}** 个项目 · 已分类 **{categorized}** 个")
readme.append("> ")
readme.append("> 由脚本从 GitHub API 自动生成，与我的 [Star Lists](https://github.com/LessUp?tab=stars) 保持同步")
readme.append("")
readme.append("## 📑 分类导航")
readme.append("")
readme.append("| 分类 | 文档 | 项目数 |")
readme.append("|------|------|--------|")
for cat in CATEGORIES:
    readme.append(f"| {cat['emoji']} {cat['title']} | [链接](./{cat['key']}.md) | {all_counts[cat['key']]} |")
readme.append("")
readme.append("## 📌 关于")
readme.append("")
readme.append("这个仓库是我在 GitHub 上 star 过的所有项目的分类索引，目的是：")
readme.append("")
readme.append("- 🧭 快速导航：按领域找到我收藏过的项目")
readme.append("- 📖 学习路径：按分类浏览，了解技术全景")
readme.append("- 🔄 持续同步：新增 star 后可运行脚本重新生成")
readme.append("")
readme.append("## 🔄 如何更新")
readme.append("")
readme.append("```bash")
readme.append("gh api --paginate 'user/starred?per_page=100' --jq '.[] | {id, node_id, full_name, description, language, topics, stargazers_count, fork, archived, html_url}' > starred_full.json")
readme.append("python3 gen_index.py")
readme.append("```")
readme.append("")

with open('README.md', 'w') as f:
    f.write('\n'.join(readme))
for key, content in files.items():
    with open(f'{key}.md', 'w') as f:
        f.write(content)

print(f"README.md 和 {len(files)} 个分类文件已生成")
print(f"总项目: {total}, 已分类: {categorized}")
for cat in CATEGORIES:
    print(f"  {cat['key']}: {all_counts[cat['key']]}")
