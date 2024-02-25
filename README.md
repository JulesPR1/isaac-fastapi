# The Binding of Isaac API & Wiki Scraper

#### Version 0.1

### Live at: https://isaac-fastapi.onrender.com/
It might take a few seconds to load the first time due to the free tier of the hosting service

## Description

This is a simple API that scrapes the wiki of the game The Binding of Isaac and returns the data in a JSON format. It is built with FastAPI and deployed with Render.

>#### Python <ins>3.12.0</ins>
>-------------------
>#### BeautifulSoup (bs4) <ins>0.0.2</ins>
>-------------------
>#### FastAPI <ins>0.109.2</ins>
>-------------------
>#### Uvicorn <ins>0.27.1</ins>

## Installation

get it on your local machine

```bash
git clone https://github.com/JulesPR1/isaac-fastapi.git
```

## Usage

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Endpoints

### GET /items

Returns a list of all items in the game

```bash
{
  "name":"Eye of Belial",
  "id":"462",
  "icon":"https://static.wikia.nocookie.net/bindingofisaacre_gamepedia/images/1/1f/Collectible_Eye_of_Belial_icon.png/revision/latest?cb=20210822015805",
  "quote":"Possessed tears!",
  "description":"Grants piercing tears. After piercing one enemy, tears start homing and deal double damage.",
  "quality":"3"
}
```

### GET /characters

Returns a list of all characters (not tainted yet) in the game

```bash
{
  "name": "Isaac",
  "Health": ["Full red heart", "Full red heart", "Full red heart"],
  "Damage": "3.5 (*1.00)", "Tears": "+0", "Shot Speed": "1", "Range": "6.5 23.75",
  "Speed": "1.0",
  "Luck": "0",
  "Starting Pickup(s)": "x1 bombs", 
  "Starting Item(s)": "The D6", 
  "achievements": [
    {"condition": "Boss Rush", "unlockable": "Isaac's Head"},
    {"condition": "Mom's Heart", "unlockable": "Lost Baby"},
    {"condition": "Satan", "unlockable": "Mom's Knife"}, 
    {"condition": "Isaac", "unlockable": "Isaac's Tears"}
    ...
  ]
}, ...
```

## Upcoming Features

- Add more endpoints : 
  - /enemies
  - /bosses
  - /rooms
  - /trinkets
  - /pickups
  - /transformations
- Upgrade the scraper to get more data
  - Get the data for the tainted characters
  - Get items details
- Add a frontend to display the data

## Legal Notice

The Binding of Isaac is a game by Edmund McMillen and Florian Himsl. All rights reserved.