import os
import subprocess
import aiohttp
import nextcord

print("Booting up with", nextcord.__version__)

from keep_alive import keep_alive
from emoji import emojize, demojize
from nextcord.ext import commands, tasks
from dotenv import load_dotenv
from utils.Storage_facility import Variables
from io import StringIO
from contextlib import redirect_stdout
from cogs.Embed import get_color
from utils.External_functions import (
    cembed,
    error_message, 
    check_command, 
    defa, 
    devop_mtext, 
    datetime, 
    wait_for_confirm, 
    safe_pfp, 
    get_async,  
    activities, 
    cog_creator, 
    get_youtube_url, 
    svg2png,
    cog_requirements
)
import traceback
import time
import psutil
import asyncio 
from io import BytesIO
import utils.assets as assets

location_of_file = os.getcwd()
start_time = time.time()
load_dotenv()
observer: list=[]
mspace: dict={}
deathrate: dict = {}
old_youtube_vid: dict = {}
youtube_cache: dict = {}
deleted_message: dict = {}
config: dict = {
    'snipe': [841026124174983188, 822445271019421746,830050310181486672, 912569937116147772],
    'respond': [],
    'youtube': {},
    'welcome': {},
    'ticket' : {},
    'security':{},
    'commands':{},
    'reactions':{},
    'connect':{},
    'slash': {},
    'roles': {}
    }
da: dict = {}
errors: list = ["```arm"]
da1: dict = {}
queue_song: dict = {}
dev_channel: int = int(os.getenv("dev"))
re: list = [0, "OK", {}, {}, -1, "", "205", {}, 5360, "48515587275%3A0AvceDiA27u1vT%3A26",{}]
youtube: list = []
autor: dict = {}
SESSIONID = None
color_message = None
wolfram: str = os.getenv("wolfram")
prefix_dict: dict = {}

# replace your id with this
dev_users: set = {"432801163126243328"}
ydl_op = {
    "format": "bestaudio/best",
    "postprocessors": [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "384",
        }
    ],
}
FFMPEG_OPTIONS = {
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
    "options": "-vn",
}

print("Starting")

async def search_vid(name):
    pass

def prefix_check(client_variable, message):
    return prefix_dict.get(message.guild.id if message.guild is not None else None, "'"),f"<@{client_variable.user.id}> "

intents = nextcord.Intents().default()
intents.members = True
intents.message_content = True

client = nextcord.ext.commands.Bot(
    command_prefix=prefix_check,
    intents=intents,
    case_insensitive=True
)

try:
    store = Variables("storage")
except:
    os.remove("storage.dat")
    store = Variables("storage")
    print("Failed to load")

def save_to_file():
    global dev_users
    print("save")
    store = Variables("storage")
    store.pass_all(
        da = client.da,
        mspace = client.mspace,
        da1 = client.da1,
        queue_song = client.queue_song,
        re = re,
        dev_users = dev_users,
        prefix_dict = prefix_dict,
        observer = observer,
        old_youtube_vid = old_youtube_vid,
        config = config,        
        autor = autor,
        time = str(datetime.now().time())
    )
    store.save()


def load_from_file(store):
    global da
    global da1
    global queue_song
    global re
    global dev_users
    global prefix_dict
    global observer
    global old_youtube_vid
    global config
    global mspace
    global autor

    v = store.show_data()    
    da = v.get("da",{})
    da1 = v.get("da1", {})
    queue_song = v.get("queue_song",{})
    re = v.get("re",re)
    dev_users = v.get("dev_users",dev_users)
    prefix_dict = v.get("prefix_dict",{})
    observer = v.get("observer",[])
    old_youtube_vid = v.get("old_youtube_vid",{})
    config = v.get("config",config)
    mspace = v.get("mspace",{})
    autor = v.get("autor",{})    

    #using these to pass to other files like cogs
    client.re = re
    client.dev_users = dev_users
    client.config = config
    client.prefix_dict = prefix_dict
    client.da = da
    client.da1 = da1
    client.queue_song = queue_song
    client.mspace = mspace
    client.observer = observer
    client.autor = autor
    
    


