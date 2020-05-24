
import requests
from trello import TrelloClient
import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import os

key = "your_api_key"
token = "your_api_token"
api_secret = "your_api_secret"
board_name = "Personal"
list_name = "A Meme A Day"
card_name = "dank memes"

links = []
cards_qty = 0

client = TrelloClient(
    api_key=key,
    api_secret=api_secret,
    token=token,
    token_secret=token
)

def get_list(board_id):
    url = f"https://api.trello.com/1/boards/{board_id}/lists"
    querystring = {"key": key, "token": token}
    response = requests.request("GET", url, params=querystring)
    list = response.json()
    return list
    
def get_card(board_id, list_name):
    url = f"https://api.trello.com/1/boards/{board_id}/lists"
    querystring = {"name": list_name, "key": key, "token": token}
    response = requests.request("GET", url, params=querystring)
    list = response.json()
    for each in list:
        if list_name in each['name']:
            return each['name']
    return None
	
def dank_meme():
    urls = ['https://www.reddit.com/r/dank_meme/','https://www.reddit.com/r/memes_of_the_dank/','https://www.reddit.com/r/dankmemes/', 
       'https://www.reddit.com/r/memes/', 'https://www.reddit.com/r/meme']
    for url in urls:
        page = requests.get(url).text
        soup = BeautifulSoup(page, 'html.parser')

        for raw_img in soup.find_all('img'):
            link = raw_img.get('src')
            if 'http' in link and '.png' not in link and link not in links:
                links.append(link)
                print(f'dank meme found: {link}')

all_boards = client.list_boards()
board = next(filter(lambda x: x.name == board_name, all_boards))
print(f'Board ID: {board.id}')
lists = get_list(board.id)

# to remove previously added meme card
for list in lists:
    my_list = board.get_list(list['id'])
    for card in my_list.list_cards():
        cards_qty += 1
        print(card)
        for a in card.attachments:
            if 'meme' in a['name']:
                card.remove_attachment(a['id'])
        
print(f'Card quantity: {cards_qty}')

meme_config = get_card(board.id, list_name).lower()
            
if 'true' in meme_config:
    while len(links) < cards_qty:
        dank_meme()
        
    for list in lists:
        my_list = board.get_list(list['id'])
        for card in my_list.list_cards():
            cardlbl = str(card)
            if card_name in cardlbl:
                print(f'Append dank meme into card: {card}')
                card.attach(name=list_name, url=links[cards_qty])
                cards_qty -= 1