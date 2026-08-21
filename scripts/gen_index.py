#!/usr/bin/env python3
"""生成 stars-index 索引仓库内容(从 data/ 下的 GitHub API 数据)

数据管线:
  scripts/fetch_stars.sh  → data/starred_full.json   (JSONL,每行一个 repo)
  scripts/fetch_lists.py  → data/list_items.json     (list_id → [repo名])
  scripts/gen_index.py    → README.md + docs/*.md     (本脚本)

用法:
  python3 scripts/gen_index.py
"""
import json
import sys
from collections import Counter

from config import CATEGORIES, ALL_INDEX, LANG_INDEX, OWNER, REPO, STAR_LISTS_URL, today

DATA_DIR = 'data'
DOCS_DIR = 'docs'

# ---------- 加载数据 ----------
def load_repos():
    repos = []
    with open(f'{DATA_DIR}/starred_full.json') as f:
        for line in f:
            line = line.strip()
            if line:
                repos.append(json.loads(line))
    return repos


def load_lists():
    list_items = json.load(open(f'{DATA_DIR}/list_items.json'))
    lists_meta = {l['id']: l for l in json.load(open(f'{DATA_DIR}/lists_meta.json'))}
    name2id = {l['name']: l['id'] for l in lists_meta.values()}
    # repo -> [list名] 与 反向映射 list名 -> [repo名]
    repo_lists = {}
    list_repos = {}
    for lid, items in list_items.items():
        name = lists_meta[lid]['name']
        for item in items:
            repo_lists.setdefault(item, []).append(name)
            list_repos.setdefault(name, []).append(item)
    return repo_lists, list_repos, name2id


# ---------- 格式化工具 ----------
def star(n):
    if n >= 1000:
        return f"{n/1000:.1f}k"
    return str(n)


def esc(text):
    if not text:
        return ''
    # 清理 markdown 表格特殊字符
    return text.replace('|', '\\|').replace('\n', ' ').strip()


def status_of(r):
    """返回仓库活跃状态标记:🟢 活跃 / 🟡 已归档 / 🔀 分叉"""
    if r.get('archived'):
        return '🟡 已归档'
    if r.get('fork'):
        return '🔀 分叉'
    return '🟢 活跃'


def repo_row(r):
    desc = esc(r.get('description') or '')
    lang = esc(r.get('language') or '')
    return (f"| [{r['full_name']}]({r['html_url']}) | ⭐ {star(r['stargazers_count'])} "
            f"| {lang} | {status_of(r)} | {desc} |")


def bar(ratio, width=16):
    """ASCII 占比条,例如 ratio=0.37 → '██████████░░░░░░';非零占比至少显示一格"""
    filled = round(ratio * width)
    if ratio > 0 and filled == 0:
        filled = 1
    return '█' * filled + '░' * (width - filled)


def badge(label, value, color):
    """shields.io 静态徽章 URL(label-value 用 -- 分隔,空格转义)"""
    label = label.replace('-', '--').replace(' ', '_')
    value = value.replace('-', '--').replace(' ', '_')
    return f"https://img.shields.io/badge/{label}-{value}-{color}"


# ---------- 数据一致性校验 ----------
def verify_consistency(repos, list_repos, counts):
    problems = []
    total = len(repos)
    sum_cats = sum(counts.values())

    # 每个 repo 必须至少属于一个分类
    covered = set()
    for cat in CATEGORIES:
        for lst in cat['lists']:
            covered.update(list_repos.get(lst, []))
    missing = [r['full_name'] for r in repos if r['full_name'] not in covered]
    if missing:
        problems.append(f"{len(missing)} 个 repo 未被任何分类覆盖,例如: {missing[:3]}")

    # 分类之和允许 > 总数:一个 repo 可同时属于多个分类(如同时属 Python生态 与 AI与LLM)
    if sum_cats < total:
        problems.append(f"分类之和 {sum_cats} < 仓库总数 {total}")

    if problems:
        print('⚠️  数据一致性检查失败:')
        for p in problems:
            print('   -', p)
        sys.exit(1)

    overlap = sum_cats - total
    print(f'✅ 数据一致性校验通过: {total} 个仓库全部被覆盖')
    if overlap:
        print(f'ℹ️  有 {overlap} 个 repo 同时属于多个分类(正常现象,会重复出现在各分类页)')


# ---------- 生成分类页 ----------
def build_category_files(repos_by_name, list_repos, counts):
    files = {}
    for cat in CATEGORIES:
        items = []
        seen = set()
        for lst in cat['lists']:
            for name in list_repos.get(lst, []):
                if name not in seen:
                    seen.add(name)
                    r = repos_by_name.get(name)
                    if r:
                        items.append(r)
        items.sort(key=lambda x: -x['stargazers_count'])
        counts[cat['key']] = len(items)

        lines = [
            f"# {cat['emoji']} {cat['title']}",
            "",
            f"> {cat['desc']}",
            "",
            f"共 **{len(items)}** 个项目,按 ⭐ 数排序",
            "",
            "| 项目 | 星数 | 语言 | 状态 | 描述 |",
            "|------|------|------|------|------|",
        ]
        for r in items:
            lines.append(repo_row(r))
        lines += ["", "---", "[⬆ 返回顶部](#top)"]
        files[cat['key']] = '\n'.join(lines) + '\n'
    return files


