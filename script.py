from lxml import html
import requests

page = requests.get('http://store.steampowered.com/app/211420/')
tree = html.fromstring(page.text)

name = tree.xpath('//div[@class="apphub_AppName"]/text()')
price = tree.xpath('//meta[@itemprop="price"]/@content')
tags = tree.xpath("//div[@class=\"glance_tags popular_tags\"]/a/text()")
genre = tree.xpath("//b[text()='Genre:']/following-sibling::a[count(following-sibling::b)=3]/text()")