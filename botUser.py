import json
import xmltodict
import discord

from tda.auth import easy_client
from tda.streaming import StreamClient
from const import TOKEN_PATH, REDIRECT_URI
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from parsers import *

class BotUser():

  def __init__(self, webhook, accountID, apiKey):
    self._webhook = webhook
    self._loginDataPath = TOKEN_PATH + accountID
    self._accountID = accountID
    self._apiKey = apiKey

  @property
  def webhook(self):
    return self._webhook

  @property
  def accountID(self):
    return self._accountID

  @property
  def apiKey(self):
    return self._apiKey

  async def stream_account_activity(self):
    client = easy_client(
            api_key=self._apiKey,
            redirect_uri=REDIRECT_URI,
            token_path=self._loginDataPath,
            webdriver_func=lambda: webdriver.Chrome(ChromeDriverManager().install()))
    stream_client = StreamClient(client, account_id=int(self._accountID))

    await self.read_stream(self.send_message, stream_client)

  async def read_stream(self, handler, stream_client):
    await stream_client.login()
    await stream_client.quality_of_service(StreamClient.QOSLevel.EXPRESS)
    await stream_client.account_activity_sub()
    stream_client.add_account_activity_handler(handler)

    while True:
      await stream_client.handle_message()

  def send_message(self, msg):
    print('RAW TDA Response:\n', json.dumps(msg, indent=2))

    for msg in msg['content']:
      msgType = msg['MESSAGE_TYPE']
      msgData = msg['MESSAGE_DATA']
      if msgData:
        parsedDict = xmltodict.parse(msgData)
        rawJsonMSG = '```json\n' + json.dumps(parsedDict, indent=4) + '\n```'

        msgToSend = ''
        if msgType == 'OrderEntryRequest':
          # Disabled this for now, needs more formatted info to be useful
          msgToSend = orderEntryRequestFormatter(parsedDict)

        elif msgType == 'OrderFill':
          msgToSend = orderFillFormatter(parsedDict)
        else:
          return

        print('Parsed Response JSON:\n', rawJsonMSG)
        try:
          self._webhook.send(msgToSend, username='TDA Trade Notifier')
        except discord.errors.HTTPException as e:
          print('Discord HTTPException: ', e, '\nMsg Attempt: ', msgToSend)

