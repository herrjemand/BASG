from lxml import html
import requests

page = requests.get('http://store.steampowered.com/app/211420/')
tree = html.fromstring(page.text)

name = tree.xpath('//div[@class=\'apphub_AppName\']/text()')[0]

price = tree.xpath('//meta[@itemprop=\'price\']/@content')[0]

tags = [
		' '.join(item.split()) for item 
		in tree.xpath('//div[@class=\'glance_tags popular_tags\']/a/text()')
	]

metacache = tree.xpath('//b[text()=\'Genre:\']/following-sibling::a/text()')

genre = metacache[:2]

publisher = metacache[2:][1]

developer = metacache[2:][0]

appid = tree.xpath('//div[@class=\'glance_tags popular_tags\']/@data-appid')[0]

release_date = tree.xpath('//div[@class=\'release_date\']/span[@class=\'date\']/text()')