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
Since this app has been uploaded on Heroku, you can run it directly on [link](si-507-final-hearthstone-app.herokuapp.com) (This could be slow)  
Or you should clone this repository, at least `HeartStone.sqlite` and `DashApp.py`
to your PC, and run `python3 DashApp.py`  
You may need to download the packages listed in `requirements.txt`  

### Core structures
##### For DashApp:
There are three main parts for this code:  
1. The layout of this app;     
2. The interactivity control;
3. Codes and functions for accessing data and processing;  

Layout:    
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
Interactivity:   
All the interactivity control codes start with `@app.callback`. They control the Interactions
between the two tables and the display of details and figures.    
There're 11 interactivity controls:  
`update_selected_row_indices_decks` and `update_selected_row_indices_cards` return the indexes of selected rows in table;  
7 functions start with `update_figure` return the data collected from Apr. 3 to now of selected rows;   
`update_deck_detail` and `update_cards_image` gives the composition of decks and images of cards

Accessing Data and Processing:    
