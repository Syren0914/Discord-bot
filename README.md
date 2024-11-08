# Tech Club Event Reminder Bot

This is a Python-based Discord bot that automatically fetches upcoming events from a public Google Sheets CSV link and sends event reminders to a specified Discord channel. The bot also posts a daily summary of events and shares interesting computer science topics daily, powered by Google Gemini AI.

## Features

- **Event Reminders**: Sends reminders in a Discord channel at a scheduled event time.
- **Daily Summary**: Posts a summary of all events scheduled for the day.
- **Daily CS Topics**: Shares daily interesting computer science topics using Google Gemini AI.
- **CSV Integration**: Fetches event data directly from a Google Sheets CSV link.

## Requirements

- Python 3.8+
- A Discord bot token (setup instructions below)
- Access to Google Sheets with a public CSV link

### Python Libraries

The bot uses the following Python libraries:
- `discord.py`: For interacting with Discord
- `requests`: To fetch CSV data from Google Sheets
- `csv`: For parsing CSV data
- `pytz`: To manage timezones
- `gemini-ai`: For generating daily computer science topics

You can install the required libraries with:

```bash
pip install discord.py requests pytz gemini-ai
