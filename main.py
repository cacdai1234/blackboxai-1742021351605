import discord
from discord.ext import commands
import sympy as sp
import math
import random
import wikipedia
import requests

TOKEN = "MTM1NDgwODg5MDE3NjMxMTQ0Nw.GzzcCe.B73Wf1Ilv8g_cYGc-wr4vMNXt4T-NCtOEdxRz4"
WEATHER_API = "d6c7760bec2ec69789632c391e7c8dbd"

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'✅ Bot đã online: {bot.user}')

# 📡 Ping bot
@bot.command()
async def ping(ctx):
    await ctx.send(f'🏓 Pong! `{round(bot.latency * 1000)}ms`')

# 🔢 Giải toán
@bot.command()
async def giai(ctx, *, expression):
    try:
        x = sp.symbols('x')
        if '=' in expression:
            expr = expression.replace('=', '-(') + ')'
            solution = sp.solve(expr, x)
            await ctx.send(f'📐 Nghiệm của `{expression}` là: `{solution}`')
        elif any(op in expression for op in ['+', '-', '*', '/', '**']):
            result = eval(expression)
            await ctx.send(f'🧮 Kết quả của `{expression}` là: `{result}`')
        else:
            await ctx.send('❌ Không hiểu yêu cầu!')
    except Exception as e:
        await ctx.send(f'⚠️ Lỗi: `{e}`')

# 🌤️ Weather
@bot.command()
async def weather(ctx, *, city):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API}&units=metric"
        data = requests.get(url).json()
        desc = data["weather"][0]["description"].capitalize()
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        await ctx.send(f"🌍 **Thời tiết tại {city}**\n🌡️ Nhiệt độ: `{temp}°C`\n💧 Độ ẩm: `{humidity}%`\n🌬️ Tốc độ gió: `{wind_speed} m/s`\n🌥️ Trạng thái: `{desc}`")
    except:
        await ctx.send("❌ Không thể lấy dữ liệu thời tiết!")

# 🎭 Meme
@bot.command()
async def meme(ctx):
    try:
        response = requests.get("https://meme-api.com/memes/random")
        data = response.json()
        await ctx.send(data["url"])
    except:
        await ctx.send("❌ Không thể lấy meme!")

# 📝 Wikipedia
@bot.command()
async def wiki(ctx, *, query):
    try:
        summary = wikipedia.summary(query, sentences=2)
        await ctx.send(f'📖 **{query}**: {summary}')
    except:
        await ctx.send("❌ Không tìm thấy thông tin!")

# 🎲 Mini games
@bot.command()
async def dice(ctx):
    await ctx.send(f'🎲 Bạn tung được `{random.randint(1, 6)}`!')

@bot.command()
async def flip(ctx):
    await ctx.send(random.choice(["🪙 Mặt ngửa!", "🪙 Mặt sấp!"]))

@bot.command()
async def rps(ctx, choice):
    options = ["rock", "paper", "scissors"]
    bot_choice = random.choice(options)
    result = "🤝 Hòa!" if choice == bot_choice else "✅ Bạn thắng!" if (choice == "rock" and bot_choice == "scissors") or (choice == "paper" and bot_choice == "rock") or (choice == "scissors" and bot_choice == "paper") else "❌ Bot thắng!"
    await ctx.send(f'✊✋✌️ Bạn chọn `{choice}`, bot chọn `{bot_choice}`. {result}')

# 🔨 Quản lý server (chỉ admin và Support)
def is_admin_or_support():
    async def predicate(ctx):
        return ctx.author.guild_permissions.administrator or discord.utils.get(ctx.author.roles, name="Support") is not None
    return commands.check(predicate)

@bot.command()
@is_admin_or_support()
async def kick(ctx, member: discord.Member, *, reason="Không có lý do"):
    await member.kick(reason=reason)
    await ctx.send(f'👢 {member.mention} đã bị kick! Lý do: `{reason}`')

@bot.command()
@is_admin_or_support()
async def ban(ctx, member: discord.Member, *, reason="Không có lý do"):
    await member.ban(reason=reason)
    await ctx.send(f'⛔ {member.mention} đã bị ban! Lý do: `{reason}`')

@bot.command()
@is_admin_or_support()
async def mute(ctx, member: discord.Member, *, reason="Không có lý do"):
    muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
    if not muted_role:
        muted_role = await ctx.guild.create_role(name="Muted")
        for channel in ctx.guild.channels:
            await channel.set_permissions(muted_role, send_messages=False)
    await member.add_roles(muted_role)
    await ctx.send(f'🔇 {member.mention} đã bị mute! Lý do: `{reason}`')

@bot.command()
@is_admin_or_support()
async def unmute(ctx, member: discord.Member):
    muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
    await member.remove_roles(muted_role)
    await ctx.send(f'🔊 {member.mention} đã được unmute!')

# 📜 Lệnh menu
@bot.command(name="menu")
async def menu(ctx):
    commands_list = """
📜 **Danh sách lệnh:**
🏓 `!ping` - Kiểm tra độ trễ bot.
🔢 `!giai <biểu thức>` - Giải toán (cộng, trừ, nhân, chia, phương trình...)
🌤️ `!weather <thành phố>` - Tra cứu thời tiết chi tiết.
🎭 `!meme` - Gửi meme ngẫu nhiên.
📝 `!wiki <từ khóa>` - Tìm kiếm thông tin trên Wikipedia.
🎲 `!dice` - Tung xúc xắc.
🪙 `!flip` - Tung đồng xu.
✊✋✌️ `!rps <rock/paper/scissors>` - Chơi kéo búa bao với bot.
🔨 `!kick @user [lý do]` - Kick người dùng.
⛔ `!ban @user [lý do]` - Ban người dùng.
🔇 `!mute @user [lý do]` - Mute người dùng.
🔊 `!unmute @user` - Bỏ mute người dùng.
📜 `!menu` - Hiển thị danh sách lệnh.
    """
    await ctx.send(commands_list)

bot.run(TOKEN)
