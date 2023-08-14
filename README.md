[![Docker](https://github.com/contextmachine/mmspeedups/actions/workflows/docker-publish.yml/badge.svg)](https://github.com/contextmachine/mmspeedups/actions/workflows/docker-publish.yml)

Available in docker 🐳 and as 🐍 python extension
# Build from source
codon compiller is required
```bash
python3 setup.py build_ext --inplace
```

# Test speedups
```shell
python3 tests/speedtest.py

```
```log
[speedup] time: 6.3658881187438965
[python] time: 44.72692084312439
```
# Usage
```python
from mmvec import Line
ln1=Line((1.0,0.0,2.0), (3.1,3.1,4.0))
ln2=Line((-1.0,2.3,0.0), (11,-6,2.0))
ln1.proximity(ln2)```
```shell
((0.962988893434207, -0.054635443025694404, 1.964751327080197),
 (-1.211492037518817, 2.4462819926171817, -0.03524867291980284))```


```python
ln1.proximity_line(ln2)
```
```shell
Line((0.962989, -0.0546354, 1.96475), (-1.21149, 2.44628, -0.0352487))

```