try:
    load_from_file(store)
except:
    print("Failed to load\n\n\n")
    
report = f"""Started at: <t:{int(start_time)}>
Current location: {location_of_file}
Requests: {re[0]:,}
Color: {nextcord.Color(re[8]).to_rgb()}
```yml
[ OK ] Loaded all modules
[ OK ] Variables initialised 
[ OK ] Load From File Completed
[ OK ] Switching Root ...
"""

@client.event
async def on_ready():
    print(client.user)    
    global report
    await client.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.watching, name="Booting in progress"))
    report+=f"[ OK ] Starting On Ready\n[ OK ] Bot named as {client.user.name}\n"
    channel = client.get_channel(dev_channel)
    if channel:
        report+="[ OK ] Devop found, let's go\n"
    try:
        print("Starting Load from file")
        load_from_file(store)
        print("Finished loading\n")
        print("\nStarting devop display")
        await devop_mtext(client, channel, re[8])
        report+="[ OK ] Sending Devop Message\n"
        print("Finished devop display")        
        
        with open("commands.txt","w") as f:
          for i in client.commands:
            f.write(i.name+"\n")
        report+="[ OK ] Updated commands txt file"
    except Exception as e:
        mess = await channel.send(
            embed=nextcord.Embed(
                title="Error in the function on_ready",
                description=str(e),
                color=nextcord.Color(value=re[8]),
            )
        )
        await mess.add_reaction("❌")
    dev_loop.start()
    print("Prepared")
    youtube_loop.start()
    send_file_loop.start()
    report+="```"
    await channel.send(
        embed=cembed(
            title="Report",
            description=report,
            color=re[8],
            thumbnail=client.user.avatar.url
        )
    )
    

@tasks.loop(hours=4)
async def send_file_loop():
    save_to_file()
    await client.get_channel(941601738815860756).send(file=nextcord.File("storage.dat",filename="storage.dat"))
    
@tasks.loop(minutes=30)
async def youtube_loop():
    await client.change_presence()
    print("Youtube_loop")    
    for i,l in config['youtube'].items():
        await asyncio.sleep(2)
        for j in l:
            try:
                a = await get_youtube_url(j[0])
                if a[0] in ["https://www.youtube.com/","https://www.youtube.com"]:
                    return
                if not old_youtube_vid.get(i, None):
                    old_youtube_vid[i] = {}
                if not old_youtube_vid[i].get(j[0], None):
                    old_youtube_vid[i][j[0]] = ""
                if old_youtube_vid[i][j[0]] == a[0]:
                    continue
                old_youtube_vid[i][j[0]] = a[0]
                try:
                    message=j[1]
                    send_channel = client.get_channel(i)
                    if not send_channel:
                        del config['youtube'][i]
                    await send_channel.send(
                        embed=cembed(
                            title="New Video out", 
                            description=f"New Video from {j[0]}",
                            url=a[0],
                            color=re[8],
                            thumbnail=send_channel.guild.icon.url
                        )
                    )
                    await send_channel.send(a[0]+"\n"+message)
                except Exception:
                    await client.get_channel(dev_channel).send(
                        embed=cembed(
                            title="Error in youtube_loop",
                            description=f"{str(traceback.format_exc())}\nSomething is wrong with channel no. {i}",
                            color=re[8]
                        )
                    )       
            except Exception as e: 
                if isinstance(e, aiohttp.client_exceptions.InvalidURL):
                    del config['youtube'][i]
                print(i)
                print(traceback.format_exc())
    print("Done")

