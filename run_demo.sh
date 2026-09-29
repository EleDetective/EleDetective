#!/usr/bin/env bash
# Install dependencies and launch the original UI, backend and grid server.
set -euo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
WORK="${ELEDETECTIVE_WORK_DIR:-$ROOT/.eledetective}"
mkdir -p "$WORK"
WORK="$(cd "$WORK" && pwd)"
source /etc/os-release
if [[ "$ID" != ubuntu ]] || ! dpkg --compare-versions "$VERSION_ID" ge 22.04 || [[ "$(uname -m)" != x86_64 ]]; then
  echo 'Use Ubuntu 22.04 or newer on x86_64.' >&2; exit 1
fi
missing=()
for package in ca-certificates curl xz-utils git build-essential libgomp1; do
  dpkg-query -W -f='${Status}' "$package" 2>/dev/null | grep -q 'install ok installed' || missing+=("$package")
done
if ((${#missing[@]})); then
  if [[ $EUID -eq 0 ]]; then elevate=(); else elevate=(sudo); fi
  "${elevate[@]}" apt-get update
  "${elevate[@]}" env DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends "${missing[@]}"
fi
mkdir -p "$WORK/tools" "$WORK/downloads" "$WORK/logs"
export UV_CACHE_DIR="$WORK/uv-cache" UV_PYTHON_INSTALL_DIR="$WORK/python" UV_PYTHON_PREFERENCE=only-managed
export XDG_CACHE_HOME="$WORK/cache" MPLCONFIGDIR="$WORK/cache/matplotlib" PYTHONDONTWRITEBYTECODE=1
if [[ ! -x "$WORK/tools/uv" ]]; then
  curl -fL --retry 4 https://github.com/astral-sh/uv/releases/download/0.9.18/uv-x86_64-unknown-linux-gnu.tar.gz -o "$WORK/downloads/uv.tar.gz"
  tar -xzf "$WORK/downloads/uv.tar.gz" --strip-components=1 -C "$WORK/tools" uv-x86_64-unknown-linux-gnu/uv
fi
UV="$WORK/tools/uv"
if [[ ! -x "$WORK/venv/bin/python" ]]; then
  "$UV" python install 3.11.10
  "$UV" venv --python 3.11.10 --seed "$WORK/venv"
fi
PYTHON="$WORK/venv/bin/python"
dependency_hash="$(sha256sum "$ROOT/scripts/requirements.txt" | cut -d' ' -f1)"
if [[ ! -f "$WORK/dependencies.sha256" ]] || [[ "$(cat "$WORK/dependencies.sha256")" != "$dependency_hash" ]]; then
  "$UV" pip sync --python "$PYTHON" "$ROOT/scripts/requirements.txt" --index-strategy unsafe-best-match
  echo "$dependency_hash" > "$WORK/dependencies.sha256"
fi
NODE="$WORK/tools/node-v22.14.0-linux-x64"
if [[ ! -x "$NODE/bin/node" ]]; then
  curl -fL --retry 4 https://nodejs.org/dist/v22.14.0/node-v22.14.0-linux-x64.tar.xz -o "$WORK/downloads/node-v22.14.0-linux-x64.tar.xz"
  curl -fL --retry 4 https://nodejs.org/dist/v22.14.0/SHASUMS256.txt -o "$WORK/downloads/node-checksums.txt"
  (cd "$WORK/downloads"; grep '  node-v22.14.0-linux-x64.tar.xz$' node-checksums.txt | sha256sum --check -)
  tar -xf "$WORK/downloads/node-v22.14.0-linux-x64.tar.xz" -C "$WORK/tools"
fi
export PATH="$NODE/bin:$PATH" npm_config_cache="$WORK/npm-cache"
for source in 'Treemap-Based Gridlayout/application/data/linear_assignment' 'Treemap-Based Gridlayout/application/data/c module_now' 'Visualization System/backend/data/scene_tree/scene_tree_cpp'; do
  (cd "$ROOT/$source"; "$PYTHON" setup.py build_ext --inplace)
done
cp "$ROOT/Treemap-Based Gridlayout/application/data/c module_now/"*.so "$ROOT/Treemap-Based Gridlayout/application/data/"
export PYTHONPATH="$ROOT/Treemap-Based Gridlayout/application/data/linear_assignment${PYTHONPATH:+:$PYTHONPATH}"
FRONTEND="$ROOT/Visualization System/frontend"
(cd "$FRONTEND"; npm ci --no-audit --no-fund)
"$PYTHON" "$ROOT/scripts/download_data.py" "$WORK"
export ELEDETECTIVE_DATASET="$WORK/data/backend"
export ELEDETECTIVE_IMAGE_DIR="$WORK/data/images" ELEDETECTIVE_IMAGE_URL=/images/
export ELEDETECTIVE_PORT="${ELEDETECTIVE_PORT:-5180}" ELEDETECTIVE_BACKEND_PORT="${ELEDETECTIVE_BACKEND_PORT:-5102}"
export OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 OMP_NUM_THREADS=4 MPLBACKEND=Agg
mkdir -p "$ROOT/Treemap-Based Gridlayout/datasets"
for link in "$FRONTEND/public/images" "$ROOT/Treemap-Based Gridlayout/datasets/infographic"; do
  if [[ -e "$link" && ! -L "$link" ]]; then echo "Refusing to replace existing data: $link" >&2; exit 1; fi
done
ln -sfn "$WORK/data/images" "$FRONTEND/public/images"
ln -sfn "$WORK/data/grid/infographic" "$ROOT/Treemap-Based Gridlayout/datasets/infographic"
"$PYTHON" - <<'PY'
import os, socket
for port in (int(os.environ['ELEDETECTIVE_PORT']), int(os.environ['ELEDETECTIVE_BACKEND_PORT']), 12121):
    with socket.socket() as sock:
        try: sock.bind(('0.0.0.0', port))
        except OSError: raise SystemExit(f'Port {port} is already in use.')
PY
pids=()
cleanup() { trap - EXIT INT TERM; for pid in "${pids[@]}"; do kill "$pid" 2>/dev/null || true; done; wait || true; }
trap cleanup EXIT INT TERM
(cd "$ROOT/Visualization System/backend"; exec "$PYTHON" -u server_new2.py) > "$WORK/logs/backend.log" 2>&1 & pids+=("$!")
(cd "$ROOT/Treemap-Based Gridlayout"; exec "$PYTHON" -u server.py) > "$WORK/logs/grid.log" 2>&1 & pids+=("$!")
for attempt in $(seq 1 180); do
  for pid in "${pids[@]}"; do if ! kill -0 "$pid" 2>/dev/null; then tail -n 30 "$WORK/logs/"*.log; exit 1; fi; done
  if curl -fsS -H 'Content-Type: application/json' -d '{"ids":[]}' "http://127.0.0.1:$ELEDETECTIVE_BACKEND_PORT/api/data_ids" >/dev/null 2>&1 && curl -fsS -H 'Content-Type: application/json' -d '{"dataset":"infographic"}' http://127.0.0.1:12121/api/metadata >/dev/null 2>&1; then break; fi
  if [[ "$attempt" == 180 ]]; then echo "Servers did not start; see $WORK/logs" >&2; exit 1; fi
  sleep 1
done
echo "Open http://localhost:$ELEDETECTIVE_PORT or forward port $ELEDETECTIVE_PORT. Ctrl+C stops all services."
(cd "$FRONTEND"; exec node node_modules/vite/bin/vite.js --host 0.0.0.0) & pids+=("$!")
wait -n "${pids[@]}"
