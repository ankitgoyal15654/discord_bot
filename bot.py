import sqlite3
import discord
from dotenv import load_dotenv
from googlesearch import search
conn = sqlite3.connect('test.db')
conn.execute('''CREATE TABLE IF NOT EXISTS information (id INTEGER PRIMARY KEY AUTOINCREMENT, username  TEXT NOT NULL, value TEXT NOT NULL, dt datetime default current_timestamp);''')

load_dotenv()
token = 'NjQ1OTY5Njk3MTg3MDM3MjE1.XdPtKw.dyjbn4rD9rVS8hlplb7-2zHsOVY'

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    message.content = message.content.lower()
    if message.content == 'hi':
        response = 'hey'
        await message.channel.send(response)
    elif message.content.startswith('!google'):
        query = message.content[8:]
        result = []
        cur = conn.cursor()
        cur.execute('INSERT INTO information (username,value) VALUES (?, ? );', (str(message.author), query))
        conn.commit()
        for j in search(query, tld="co.in", num=10, stop=5, pause=2):
            result.append(j)
        await message.channel.send(result)
    elif message.content.startswith('!recent'):
        query = message.content[8:]
        cur = conn.cursor()
        cur.execute("SELECT username, value FROM information where username = ? order by dt desc;", (str(message.author),))
        rows = cur.fetchall()
        result = []
        for row in rows:
            if query in row[1]:
                result.append(row[1])
        await message.channel.send(result)
client.run(token)