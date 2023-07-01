# Build from source
codon compiller is required
```shell
python3 setup.py build_ext --inplace
```

# Test speedups
```shell
python3 tests/speedtest.py

```
```log
[spedup] time: 6.3658881187438965
[python] time: 44.72692084312439
```

```python
from mmvec import Line
ln=Line((1.0,0.0,2.0), (3.1,3.1,4.0))
```
