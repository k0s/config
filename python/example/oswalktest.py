import os
import shutil
import tempfile

tmpd = tempfile.mkdtemp()
try:
    sub = os.path.join(tmpd, 'sub')
    link = os.path.join(tmpd, 'link')
    subsub = os.path.join(sub, 'sub')
    os.makedirs(sub)
    os.symlink(tmpd, link)
    os.symlink(tmpd, subsub)

    for item in os.walk(tmpd, followlinks=True):
        print item
finally:
    shutil.rmtree(tmpd)
