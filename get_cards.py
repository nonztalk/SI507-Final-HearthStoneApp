import requests
import json
import secret


def get_cards():

    try:
        response = json.load(open('cards_cache.json'))
    except:
        cards_url = 'https://api.hearthstonejson.com/v1/latest/enUS/cards.collectible.json'
        response = requests.get(cards_url).json()
        with open("cards_cache.json", "w") as js:
            json.dump(response, js, indent = "\t")

    cards_records = []
    for card in response:
        card_id = card['dbfId']
        card_name = card['name']
        card_type = card['type']
        card_class = card['cardClass']
        card_rarity = card['rarity']
        try:
            card_set = card['set']
        except:
            card_set = ''
        try:
            card_cost = card['cost']
        except:
            card_cost = ''
        try:
            card_attack = card['attack']
        except:
            card_attack = ''
        try:
            card_health = card['health']
        except:
            card_health = ''
        cards_records.append([card_id, card_name, card_type, card_class, card_rarity, card_set, card_cost, card_attack, card_health])

    return cards_records

def get_cards_image():

    records = []
    cards_collectable = json.load(open('cards_cache.json'))

    try:
        card_img_cache = json.load(open('card_img_cache.json'))
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
