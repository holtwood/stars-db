import json, subprocess, time

# ---------- 数据加载 ----------
repos = {}
with open('starred_full.json') as f:
    for line in f:
        line = line.strip()
        if line:
            r = json.loads(line)
            repos[r['full_name']] = r

list_items = json.load(open('list_items.json'))
lists_meta = {l['id']: l for l in json.load(open('lists_meta.json'))}
repo_lists = {}
for lid, items in list_items.items():
    for item in items:
        repo_lists.setdefault(item, []).append(lid)

name2id = {l['name']: l['id'] for l in lists_meta.values()}
id2name = {l['id']: l['name'] for l in lists_meta.values()}

# ---------- 任务定义 ----------
# 1) 补全：25 个未归类 -> 目标 list
add_map = {
    'AI与LLM': ['baidu-baige/LoongForge', 'karpathy/minGPT', 'dataflowr/notebooks'],
    'AI-Agent与MCP': ['deepseek-ai/deepseek-harness', 'xiaobright/dsh-anchored-standard',
                      'yjh051108/dsh-router-standard', 'yjh051108/dsh-routing-suite',
                      'huangguang1999/ccstatusline-zh'],
    '高性能计算': ['gpu-mode/lectures', 'siboehm/SGEMM_CUDA'],
    'DevOps与云原生': ['dani-garcia/vaultwarden', 'docker-mailserver/docker-mailserver',
                       'Mailu/Mailu', 'ttionya/vaultwarden-backup'],
    '系统与桌面工具': ['bin456789/reinstall', 'wesleyel/opendict-apple'],
    '网络与代理': ['v2rayA/v2rayA'],
    'CLI与终端工具': ['reubeno/brush', 'manaflow-ai/cmux', 'LoosePrince/cursor-zh-cn-pack'],
    '编辑器与文档笔记': ['vrtmrz/obsidian-livesync'],
    '移动开发': ['mudkipme/MoeMemosAndroid'],
    '学习资源与清单': ['DigitalPlatDev/FreeDomain', 'open-genomics/awesome-bioinfo-algorithms',
                      'vibe-knight/awesome-compression'],
}

# 2) 修正：repo -> (移除的list名集合, 加入的list名集合)
fix_map = {
    'caddyserver/caddy': ({'安全与逆向'}, {'DevOps与云原生'}),
    'nginx/nginx': ({'安全与逆向'}, {'DevOps与云原生'}),
    'twpayne/chezmoi': ({'安全与逆向'}, {'系统与桌面工具'}),
    'ChenYilong/iOSInterviewQuestions': ({'安全与逆向'}, {'算法与面试'}),
    'StevenBlack/hosts': ({'安全与逆向'}, {'网络与代理'}),
    'lennylxx/ipv6-hosts': ({'安全与逆向'}, {'网络与代理'}),
    'ClementTsang/bottom': ({'AI与LLM'}, {'CLI与终端工具'}),
    'Sophia-Community/SophiApp': ({'AI与LLM'}, {'系统与桌面工具'}),
    'LC044/WeChatMsg': ({'AI与LLM'}, {'其他与杂项'}),
    'NVIDIA/cccl': ({'AI与LLM'}, {'高性能计算'}),
    'NVIDIA/cuda-samples': ({'AI与LLM'}, {'高性能计算'}),
    '0xJacky/nginx-ui': ({'AI-Agent与MCP'}, {'DevOps与云原生'}),
    'QuantumNous/new-api': ({'AI-Agent与MCP'}, {'网络与代理'}),
    'PDFMathTranslate/PDFMathTranslate': ({'AI-Agent与MCP'}, {'AI与LLM'}),
    'amitshekhariitbhu/ai-engineering-interview-questions': ({'AI-Agent与MCP', 'AI-Infra'}, {'算法与面试'}),
    'matrixorigin/matrixone': ({'AI-Infra', 'AI与LLM'}, {'数据库与存储'}),
}

# ---------- 汇总所有任务 ----------
tasks = []  # (repo, final_list_ids)
for lst, items in add_map.items():
    for repo in items:
        if repo not in repos:
            print(f"[WARN] {repo} 不在 star 列表"); continue
        tasks.append((repo, [name2id[lst]]))

for repo, (remove, add) in fix_map.items():
    if repo not in repos:
        print(f"[WARN] {repo} 不在 star 列表"); continue
    cur = set(repo_lists.get(repo, []))
    for r in remove:
        cur.discard(name2id[r])
    for a in add:
        cur.add(name2id[a])
    tasks.append((repo, sorted(cur)))

print(f"总任务数: {len(tasks)}")
for repo, lids in tasks:
    print(f"  {repo} -> {[id2name[l] for l in lids]}")

# ---------- 执行 ----------
def gql_mut(item_id, list_ids):
    ids = '", "'.join(list_ids)
    q = f'''mutation {{ updateUserListsForItem(input: {{itemId: "{item_id}", listIds: ["{ids}"]}}) {{ item {{ ... on Repository {{ nameWithOwner }} }} lists {{ name }} }} }}'''
    r = subprocess.run(['gh', 'api', 'graphql', '-f', f'query={q}'], capture_output=True, text=True)
    return r

ok, fail = 0, 0
for i, (repo, lids) in enumerate(tasks, 1):
    r = gql_mut(repos[repo]['node_id'], lids)
    if r.returncode == 0:
        try:
            payload = json.loads(r.stdout)['data']['updateUserListsForItem']
            got = [x['name'] for x in payload['lists']]
            ok += 1
            print(f"[{i}/{len(tasks)}] OK  {repo} -> {sorted(got)}")
        except Exception as e:
            fail += 1
            print(f"[{i}/{len(tasks)}] PARSE-ERR {repo}: {r.stdout[:150]}")
    else:
        fail += 1
        print(f"[{i}/{len(tasks)}] FAIL {repo}: {r.stderr[:150]}")
    time.sleep(0.3)

print(f"\n完成: 成功 {ok}, 失败 {fail}")
