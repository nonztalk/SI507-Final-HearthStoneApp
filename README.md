# SI507 Final HearthStoneApp
### Data source:   
[HSReplay.net](https://hsreplay.net/)      
For the statistical data, although the API is public, there is no clear document for these API.
To access the data, you need to inspect the webpage elements, and find the data these pages
are loading under the "Network" and choose "Other".  
Now you may see the data links, and you can retrieve the data directly:  
```python
import request
import json
response = request.get(file_url).json()
```
For deck information, you need to view at this [page](https://hsreplay.net/decks/)   
For card information, you need to view at this [page](https://hsreplay.net/cards/)  

[HearthstoneAPI](http://hearthstoneapi.com/#start)   
This api have quite clear document, you can find their tutorial [here](https://market.mashape.com/omgvamp/hearthstone)  
Note that before you use the api, you need to register an account and get the X-Mashape-key   
I use this API for getting the card image, so I just follow the instruction of getting cards by their name:
```python
import unirest
response = unirest.get("https://omgvamp-hearthstone-v1.p.mashape.com/cards/search/{name}",
  headers={
    "X-Mashape-Key": Your_Key
  }
)
```
For those who fail to install unirest, just replace `unirest.get` with `requests.get`

### To run this app
Since this app has been uploaded on Heroku, you can run it directly on [link](https://si-507-final-hearthstone-app.herokuapp.com/) (This could be slow)  
Or you should clone this repository, at least `HeartStone.sqlite` and `DashApp.py`
to your PC, and run `python3 DashApp.py`  
You may need to download the packages listed in `requirements.txt`  

### Core structures
#### For DashApp:
There are three main parts for this code:  
1. The layout of this app;     
2. The interactivity control;
3. Codes and functions for accessing data and processing;  

**Layout:**       
To view the codes for layout, just look at the variable `app.layout`, which includes:  
a deck information table, following with an area for presenting deck details and three plotly
figures for game counts, win rate and average time consumption;  
a card information table, following with another area for presenting card images, and another
four plotly figures.  
Note that both of the two tables are implemented by `dash_table_experiments`  
Here is a standard structure, also used in my code:  
```python
dt.DataTable(
  rows = df.to_dict('records'),
  sortable = True,
  row_selectable=True,
  filterable=True,
  selected_row_indices=[],
  id = 'DecksTable'
)
```   
**Interactivity:**      
All the interactivity control codes start with `@app.callback`. They control the Interactions
between the two tables and the display of details and figures.    
There're 11 interactivity controls:  
`update_selected_row_indices_decks` and `update_selected_row_indices_cards` return the indexes of selected rows in table;  
7 functions start with `update_figure` return the data collected from Apr. 3 to now of selected rows;   
`update_deck_detail` and `update_cards_image` gives the composition of decks and images of cards

**Accessing Data and Processing:**    
Data for presenting in tables are always the latest. A `SELECT CollectTime FROM Decks ORDER BY CollectTime DESC LIMIT 1` is used in SQL query to ensure this.
Another three functions serve for presenting details in App:   
`get_deck_detail` converts a string of list of card ids and copies to a string of card names     
`cards_in_decks_detail` returns the descriptive statistics of card cost, attack and health     
`cards_images` returns the image links and sets of cards, where a large dictionary is used to convert the abbreviative set names to full ones:
```python
{
  'CORE': 'Base',
  'EXPERT1': 'Core',
  'TGT': 'The Grand Tournament',
  'BRM': 'Blackrock Mountain',
  'GANGS': 'Mean Streets of Gadgetzan',
  'HOF': 'Hall of Fame',
  'NAXX': 'Curse of Naxxramas',
  'GVG': 'Goblins vs Gnomes',
  'HERO_SKINS': 'Heros',
  'ICECROWN': 'Knights of the Frozen Throne',
  'KARA': 'One Night in Karazhan',
  'LOE': 'The League of Explorers',
  'LOOTAPALOOZA': 'Kobolds & Catacombs',
  'OG': 'Whispers of the Old Gods',
  'UNGORO': 'Journey to Un\'Goro',
  'GILNEAS': 'The Witchwood'
}
```

#### For Databases:  
**Get Core Data:**      
`get_decks(mode)` and `get_cards_info(mode)` are used for retrieving the decks and cards game records. Since the records will change along with time, in order to avoid repeating data, a time stamp was set when first retreving.   
**Get More Details:**    
For card information, since it is the most stable one (compared with others), I define a class `Card` and a cache `cards_cache.json` here. `Card` has a method to output all attributions as list, in the convenience of giving it to database. Cache is constructed as the reference of collectable card for retrieving images.    
In table `CardDetail` and `DeckDetail`, also to avoid repeating data, I set the `DeckId` and `CardId` as unique, and use `INSERT OR IGNORE INTO` when update the tables.

### Usage  
To update the deck game records:   
```bash
python3 Database.py --update Decks
```
To update the card game records:    
```bash
python3 Database.py --update CardsPlay
```
**DANGER!!!! PLEASE DO NOT RUN --init!!!**   

To play with the app:   
Click the rows in tables, and the app will automatically show corresponding figures and details. You can choose multiple rows at the same time.

### Limitation
The previous selections will disappear when you filtering the tables if the selections are not included in the new tables. This limitation comes from `dash_table_experiments` itself as it is still under development.
