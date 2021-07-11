# Discord Trade Activity Bot

## Pre Reqs
1. Create a TDA developer account here https://developer.tdameritrade.com/ and make a new app with a callback url of "http://127.0.0.1" and take note of the "Consumer Key" this is the api key you will give this script
2. Create webhook in the discord text channel you want to use by going to the text channels settings -> Integrations -> Webhooks -> New Webhook then copy the URL

## How To Run From Source
1. In Terminal Run: `python main.py`
2. Enter TDA Account ID and Webhook URL
3. Done! You can shut down the bot at anytime when you don't need it and to restart it repeat step #2

Note: Config is saved in userData folder. To change webhook url and TDA account ID delete the savedconfig file
