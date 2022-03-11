
from replit import db

import discord #upm package(py-cord)
from discord.ext import commands

import requests #upm package(requests)
import time

from dotenv import load_dotenv #upm package(dotenv)
import os

# We load the environment variables
load_dotenv()

DISCORD_TOKEN = os.environ['DISCORD_TOKEN']
 
DEFAULT_PREFIX = ">"

bot = discord.Client()
bot = commands.Bot(command_prefix=DEFAULT_PREFIX)

COLOR = 0xe36e00

# ─── UTILS ──────────────────────────────────────────────────────────────────────

async def reply(message):
	# We reply with a random cat image
	cat = requests.get(f'https://api.thecatapi.com/v1/images/search?api_key=c1404cc3-7fae-4c6e-8cb0-4d14303ae6d1').json()[0]

	if len(cat['breeds']) == 0:
		embed = discord.Embed(title="**Cat fan detected!**", description="Take this with you", color=COLOR)
		embed.set_image(url=cat['url'])
		await message.channel.send(embed=embed)
	else:
		embed = discord.Embed(title="**Cat fan detected!**", description="Take this with you", color=COLOR)
		embed.add_field(name="Breed", value=cat['breeds'][0]['name'], inline=False)
		embed.set_image(url=cat['url'])
		await message.channel.send(embed=embed)


# ─── DATABASE ───────────────────────────────────────────────────────────────────

from dataclasses import dataclass

@dataclass
class user:
	guild_id: int
	user_id: int
	cat_counter: int
	last_time: int

	def more_cats(self, new_cats):
		self.cat_counter += new_cats
		self.last_time = time.time()

	def reset_cats(self):
		self.cat_counter += 1
		self.last_time = time.time()

# ─── COMMANDS ───────────────────────────────────────────────────────────────────

@bot.command()
async def ping(ctx):
	await ctx.send("Yes, I'm conected to the server")

@bot.command()
async def cat(ctx):
	await reply(ctx)

# ─── EVENTS ─────────────────────────────────────────────────────────────────────

from typing import List

@bot.event
async def on_ready():
	# db = {
	# 	"serverid": [list of users]
	# }
	print("Bot is ready")

@bot.event
async def on_message(message):

	# We see if the last time someone used the bot is more than a day, we just clear
  the list (data is expensive) 	if time() - db[message.guild.id][0] >= 3600 * 24:
	    db[message.guild.id][1].clear()

	list_users = db[message.guild.id][1]
	# We check if the user is registered
	if message.author.id not in list_users:
		# We register the user
		list_users.append(user(message.guild.id, message.author.id, 0, time.time()))
		print(f"{message.author.name} has been registered")
	else:
		if any(x in message.content.lower() for x in ["cat", "kitty", "kitten", "kittycat", "kittens", "kittycats", "kitties"]):
			for keyw in ["cat", "kitty", "kitten", "kittycat", "kittens", "kittycats", "kitties"]:
				if keyw in message.content.lower():
					cat_counter += message.content.lower().count(keyw)
			
	  # Now we update the user
			list_users[message.author.id].more_cats(cat_counter)

		if time.time() - list_users[message.author.id].last_time > 60:

			list_users[message.author.id].reset_cats()
		
		else:
			if list_users[message.author.id].cat_counter >= 3:
				await reply(message)
				list_users[message.author.id].reset_cats()

bot.run(DISCORD_TOKEN)
