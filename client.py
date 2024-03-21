import discord, os
from datetime import datetime

client = discord.Client(intents=discord.Intents.all())

if not os.path.exists('logs'):
    os.makedirs('logs')
log_filename = f"logs/{datetime.now().strftime('%Y-%m-%d')}.txt"
log_file = open(log_filename, 'a', encoding='utf-8')

def log_action(action):
    log_file.seek(0)
    log_file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {action}\n")
    log_file.flush()
    log_file.truncate()
    print(action)

@client.event
async def on_voice_state_update(member, before, after):
    with open("USERID.txt", "r", encoding='utf-8') as userid_file:
        userid = int(userid_file.read().strip())
        if member.id == userid:
            if before.channel != after.channel:
                if after.channel is not None:
                    log_action(f"Пользователь {member.display_name} вошел в голосовой канал: {after.channel.name} на сервере: {after.channel.guild.name}")
                if before.channel is not None:
                    log_action(f"{member.display_name} покинул голосовой канал: {before.channel.name} на сервере: {before.channel.guild.name}")

@client.event
async def on_message(message):
    with open("USERID.txt", "r", encoding='utf-8') as userid_file:
        userid = int(userid_file.read().strip())
        if message.author.id == userid:
            log_action(f"Пользователь {message.author.display_name} отправил сообщение на сервере: {message.guild.name} в канал {message.channel.name}")
            
@client.event
async def on_member_join(member):
    with open("USERID.txt", "r", encoding='utf-8') as userid_file:
        userid = int(userid_file.read().strip())
        if member.id == userid:
            log_action(f"Пользователь {member.display_name} зашёл на сервер {member.guild.name}")

@client.event
async def on_member_remove(member):
    with open("USERID.txt", "r", encoding='utf-8') as userid_file:
        userid = int(userid_file.read().strip())
        if member.id == userid:
            log_action(f"Пользователь {member.display_name} вышел с сервера {member.guild.name}")

@client.event
async def on_member_ban(guild, member):
    with open("USERID.txt", "r", encoding='utf-8') as userid_file:
        userid = int(userid_file.read().strip())
        if member.id == userid:
            log_action(f"Пользователь {member.display_name} получил бан на сервере {guild.name}")
@client.event
async def on_member_update(before, after):
    with open("USERID.txt", "r", encoding='utf-8') as userid_file:
        userid = int(userid_file.read().strip())
        member = await client.fetch_user(userid)
        if before.id == userid:
            if before.nick != after.nick:
                log_action(f"Никнейм пользователя {before.display_name} изменился: {before.nick} -> {after.nick} ( {member.display_name} )")
            if before.roles != after.roles:
                removed_roles = [role.name for role in before.roles if role not in after.roles]
                added_roles = [role.name for role in after.roles if role not in before.roles]
                if removed_roles:
                    log_action(f"Пользователь {before.display_name} потерял роли: {', '.join(removed_roles)} ( {member.display_name} )")
                if added_roles:
                    log_action(f"Пользователь {before.display_name} получил роли: {', '.join(added_roles)} ( {member.display_name} )")

@client.event
async def on_message_edit(before, after):
    with open("USERID.txt", "r", encoding='utf-8') as userid_file:
        userid = int(userid_file.read().strip())
        if before.author.id == userid:
            log_action(f"Пользователь {before.author.display_name} отредактировал сообщение на сервере: {before.guild.name} в канале {before.channel.name}")


@client.event
async def on_message_delete(message):
    with open("USERID.txt", "r", encoding='utf-8') as userid_file:
        userid = int(userid_file.read().strip())
        if message.author.id == userid:
            log_action(f"Пользователь {message.author.display_name} удалил сообщение на сервере {message.guild.name} в канале {message.channel.name}")

@client.event
async def on_ready():
    log_action("Клиент запущен")
    print(f"Информация об акаунте {client.user.name}\nДата создания аккаунта {client.user.created_at.strftime('%Y.%m.%d')}")

@client.event
async def on_disconnect():
    log_action("Клиент Отключен")
    log_file.close()


with open("token.txt", "r", encoding='utf-8') as tokenfile:
    token = str(tokenfile.read().strip())
client.run(token, bot=False)