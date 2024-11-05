import requests
import csv
import datetime
import asyncio
import os
import pytz
import discord  # Import discord for Intents
from discord.ext import commands
import random
import schedule
import time
import news

# Constants

CSV_URL = os.getenv("GOOGLE_SPREADSHEET")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
TIMEZONE = os.getenv("TIMEZONE", "US/Eastern")
eastern = pytz.timezone(TIMEZONE)
UNDERRATED_TECH = os.getenv("UNDERRATED_TECH")

# Discord Bot Setup
intents = discord.Intents.default()  # Corrected here
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Helper function: Fetch data from Google Sheets CSV link
def fetch_csv_data(url):
    response = requests.get(url)
    response.raise_for_status()  # Check for request errors
    data = response.content.decode('utf-8')
    return list(csv.reader(data.splitlines()))

# Event: Bot login
@bot.event
async def on_ready():
    print(f'✅ Logged in as {bot.user}')
    
    await check_and_send_messages()
    await send_daily_summary()
    schedule_daily_summary()
    while True:
        schedule.run_pending()
        time.sleep(1)
    



# Function: Check and send event reminders
async def check_and_send_messages():
    channel = bot.get_channel(CHANNEL_ID)
    if channel is None:
        print("❌ Error: Channel not found.")
        return

    while True:
        data = fetch_csv_data(CSV_URL)  # Fetch CSV data directly from URL
        now = datetime.datetime.now(eastern)

        for row in data[1:]:  # Skip header row
            # Ensure the row has enough columns
            if len(row) < 4:
                print(f"❌ Skipping row due to insufficient data: {row}")
                continue

            # Unpack values
            date_str, time_str, description, zoom_link = row[:4]
            if not date_str.strip() or not time_str.strip():
                print(f"Skipping row with missing date/time: {row}")
                continue
            try:
                event_time_naive = datetime.datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
                event_time = eastern.localize(event_time_naive)
                
                # Send reminder if event time matches the current time
                if now >= event_time and now < event_time + datetime.timedelta(minutes=1):
                    await channel.send(
                        f"🔔 **Event Reminder** 🔔\n\n**📅 {description}**\n\n"

                        f"🔗 [Zoom link]({zoom_link})"
                    )
            except ValueError as e:
                print(f"❌ Error parsing date and time for row {row}: {e}")

        await asyncio.sleep(60)  # Check every minute


# Function: Send daily summary of events
async def send_daily_summary():
    channel = bot.get_channel(UNDERRATED_TECH)
    if channel is None:
        print("❌ Error: Channel not found.")
        return

     # Call news.ai_news() to fetch the daily summary
    await news.ai_news()
    
def schedule_daily_summary():
    schedule.every().day.at("12:00").do(lambda: bot.loop.create_task(send_daily_summary()))



@bot.event
async def on_message(message):
    channel = bot.get_channel(1289451911702904834)
    if channel is None:
        print("❌ Error: Channel not found.")
        return
    if message.author == bot.user:
        return
    
    if message.content.startswith('$pp'):
        random_number = random.randint(1, 10)
        await message.channel.send("8" + "=" * random_number + "D")

        # Add reactions or send GIFs based on the random number
        if random_number >= 7:
            # Send reaction for "pretty big"
            await message.add_reaction('👍')  # You can change the emoji if needed
            await message.channel.send("Drake ?!?!")
            await message.channel.send("https://media.giphy.com/media/cL4pqu8GGRIihabgSM/giphy.gif?cid=790b7611lfnv80ed7xj6pqjgd9capywp531tr7z5dxohsktq&ep=v1_gifs_search&rid=giphy.gif&ct=g")
        
        elif 3 <= random_number <= 6:
            # Send reaction and a GIF for "not bad"
            await message.add_reaction('👌')  # Reaction for "not bad"
            await message.channel.send("Not bad!")
            await message.channel.send("https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExZjljZnplNTRvYnQwOGdydGd1MHd5OGZza2U0ZDF0anptemptMXk5bCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/xThuW2Vrx2ruC42Dcc/giphy.gif")  # Replace with your GIF link
        
        elif random_number <= 2:
            # Send reaction and a GIF for "laughing"
            await message.add_reaction('😂')  # Reaction for "laughing"
            await message.channel.send("LMAO")
            await message.channel.send("https://media.giphy.com/media/3o6Zt4HU9uwXmXSAuI/giphy.gif?cid=790b7611lawpdpj3bqs7ynh1tzi0vhmnmdh3xcvrurnl9s8p&ep=v1_gifs_search&rid=giphy.gif&ct=g")  # Replace with your GIF link

 


# Run the bot
bot.run(os.getenv("BOT_TOKEN"))
