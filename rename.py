import os

def rename(path,name):
    f = os.listdir(path)
    n = 0
    for i in f:
        oldname = path + f[n]
        newname = path + name + str(n + 114) + '.jpg'
        os.rename(oldname, newname)
        print(oldname, '======>', newname)
        n += 1