import unittest
import random
import sqlite3
from datetime import datetime
from get_cards import *
from get_game_records import *
from DashApp import get_deck_detail, cards_in_decks_detail, cards_images

class TestIt(unittest.TestCase):

    # test get data
    def test_get_cards(self):
        card_records = get_cards()

        classes = set([card[3] for card in card_records])
        expect_classes = ['MAGE', 'DRUID', 'HUNTER', 'PRIEST', 'NEUTRAL', 'WARLOCK',
        'ROGUE', 'SHAMAN', 'WARRIOR', 'PALADIN']

        types = set([card[2] for card in card_records])
        expect_types = ['SPELL', 'MINION', 'WEAPON', 'HERO']

        rarities = set([card[4] for card in card_records])
        expect_rarities = ['COMMON', 'RARE', 'EPIC', 'LEGENDARY', 'FREE']

        sets = set([card[5] for card in card_records])

        self.assertEqual(len(classes), 10)
        self.assertTrue(all([Class in classes for Class in expect_classes]))
        self.assertEqual(len(types), 4)
        self.assertTrue(all([Type in types for Type in expect_types]))
        self.assertEqual(len(rarities), 5)
        self.assertTrue(all([Rarity in rarities for Rarity in expect_rarities]))
        self.assertEqual(len(sets), 17)
        self.assertTrue('GILNEAS' in sets)
        self.assertTrue('ICECROWN' in sets)
        self.assertTrue('LOOTAPALOOZA' in sets)

        for i in [random.randint(1, 1000) for _ in range(5)]:
            card = card_records[i]
            if card[2] is 'SPELL':
                self.assertTrue(isinstance(card[6], int))
                self.assertTrue(card[7] == '')
                self.assertTrue(card[8] == '')
            if card[2] is 'MINION':
                self.assertTrue(isinstance(card[6], int))
                self.assertTrue(isinstance(card[7], int))
                self.assertTrue(isinstance(card[8], int))
                self.assertTrue(card[8] > 0)
            if card[2] is 'WEAPON':
                self.assertTrue(isinstance(card[6], int))
                self.assertTrue(isinstance(card[7], int))
                self.assertTrue(card[8] == '')

    def test_get_decks(self):
        decks = get_decksDetail()
        ids = [r[0] for r in decks]
        records_standard = get_decks('Standard')
        expect_classes = ['MAGE', 'DRUID', 'HUNTER', 'PRIEST', 'WARLOCK',
        'ROGUE', 'SHAMAN', 'WARRIOR', 'PALADIN']

        self.assertTrue(all([r[9] == datetime.now().strftime("%m-%d %H:%M") for r in records_standard]))
        self.assertTrue(all([r[2] in expect_classes for r in records_standard]))
        self.assertTrue(all([r[1] in ids for r in records_standard if r[1] > 0]))
        self.assertTrue(all([r[8] is 'Standard' for r in records_standard]))
        self.assertTrue(all([0 <= r[4] <= 100 for r in records_standard]))

        records_wild = get_decks('Wild')

        self.assertTrue(all([r[2] in expect_classes for r in records_wild]))
        self.assertTrue(all([r[8] is 'Wild' for r in records_wild]))
        self.assertTrue(all([0 <= r[4] <= 100 for r in records_wild]))

    def test_get_cards_info(self):
        cards = get_cards()

        records_standard = get_cards_info('Standard')
        self.assertTrue(all([r[6] == datetime.now().strftime("%m-%d %H:%M") for r in records_standard]))
        self.assertTrue(all([0 <= r[3] <= 100 for r in records_standard]))
        self.assertTrue(all([1 <= r[4] <= 2 for r in records_standard]))
        self.assertTrue(all([r[5] is 'Standard' for r in records_standard]))

        records_wild = get_cards_info('Wild')
        self.assertTrue(all([r[6] == datetime.now().strftime("%m-%d %H:%M") for r in records_wild]))
        self.assertTrue(all([0 <= r[3] <= 100 for r in records_wild]))
        self.assertTrue(all([1 <= r[4] <= 2 for r in records_wild]))
        self.assertTrue(all([r[5] is 'Wild' for r in records_wild]))

        records_arena = get_cards_info('Arena')
        self.assertTrue(all([0 <= r[3] <= 100 for r in records_arena]))
        self.assertTrue(all([1 <= r[4] <= 2 for r in records_arena]))
        self.assertTrue(all([r[5] is 'Arena' for r in records_arena]))

    # test storage
    def test_card_storage(self):
        conn = sqlite3.connect('HeartStone.sqlite')
        cur = conn.cursor()
        card_minion = '''
        SELECT * FROM CardDetail
        WHERE Name = 'Cryomancer'
        '''
        cur.execute(card_minion)
        response = cur.fetchone()
        self.assertEqual(response[0], 40988)
        self.assertEqual(response[2], 'MINION')
        self.assertEqual(response[3], 'MAGE')
        self.assertEqual(response[4], 'COMMON')
        self.assertEqual(response[5], 'GANGS')
        self.assertEqual(response[6], 5)
        self.assertEqual(response[7], 5)
        self.assertEqual(response[8], 5)

        card_spell = '''
        SELECT * FROM CardDetail
        WHERE Name = 'Living Roots'
        '''
        cur.execute(card_spell)
        response = cur.fetchone()
        self.assertEqual(response[0], 2792)
        self.assertEqual(response[2], 'SPELL')
        self.assertEqual(response[6], 1)
        self.assertEqual(response[7], '')
        self.assertEqual(response[8], '')

        card_weapon = '''
        SELECT * FROM CardDetail
        WHERE Name = 'Twig of the World Tree'
        '''
        cur.execute(card_weapon)
        response = cur.fetchone()
        self.assertEqual(response[0], 46107)
        self.assertEqual(response[2], 'WEAPON')
        self.assertEqual(response[6], 4)
        self.assertEqual(response[7], 1)
        self.assertEqual(response[8], '')

        card_play = '''
        SELECT * FROM CardsPlay
        WHERE CardId = '41252'
        '''
        cur.execute(card_play)
        response = cur.fetchall()
        self.assertTrue(all([r[1] > 0 for r in response]))
        self.assertTrue(all([r[2] > 0 for r in response]))
        self.assertTrue(all([0 < r[3] < 100 for r in response]))
        self.assertTrue(all([1 <= r[4] <= 2 for r in response]))
        self.assertTrue(all([r[5] in ['Standard', 'Wild', 'Arena'] for r in response]))

    def test_deck_storage(self):
        conn = sqlite3.connect('HeartStone.sqlite')
        cur = conn.cursor()
        deck1 = '''
        SELECT * FROM Decks
        JOIN DeckDetail ON Decks.NameId = DeckDetail.DeckId
        WHERE UId = 'D5dZ5PwKW39digsf23VDs' AND Mode = 'Standard'
        '''
        cur.execute(deck1)
        response = cur.fetchall()
        self.assertTrue(all([r[1] == 216 for r in response]))
        self.assertTrue(all([r[2] == 'PALADIN' for r in response]))
        self.assertEqual(len(set([r[7] for r in response])), 1)
        self.assertEqual(len(set([r[9] for r in response])), len([r[9] for r in response]))
        self.assertTrue(all([r[-1] == 'Odd Paladin' for r in response]))

        deck2 = '''
        SELECT * FROM Decks
        JOIN DeckDetail ON Decks.NameId = DeckDetail.DeckId
        WHERE UId = 'VEFq4jLsJMnyY3MIQb1y3c' AND Mode = 'Wild'
        '''
        cur.execute(deck2)
        response = cur.fetchall()
        self.assertTrue(all([r[1] == 129 for r in response]))
        self.assertTrue(all([r[2] == 'PRIEST' for r in response]))
        self.assertEqual(len(set([r[7] for r in response])), 1)
        self.assertEqual(len(set([r[9] for r in response])), len([r[9] for r in response]))
        self.assertTrue(all([r[-1] == 'Big Priest' for r in response]))

    # test the functions under DashApp
    def test_dash_get_deck_detail(self):
        sample_list = '[[40523,2],[1029,2],[40397,2],[40596,1],[43417,1],[40797,2],[95,2],[39841,1],[64,2],[42759,2],[43288,2],[43294,2],[1124,2],[45828,2],[42656,2],[38318,1],[40372,2]]'
        res = get_deck_detail(sample_list).split("; ")
        self.assertTrue('Jade Blossom*2' in res)
        self.assertTrue('Aya Blackpaw*1' in res)
        self.assertTrue('Aya Blackpaw*2' not in res)
        self.assertTrue('Jade Chieftain*1' not in res and 'Jade Chieftain*2' not in res)


    def test_dash_cards_in_decks_detail(self):
        sample_list = '[[40523,2],[1029,2],[40397,2],[40596,1],[43417,1],[40797,2],[95,2],[39841,1],[64,2],[42759,2],[43288,2],[43294,2],[1124,2],[45828,2],[42656,2],[38318,1],[40372,2]]'
        cost, attack, health = cards_in_decks_detail(sample_list)
        self.assertEqual(cost['0'], 0)
        self.assertEqual(cost['7'], 4)
        self.assertEqual(cost['5'], 2)
        self.assertEqual(attack['7'], 1)
        self.assertTrue(attack['0'] == 0 and attack['1'] == 0 and attack['2'] == 0 and attack['4'] == 0)
        self.assertEqual(health['0'], 0)
        self.assertEqual(health['7'], 2)

    def test_dash_cards_images(self):
        sample1 = '2286'
        sample2 = '41118'
        name1, set1, Img1, ImgGold1 = cards_images(sample1)
        name2, set2, Img2, ImgGold2 = cards_images(sample2)

        self.assertEqual(name1, 'Twilight Whelp')
        self.assertEqual(name2, 'Sergeant Sally')
        self.assertEqual(set1, 'Blackrock Mountain')
        self.assertEqual(set2, 'Mean Streets of Gadgetzan')
        self.assertEqual(Img1, 'http://media.services.zam.com/v1/media/byName/hs/cards/enus/BRM_004.png')
        self.assertEqual(ImgGold1, 'http://media.services.zam.com/v1/media/byName/hs/cards/enus/animated/BRM_004_premium.gif')
        self.assertEqual(Img2, 'http://media.services.zam.com/v1/media/byName/hs/cards/enus/CFM_341.png')
        self.assertEqual(ImgGold2, 'http://media.services.zam.com/v1/media/byName/hs/cards/enus/animated/CFM_341_premium.gif')

unittest.main(verbosity = 2)
