import glob, os

with open(r'\\USER1-PC\Users\Public\test.txt', 'w') as f:
    f.write('hello')    # write a file on a distant Samba share

for f in glob.glob(r'\\USER1-PC\Users\**\*', recursive=True):
    print(f)   # glob works too
    if os.path.isfile(f):
        print(os.path.getmtime(f))  # we can get filesystem information