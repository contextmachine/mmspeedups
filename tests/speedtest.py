
import mmvec
import pure_module
import numpy as np

import time

def test_time(fn):

    def wrapper(*args,**kwargs):
            s = time.time()
            res1=fn(*args,**kwargs)
            end1=time.time()-s
            print(f"time:{end1}")



    return wrapper


pairs1=zip(np.random.random((10000000,3)).tolist(),np.random.random((10000000,3)).tolist())
pairs2=zip(np.random.random((10000000,3)).tolist(),np.random.random((10000000,3)).tolist())
@test_time
def vecdisttest(m, pairs):

    for a, b in pairs:
        v1,v2=m.Vector(*a), m.Vector(*b)
        v2.unit().dot(v1.unit())
        v2.unit().cross(v1.unit())
        v2.dist(v1)
        v1.norm()
        v2.unit().angle(v1.unit())





import rich
#res=disttest()
#rich.print_json(res)


vecdisttest(mmvec, pairs1)
vecdisttest(pure_module, pairs2)


