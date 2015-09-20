
import requests
import config
import random
import pprint

from words import NOUNS
from amazonproduct import API
from amazonproduct.errors import NoExactMatchesFound

#categories = ['All','Wine','Wireless','ArtsAndCrafts','Miscellaneous','Electronics','Jewelry','MobileApps','Photo','Shoes','KindleStore','Automotive','MusicalInstruments','DigitalMusic','GiftCards','FashionBaby','FashionGirls','GourmetFood','HomeGarden','MusicTracks','UnboxVideo','FashionWomen','VideoGames','FashionMen','Kitchen','Video','Software','Beauty','Grocery',,'FashionBoys','Industrial','PetSupplies','OfficeProducts','Magazines','Watches','Luggage','OutdoorLiving','Toys','SportingGoods','PCHardware','Movies','Books','Collectibles','VHS','MP3Downloads','Fashion','Tools','Baby','Apparel','Marketplace','DVD','Appliances','Music','LawnAndGarden','WirelessAccessories','Blended','HealthPersonalCare','Classical']
#word_file = "/usr/share/dict/words"
#WORDS = open(word_file).read().splitlines()

api  = API(cfg = config.keys)


def get_images(ASIN):
	item = api.item_lookup(ASIN, ResponseGroup = 'Images', Condition = 'New')
	images = {}
	try:
	        images['small_image'] = str(item.Items.Item.SmallImage.URL)
        except AttributeError:
		pass
	try:
	        images['medium_image'] = str(item.Items.Item.MediumImage.URL)
	except AttributeError:
	        pass

	try:
                images['large_image'] = str(item.Items.Item.LargeImage.URL)
	except AttributeError:
	        pass
	return images

def get_price(ASIN):
	item = api.item_lookup(ASIN, ResponseGroup = 'Offers', Condition = 'New', Availability = 'Available')

	try:
                return float(str(item.Items.Item.OfferSummary.LowestNewPrice.FormattedPrice)[1:])
	except AttributeError:
		return None

def find_item(max_price, num_items):
	items = []
        max_price *= 100
        
	while True:
                try:
                        word = random.choice(NOUNS)
                        print(word)
                        page = api.item_search('All', Keywords = word, Condition = "New",  MaximumPrice = max_price, MinimumPrice = (max_price - 100),  Availability='Available')

                        for item in page:
                                asin = str(item.ASIN)
                                title = str(item.ItemAttributes.Title)
                                price = get_price(asin)
                                images = get_images(asin)

                                if price and title and images:
                                        item_data = {
                                                'code': asin,
                                                'title': title,
                                                'price': price
                                        }
                                        item_data.update(images)
                                        items.append(item_data)

                                        break
                except NoExactMatchesFound, UnicodeEncodeError:
                        pass

                if len(items) == num_items:
                    break

	return items

if __name__ == '__main__':
	pprint.pprint(find_item(6.89, 3))
