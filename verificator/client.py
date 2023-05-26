import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='/', description='Role bot')

ALLOWED_ROLE_IDS = [1007628548682559499, 1007628632874823793, 1094558594185318511]
ADMIN_ROLE_ID = 1094558594185318511
SUPPORT_ROLE_ID = 1007550395838631996
@bot.event
async def on_ready():
    print(f'{bot.user.name} подключен к серверам Discord')

@bot.command(name='verify')
@commands.has_any_role(ADMIN_ROLE_ID, SUPPORT_ROLE_ID)
async def add_role(ctx, member: discord.Member, *, role_name: str):
    role = discord.utils.get(ctx.guild.roles, name=role_name)
    if role is not None:
        if role.id in ALLOWED_ROLE_IDS:
            await member.add_roles(role)
            await ctx.send(f'Роль **{role_name}** успешно выдана пользователю {member.mention}!')
        else:
            await ctx.send(f'Извините, роль **{role_name}** не может быть назначена ботом, если это ошибка обратитесь к Администрации.')
    else:
        await ctx.send(f'Извините, роль **{role_name}** не найдена на этом сервере.')

@bot.command(name='unverify')
@commands.has_any_role(ADMIN_ROLE_ID, SUPPORT_ROLE_ID)
async def remove_roles_and_verify(ctx, member: discord.Member):
    await member.edit(roles=[], reason='Unverify command used')
    await member.add_roles(discord.utils.get(ctx.guild.roles, id=1111625903286530058), reason='Unverify command used')
    await ctx.send(f'Пользователь {member.mention} был не допущен на сервер.')

@bot.command(name='clear')
@commands.has_role(1094558594185318511)
async def clear_chat(ctx, amount=5):
    await ctx.channel.purge(limit=amount)
    await ctx.send(f'{amount} сообщений было успешно удалено из чата!')

with open('token.txt', 'r') as fp:
    TOKEN = fp.readline().strip()

bot.run(TOKEN)