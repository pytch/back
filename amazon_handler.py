
import requests
import config
import random

from amazonproduct import API

#categories = ['All','Wine','Wireless','ArtsAndCrafts','Miscellaneous','Electronics','Jewelry','MobileApps','Photo','Shoes','KindleStore','Automotive','MusicalInstruments','DigitalMusic','GiftCards','FashionBaby','FashionGirls','GourmetFood','HomeGarden','MusicTracks','UnboxVideo','FashionWomen','VideoGames','FashionMen','Kitchen','Video','Software','Beauty','Grocery',,'FashionBoys','Industrial','PetSupplies','OfficeProducts','Magazines','Watches','Luggage','OutdoorLiving','Toys','SportingGoods','PCHardware','Movies','Books','Collectibles','VHS','MP3Downloads','Fashion','Tools','Baby','Apparel','Marketplace','DVD','Appliances','Music','LawnAndGarden','WirelessAccessories','Blended','HealthPersonalCare','Classical']
word_file = "/usr/share/dict/words"
WORDS = open(word_file).read().splitlines()

api  = API(cfg = config.keys)


def get_images(ASIN):
	item = api.item_lookup(ASIN, ResponseGroup = 'Images', Condition = 'New')
	images = {}
	try:
		images['smallimage'] = item.Items.Item.SmallImage.URL	
	except:
		pass
	try:
		images['mediumimage'] = item.Items.Item.MediumImage.URL
	except:
		pass

	try:
		images['largeimage'] = item.Items.Item.LargeImage.URL
	except:
		pass
	return images

def get_price(ASIN):
	price = {}
	item = api.item_lookup(ASIN, ResponseGroup = 'Offers', Condition = 'New', Availability = 'Available')
	try:
		price['price'] = item.Items.Item.OfferSummary.LowestNewPrice.FormattedPrice
	except:
		pass
	return price

def find_item(price):
	results = []
	items = {}
	while len(results) < 5:
		word = random.choice(WORDS)
		try:
			result =  api.item_search('All', Keywords = word, Condition = "New",  MaximumPrice = price, MinimumPrice = (price-100),  Availability='Available')
			results.append(result)
		except:
			pass
	for page in results:
		for item in page:
			items[str(item.ASIN)] = [{'title':item.ItemAttributes.Title}, get_images(str(item.ASIN)), get_price(str(item.ASIN))]
			break
	return items

if __name__ == '__main__':
	pass