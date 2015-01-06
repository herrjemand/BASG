from lxml import html
import requests, time, os.path, json

DEBUG = int(os.environ.get('BASG_DEBUG', '0'))
def add_record(item):
	loc = 'games.json'
	if not os.path.isfile(loc):
		with open(loc, 'w') as w:
			w.write(json.dumps({item.appid:item}, sort_keys=True, indent=4, separators=(',', ': '))
	else
		with open(loc) as r:
			data = json.parse(r.read())
			data[item.appid] = item
			with open(loc,'w') as w:
				w.write(json.dumps(data, sort_keys=True, indent=4, separators=(',', ': ')))



def strip(id):
	try:
		page = requests.get('http://store.steampowered.com/app/' + str(id))
		tree = html.fromstring(page.text)

		game = {
			'name'			:	' '.join(tree.xpath('//div[@class=\'apphub_AppName\']/text()')),
			'price'			:	float(' '.join(tree.xpath('//meta[@itemprop=\'price\']/@content'))),
			'tags'			:	[' '.join(item.split()) for item in tree.xpath('//div[@class=\'glance_tags popular_tags\']/a/text()')],
			'genre'			:	tree.xpath('//b[text()=\'Genre:\']/following-sibling::a/text()')[:2],
			'publisher'		:	tree.xpath('//b[text()=\'Genre:\']/following-sibling::a/text()')[2:][1],
			'developer'		:	tree.xpath('//b[text()=\'Genre:\']/following-sibling::a/text()')[2:][0],
			'appid'			:	int(' '.join(tree.xpath('//div[@class=\'glance_tags popular_tags\']/@data-appid'))),
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