@tasks.loop(seconds = 30)
async def dev_loop():
    save_to_file()
    try:
        a = await get_async("https://suicide-detector-api-1.yashvardhan13.repl.co/")
        if a != '{"message":"API is running"}':
            ch = client.get_channel(976470062691135529)
            await ch.send(
                embed=cembed(
                    title="Fix her",
                    description="Your server is offline Master Bruce, Go check it out ||plssssss||",
                    color=re[8],
                    footer="Why does this server fall sir?",
                    thumbnail=client.user.avatar.url
                )
            )
        await get_async("https://viennabot.declan1529.repl.co")
    except:
        await client.get_channel(dev_channel).send(
            embed=cembed(
                description=str(traceback.format_exc()),
                color=re[8],
                footer="Error in keep alive dev_loop",
                thumbnail=client.user.avatar.url
            )
        )
    await client.change_presence(activity=activities(client))

@client.command()
@commands.check(check_command)
async def svg(ctx, *, url):
    img = svg2png(url)
    await ctx.send(file=nextcord.File(BytesIO(img), "svg.png"))

@dev_loop.before_loop
@send_file_loop.before_loop
@youtube_loop.before_loop
async def wait_for_ready():
    await client.wait_until_ready()

@client.slash_command(name="emoji", description="Get Emojis from other servers")
async def emoji_slash(ctx, emoji_name, number=1):
    req()
    number=int(number) - 1
    if nextcord.utils.get(client.emojis, name=emoji_name) != None:
        emoji_list = [names.name for names in client.emojis if names.name == emoji_name]
        le = len(emoji_list)
        if le >= 2:
            if number > le - 1:
                number = le - 1
        emoji = [names for names in client.emojis if names.name == emoji_name][number].id
        await ctx.send(str(nextcord.utils.get(client.emojis, id=emoji)))
    else:
        await ctx.send(
            embed=nextcord.Embed(
                description="The emoji is not available",
                color=nextcord.Color(value=re[8]),
            )
        )


@client.command(aliases=["e", "emoji"])
@commands.check(check_command)
@commands.cooldown(1,5,commands.BucketType.guild)
async def uemoji(ctx, emoji_name, number=1):
    req()
    number-=1
    try:
        await ctx.message.delete()
    except:
        pass
    if emoji_name.startswith(":"):
        emoji_name = emoji_name[1:]
    if emoji_name.endswith(":"):
        emoji_name = emoji_name[:-1]
    if nextcord.utils.get(client.emojis, name=emoji_name) != None:
        emoji_list = [names.name for names in client.emojis if names.name == emoji_name]
        le = len(emoji_list)
        if le >= 2:
            if number > le - 1:
                number = le - 1
        user = getattr(ctx, 'author', getattr(ctx, 'user', None))
        emoji = [names for names in client.emojis if names.name == emoji_name][number]
        webhook = await ctx.channel.create_webhook(name=user.name)
        await webhook.send(emoji, username=user.name, avatar_url=safe_pfp(user))
        await webhook.delete()

    else:
        await ctx.send(
            embed=nextcord.Embed(
                description="The emoji is not available",
                color=nextcord.Color(value=re[8]),
            )
        )


@client.slash_command(name="svg2png", description="Convert SVG image to png format")
async def svg2png_slash(ctx, url):
    req()
    await ctx.response.defer()
    img = svg2png(url)
    await ctx.send(file=nextcord.File(BytesIO(img), "svg.png"))
    
@client.command(aliases=["cw"])
@commands.check(check_command)
async def clear_webhooks(ctx):
    webhooks = await ctx.channel.webhooks()
    print(webhooks)
    for webhook in webhooks:
        try:
            if webhook.user is client.user:
                await webhook.delete()            
        except Exception as e:
            print(e)
    await ctx.send(
        embed=cembed(
            title="Done",
            description="Deleted all the webhooks by alfred",
            color=re[8],
            thumbnail=client.user.avatar.url
        )
    )

