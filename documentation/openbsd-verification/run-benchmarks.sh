#!/bin/sh
set -eu
cd /home/folimeld/Folimeld
py=.venv-openbsd/bin/python
export QT_QPA_PLATFORM=offscreen
mkdir -p build/openbsd-verification
for n in 1 2 3; do
 "$py" -m tools.benchmark_pdf --pages 100 --output "build/openbsd-verification/text-100-$n.json"
 "$py" -m tools.benchmark_pdf --pages 100 --image-size 256 --output "build/openbsd-verification/images-100-$n.json"
 "$py" -m tools.benchmark_pdf --pages 1000 --output "build/openbsd-verification/text-1000-$n.json"
done
echo OPENBSD_BENCHMARKS_OK
