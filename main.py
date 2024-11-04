import requests
import csv
import datetime
import asyncio
import os
import pytz
import discord  # Import discord for Intents
from discord.ext import commands

# Constants
CSV_URL = os.getenv("GOOGLE_SPREADSHEET")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
TIMEZONE = os.getenv("TIMEZONE", "US/Eastern")
eastern = pytz.timezone(TIMEZONE)

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
            try:
                event_time_naive = datetime.datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
                event_time = eastern.localize(event_time_naive)
                
                # Send reminder if event time matches the current time
                if now >= event_time and now < event_time + datetime.timedelta(minutes=1):
                    await channel.send(
                        f"🔔 **Event Reminder** 🔔\n\n**{description}**\n\n"
                        f"📅 Date & Time: {event_time.strftime('%Y-%m-%d %H:%M %p')}\n\n"
                        f"🔗 [Zoom link]({zoom_link})"
                    )
            except ValueError as e:
                print(f"❌ Error parsing date and time for row {row}: {e}")

        await asyncio.sleep(60)  # Check every minute


# Function: Send daily summary of events
async def send_daily_summary():
    channel = bot.get_channel(CHANNEL_ID)
    if channel is None:
        print("❌ Error: Channel not found.")
        return

    data = fetch_csv_data(CSV_URL)  # Fetch CSV data directly from URL
    now = datetime.datetime.now(eastern).date()
    summary_message = "📅 **Today's Upcoming Events**:\n"

    for row in data[1:]:
        date_str, time_str, description, _, _ = row
        event_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        if event_date == now:
            summary_message += f"- 📝 {description} at 🕒 {time_str}\n"

    if summary_message.strip():
        await channel.send(summary_message)

# Run the bot
bot.run(os.getenv("BOT_TOKEN"))
