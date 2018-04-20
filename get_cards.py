import requests
import json
import secret

class Card:

    def __init__(self, Id = '', Name = '', Type = '', Class = '', Rarity = '',
    Set = '', Cost = '', Attack = '', Health = ''):
        self.Id = Id
        self.Name = Name
        self.Type = Type
        self.Class = Class
        self.Rarity = Rarity
        self.Set = Set
        self.Cost = Cost
        self.Attack = Attack
        self.Health = Health

    def setId(self, newId):
        self.Id = newId
    def setName(self, newName):
        self.Name = newName
    def setType(self, newType):
        self.Type = newType
    def setClass(self, newClass):
        self.Class = newClass
    def setRarity(self, newRarity):
        self.Rarity = newRarity
    def setSet(self, newSet):
        self.Set = newSet
    def setCost(self, newCost):
        self.Cost = newCost
    def setAttack(self, newAttack):
        self.Attack = newAttack
    def setHealth(self, newHealth):
        self.Health = newHealth

    def getAttributes(self):
        return [self.Id, self.Name, self.Type, self.Class, self.Rarity,
        self.Set, self.Cost, self.Attack, self.Health]


def get_cards():

    try:
        with open('cards_cache.json') as f:
            response = json.load(f)
    except:
        cards_url = 'https://api.hearthstonejson.com/v1/latest/enUS/cards.collectible.json'
        response = requests.get(cards_url).json()
        with open("cards_cache.json", "w") as js:
            json.dump(response, js, indent = "\t")

    cards_records = []
    for card in response:
        aCard = Card()
        aCard.setId(card['dbfId'])
        aCard.setName(card['name'])
        aCard.setType(card['type'])
        aCard.setClass(card['cardClass'])
        aCard.setRarity(card['rarity'])
        try:
            aCard.setSet(card['set'])
        except:
            pass
        try:
            aCard.setCost(card['cost'])
        except:
            pass
        try:
            aCard.setAttack(card['attack'])
        except:
            pass
        try:
            card.setHealth(card['health'])
        except:
            pass
        cards_records.append(aCard.getAttributes())

    return cards_records

def get_cards_image():

    records = []
    with open('cards_cache.json') as f:
        cards_collectable = json.load(f)

    try:
        with open('card_img_cache.json') as f:
            card_img_cache = json.load(f)
    except:
        card_img_cache = {}

    count = 0
    for card in cards_collectable:
        card_name = card['name']
        print('Acquire %s, %d cards acquired' % (card_name, count))
        if card_name in card_img_cache.keys():
            img = card_img_cache[card_name]['img']
            imgGold = card_img_cache[card_name]['imgGold']
        else:
            url = 'https://omgvamp-hearthstone-v1.p.mashape.com/cards/search/{}'.format(card_name)
            response = requests.get(url, headers={"X-Mashape-Key": secret.key}).json()
            for r in response:
                if "img" in r.keys():
                    img = r['img']
                    imgGold = r['imgGold']
                    break
                else:
                    continue
            print(card_name, img, imgGold)
            card_img_cache[card_name] = {'img': img, 'imgGold': imgGold}

        records.append([card_name, img, imgGold])
        count += 1

    with open('card_img_cache.json', 'w') as js:
        json.dump(card_img_cache, js, indent = "\t")

    return records
