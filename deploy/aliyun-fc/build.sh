#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
BUILD_DIR="$PROJECT_ROOT/build"

rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"

cp -r "$PROJECT_ROOT/src/github_to_dingtalk" "$BUILD_DIR/"
uv export --no-dev --no-hashes -o "$BUILD_DIR/requirements.txt" --quiet
uv pip install \
    -r "$BUILD_DIR/requirements.txt" \
    --target "$BUILD_DIR" \
    --python-platform manylinux2014_x86_64 \
    --python-version 3.13 \
    --quiet
rm "$BUILD_DIR/requirements.txt"

echo "Build complete: $BUILD_DIR"
