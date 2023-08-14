import sys
import os


if __name__=="__main__":
    import subprocess as sp
    target = None
    for d in os.scandir(os.getenv("HOME")):
        if d.name == ".codon":
            target = d
            break
        continue

    
    if target is None:
        proc = sp.Popen(
            ["/bin/bash", "-c", '"$(curl -fsSL https://exaloop.io/install.sh)"'],
            stdout=sp.PIPE,
        )
        proc.communicate()
    args=[sys.executable,"setup.py", "build_ext", "install", "--force"]
    proc=sp.Popen(args, stdout=sp.PIPE)
    proc.communicate()