@client.slash_command(name="color",description="Change color theme", guild_ids=[822445271019421746])
async def color_slash(
    inter, 
    rgb_color=str(nextcord.Color(re[8]).to_rgb())
):    
    rgb_color = get_color(rgb_color)
    if str(inter.user.id) not in dev_users:
        await inter.send(
            embed=cembed(
                title="Woopsies",
                description="This is a `developer-only` function",
                color=nextcord.Color.red(),
                thumbnail=client.user.avatar.url
            )
        )
        return

    re[8] = rgb_color.value
    if re[8]>16777215: re[8] = 16777215
    embed=cembed(
        title="Done",
        description=f"Color set as {nextcord.Color(re[8]).to_rgb()}\n`{re[8]}`",
        color=re[8],
        thumbnail = client.user.avatar.url,
        footer=f"Executed by {inter.user.name} in {inter.channel.name}"
    )
    await inter.send(embed=embed)
    await client.get_channel(dev_channel).send(embed=embed)

    
@client.command()
@commands.check(check_command)
async def load(ctx):
    print("Load", str(getattr(ctx, 'author', getattr(ctx, 'user', None))))
    req()
    try:
        cpu_per = str(int(psutil.cpu_percent()))
        cpu_freq = str(int(psutil.cpu_freq().current))
        ram = str(psutil.virtual_memory().percent)
        swap = str(psutil.swap_memory().percent)
        usage = f"""
        CPU Percentage: {cpu_per}%
        CPU Frequency : {cpu_freq}Mhz
        RAM usage: {ram}%
        Swap usage: {swap}%
        Nextcord: {nextcord.__version__}
        """
        embed = nextcord.Embed(
            title="Current load",
            description='\n'.join([i.strip() for i in usage.split('\n')]),
            color=nextcord.Color(value=re[8]),
        )
        embed.set_thumbnail(url=client.user.avatar.url)        
    except Exception as e:
        channel = client.get_channel(dev_channel)
        embed = nextcord.Embed(
            title="Load failed",
            description=str(e),
            color=nextcord.Color(value=re[8]),
        )
        embed.set_thumbnail(url=client.user.avatar.url)
        await channel.send(embed)
    await ctx.channel.send(embed=embed)



@client.slash_command(name="pr", description="Prints what you ask it to print")
async def pr_slash(inter, text: str):
    req()
    await inter.send(text)

@client.command()
@commands.check(check_command)
async def dev_op(ctx):
    if str(getattr(ctx, 'author', getattr(ctx, 'user', None)).id) in list(dev_users):
        print("devop", str(getattr(ctx, 'author', getattr(ctx, 'user', None))))
        channel = client.get_channel(dev_channel)
        await devop_mtext(client, channel, re[8])
    else:
        await ctx.send(embed=cembed(title="Permission Denied",description="You cannot use the devop function, only a developer can",color=re[8]))

@client.command()
@commands.check(check_command)
async def docs(ctx, name):
    try:
        if name.find("(") == -1:
            await ctx.send(
                embed=nextcord.Embed(
                    title="Docs",
                    description=str(eval(name + ".__doc__")),
                    color=nextcord.Color(value=re[8]),
                )
            )
        else:
            await ctx.send(
                embed=nextcord.Embed(
                    title="Permissions Denied",
                    description="Functions are not allowed. Try without the brackets to get the information",
                    color=nextcord.Color(value=re[8]),
                )
            )
    except Exception as e:
        await ctx.send(
            embed=nextcord.Embed(
                title="Error", description=str(e), color=nextcord.Color(value=re[8])
            )
        )

@client.event
async def on_member_join(member):
    if member.guild.id in config['security']:
        audit_log = await member.guild.audit_logs(limit=10).flatten()
        latest=audit_log[0]
        if member.bot:
            channel = client.get_channel(config['security'][member.guild.id])
            if channel:
                await channel.send(
                    embed=cembed(
                        title="Bot added",
                        description=f"{latest.target.mention} was added by {latest.user.mention}, please be careful while handling bots and try not to provide it with all the permissions as it can be dangerous",
                        color=re[8],
                        footer="Security alert by Alfred"
                    )
                )

