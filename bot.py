from bs4 import BeautifulSoup
import pandas as pd
import requests 
import discord 
import os 

intents = discord.Intents.all()
client = discord.Client(intents=intents)

def scrape_deals():
    pre_frame = {
        "date": [],
        "deal_url": [],
        "image_url": []
    }

    resp = requests.get("https://deal-ins.com")
    bs_object = BeautifulSoup(resp.text, "lxml")

    for deal, date, img in zip(bs_object.find_all("div", class_="entry-summary"), bs_object.find_all("time", class_="entry-date published"), bs_object.find_all("div", class_="entry-image-float")):
        pre_frame['deal_url'].append(deal.text.strip().split("👉")[1][0:23])
        pre_frame['date'].append(date.text.strip())
        pre_frame['image_url'].append(img.find('img').get('src'))

    df = pd.DataFrame(pre_frame)
    return df

@client.event
async def on_ready():
    print("Bot is online and ready...")

@client.event
async def on_message(message):
    if message.content.startswith("!show-deals"):
        deals_data = scrape_deals()
        await message.channel.send(deals_data[['date', 'deal_url']].head(30))

    # create an elif block, and under it look for a new command and do something upon receiving that command

client.run("")