from urllib import urlopen, re
import sys

base = 'http://www.spoj.com/SPOJ/problems/'

re_c = re.compile('/problems/(.+?)/">&nbsp')
re_n = re.compile('<h1>(.+?)</h1>')
re_u = re.compile('Added by:</td><td><a href="/SPOJ/users/(.+?)"')

pbeg = '<table width="100%" style="margin-top:10px">'
pend = '<!-- google_ad_section_end -->'

get_source = lambda url: urlopen(url).read()
get_codes = re_c.findall

def problem(code, names, probs, users):
    tsrc = urlopen(base + code).read()
    psrc = tsrc[tsrc.index(pbeg): tsrc.index(pend)].decode('utf-8')
    name = re_n.search(psrc).group(1)
    user = re_u.search(psrc).group(1)
    names[code] = name
    probs.append([code, psrc])
    users.setdefault(user, []).append(code)

def print_progress(i, p):
    sys.stdout.write('\r[page #%s] problems: [%s%s] %2s/%s' % (i, (p/2)*'#', (25 - p/2)*'-', p, 50))
    sys.stdout.flush()
