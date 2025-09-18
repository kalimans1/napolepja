import os
import discord
from discord.ext import commands,tasks
import aiohttp
import json
import random
from colorama import Fore, Style
import httpx
import asyncio
import threading
from flask import Flask
import pyfiglet
import time

# ESM bypass denemesi
try:
    import discord_self
    discord_self.browser = True
    print("✅ ESM bypass aktif!")
except:
    print("⚠️  ESM yüklenmedi, normal devam...")

os.system("clear||cls")

with open("config.json", "r", encoding="utf-8") as f:
    cf = json.load(f)

mobile_status = cf["Mobile_Status"]
status_texts = cf["Status_Texts"]
status_emojis = cf["Status_Emojis"]
webhook = cf["Webhook"]
invg = cf["Invite_Guild_ID"]
stype = cf["Status"]
delay = cf["Delay"]
guild_id_ = cf["Guild_ID"]
channels = cf["J4J_Channel_Names"]
cmsgs = cf["Channel_Messages"]
dmsgs = cf["DM_Messages"]
dnmsgs = cf["Done_Messages"]
wb_ = cf["WebServer"]
webhook = webhook.replace("https://discord.com", "https://canary.discord.com")

# PROXY EKLENTİSİ - BAŞLANGIÇ
PROXIES = []
try:
    with open("proxies.txt", "r") as f:
        PROXIES = [line.strip() for line in f if line.strip()]
except:
    pass

def get_proxy():
    if PROXIES:
        return random.choice(PROXIES)
    return None

class logger:
    def log(content):
        try:
            httpx.post(webhook, json={'content': content})
        except Exception as e:
            print(e)
            colors.warning("Failed To Send Log")

class colors:
    def ask(qus):
        print(f"{Fore.LIGHTMAGENTA_EX}[?]{Fore.RESET}{Style.BRIGHT} {qus}{Fore.RESET}{Style.NORMAL}")

    def what(txt):
        print(f"{Fore.LIGHTBLUE_EX}[?]{Fore.RESET}{Style.BRIGHT} {txt}{Fore.RESET}{Style.NORMAL}")

    def banner(txt):
        print(f"{Fore.LIGHTMAGENTA_EX}{Style.BRIGHT}{txt}{Fore.RESET}{Style.NORMAL}")

    def error(txt):
        print(f"{Fore.RED}[{random.choice(['-', '!'])}]{Fore.RESET}{Style.DIM} {txt}{Fore.RESET}{Style.NORMAL}")

    def sucess(txt):
        print(f"{Fore.GREEN}[+]{Fore.RESET}{Style.BRIGHT} {txt}{Fore.RESET}{Style.NORMAL}")

    def warning(txt):
        print(f"{Fore.LIGHTYELLOW_EX}[!]{Fore.RESET}{Style.DIM} {txt}{Fore.RESET}{Style.NORMAL}")

    def log(txt):
        print(f"{Fore.LIGHTMAGENTA_EX}[!]{Fore.RESET}{Style.BRIGHT} {txt}{Fore.RESET}{Style.NORMAL}")

    def msg(txt, idx):
        return f"{Fore.LIGHTBLUE_EX}[{idx+1}]{Fore.RESET}{Style.BRIGHT} {txt}{Fore.RESET}{Style.NORMAL}"

    def ask2(qus):
        print(f"{Fore.LIGHTMAGENTA_EX}[+]{Fore.RESET}{Style.BRIGHT} {qus}{Fore.RESET}{Style.NORMAL}")

    def ask3(qus):
        print(f"{Fore.LIGHTBLUE_EX}[+]{Fore.RESET}{Style.BRIGHT} {qus}{Fore.RESET}{Style.NORMAL}")

async def start(self, token: str, *, reconnect: bool = True) -> None:
    """|coro|
    A shorthand coroutine for :meth:`login` + :meth:`connect`.
    """
    # User token için özel temizleme
    token = token.strip().strip('"').strip("'").strip()
    
    # Token'ın başında "Bot " varsa kaldır (user token için gerekli değil)
    if token.startswith("Bot "):
        token = token[4:]
        
    colors.warning(f"🔑 Logging In As -> {token[:12]}*****!")
    try:
        # User token için login (bot parametresi olmadan)
        await self.login(token)
        await self.connect(reconnect=reconnect)
    except Exception as e:
        print(f"[!] Login Hatası: {e}")
        if "improper" in str(e).lower() or "unauthorized" in str(e).lower():
            colors.error(f"❌ INVALID TOKEN -> {token[:12]}*****!")
            colors.warning("⚠️ User token'ını yeniden alın. F12 -> Network -> XHR -> Authorization header'dan alabilirsiniz.")
        elif "forbidden" in str(e).lower():
            colors.error(f"🚫 User Account Disabled/Suspended -> {token[:12]}*****!")
        else:
            colors.warning("🔧 Başka bir hata oluştu. (Rate Limit, Timeout, Bağlantı sorunu vs.)")

discord.Client.start = start
commands.Bot.start = start

def reset_db():
    with open("database.json", "r") as f:
        file = json.load(f)
    file["ignore"] = []
    with open("database.json", "w") as f:
        json.dump(file, f, indent=4)

def set_db(id,bid):
    with open("database.json", "r") as f:
        file = json.load(f)
    file["ignore"].append(f"{id}:{bid}")
    with open("database.json", "w") as f:
        json.dump(file, f, indent=4)

def has_ignore(id,bid):
    with open("database.json", "r") as f:
        file = json.load(f)
        ids = file["ignore"]
    toreturn = True if f"{id}:{bid}" in ids else False
    return toreturn

