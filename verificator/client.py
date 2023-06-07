import discord
import disnake
from disnake import commands

bot = commands.Bot(command_prefix='/', description='Role bot')

ALLOWED_ROLE_IDS = [1007628548682559499, 1007628632874823793, 1094558594185318511] #роли которые могут выдавать саппорты
ADMIN_ROLE_ID = 1094558594185318511 #админская роль
SUPPORT_ROLE_ID = 1007550395838631996 #роль саппортов

@bot.event
async def on_ready():
    print(f'{bot.user.name} подключен к серверам Discord')

@bot.slash_command(name='verify', description='Выдать роль пользователю')
@commands.has_any_role(ADMIN_ROLE_ID, SUPPORT_ROLE_ID)
async def add_role(ctx: disnake.SlashContext, member: disnake.Member, role_name: str):
    role = disnake.utils.get(ctx.guild.roles, name=role_name)
    if role is not None:
        if role.id in ALLOWED_ROLE_IDS:
            await member.add_roles(role)
            await ctx.send(f'Роль {role_name} успешно выдана пользователю {member.mention}!')
        else:
            await ctx.send(f'Извините, роль {role_name} не может быть назначена ботом, если это ошибка обратитесь к Администрации.')
    else:
        await ctx.send(f'Извините, роль {role_name} не найдена на этом сервере.')

@bot.slash_command(name='unverify', description='Исключить пользователя и выдать стандартную роль')
@commands.has_any_role(ADMIN_ROLE_ID, SUPPORT_ROLE_ID)
async def remove_roles_and_verify(ctx: disnake.SlashContext, member: disnake.Member):
    await member.edit(roles=[], reason='Unverify command used')
    await member.add_roles(discord.utils.get(ctx.guild.roles, id=1111625903286530058), reason='Unverify command used')
    await ctx.send(f'Пользователь {member.mention} был не допущен на сервер.')

@bot.slash_command(name='clear', description='Очистить чат') #команда очисти сообщений из чата(вдруг пригодится)
@commands.has_role(ADMIN_ROLE_ID)
async def clear_chat(ctx: disnake.SlashContext, amount: int = 5):
    await ctx.channel.purge(limit=amount)
    await ctx.send(f'{amount} сообщений было успешно удалено из чата!')

with open('token.txt', 'r') as fp:
    TOKEN = fp.readline().strip()

bot.run(TOKEN) #либо укажите тут токен вашего бота, либо для удобства создайте token.txt и впишите его туда
