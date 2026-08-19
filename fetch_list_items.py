import json, subprocess, time

lists = json.load(open('lists_meta.json'))
all_items = {}  # list_id -> set of nameWithOwner

def gql(query, var=None):
    cmd = ['gh', 'api', 'graphql', '-f', f'query={query}']
    if var:
        cmd += ['-F', f'var={json.dumps(var)}']
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print('ERR', r.stderr[:200]); return None
    return json.loads(r.stdout)

for l in lists:
    lid = l['id']
    items = set()
    cursor = None
    while True:
        cursor_arg = f', after: "{cursor}"' if cursor else ''
        q = f'''query {{ node(id: "{lid}") {{ ... on UserList {{ items(first: 100{cursor_arg}) {{ pageInfo {{ hasNextPage endCursor }} nodes {{ ... on Repository {{ nameWithOwner }} }} }} }} }} }}'''
        data = gql(q)
        if not data: break
        node = data['data']['node']
        items.update(i['nameWithOwner'] for i in node['items']['nodes'])
        pi = node['items']['pageInfo']
        if pi['hasNextPage'] and pi['endCursor']:
            cursor = pi['endCursor']
        else:
            break
    all_items[lid] = items
    print(f"{l['slug']}: {len(items)} items")

json.dump({k: sorted(v) for k, v in all_items.items()}, open('list_items.json', 'w'), ensure_ascii=False, indent=1)
print('saved list_items.json')
