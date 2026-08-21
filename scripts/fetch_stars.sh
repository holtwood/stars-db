#!/usr/bin/env bash
# 拉取当前用户的 GitHub Star 数据到 data/starred_full.json
#
# 需要 gh CLI 已认证(gh auth login)。CI 中使用 STARS_TOKEN 环境变量认证。
set -euo pipefail

OUT="${1:-data/starred_full.json}"

gh api --paginate 'user/starred?per_page=100' --jq \
  '.[] | {id, node_id, full_name, description, language, topics, stargazers_count, fork, archived, html_url}' \
  > "$OUT"

echo "✅ 已保存 $(wc -l < "$OUT") 个仓库到 $OUT"