# ---------- 生成全量索引 all.md ----------
def build_all_index(repos):
    items = sorted(repos, key=lambda x: -x['stargazers_count'])
    lines = [
        "# 📦 全量索引",
        "",
        f"> 全部 **{len(items)}** 个 Star 项目,按 ⭐ 数排序",
        "",
        "| 项目 | 星数 | 语言 | 状态 | 描述 |",
        "|------|------|------|------|------|",
    ]
    for r in items:
        lines.append(repo_row(r))
    lines += ["", "---", "[⬆ 返回顶部](#top)"]
    return '\n'.join(lines) + '\n'


# ---------- 生成按语言索引 by-language.md ----------
def build_lang_index(repos):
    by_lang = Counter(r.get('language') or '未标注' for r in repos)
    lines = [
        "# 🗣️ 按语言浏览",
        "",
        f"> 全部 **{len(repos)}** 个项目按语言分组,共 {len(by_lang)} 种语言",
        "",
        "| 语言 | 项目数 | 占比 |",
        "|------|--------|------|",
    ]
    for lang, cnt in by_lang.most_common():
        lines.append(f"| {esc(lang)} | {cnt} | {bar(cnt / len(repos))} |")
    lines += ["", "---", "[⬆ 返回顶部](#top)"]
    return '\n'.join(lines) + '\n'


# ---------- 生成 README ----------
def build_readme(total, counts, list_count):
    readme = []
    today_str = today()
    readme.append("# ⭐ Stars Index")
    readme.append("")
    readme.append("> 我的 GitHub Star 分类索引 · 由脚本自动生成 · 与 [Star Lists](https://github.com/LessUp?tab=stars) 同步")
    readme.append("")
    readme.append(f"![项目数]({badge('Star 项目', str(total), '8A2BE2')}) "
                  f"![最后同步]({badge('最后同步', today_str, '2ea44f')}) "
                  f"![自动更新]({badge('自动更新', 'GitHub Actions', '007ec6')})")
    readme.append("")
    readme.append(f"> 📈 **{total}** 个项目 · **{len(CATEGORIES)}** 个分类 · **{list_count}** 个 Star Lists · 每日自动同步")
    readme.append("")
    readme.append("## 📑 分类导航")
    readme.append("")
    readme.append("| 分类 | 项目数 | 占比 | 文档 |")
    readme.append("|------|--------|------|------|")
    for cat in CATEGORIES:
        cnt = counts[cat['key']]
        ratio = cnt / total if total else 0
        readme.append(f"| {cat['emoji']} {cat['title']} | {cnt} | `{bar(ratio)}` "
                      f"({ratio*100:.0f}%) | [docs/{cat['key']}.md](docs/{cat['key']}.md) |")
    readme.append("")
    readme.append("## 📊 快速入口")
    readme.append("")
    readme.append(f"- 📦 [全量索引({total})](docs/{ALL_INDEX}) — 所有项目按 ⭐ 排序")
    readme.append(f"- 🗣️ [按语言浏览](docs/{LANG_INDEX}) — 语言分布一览")
    readme.append("")
    readme.append("## 🔄 自动同步")
    readme.append("")
    readme.append("本仓库由 [GitHub Actions](.github/workflows/sync.yml) 每日自动拉取最新的 Star 数据并重新生成,"
                  "也可在 Actions 页面手动触发 `workflow_dispatch`。")
    readme.append("")
    readme.append("### 本地手动更新")
    readme.append("")
    readme.append("```bash")
    readme.append("# 1. 拉取 stars 数据(需要 GitHub 认证)")
    readme.append("bash scripts/fetch_stars.sh")
    readme.append("# 2. 拉取 Star Lists 归属(需要认证)")
    readme.append("python3 scripts/fetch_lists.py")
    readme.append("# 3. 重新生成 README 与 docs/")
    readme.append("python3 scripts/gen_index.py")
    readme.append("```")
    readme.append("")
    return '\n'.join(readme) + '\n'


# ---------- 主流程 ----------
def main():
    repos = load_repos()
    _, list_repos, _ = load_lists()
    repos_by_name = {r['full_name']: r for r in repos}
    total = len(repos)
    list_count = len(list_repos)

    counts = {}
    files = build_category_files(repos_by_name, list_repos, counts)
    files[ALL_INDEX] = build_all_index(repos)
    files[LANG_INDEX] = build_lang_index(repos)

    verify_consistency(repos, list_repos, counts)

    # 写分类页(分类 key 需补 .md,全量/语言索引 key 已带扩展名)
    for key, content in files.items():
        fname = key if key.endswith('.md') else f'{key}.md'
        with open(f'{DOCS_DIR}/{fname}', 'w') as f:
            f.write(content)

    # 写 README
    with open('README.md', 'w') as f:
        f.write(build_readme(total, counts, list_count))

    print(f"✅ 生成完成: README.md + docs/ 下 {len(files)} 个文件")
    print(f"   总项目: {total}")
    for cat in CATEGORIES:
        print(f"   {cat['key']}: {counts[cat['key']]}")


if __name__ == '__main__':
    main()
