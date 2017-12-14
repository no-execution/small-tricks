import requests

fr = open('items.json')
s = fr.read()
a = s.split()
res = []
for x in a:
	if x[0] == '"':
		res.append(x[1:-3])
count = 0
for i in range(len(res)):
	count += 1
	if res[i][-1] != 'g':
		res[i] += 'g'
count = 1
for x in res:
	name = str(count)+'.jpg'
	count += 1
	r = requests.get(x,stream=True)
	with open(name,'wb') as fd:
		for pic in r.iter_content():
			fd.write(pic)