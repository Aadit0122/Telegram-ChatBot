import os
import youtube_dl
import telebot
import requests
from bs4 import BeautifulSoup
import yfinance as yf
API__Key = os.environ['API_KEY']
bot = telebot.TeleBot(API__Key)



@bot.message_handler(commands=['start'])
def greet(message):
    bot.reply_to(message, 'Hey! Hows it going?')

@bot.message_handler(commands=['Help'])
def help(message):
  bot.reply_to(message, 'What can I help you with?')
  bot.send_message(message.chat.id,'1. /Wall_Street_Bets')
  bot.send_message(message.chat.id,'2. /Weather')
  bot.send_message(message.chat.id,'2. /Mp3')
  
@bot.message_handler(commands=['Hello','Hi','Supp'])
def hello(message):
    bot.send_message(message.chat.id, 'Hello!')

@bot.message_handler(commands=['Thanks','TY','tenks'])
def Bye(message):
    bot.send_message(message.chat.id, 'Thank you for using my services')

@bot.message_handler(commands=['Wall_Street_Bets'], )
def get_stocks(message):
  response =''
  print('All values in USD\n')
  stocks = ['veru','aosl','dis','rblx','plug','hrtx','nvta','bngo','cvna','bbby']
  stock_data =[]
  for stock in stocks:
    data = yf.download(tickers=stock, period = '5d', interval = '5d')
    data = data.reset_index()
    response += f'-----{stock}-----\n'
    stock_data.append([stock])
    columns = ['stock']
    for index,row in data.iterrows():
      stock_position = len(stock_data) - 1
      price = round(row['Close'],2)
      format_date = row['Date'].strftime('%m/%d')
      response += f'{format_date}: {price}\n'
      stock_data[stock_position].append(price)
      columns.append(format_date)
    print()
  response = f'{columns[0] : <10}{columns[1] : ^10}{columns[2] : >10}\n'
  for row in stock_data:
    response+= f'{row[0] : <10}{row[1] : ^10}{row[2] : >10}\n'
  response += '\nStock Data'
  print(response)
  bot.send_message(message.chat.id, response)

def extract_arg(arg):
    return arg.split()[1]
@bot.message_handler(commands=['Weather'])
def Weather(message):
  city = extract_arg(message.text)
  response = 'Weather Report\n'
# creating url and requests instance
  url = "https://www.google.com/search?q="+"weather"+city
  html = requests.get(url).content
   
  # getting raw data
  soup = BeautifulSoup(html, 'html.parser')
  temp = soup.find('div', attrs={'class': 'BNeawe iBp4i AP7Wnd'}).text
  str = soup.find('div', attrs={'class': 'BNeawe tAd8D AP7Wnd'}).text
   
  # formatting data
  data = str.split('\n')
  time = data[0]
  sky = data[1]
   
  # getting all div tag
  listdiv = soup.findAll('div', attrs={'class': 'BNeawe s3v9rd AP7Wnd'})
  strd = listdiv[5].text
   
  # getting other required data
  pos = strd.find('Wind')
  other_data = strd[pos:]
  response+="Temperature is "+ temp+'\n'
  response+="Time: "+ time+'\n'
  response+="Sky Description: "+ sky+'\n'
  response+=other_data
  # printing all data
  print("Temperature is", temp)
  print("Time: ", time)
  print("Sky Description: ", sky)
  print(other_data)
  bot.send_message(message.chat.id, response)

@bot.message_handler(commands=['Mp3'])
def audio(message):
  video_url = extract_arg(message.text)
  video_info = youtube_dl.YoutubeDL().extract_info(url = video_url,download=False)
  filename = "audio.mp3"
  options={
      'format':'bestaudio/best',
      'keepvideo':False,
      'outtmpl':filename,
  }

  with youtube_dl.YoutubeDL(options) as ydl:
      ydl.download([video_info['webpage_url']])

  print("Download complete... {}".format(filename))
  bot.send_audio(message.chat.id,audio = open('audio.mp3','rb'))
  
bot.polling(non_stop = True)

