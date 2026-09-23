set -e
cp -r /src /work && cd /work
M=https://pypi.tuna.tsinghua.edu.cn/simple
python -m pip install -q --disable-pip-version-check -i $M --timeout 120 -r /req.txt
python -m pip install -q --disable-pip-version-check -i $M --no-deps --no-build-isolation -e . || python -m pip install -q -i $M --no-deps -e .
python -c "import platform,sys,numpy,selcal;print('ENV',platform.machine(),platform.platform(),sys.version.split()[0],numpy.__version__,selcal.__version__)"
python -m pytest -q --no-header -p no:cacheprovider 2>&1 | grep -E "^(FAILED|ERROR)|passed|failed"
