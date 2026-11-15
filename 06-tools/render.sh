#!/bin/sh
# Render seluruh berkas .puml dan .dot dalam folder menjadi PNG.
# Pemakaian: render.sh <folder>
set -e
DIR="${1:?folder wajib diisi}"
cd "$DIR"
fail=0
for f in *.puml; do
  [ -e "$f" ] || continue
  if plantuml -tpng -charset UTF-8 "$f" >/dev/null 2>&1; then
    echo "OK   $f"
  else
    echo "FAIL $f"
    fail=1
  fi
done
for f in *.dot; do
  [ -e "$f" ] || continue
  if dot -Tpng -Gdpi=150 "$f" -o "${f%.dot}.png"; then
    echo "OK   $f"
  else
    echo "FAIL $f"
    fail=1
  fi
done
exit $fail
