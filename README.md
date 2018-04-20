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

