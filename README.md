# botisimo-exporter

Export Data from [Botisimo](https://botisimo.com) and import it into [StreamerBot](https://streamer.bot)


# Requirements
1. Botisimo account (Might need pro)
2. Streamer Bot
3. Streamer Bot [Points System] (https://extensions.streamer.bot/docs?topic=49)
4. Python 3.6+5. 

# How to use
## Get your API Client Key from Botisimo
Should be the bottom of your profile page

## Install the python requirements
`pip3 install --no-cache-dir -r requirements.txt`

## Run the exporter
`./export.py <Botisimo API Client Key>`
This will show you what page it is working on and output two files.

viewers.jsonl - Raw response from the API
viewers.csv - CSV file used by the importer to import users with more than zero points

## Import the botisimo_importer.sb into Streamer Bot
1. Open the `botisimo_importer.sb` file in a text editor and copy the contents
2. In Streamer.bot, click Import
3. Paste the string from the first step

## Configured the Streamer.bot Action
There will be an Action named "Botisimo Points Import" in the "Utility" group.
Edit the `Set Argument %filePath%...` sub-actions and change the "Value" field to point to the `viewers.csv` file from above

# Now what??
When Streamer.bot checks for who is in Twitch chat, it will run this Action which will look in the CSV file, find any users that have not had their points imported, and import them.