@client.event
async def on_member_remove(member):
    if member.guild.id in config['security']:
        print(member.guild)
        a = member.guild
        audit_log = await a.audit_logs(limit=10).flatten()
        latest = audit_log[0]
        if latest.target == member:
            channel = client.get_channel(config['security'][member.guild.id])
            if latest.action == nextcord.AuditLogAction.ban:
                await channel.send(
                    embed=cembed(
                        title=f"Banned",
                        description=f"{latest.user.mention} banned {latest.target.name}",
                        color=re[8],
                        footer="Security alert by Alfred",
                        thumbnail=member.guild.icon.url
                    )
                )
            elif latest.action == nextcord.AuditLogAction.kick:
                await channel.send(
                    embed=cembed(
                        title=f"Kicked",
                        description=f"{latest.user.mention} kicked {latest.target.name}",
                        color=re[8],
                        footer="Security alert by Alfred",
                        thumbnail=member.guild.icon.url
                    )
                )

@client.command()
async def feedback(ctx, *, text):
    embed = cembed(
        title=f"Message from {getattr(ctx, 'author', getattr(ctx, 'user', None)).name}: {ctx.guild.name}",
        description=text,
        color=re[8],
        thumbnail=client.user.avatar.url
    )
    await ctx.send(embed=embed)
    confirmation = await wait_for_confirm(ctx,client,"Do you want to send this to the developers?",color=re[8])
    if not confirmation:
        return
    auth = getattr(ctx, 'author', getattr(ctx, 'user', None)).id
    await client.get_channel(932890298013614110).send(
        content=str(ctx.channel.id)+" "+str(auth),
        embed=embed
        
    )
    await ctx.send(
        embed=cembed(
            title="Done",
            description="I've given this info to the developers, they will try fixing it asap :smiley:",
            color=re[8]
        )
    )

@client.command()
async def rollback(ctx):
    if str(ctx.author.id) not in dev_users or ctx.channel.id != 941601738815860756:
        return
    if not ctx.message.reference:
        await ctx.send("Not replied to a message")
        return
    m = await ctx.channel.fetch_message(ctx.message.reference.message_id)
    if m.attachments == []:
        await ctx.send("No file found")
        return
    attachment = m.attachments[0].url
    if not attachment.endswith("storage.dat"):
        await ctx.send("Not a storage file")
        return
    os.remove("storage.dat")
    await get_async(attachment, kind="file>storage.dat")
    store=Variables("storage")
    load_from_file(store)
    save_to_file()
    await m.reply("Reverted to this")
    

@client.slash_command(name = "feedback",description="Send a feedback to the developers")
async def f_slash(inter, text):
    await feedback(inter, text=text)

@client.slash_command(name="eval", description = "This is only for developers", guild_ids = [822445271019421746])
async def eval_slash(inter, text, ty = defa(choices=['python','bash'])):
    if ty == 'bash':
        await shell(inter, text = text)
    else:
        await python_shell(inter, text = text)

@client.command(aliases=["!"])
async def restart_program(ctx):
    if str(getattr(ctx, 'author', getattr(ctx, 'user', None)).id) in list(dev_users):
        save_to_file()        
        try:
            if len(client.voice_clients)>0:
                confirmation = await wait_for_confirm(
                    ctx, client, f"There are {len(client.voice_clients)} servers listening to music through Alfred, Do you wanna exit?", color=re[8]                        
                )
                if not confirmation:
                    return
        except:
            print("Restarting without confirmation")
        try:
            for voice in client.voice_clients:
                voice.stop()
                await voice.disconnect()
        except:
            pass
        await client.change_presence(activity = nextcord.Activity(type = nextcord.ActivityType.listening, name= "Restart"))        
        print("Restart")
        try:
            await ctx.channel.send(
                embed=cembed(
                    title="Restarted",
                    description="The program is beginning it's restarting process",
                    color=re[8],
                    thumbnail=client.user.avatar.url
                )
            )
            await client.get_channel(dev_channel).send(
                embed=cembed(
                    title="Restart",
                    description=f"Requested by {getattr(ctx, 'author', getattr(ctx, 'user', None)).name}",
                    thumbnail=client.user.avatar.url,
                    color=re[8]
                    
                )
            )
        except:
            print("Restarting without sending messages")
        os.system("busybox reboot")
    else:
        await ctx.channel.send(embed=cembed(title="Permission Denied",description="Only developers can access this function",color=re[8],thumbnail=client.user.avatar.url))
        await client.get_channel(dev_channel).send(embed=cembed(description=f"{getattr(ctx, 'author', getattr(ctx, 'user', None)).name} from {ctx.guild.name} tried to use restart_program command",color=re[8]))
