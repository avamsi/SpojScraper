from urllib import re, urlopen
from os.path import isfile, join
import itertools, json, sys
if isfile('cache_i.json'):
    with open('cache_i.json', 'rb') as fp:
        prev = json.load(fp)
else:
    prev = -1
    with open('cache_u.json', 'wb') as ufp,\
    open('cache_p.json', 'wb') as pfp, open('cache_n.json', 'wb') as nfp:
        json.dump({}, ufp)
        json.dump([], pfp)
        json.dump({}, nfp)
base = 'http://www.spoj.com/SPOJ/problems/'
clsc = base + 'classical/sort=0,start='
re_c = re.compile('/problems/(.+?)/">&nbsp')
re_n = re.compile('<h1>(.+?)</h1>')
re_u = re.compile('Added by:</td><td><a href="/SPOJ/users/(.+?)"')
pbeg = '<table width="100%" style="margin-top:10px">'
pend = '<!-- google_ad_section_end -->'
codo = []
for i in itertools.count(start=prev + 1):
    url = clsc + str(i*50)
    src = urlopen(url).read()
    codes = re_c.findall(src)
    if codes == codo:
        break
    codo = codes
    with open('cache_u.json', 'rb') as ufp,\
    open('cache_p.json', 'rb') as pfp, open('cache_n.json', 'rb') as nfp:
        users = json.load(ufp)
        probs = json.load(pfp)
        names = json.load(nfp)
    for p, code in enumerate(codes):
        p += 1
        sys.stdout.write('\r[page #%s] problems: [%s%s] %2s/%s' % (i, (p/2)*'#', (25 - p/2)*'-', p, 50))
        sys.stdout.flush()
        psrc = urlopen(base + code).read()
        psrc = psrc[psrc.index(pbeg): psrc.index(pend)].decode('utf-8')
        name = re_n.search(psrc).group(1)
        user = re_u.search(psrc).group(1)
        names[code] = name
        probs.append((code, psrc))
        users.setdefault(user, []).append(code)
    if len(codes) == 50:
        with open('cache_u.json', 'wb') as ufp, open('cache_p.json', 'wb') as pfp,\
        open('cache_n.json', 'wb') as nfp, open('cache_i.json', 'wb') as ifp:
            json.dump(users, ufp)
            json.dump(probs, pfp)
            json.dump(names, nfp)
            json.dump(i, ifp)
print '\ncompleted parsing, writing to files..'
slgen = '<a href="http://www.spoj.com/problems/{0}"target="_blank">{1}</a><br>\n'.format
llgen = '<a href="/SPOJ/problems/{0}" target="_blank">{1}</a>'.format
trgen = '<tr><td>{0}</td><td>{1}</td></tr>\n'.format
style =\
'''\
<head>
<meta charset="utf-8">
</head>
<style type="text/css">
    a { text-decoration: none }
    p { line-height: 1.8; }
    th {text-align: left; }
</style>
<font face="verdana"><p>
'''
table =\
'''\
Note: Click on problem name to open local file and code to view on Spoj.
<br><br>
<table width="50%">
<tr><th>Problem Name</th> <th>Problem Code</th></tr>
'''
names = {code: name.encode('utf-8') for code, name in names.iteritems()}
with open('classical.html', 'w') as out:
    out.write(style)
    out.write(table)
    for code, psrc in probs:
        with open(join('problems', code), 'w') as f:
            f.write(style)
            f.write(slgen(code, 'View problem on Spoj'))
            f.write(psrc.encode('utf-8'))
        out.write(trgen(llgen(code, names[code]), slgen(code, code)))
for user, codes in users.iteritems():
    with open(join('users', user), 'a') as f:
        f.write(style)
        f.write(slgen(user, 'View user profile on Spoj'))
        f.write(table)
        for code in codes:
            f.write(trgen(llgen(code, names[code]), slgen(code, code)))
