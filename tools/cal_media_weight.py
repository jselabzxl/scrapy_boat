#-*-coding=utf-8-*-

import json

media_weight = {}
f = open('../items.jl')
for line in f:
    item = json.loads(line.strip())
    try:
        media_weight[item['author']] += 1
    except KeyError:
        media_weight[item['author']] = 1
f.close()

f = open('media_weight.txt', 'w')
results = sorted(media_weight.iteritems(), key=lambda(k, v):v, reverse=True)
for k, v in results:
    print k, v
    f.write('%s\t%s\n' % (k.encode('utf-8'), v))
f.close()
