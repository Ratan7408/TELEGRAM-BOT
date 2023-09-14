"""
@author: RATAN
"""

import telebot #Telegram library
from telebot import types
import urllib.request
import json

telegramBotToken =  '5788472918:AAFSc5O0vSriF7ij192uqMC2NnpO35Auq3g' #by making a bot with BotFather in Telegram
bot = telebot.TeleBot(telegramBotToken)

@bot.message_handler(commands=['movie']) #the name of the command which will be called in the following way: /movie <movie name>
def movie(message):
    messageTxt = str(message.text)
    NameList = [x.strip() for x in messageTxt.split()]
    clearMovieName = ""
    for element in NameList[1:]: #starts after the /movie command
        clearMovieName = clearMovieName + element + "+" 
    clearMovieName = clearMovieName[:-1] #without the last + sign
    api = f'http://www.omdbapi.com/?t={clearMovieName}&apikey=<API-key>' #From http://www.omdbapi.com/
    #requesting the data of the movie from the website 
    req = urllib.request.Request(api, headers={'User-Agent': 'Mozilla/5.0'})
    resp = urllib.request.urlopen(req)
    text = resp.read().decode('utf-8')
    movieDict = json.loads(text) #transforming it into a dictionary
    errorKey = 'Error' 
    if errorKey in movieDict.keys(): #cheking if the movie exists and that the website and API are working
        error = movieDict.get('Error')
        bot.send_message(message.chat.id, error)
    else:
        movie = movieDict.get('Title')
        year = movieDict.get('Year')
        director = movieDict.get('Director')
        genre = movieDict.get('Genre')
        ratingInternet = movieDict.get('Ratings')
        ratingTextDict = ratingInternet[0]
        ratingInternet2 = ratingTextDict.get('Value')
        photoUrl = movieDict.get('Poster')
        textToShow = "Movie name: " + movie + "\nYear: " + str(year) + "\nDirector: " + director + "\nGenre: " + genre + "\nInternet Rating: " + ratingInternet2 + "\n"
        bot.send_message(message.chat.id, textToShow) #sending to the chat (by chad id) the data on the movie
        bot.send_photo(message.chat.id, photo=photoUrl) #sending to the chat (by chad id) the poster of the movie

bot.polling() #starting the bot
