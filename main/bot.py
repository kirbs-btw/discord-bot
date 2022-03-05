import discord
import sqlite3
import datetime

client = discord.Client()


@client.event
async def on_ready():
    print(f"hello i´m {client.user.name}")
    client.loop.create_task(status_task())
async def status_task():
    while True:
        await client.change_presence(activity=discord.Game('mit marlin'), status=discord.Status.online)


@client.event
async def on_message(message):
    if message.author.bot:
        return

    streak_print = 0
    if message.content == '%daily':
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
    await message.channel.send(f"daily streak = [{streak_print}]")

client.run('OTQ5NDAxNzAzNzUxNTAzOTEz.YiJ1PQ._q_oAkVmy8DYAat6adTI_9NlYag')