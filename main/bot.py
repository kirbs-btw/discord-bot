import discord
import sqlite3
import datetime
import re
import random
from key import *

print("starting bot...")
client = discord.Client()


@client.event
async def on_ready():
    now = datetime.datetime.now().strftime("%H:%M:%S")

    print(f"Bot online:     {client.user.name}")
    print(f"Online at:      {now}\n")
    client.loop.create_task(status_task())

async def status_task():
    while True:
        await client.change_presence(activity=discord.Game('kw-corp.de'), status=discord.Status.online)


@client.event
async def on_message(message):

    if message.author.bot:
        return

    if message.content == '%daily':
        streak_print = 0

        conn = sqlite3.connect("db.sql")
        cur = conn.cursor()
        command = "CREATE TABLE IF NOT EXISTS daily(discord_id INT, daily_streak INT, last_daily DATE)"
        cur.execute(command)
        conn.commit()

        discordId = message.author.id

        conn = sqlite3.connect("db.sql")
        cur = conn.cursor()

        today = datetime.date.today()
        yesterday = datetime.date.today() - datetime.timedelta(days=1)

        # missing checks if existent
        userNotExist = False

        command = f"SELECT * FROM daily WHERE discord_id = '{discordId}'"
        userData = cur.execute(command).fetchall()

        if userData == []:
            userNotExist = True
        if userNotExist:
            command = f"INSERT INTO daily VALUES({discordId}, 1, '{today}')"
            cur.execute(command)
            conn.commit()
            lastDaily = yesterday
        else:
            userData = userData[0]
            streak = int(userData[1])
            lastDaily = userData[2]

            if str(lastDaily) == str(yesterday):
                streak += 1
            elif str(lastDaily) == str(today):
                pass
            elif str(lastDaily) != str(yesterday):
                streak = 1

            streak_print = streak

            command = f"UPDATE daily SET daily_streak = '{streak}', last_daily = '{today}' WHERE discord_id = '{discordId}'"
            cur.execute(command)
            conn.commit()
            conn.close()

        info = addMoney(discordId, streak_print, str(lastDaily))

        logMsg = f"{message.author.name} | {message.author.nick} | %daily | current money = {info[0]} | money added = {info[1]} | id = {discordId}"
        print(logMsg)

        embedVar = discord.Embed(title=f"Daily!",
                                 color=discord.Color.from_rgb(113, 235, 61),
                                 description=f"{message.author.nick}: {info[0]} \nStreak: {streak_print}")
        await message.channel.send(embed=embedVar)

    if re.search("^%flip", message.content):
        try:
            nameUser = message.author.nick
            if nameUser == None:
                nameUser = message.author.name

            coin = ["HEAD", "TAIL"]
            flip = random.randint(0, 1)
            if "%flip head" in message.content:
                pick = 0

            else:
                pick = 1

            amount = int(message.content[11::])
            discordId = message.author.id

            conn = sqlite3.connect("db.sql")
            cur = conn.cursor()

            command = f"SELECT * FROM userData WHERE id = '{discordId}'"
            userRow = cur.execute(command).fetchall()[0]

            currentMoney = userRow[1]
            if int(amount) > int(currentMoney):
                embedVar = discord.Embed(title=f"Not enough money!",
                                         color=discord.Color.from_rgb(235, 64, 52),
                                         description=f"Current balance = {currentMoney} : {nameUser}")
                await message.channel.send(embed=embedVar)

            elif int(amount) <= int(currentMoney) and int(amount) > 0:
                if pick == flip:
                    newMoney = int(currentMoney + amount)
                    command = f"UPDATE userData SET money = '{newMoney}' WHERE id = '{discordId}'"
                    embedVar = discord.Embed(title=f"{coin[flip]} - {nameUser}:",
                                             color=discord.Color.from_rgb(113, 235, 61),
                                             description=f"Balance: {newMoney}")
                    await message.channel.send(embed=embedVar)
                else:
                    newMoney = int(currentMoney - amount)
                    command = f"UPDATE userData SET money = '{newMoney}' WHERE id = '{discordId}'"

                    embedVar = discord.Embed(title=f"{coin[flip]} - {message.author.nick}:",
                                             color=discord.Color.from_rgb(235, 64, 52),
                                             description=f"Balance: {newMoney}")
                    await message.channel.send(embed=embedVar)
                cur.execute(command)
                conn.commit()

                logMsg = f"{message.author.name} | {message.author.nick} | %flip | current money = {currentMoney} | money added = {(newMoney - currentMoney)} | id = {discordId}"
                print(logMsg)
            elif int(amount) < 0:
                embedVar = discord.Embed(title=f"NAAAHHHH :/",
                                         color=discord.Color.from_rgb(235, 64, 52))
                await message.channel.send(embed=embedVar)
        except:
            embedVar = discord.Embed(title=f"That´s not a number! :)",
                                     color=discord.Color.from_rgb(86, 189, 230))
            await message.channel.send(embed=embedVar)

    if message.content == "%bal":
        discordId = message.author.id
        conn = sqlite3.connect("db.sql")
        cur = conn.cursor()

        command = f"SELECT * FROM userData WHERE id = '{discordId}'"
        userRow = cur.execute(command).fetchall()[0]

        currentMoney = userRow[1]

        embedVar = discord.Embed(title=f"Balance - {message.author.nick}:",
                                 color=discord.Color.from_rgb(86, 189, 230),
                                 description=f"{currentMoney}")
        await message.channel.send(embed=embedVar)

        #await message.channel.send(f"Current balance: \n{currentMoney} : {message.author.nick}")


def addMoney(discordId, streak, lastDaily):
    today = datetime.date.today()

    newMoney = 0
    moneyAdd = 0

    conn = sqlite3.connect("db.sql")
    cur = conn.cursor()

    command = f"SELECT * FROM userData WHERE id = '{discordId}'"
    userRow = cur.execute(command).fetchall()

    streakValue = streak * 100

    if userRow == []:
        moneyAdd = streakValue
        command = f"INSERT INTO userData VALUES({discordId}, {moneyAdd})"
        cur.execute(command)
        conn.commit()
        newMoney = moneyAdd
    elif str(lastDaily) == str(today) and userRow != []:
        moneyAdd = 0
        newMoney = userRow[0][1]
    else:
        currentMoney = userRow[0][1]

        moneyAdd = streakValue
        newMoney = currentMoney + streakValue
        command = f"UPDATE userData SET money = '{newMoney}' WHERE id = '{discordId}'"
        cur.execute(command)
        conn.commit()

    return [newMoney, moneyAdd]


client.run(key)