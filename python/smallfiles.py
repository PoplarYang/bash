import os
import os.path
import sys
import threading
import time

def create_files(d, n):
    st = time.time()
    for i in range(n):
        with open(os.path.join(d, str(i)), 'w') as f:
            f.write('0' * (128<<10))

d = sys.argv[1]
threads = int(sys.argv[2])
files = int(sys.argv[3])

if os.path.exists(d):
    os.system("rm -rf %s/*" % d)
else:
    os.mkdir(d)

start = time.time()
ts = []
for i in range(threads):
    dd = os.path.join(d, str(i))
    os.mkdir(dd)
    t = threading.Thread(target=create_files, args=(dd, files))
    t.daemon = True
    t.start()
    ts.append(t)

for t in ts:
    t.join()

used = time.time() - start

print files * threads / used, "iops"
