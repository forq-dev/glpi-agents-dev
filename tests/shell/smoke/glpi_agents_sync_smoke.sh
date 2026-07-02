#!/usr/bin/env bash

set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "${script_dir}/../../../" && pwd)"
source_repo="$(mktemp -d)"
consumer_root="$(mktemp -d)"

cleanup() {
  rm -rf "${source_repo}" "${consumer_root}"
}

trap cleanup EXIT

mkdir -p "${source_repo}/.agents" "${source_repo}/system-prompts"

cat > "${source_repo}/.agents/example.txt" <<'EOF'
example
EOF

cat > "${source_repo}/system-prompts/AGENTS.md" <<'EOF'
# AGENTS
EOF

cat > "${source_repo}/mcp.json" <<'EOF'
{
  "mcpServers": {
    "context7": {
      "type": "http",
      "url": "https://mcp.context7.com/mcp"
    }
  }
}
EOF

(
  cd "${source_repo}"
  git init -b master >/dev/null
  git config user.email test@example.com
  git config user.name Test
  git add .
  git commit -m init >/dev/null
)

cat > "${consumer_root}/mcp.json" <<'EOF'
{
  "mcpServers": {
    "local-only": {
      "type": "http",
      "url": "https://example.invalid"
    }
  }
}
EOF

PYTHONPATH="${repo_root}/src" "${repo_root}/bin/glpi-agents-sync" bootstrap \
  --root "${consumer_root}" \
  --source "${source_repo}" >/dev/null

if [[ ! -f "${consumer_root}/.agents/example.txt" ]]; then
  echo "[FAIL] bootstrap nao criou o arquivo da origem" >&2
  exit 1
fi

if [[ ! -L "${consumer_root}/CLAUDE.md" ]]; then
  echo "[FAIL] bootstrap nao criou o symlink CLAUDE.md" >&2
  exit 1
fi

if ! grep -q '"local-only"' "${consumer_root}/mcp.json"; then
  echo "[FAIL] bootstrap removeu MCP local" >&2
  exit 1
fi

rm "${source_repo}/.agents/example.txt"

(
  cd "${source_repo}"
  git add -A
  git commit -m remove-example >/dev/null
)

set +e
status_output="$(PYTHONPATH="${repo_root}/src" "${repo_root}/bin/glpi-agents-sync" sync \
  --root "${consumer_root}" \
  --source "${source_repo}" 2>&1)"
sync_status=$?
set -e

if [[ ${sync_status} -ne 2 ]]; then
  echo "[FAIL] sync sem confirmacao deveria retornar 2" >&2
  echo "${status_output}" >&2
  exit 1
fi

if [[ ! -f "${consumer_root}/.agents/example.txt" ]]; then
  echo "[FAIL] sync sem confirmacao removeu arquivo indevidamente" >&2
  exit 1
fi

confirmed_output="$(PYTHONPATH="${repo_root}/src" "${repo_root}/bin/glpi-agents-sync" sync \
  --root "${consumer_root}" \
  --source "${source_repo}" \
  --yes 2>&1)"

if [[ -f "${consumer_root}/.agents/example.txt" ]]; then
  echo "[FAIL] sync confirmado nao removeu arquivo" >&2
  echo "${confirmed_output}" >&2
  exit 1
fi

if ! grep -q '\[REMOVER\]' <<<"${confirmed_output}"; then
  echo "[FAIL] sync confirmado nao reportou remocao" >&2
  echo "${confirmed_output}" >&2
  exit 1
fi

echo "[PASS] glpi_agents_sync_smoke"
