import json
import requests
from datetime import datetime

time = datetime.now().strftime("%m-%d %H:%M")

def get_decksDetail():

    records = []
    try:
        response = json.load(open('deck_cache.json'))
    except:
        url = 'https://hsreplay.net/api/v1/archetypes/'
        response = requests.get(url).json()
        with open('deck_cache.json', 'w') as js:
            json.dump(response, js, indent = "\t")

    for deck in response:
        deck_id = deck['id']
        deck_name = deck['name']
        records.append([deck_id, deck_name])

    return records

def get_decks(mode):

    records = []
    url = 'https://hsreplay.net/analytics/query/list_decks_by_win_rate/?GameType=RANKED_{}&RankRange=ALL&Region=ALL&TimeRange=LAST_30_DAYS'.format(mode.upper())
    response = requests.get(url).json()

    for Class in response['series']['data'].keys():
        for rcd in response['series']['data'][Class]:
            deck_uid = rcd['deck_id']
            deck_nid = rcd['archetype_id']
            deck_count = rcd['total_games']
            deck_winrate = rcd['win_rate']
            deck_len = rcd['avg_game_length_seconds']
            deck_turns = rcd['avg_num_player_turns']
            deck_cards = rcd['deck_list']

            deck_info = [deck_uid, deck_nid, Class, deck_count, deck_winrate, deck_len,
            deck_turns, deck_cards, mode, time]

            records.append(deck_info)

    return records


def get_cards_info(mode):

    if mode is 'Standard':
        url = 'https://hsreplay.net/analytics/query/card_included_popularity_report/?GameType=RANKED_STANDARD&TimeRange=LAST_14_DAYS&RankRange=ALL'
    elif mode is 'Wild':
        url = 'https://hsreplay.net/analytics/query/card_included_popularity_report/?GameType=RANKED_WILD&TimeRange=LAST_14_DAYS&RankRange=ALL'
    elif mode is 'Arena':
        url = 'https://hsreplay.net/analytics/query/card_included_popularity_report/?GameType=ARENA&TimeRange=LAST_14_DAYS'

    response = requests.get(url).json()

    records = []
    for card in response['series']['data']['ALL']:
        card_id = card['dbf_id']
        card_popularity = card['popularity']
        card_count = card['decks']
        card_winrate = card['winrate']
        card_freq = card['count']
        records.append([card_id, card_popularity, card_count, card_winrate,
        card_freq, mode, time])

    return records