DB_RESET = False

class BotCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.prop = None

    @tasks.loop(seconds=15)
    async def activity_task(self):
        emo = random.choice(status_emojis)
        text = random.choice(status_texts)
        if stype == "online":
            stf = discord.Status.online
        elif stype == "idle":
            stf = discord.Status.idle
        elif stype == "dnd":
            stf = discord.Status.dnd
        await self.bot.change_presence(activity=discord.CustomActivity(name=text, emoji=emo), status=stf)

    @tasks.loop(seconds=delay)
    async def channel_task(self):
        guild = self.bot.get_guild(guild_id_)
        try:
            for channel in guild.channels:
                for cnl in channels:
                    if cnl in channel.name:
                        if self.bot:
                            msg = random.choice(cmsgs)
                            async with channel.typing():
                                await asyncio.sleep(random.randint(5, 15))
                                await channel.send(msg)
                            # ✅ MESAJ BAŞARIYLA GÖNDERİLDİ BİLDİRİMİ
                            colors.sucess(f"✅ MESAJ GÖNDERİLDİ -> {msg} | Kanal: {channel.name} | Bot: {self.bot.user}")
                            logger.log(f"✅ MESAJ GÖNDERİLDİ -> {msg} | Kanal: {channel.name} | Bot: {self.bot.user}")
        except Exception as e:
            colors.error(f"error -> {e}")
            logger.log(f"error -> {e}, @")
            
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if message.guild:
            return
        if message.author.id == self.bot.user.id:
            return
        try:
            snap = has_ignore(message.author.id, self.bot.user.id)
            if snap:
                return
            set_db(message.author.id, self.bot.user.id)

            # Mesaj varyasyon fonksiyonu
            def vary_msg(msg):
                extras = ["!", " :)", " 😅", " 😉", "🔥", ""]
                return msg + random.choice(extras)

            # İlk cevap
            async with message.channel.typing():
                await asyncio.sleep(random.randint(5, 15))
                msg = vary_msg(random.choice(dmsgs))
                await message.channel.send(msg)
                # ✅ DM MESAJI GÖNDERİLDİ BİLDİRİMİ
                colors.sucess(f"✅ DM GÖNDERİLDİ -> {msg} | Kullanıcı: {message.author} | Bot: {self.bot.user}")

            # İkinci cevap
            async with message.channel.typing():
                await asyncio.sleep(random.randint(12, 35))
                done_msg = vary_msg(random.choice(dnmsgs))
                await message.channel.send(done_msg)
                # ✅ DM MESAJI GÖNDERİLDİ BİLDİRİMİ
                colors.sucess(f"✅ DM GÖNDERİLDİ -> {done_msg} | Kullanıcı: {message.author} | Bot: {self.bot.user}")

            colors.sucess(f"✅ DM TAMAMLANDI -> {message.author} | Bot: {self.bot.user}")

        except Exception as e:
            colors.error(f"❌ DM HATASI -> {e}")
            logger.log(f"❌ DM HATASI -> {e}, @everyone")
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        id = member.guild.id
        if id != invg:
            return
        colors.sucess(f"✅ {member} sunucuya katıldı!")
        logger.log(f"✅ {member} sunucuya katıldı!")
        
    @commands.Cog.listener("on_connect")
    async def on_connect_two(self):
        await self.channel_task.start()
        
    @commands.Cog.listener()
    async def on_disconnect(self):
        colors.warning("🔌 Discord bağlantısı kesildi.")
        logger.log("🔌 Discord bağlantısı kesildi.")
        
    @commands.Cog.listener()
    async def on_ready(self):
        global DB_RESET
        colors.sucess(f"✅ Bağlantı başarılı -> {self.bot.user}!")
        logger.log(f"✅ Bağlantı başarılı -> {self.bot.user}!")
        
        # Start tasks
        try:
            if not self.activity_task.is_running():
                self.activity_task.start()
            colors.sucess(f"✅ Görevler başlatıldı -> {self.bot.user}")
        except Exception as e:
            colors.warning(f"⚠️ Görev başlatılamadı: {e}")
        
        if DB_RESET:
            return
        DB_RESET = True
        reset_db()

tokens = open("tokens.txt", "r").read().split("\n")

cleaned_tokens = []
for token in tokens:
    token = token.strip().strip('"').strip("'")
    if token and len(token) > 50:
        cleaned_tokens.append(token)

tokens = cleaned_tokens

app = Flask(__name__)

@app.route("/")
def index():
    return "J4J Bot, 24/7 Web Server"

def run_app():
    app.run(port=8080, host="0.0.0.0")

if wb_:
    threading.Thread(target=run_app).start()
    time.sleep(2)

bnr = pyfiglet.figlet_format("J4J BOT")
colors.banner(bnr+"\n")
colors.warning("© Developed By Alien")

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

async def run_bots():
    tasks = []
    for token in tokens:
        client = commands.Bot(
            command_prefix="^", 
            help_command=None, 
            self_bot=True
        )
        await client.add_cog(BotCog(client))
        task = asyncio.create_task(client.start(token, reconnect=True))
        tasks.append(task)
        await asyncio.sleep(1)
    
    await asyncio.gather(*tasks, return_exceptions=True)

try:
    loop.run_until_complete(run_bots())
except KeyboardInterrupt:
    colors.warning("⏹️ Bot kullanıcı tarafından durduruldu")
except Exception as e:
    colors.error(f"❌ Bot çalıştırma hatası: {e}")
finally:
    loop.close()
