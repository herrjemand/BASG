from lxml import html
import requests, time, os.path, json

DEBUG = 1#int(os.environ.get('BASG_DEBUG', '0'))
def add_record(item):
	loc = 'games.json'
	
	if not os.path.isfile(loc):
		with open(loc, 'w') as w:
			temp = {}
			temp[int(item['appid'])] = item
			w.write(json.dumps(temp, indent=4, separators=(',', ': ')))
	else:
		with open(loc) as r:
			data = json.loads(r.read())
			data[int(item['appid'])] = item
			with open(loc,'w') as w:
				w.write(json.dumps(data, indent=4, separators=(',', ': ')))
		

def strip(id):
	try:
		page = requests.get('http://store.steampowered.com/app/' + str(id))
		print(page.url)
		tree = html.fromstring(page.text)

		game = {
			'name'			:	' '.join(tree.xpath('//div[@class=\'apphub_AppName\']/text()')),
			'price'			:	float(' '.join(tree.xpath('//meta[@itemprop=\'price\']/@content'))),
			'tags'			:	[' '.join(item.split()) for item in tree.xpath('//div[@class=\'glance_tags popular_tags\']/a/text()')],
			# 'genre'			:	tree.xpath('//b[text()=\'Genre:\']/following-sibling::a/text()')[:2],
			# 'publisher'		:	tree.xpath('//b[text()=\'Genre:\']/following-sibling::a/text()')[2:][1],
			# 'developer'		:	tree.xpath('//b[text()=\'Genre:\']/following-sibling::a/text()')[2:][0],
			'appid'			:	int(id),
			'release_date'	:	' '.join(tree.xpath('//div[@class=\'release_date\']/span[@class=\'date\']/text()')),
			'raiting'		:	{
									'counts'	: 	int(' '.join(tree.xpath('//div[@class=\'release_date\']/meta[@itemprop=\'reviewCount\']/@content'))),
									'raiting'	:	int(' '.join(tree.xpath('//div[@class=\'release_date\']/meta[@itemprop=\'ratingValue\']/@content')))
								}
		}
		return game
	except Exception as e:
		if DEBUG:
			print('Error on: ', id, '\n', e)

		return	{
			'name'			:	''	,
			'price'			:	0.0	,
			'tags'			:	[]	,
			'genre'			:	[]	,
			'publisher'		:	''	,
			'developer'		:	''	,
			'appid'			:	0	,
			'release_date'	:	''	,
			'raiting'		:	{'counts' : 0, 'raiting' : 0}
		}

def do_the_thing(max):
	for i in range(9,max):
		print('\n',i)
		data = strip(i)
		if data['appid'] != 0:
			print('Done ',i)

			add_record(data)

		time.sleep(1)
		