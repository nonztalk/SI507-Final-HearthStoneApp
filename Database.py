import sqlite3
import sys
from get_cards import *
from get_game_records import *

def init_db():
    conn = sqlite3.connect('HeartStone.sqlite')
    cur = conn.cursor()

    s_clean_CardDetail = '''
        DROP TABLE IF EXISTS 'CardDetail';
    '''
    cur.execute(s_clean_CardDetail)
    s_clean_Decks = '''
        DROP TABLE IF EXISTS 'Decks';
    '''
    cur.execute(s_clean_Decks)
    s_clean_CardsPlay ='''
        DROP TABLE IF EXISTS 'CardsPlay';
    '''
    cur.execute(s_clean_CardsPlay)
    s_clean_DeckDetail = '''
        DROP TABLE IF EXISTS 'DeckDetail';
    '''
    cur.execute(s_clean_DeckDetail)
    s_clean_CardImg = '''
        DROP TABLE IF EXISTS 'CardImg';
    '''
    cur.execute(s_clean_CardImg)
    conn.commit()

    s_construct_CardDetail = '''
    CREATE TABLE 'CardDetail' (
        'CardId' INTEGER NOT NULL UNIQUE,
        'Name' TEXT NOT NULL,
        'Type' TEXT NOT NULL,
        'Class' TEXT NOT NULL,
        'Rarity' TEXT NOT NULL,
        'Set' TEXT NOT NULL,
        'Cost' INTEGER NOT NULL,
        'Attack' INTEGER NOT NULL,
        'Health' INTEGER NOT NULL
    );
    '''
    cur.execute(s_construct_CardDetail)
    s_construct_Decks = '''
    CREATE TABLE 'Decks' (
        'UId' TEXT NOT NULL,
        'NameId' INTEGER NOT NULL,
        'DeckClass' TEXT NOT NULL,
        'TotalGames' INTEGER NOT NULL,
        'WinRate' TEXT NOT NULL,
        'AverageGameTime' NUMERIC NOT NULL,
        'AverageGameTurns' NUMERIC NOT NULL,
        'CardsIncluded' TEXT NOT NULL,
        'Mode' TEXT NOT NULL,
        'CollectTime' TEXT NOT NULL
    );
    '''
    cur.execute(s_construct_Decks)
    s_construct_CardsPlay = '''
    CREATE TABLE 'CardsPlay' (
        'CardId' INTEGER NOT NULL,
        'Popularity' NUMERIC NOT NULL,
        'UseFrequency' INTEGER NOT NULL,
        'CardWinRate' NUMERIC NOT NULL,
        'Copies' NUMERIC NOT NULL,
        'Mode' TEXT NOT NULL,
        'CollectTime' TEXT NOT NULL
    );
    '''
    cur.execute(s_construct_CardsPlay)
    s_construct_DeckDetail = '''
    CREATE TABLE 'DeckDetail' (
        'DeckId' INTEGER NOT NULL UNIQUE,
        'DeckName' TEXT NOT NULL
    );
    '''
    cur.execute(s_construct_DeckDetail)
    s_construct_CardImg = '''
    CREATE TABLE 'CardImg' (
        'CardName' TEXT NOT NULL UNIQUE,
        'ImageLink' TEXT NOT NULL,
        'ImageGoldLink' TEXT NOT NULL
    );
    '''
    cur.execute(s_construct_CardImg)
    conn.commit

    conn.close()

def update_cards():
    conn = sqlite3.connect('HeartStone.sqlite')
    cur = conn.cursor()

    update = '''
    INSERT OR IGNORE INTO 'CardDetail'
    VALUES (?,?,?,?,?,?,?,?,?);
    '''
    cards = get_cards()
    for card in cards:
        cur.execute(update, tuple(card))

    conn.commit()
    conn.close()

def update_decks():
    conn = sqlite3.connect('HeartStone.sqlite')
    cur = conn.cursor()

    update = '''
    INSERT INTO 'Decks'
    VALUES (?,?,?,?,?,?,?,?,?,?);
    '''
    for mode in ['Standard', 'Wild']:
        decks = get_decks(mode)
        for deck in decks:
            cur.execute(update, tuple(deck))

    conn.commit()
    conn.close()

def update_cardplay():
    conn = sqlite3.connect('HeartStone.sqlite')
    cur = conn.cursor()

    update = '''
    INSERT INTO 'CardsPlay'
    VALUES (?,?,?,?,?,?,?);
    '''
    for mode in ['Standard', 'Wild', 'Arena']:
        cards = get_cards_info(mode)
        for card in cards:
            cur.execute(update, tuple(card))

    conn.commit()
    conn.close()

def update_deckdetail():
    conn = sqlite3.connect('HeartStone.sqlite')
    cur = conn.cursor()

    update = '''
    INSERT OR IGNORE INTO 'DeckDetail'
    VALUES (?,?);
    '''
    decks_info = get_decksDetail()
    for deck_info in decks_info:
        cur.execute(update, tuple(deck_info))

    conn.commit()
    conn.close()

def update_cardImg():
    conn = sqlite3.connect('HeartStone.sqlite')
    cur = conn.cursor()

    update = '''
    INSERT OR IGNORE INTO 'CardImg'
    VALUES (?,?,?);
    '''
    card_images = get_cards_image()
    for card_image in card_images:
        cur.execute(update, tuple(card_image))

    conn.commit()
    conn.close()

def isUpdated(table):
    conn = sqlite3.connect('HeartStone.sqlite')
    cur = conn.cursor()

    test = '''
    SELECT CollectTime FROM {} ORDER BY CollectTime DESC LIMIT 1;
    '''

    cur.execute(test.format(table))
    response = cur.fetchone()
    try:
        if response[0] == time:
            return True
        else:
            return False
    except:
        return False

if __name__ == '__main__':
    if sys.argv[1] == '--init':
        init_db()
        print('Databases created')
    if sys.argv[1] == '--update':
        if sys.argv[2] == 'CardDetail':
            update_cards()
            print('Table of card message updated')
        elif sys.argv[2] == 'DeckDetail':
            update_deckdetail()
            print('Table of deck message updated')
        elif sys.argv[2] == 'CardImg':
            update_cardImg()
            print('Image of cards updated')
        elif sys.argv[2] == 'Decks':
            if isUpdated('Decks'):
                print('Table has already updated')
            else:
                print('Updating ... ')
                update_decks()
        elif sys.argv[2] == 'CardsPlay':
            if isUpdated('CardsPlay'):
                print('Table has already updated')
            else:
                print('Updating ... ')
                update_cardplay()
