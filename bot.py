import os
import discord
import re
from dotenv import load_dotenv
from random import randint

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

fnames = [fname for fname in os.listdir('.') if fname.endswith('.txt')]

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    content = str(message.content.lower()).strip()

    if content == '=version' or content == '=about':
        await message.channel.send('```\nVersion  : 0.0.2-1\nCodename : LOIS\n```')
        return

    if content == '=usage' or content == '=help':
        await message.channel.send('```\nSeason <season> <episode>:<line>\nOR\nSeason <season> <episode>:<begin>-<end>\n```')
        return

    if content == '=random':
        fnames = [fname for fname in os.listdir('.') if fname.endswith('.txt')]
        infilename = fnames[randint(0, len(fnames) - 1)]
        season, episode = infilename[:-4].split('_')
        infile = open(infilename, 'r')
        verses = infile.readlines()
        lo = randint(0, len(verses) - 1)
        hi = randint(lo, lo + (len(verses) if len(verses) - lo < 21 else 18))
        msg = f'```\nSEASON {season} EPISODE {episode} LINES {lo + 1}-{hi}\n{"".join(verses[lo : hi])}\n```'
        await message.channel.send(msg)
        infile.close()
        return


    infile = None
    try:
        re_obj = re.findall('season ([0-9][0-9]?) ([0-9][0-9]?)+:(.+)', content)[0]
        season = int(re_obj[0])
        episode = int(re_obj[1])
        verse = re_obj[2] if '-' in re_obj[2] else int(re_obj[2])

        infile = open(f'{season}_{episode}.txt', 'r')
        verses = infile.readlines()

        if type(verse) is int:
            await message.channel.send(f'```\n{verses[verse - 1]}```')
        else:
            lo, hi = map(int, verse.split('-'))
            msg = '```\n' + ''.join(verses[lo - 1 : hi]) + '```'
            await message.channel.send(msg)

        infile.close()

    except Exception:
        if infile is not None:
            infile.close()
    finally:
        return

client.run(TOKEN)