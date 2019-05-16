#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.
#
# THIS EXAMPLE HAS BEEN UPDATED TO WORK WITH THE BETA VERSION 12 OF PYTHON-TELEGRAM-BOT.
# If you're still using version 11.1.0, please see the examples at
# https://github.com/python-telegram-bot/python-telegram-bot/tree/v11.1.0/examples

"""
Simple Bot to reply to Telegram messages.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
import os.path

from datetime import datetime
from threading import Timer
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

#Define a global variables
answer_list = ()
Game = False
Players = {}
#Time_timer = 7200.0
Time_timer = 30.0

# Define a class for players in game
class Player (object):
	"""docstring"""

	def __init__(self, id):
		"""Constructor"""
		self.id = id
		self.answer = set()
		self.count_answer = 0

	def check_answer(self, answer_in):
		self.answer.add(answer_in)
		if len(self.answer) != self.count_answer:
			self.count_answer = len(self.answer)
			string_log = '{} - {} - {}'.format(id, answer_in, datetime.today().isoformat(sep='T'))
			add_to_file(self.id, string_log)

	def show_stats(self):
		return([self.id,self.answer,self.count_answer])

# Define support function
def rewrite_file(filename):
	f = open(filename, "w")
	f.close()

def write_to_file(filename, string):
	f = open(filename, "w")
	f.write(string + '\n')
	f.close()

def append_to_file(filename, string):
	f = open(filename, "a")
	f.write(string + '\n')
	f.close()

def add_to_file(filename, string):
	if os.path.isfile(filename):
		append_to_file(filename, string)
	else:
		write_to_file(filename, string)

def load_game(filename):
	f = open(filename, "r")
	content = f.readlines()
	f.close()
	content = [x.strip() for x in content]
	return content

def game_of_on():
	#print("hello, world")
	global Game
	if Game == True:
		Game = False
	else:
		Game = True


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
	"""Send a message when the command /start is issued."""
	global Time_timer
	update.message.reply_text('Game started')
	game_of_on()
	t = Timer(Time_timer, game_of_on)
	t.start()

def finish(update, context):
	game_of_on()
	update.message.reply_text('Bay!')

def help(update, context):
	"""Send a message when the command /help is issued."""
	help_mes = '''Comands list:
	finish
	start
	addlist
	add
	load
	login
	resetanswer
	resetgame
	stats'''
	update.message.reply_text(help_mes)

def add(update, context):
	In_str = update.message.text[4:].strip()
	add_to_file('game_answer', In_str)
	update.message.reply_text('Answer:' + In_str)


def addlist(update, context):
	In_str = update.message.text[8:].split(' ')
	#print(In_str)
	for item in In_str:
		add_to_file('game_answer', item)
	update.message.reply_text(len(answer_list))

def load(update, context):
	global answer_list
	answer_list = load_game('game_answer')
	update.message.reply_text(len(answer_list))

def login(update, context):
	global Players
	Players[update.message.chat.id] = Player(update.message.chat.id)
	update.message.reply_text(update.message.chat.id)

def resetanswer(update, context):
	global answer_list
	rewrite_file('game_answer')
	answer_list = load_game('game_answer')
	update.message.reply_text(len(answer_list))
	#print(answer_list)

def resetgame(update, context):
	global Players
	for player in Players.keys():
		rewrite_file(player)
	Players.clear()
	update.message.reply_text('Game reseted!')

def stats(update, context):
	total_answer = len(answer_list)
	result = ''
	for player in Players.values():
		result += '{}: {}/{}\n'.format(player.show_stats()[0], player.show_stats()[-1], total_answer)
	#print(result)
	update.message.reply_text(result)

def cheat(update, context):
	global answer_list,Game,Players,Time_timer
	update.message.reply_text(answer_list)
	update.message.reply_text(Game)
	update.message.reply_text(len(Players))
	update.message.reply_text(Time_timer)

def echo(update, context):
	"""Echo the user message."""
	if update.message.text.startswith('.'):
			answer_for_check = update.message.text[1:].strip()
			if Game and answer_for_check in answer_list:
				update.message.reply_text('+')
				Players[update.message.chat.id].check_answer(answer_for_check)
				print(Players[update.message.chat.id].show_stats())
			else:
				update.message.reply_text('-')

def error(update, context):
	"""Log Errors caused by Updates."""
	logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("238706968:AAErHt_qyT5ZZJc4PoWgAWqeo9tFIS8msF8", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    #dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    # My commands
    dp.add_handler(CommandHandler("start", start)) #start game
    dp.add_handler(CommandHandler("finish", finish)) #stop game
    dp.add_handler(CommandHandler("addlist", addlist)) #add list of answer
    dp.add_handler(CommandHandler("add", add)) #add anwer
    dp.add_handler(CommandHandler("load", load)) #load answer
    dp.add_handler(CommandHandler("login", login)) #LoginUP player
    dp.add_handler(CommandHandler("resetanswer", resetanswer)) #delet all answer
    dp.add_handler(CommandHandler("resetgame", resetgame)) #Kick all playesrs
    #dp.add_handler(CommandHandler("setuptest", setuptest)) #test login 3 bots
    dp.add_handler(CommandHandler("stats", stats)) #stats of game
    dp.add_handler(CommandHandler("cheat", cheat)) #stats of game


    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()