@client.event
async def on_message_edit(message_before, message_after):
    await client.process_commands(message_after)
      
@client.event
async def on_reaction_add(reaction, user):
    req()
    ctx = reaction.message
    try:
        if (not user.bot) and str(user.id) in list(dev_users):
            global dev_channel
            channel = client.get_channel(dev_channel)
            if (
                reaction.emoji == emojize(":laptop:")
                and str(reaction.message.channel.id) == str(channel.id)
                and reaction.message.author == client.user
            ):
                st = "\n".join([str(getattr(client.get_user(i), 'name', None)) for i in dev_users])
                await reaction.remove(user)
                await channel.send(
                    embed=cembed(
                        title="Developers",
                        description=st,
                        author=user,
                        footer="Thank you for supporting",
                        color=nextcord.Color(value=re[8]),
                    )
                )
            if reaction.emoji == emojize(":bar_chart:") and str(
                reaction.message.channel.id
            ) == str(channel.id):
                await reaction.remove(user)
                reaction.message.author == user
                await load(reaction.message)              
            if reaction.emoji == "⭕" and ctx.channel.id == channel.id:
                await reaction.remove(user)
                await channel.send(
                    embed=nextcord.Embed(
                        title="Servers",
                        description='\n'.join([i.name+"" for i in client.guilds]),
                        color=nextcord.Color(value=re[8]),
                    )
                )
            if reaction.emoji == emojize(":fire:") and str(
                reaction.message.channel.id
            ) == str(channel.id):
                reaction.message.author = user
                await restart_program(reaction.message,re[1])
            if reaction.emoji == '💾' and reaction.message.channel.id == channel.id:
                save_to_file()                    
                await reaction.remove(user)
            if reaction.emoji == emojize(":cross_mark:") and str(
                reaction.message.channel.id
            ) == str(channel.id):
                await reaction.remove(user)
                if len(client.voice_clients)>0:
                    confirmation = await wait_for_confirm(
                        reaction.message, client, f"There are {len(client.voice_clients)} servers listening to music through Alfred, Do you wanna exit?", color=re[8], usr=user                        
                    )
                    if not confirmation:
                        return
                try:
                    for voice in client.voice_clients:
                        voice.stop()
                        await voice.disconnect()
                except:
                    pass
                await channel.purge(limit=10000000000)
                await channel.send(
                    embed=nextcord.Embed(
                        title="Exit",
                        description=("Requested by " + str(user)),
                        color=nextcord.Color(value=re[8]),
                    )
                )
                os.system("pkill python3")
            
            if reaction.emoji == emojize(":black_circle:") and str(
                reaction.message.channel.id
            ) == str(channel.id):
                await devop_mtext(client, channel, re[8])
    except PermissionError:
        await reaction.message.channel.send(embed=cembed(
            title="Missing Permissions",
            description="Alfred is missing permissions, please try to fix this, best recommended is to add Admin to the bot",
            color=re[8],
            thumbnail=client.user.avatar.url)
        )
    except Exception as e:        
        channel = client.get_channel(dev_channel)
        await channel.send(
            embed=cembed(
                title="Error in on_reaction_add",
                description=f"{traceback.format_exc()}",
                footer=f"{reaction.message.guild.name}:{reaction.message.channel.name}",
                color=nextcord.Color(value=re[8]),
            )
        )

