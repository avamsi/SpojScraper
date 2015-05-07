import parse, cache, itertools, files

link = parse.base + 'classical/sort=0,start='

prev = cache.load_prev()
codes_old = []
for i in itertools.count(start=prev + 1):
    src = parse.get_source(link + str(i*50))
    codes = parse.get_codes(src)
    if codes == codes_old:
        break
    codes_old = codes
    names, probs, users = cache.load()
    for p, code in enumerate(codes):
        parse.print_progress(i, p + 1)
        parse.problem(code, names, probs, users)
    if len(codes) == 50:
        cache.dump(i, names, probs, users)

for code, name in names.items():
    names[code] = name.encode('utf-8')

files.clear()
files.write(names, probs, users)
