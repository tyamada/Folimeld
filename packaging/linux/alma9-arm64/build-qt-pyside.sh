set -euo pipefail
b=$HOME/alma9-arm64-035
cd "$b"
export PATH="$b/bootstrap/bin:$PATH"
export SOURCE_DATE_EPOCH=1794528000 TZ=UTC PYTHONHASHSEED=0
python - <<'PY'
from pathlib import Path
import json,hashlib,tarfile
b=Path.home()/'alma9-arm64-035'
for p in sorted((b/'inputs').glob('*.tar.xz')):
 r=json.load(open(str(p)+'.json'));assert hashlib.file_digest(p.open('rb'),'sha256').hexdigest()==r['sha256'];print('VERIFIED_UPSTREAM_INPUT',p.name,r['sha256'])
 if not (b/'dependency-source'/p.name.removesuffix('.tar.xz')).exists():
  (b/'dependency-source').mkdir(exist_ok=True)
  with tarfile.open(p) as t:t.extractall(b/'dependency-source',filter='data')
PY
mkdir -p "$b/dependency-build/qtbase"
cd "$b/dependency-build/qtbase"
cmake -G Ninja "$b/dependency-source/qtbase-everywhere-src-6.11.2" \
 -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX="$b/qt6.11.2" \
 -DQT_BUILD_EXAMPLES=OFF -DQT_BUILD_TESTS=OFF -DQT_FEATURE_xcb=ON -DQT_FEATURE_dbus=ON \
 -DQT_FEATURE_icu=ON -DQT_FEATURE_openssl=ON \
 -DPython_EXECUTABLE="$b/bootstrap/bin/python" -DPython3_EXECUTABLE="$b/bootstrap/bin/python"
cmake --build . --parallel 4
cmake --install .
mkdir -p "$b/dependency-build/qtsvg"
cd "$b/dependency-build/qtsvg"
"$b/qt6.11.2/bin/qt-cmake" -G Ninja "$b/dependency-source/qtsvg-everywhere-src-6.11.2" -DCMAKE_BUILD_TYPE=Release -DQT_BUILD_EXAMPLES=OFF -DQT_BUILD_TESTS=OFF
cmake --build . --parallel 4
cmake --install .
cd "$b/dependency-source/pyside-setup-everywhere-src-6.11.2"
python -m pip install --only-binary=:all: numpy==2.4.6
python setup.py bdist_wheel --qtpaths="$b/qt6.11.2/bin/qtpaths6" --ignore-git --parallel=3 --module-subset=Core,Gui,Widgets,PrintSupport,Svg --standalone --limited-api=yes --no-qt-tools
mkdir -p "$b/custom-wheels"
cp -n dist/*.whl "$b/custom-wheels/"
sha256sum "$b/custom-wheels/"*.whl
rpm -qa --qf '%{NEVRA}\t%{SOURCERPM}\n' | sort > "$b/dependency-build-os-rpms.tsv"
echo ALMA9_ARM64_QT_PYSIDE_SOURCE_BUILD_PASS