@client.event
async def on_command_error(ctx, error):    
    print(type(error))
    if isinstance(error, commands.errors.CommandNotFound):
        return
    if isinstance(error, commands.errors.CommandInvokeError):
        if isinstance(getattr(error, 'original', None), nextcord.errors.HTTPException):
            os.system("busybox reboot")
    elif isinstance(error, commands.errors.CheckFailure):
        await ctx.send(
            embed=cembed(
                title="Disabled command",
                description="This command has been disabled by your admin, please ask them to enable it to use this\n\nIf you're an admin and you want to enable this command, use `/commands <enable> <command_name>`",
                color=client.re[8],
                thumbnail=safe_pfp(ctx.author)
            )
        )       
    elif isinstance(error, commands.errors.MissingRequiredArgument):
        prefix = prefix_dict.get(ctx.guild.id, "'")
        await ctx.send(
            embed=cembed(
                title="Missing Required Argument",
                author=ctx.author,
                color=nextcord.Color.red(),
                thumbnail=client.user.avatar.url,
                description="You have missed out one or more of the required argument",
                fields=[
                    {
                        'name': 'Correct usage',
                        'value':f'`{prefix}{ctx.command.name} {ctx.command.signature}`'
                    }
                ],
                footer={
                    'text': 'Go through /help',
                    'icon_url': client.user.avatar.url
                }
            )
        )   
    else:
        await ctx.send(embed=error_message(str(error)))
    channel = client.get_channel(dev_channel)
    await channel.send(embed=cembed(title="Error",description=f"\n{str(error)}", color=re[8], thumbnail=client.user.avatar.url, footer = f"{getattr(ctx, 'author', getattr(ctx, 'user', None)).name}:{ctx.guild.name}"))

@client.event
async def on_message(msg):
    await client.process_commands(msg)             
    try:
        if msg.channel.id in autor:
            for emo in autor[msg.channel.id]:                
                await msg.add_reaction(emojize(emo.strip()))  
                await asyncio.sleep(1)       
        
    except Exception as e:
        channel = client.get_channel(dev_channel)
        await channel.send(
            embed=nextcord.Embed(
                title="Error", description=str(traceback.format_exc()), color=nextcord.Color(value=re[8])
            )
        )



@client.command(aliases=["m"])
async def python_shell(ctx, *, text):
    req()
    user = getattr(ctx, 'author', getattr(ctx, 'user', None))
    print("Python Shell", text, user)
    global dev_users
    if str(user.id) in dev_users:
        try:
            text = text.replace("```py", "").replace("```", "")
            await client.get_channel(946381704958988348).send(
                embed=cembed(
                    title="Python Eval Executed",
                    description = f"```py\n{text}\n```",
                    color=re[8],
                    author=user,
                    url=getattr(ctx.message, 'jump_url', None)
                )
            )
            a = eval(text)
            print(text)
            em = cembed(
                title=text,
                description=str(a),
                color=nextcord.Color(value=re[8]),
                thumbnail="https://engineering.fb.com/wp-content/uploads/2016/05/2000px-Python-logo-notext.svg_.png"
            )
            await ctx.send(embed=em)
        except Exception as e:
            await ctx.send(
                embed=nextcord.Embed(
                    title="Error_message",
                    description=str(e),
                    color=nextcord.Color(value=re[8]),
                )
            )
        
    else:
        try:
            await ctx.message.delete()
        except:
            pass
        await ctx.send(
            embed=nextcord.Embed(
                description="Permissions Denied",
                color=nextcord.Color(value=re[8]),
            )
        )

