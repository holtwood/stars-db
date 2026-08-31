#!/usr/bin/env python3
"""将 GitHub Star 仓库描述翻译为中文（增量缓存到 data/desc_zh.json）

数据管线中的一环：
  scripts/fetch_stars.sh  → data/starred_full.json
  scripts/translate.py    → data/desc_zh.json   (full_name → 中文描述)
  scripts/gen_index.py    → README.md + docs/*.md + data/stars.json

用法:
  python3 scripts/translate.py              # 只翻译缺失条目（增量）
  python3 scripts/translate.py --dry-run    # 只打印待翻译数量，不调用 API

依赖环境变量（OpenAI 兼容接口）:
  NEWAPI_BASE_URL   接口地址
  NEWAPI_API_KEY    密钥
  AI_MODEL          模型名（默认 doubao-seed-2.0-lite，需支持 thinking disabled）
"""
import argparse
import json
import os
import re
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE = os.environ.get("NEWAPI_BASE_URL", "").rstrip("/")
KEY = os.environ.get("NEWAPI_API_KEY", "")
MODEL = os.environ.get("AI_MODEL", "doubao-seed-2.0-lite")
CACHE = "data/desc_zh.json"
CONCURRENCY = 6
RETRIES = 2

HAN = re.compile(r"[\u4e00-\u9fff]")


def load_repos():
    repos = []
    with open("data/starred_full.json") as f:
        for line in f:
            line = line.strip()
            if line:
                repos.append(json.loads(line))
    return repos


def load_cache():
    if os.path.exists(CACHE):
        with open(CACHE, encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_cache(cache):
    tmp = CACHE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=1, sort_keys=True)
    os.replace(tmp, CACHE)


def translate_one(text, timeout=60):
    body = {
        "model": MODEL,
        "messages": [
            {"role": "system",
             "content": "你是翻译助手。把 GitHub 仓库的一句话描述翻译成简洁地道的中文。"
                        "只输出译文本身，不要解释、不要引号、不要多余文字。"
                        "专有名词（框架/工具/公司名）可保留英文。"},
            {"role": "user", "content": text},
        ],
        "max_tokens": 128,
        "temperature": 0.2,
        "thinking": {"type": "disabled"},
    }
    req = urllib.request.Request(
        f"{BASE}/chat/completions",
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json",
                 "Authorization": f"Bearer {KEY}"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        data = json.load(r)
    content = data["choices"][0]["message"]["content"].strip()
    return content


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="只打印待翻译数量")
    args = ap.parse_args()

    if not BASE or not KEY:
        print("ERROR: 需要环境变量 NEWAPI_BASE_URL 与 NEWAPI_API_KEY", file=sys.stderr)
        sys.exit(2)

    repos = load_repos()
    cache = load_cache()
    todo = []
    for r in repos:
        name = r["full_name"]
        desc = (r.get("description") or "").strip()
        if not desc:
            cache.setdefault(name, "")
            continue
        if name in cache and cache[name]:
            continue
        if HAN.search(desc):
            cache.setdefault(name, desc)
            continue
        todo.append((name, desc))

    if args.dry_run:
        print(f"待翻译: {len(todo)} / 总仓库: {len(repos)} / 已缓存: {len(cache)}")
        return

    print(f"开始翻译 {len(todo)} 条（模型 {MODEL}）...")
    done = 0
    fail = 0
    with ThreadPoolExecutor(max_workers=CONCURRENCY) as ex:
        futures = {ex.submit(translate_one, desc): (name, desc)
                   for name, desc in todo}
        for fut in as_completed(futures):
            name, desc = futures[fut]
            ok = False
            for _ in range(RETRIES):
                try:
                    cache[name] = fut.result()
                    ok = True
                    break
                except Exception as e:
                    time.sleep(1)
            if not ok:
                fail += 1
                print(f"[FAIL] {name}: {desc[:60]}")
            done += 1
            if done % 50 == 0 or done == len(todo):
                print(f"  进度 {done}/{len(todo)}")
                save_cache(cache)

    save_cache(cache)
    print(f"完成: 成功 {done - fail}, 失败 {fail}, 缓存 {len(cache)} 条")


if __name__ == "__main__":
    main()
