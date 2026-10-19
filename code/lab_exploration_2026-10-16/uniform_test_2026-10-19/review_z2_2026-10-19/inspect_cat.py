import gzip, json, sys
CAT = sys.argv[1]
d = json.loads(gzip.decompress(open(CAT,'rb').read()))
print(type(d), list(d.keys())[:20])
print('n open', len(d['open']))
e = d['open'][9748]
print(json.dumps({k: (v if k!='template' else None) for k,v in e.items()})[:1500])
print(json.dumps(e['template'])[:3000])