@client.command(aliases=['sh'])
async def shell(ctx, *, text):
    if isinstance(ctx, nextcord.Interaction):
        await ctx.response.defer()
    user = getattr(ctx, 'author', getattr(ctx, 'user', None))
    if not str(user.id) in dev_users:
        await ctx.send(
            embed=cembed(
                title="Permissions Denied",
                description="This is an `only developer command`, please refrain from using this",
                color=re[8],
                thumbnail=client.user.avatar.url
            )
        )
        return
    print("Shell", user.name, text)
    await client.get_channel(946381704958988348).send(
        embed=cembed(
            author=user,
            title=f"Shell Executed by {user}",
            description=text,
            color=re[8],
            thumbnail=client.user.avatar.url,
            footer=f"This happened in {ctx.guild}",
            url=getattr(ctx.message, 'jump_url', None)
        )
    )
    await ctx.send(
        embed=cembed(
            title="Shell Execution",
            description="```bash\n"+subprocess.getoutput(text)[:4000]+"\n```",
            color=re[8],
            author=user,
            thumbnail=client.user.avatar.url,
            footer={
                'text': 'A copy of the query is send to Wayne Enterprises for security reasons',
                'icon_url': safe_pfp(client.get_guild(822445271019421746))
            }
            
        )
    )

@client.command()
@commands.check(check_command)
async def exe(ctx, *, text):
    req()
    if (
        str(getattr(ctx, 'author', getattr(ctx, 'user', None)).id) in dev_users
    ):
        if ctx.guild.id!=822445271019421746:
            await ctx.send(
                embed=cembed(
                    title="Permissions Denied",
                    description = "You can only use this command in Wayne Enterprises",
                    color=re[8]                    
                )
            )
            return
        await client.get_channel(946381704958988348).send(
            embed=cembed(
                title="Execute command used",
                description=text,
                color=re[8],
                author = ctx.author,
                url = getattr(ctx.message, 'jump_url', None)         
            )
        )
        text = text.replace("```py", "```")
        text = text[3:-3].strip()
        f = StringIO()
        with redirect_stdout(f):
            try:
                exec(text)
            except Exception as e:
                traceback.print_tb(e.__traceback__)
                error_mssg = "Following Error Occured:\n\n"+traceback.format_exc()
                await ctx.send(embed = error_message(error_mssg))
        output = f.getvalue()
        embeds = []
        if output == "":
            output = "_"
        all_outputs = ['']
        for ch in output:
            all_outputs[-1]+=ch
            if len(all_outputs[-1]) == 2000:
                all_outputs.append('')
        embeds = []
        for description in all_outputs:
            embeds.append(
                cembed(
                    title="Output",
                    description=description,
                    color=re[8],
                    thumbnail=client.user.avatar.url
                )
            )            
        await assets.pa(ctx, embeds, start_from=0, restricted=False)
    else:
        await ctx.send(
            embed=nextcord.Embed(
                title="Denied",
                description="Ask Devs to give access for scripts",
                color=nextcord.Color(value=re[8]),
            )
        )

def addt(p1, p2):
    da[p1] = p2
    return "Done"


def get_elem(k):
    return da.get(k, "Not assigned yet")

def de(k):
    del da[k]
    return "Done"


def req():
    re[0] = re[0] + 1


def g_req():
    return re[0]

def reload_extension(name):
    client.unload_extension(f'cogs.{name}')
    return load_extension(name)

def load_extension(name):
    '''
    This will safely add cog for alfred with all the requirements
    '''
    try:     
        print("Loading", name, end="")   
        l = cog_requirements(name)
        d = {}
        for i in l:
            d[i] = globals()[i]
        client.load_extension(f'cogs.{name}', extras=d)
        print(" :Done")
        return f"[ OK ] Added {name}\n"
    except:
        return f"Error in cog {name}:\n"+traceback.format_exc()+"\n"

def load_all():
    for i in os.listdir(os.getcwd()+"/cogs"):
        if i.endswith(".py"):
            global report
            report+=load_extension(i[:-3])
client.remove_command("help")
load_all()
keep_alive()

try: 
    client.run(os.getenv("token"))
except: 
    print(traceback.format_exc())
    time.sleep(20)
    os.system("busybox reboot")
