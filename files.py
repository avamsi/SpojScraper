from html import style, table
import os, shutil

slgen = '<a href="http://www.spoj.com/problems/{0}"target="_blank">{1}</a><br>\n'.format
llgen = '<a href="/SPOJ/problems/{0}" target="_blank">{1}</a>'.format
trgen = '<tr><td>{0}</td><td>{1}</td></tr>\n'.format

def clear():
    for fld in ('problems', 'users'):
        try:
            shutil.rmtree(fld)
        except OSError:
            pass
        os.mkdir(fld)

def write_probs(names, probs):
    with open('classical.html', 'w') as out:
        out.write(style)
        out.write(table)
        for code, psrc in probs:
            with open(os.path.join('problems', code), 'w') as f:
                f.write(style)
                f.write(slgen(code, 'View problem on Spoj'))
                f.write(psrc.encode('utf-8'))
            out.write(trgen(llgen(code, names[code]), slgen(code, code)))

def write_users(names, users):
    for user, codes in users.iteritems():
        with open(os.path.join('users', user), 'a') as f:
            f.write(style)
            f.write(slgen(user, 'View user profile on Spoj'))
            f.write(table)
            for code in codes:
                f.write(trgen(llgen(code, names[code]), slgen(code, code)))

def write(names, probs, users):
    write_probs(names, probs)
    write_users(names, users)
