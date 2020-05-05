import discord
import asyncio
from discord.ext import tasks
from bs4 import BeautifulSoup
import urllib.request
import traceback
import pyautogui



client = discord.Client()
global messages
messages = [f"깃도움", f"{len(client.users)}명의 사람들과 함께", f"{len(client.guilds)}개의 길드와 함께", "깃허브 공부"]



@tasks.loop(seconds=7)  #상매 백그라운드 루프 함수 만들기
async def active(messages):
    await client.change_presence(activity=discord.Game(messages[0]))  #message리스트중 첫번째를 상매로 띄운다
    messages.append(messages[0])  #리스트 맨 뒤에 맨 앞에있는걸 추가한다
    del messages[0]  #맨 앞에있는걸 지운다

@client.event
async def on_ready():
    print('Bot Online')
    print(client.user.name)
    print(client.user.id)
    messages = [f"깃도움", f"{len(client.users)}명의 사람들과 함께", f"{len(client.guilds)}개의 길드와 함께", "깃허브 공부"]
    active.start(messages)

@client.event
async def on_message(message):
    if message.author.bot:
        return None
    if message.content.startswith("RL"):
        go = message.content.split(" ")
        pyautogui.moveRel(int(go[1]), 0, 2)
        await message.channel.send(f"x좌표{go[1]}만큼 갔습니다")

    if message.content.startswith("SH"):
        pyautogui.screenshot("SH.png")
        file = discord.File("SH.png")
        await message.channel.send(file=file)

    if message.content.startswith("UD"):
        go = message.content.split(" ")
        pyautogui.moveRel(0, int(go[1]), 2)
        await message.channel.send(f"y좌표{go[1]}만큼 갔습니다")

    if message.content.startswith("OC"):
        pyautogui.click()
        await message.channel.send("클릭했습니다")

    if message.content.startswith("DC"):
        pyautogui.doubleClick()
        await message.channel.send("더블클릭 했습니다")
    
    if message.content.startswith("CK"):
        try:
            go = message.content.split(" ")
            pyautogui.typewrite([f"{go[1:]}"])
            await message.channel.send(f"{go[1:]}를 눌렀습니다")
        except:
            await message.channel.send("키는 하나만 입력해 주세요")

    if message.content.startswith("WT"):
        key = message.content[3:]
        pyautogui.typewrite(f"{key}")
        await message.channel.send(f"{key}라고 입력하였습니다")

    if message.content.startswith("깃"):
        try:
            if message.content.startswith("깃초대"):
                embed = discord.Embed(title="깃허브봇   ", description="📫[깃허브봇 초대링크](https://discordapp.com/api/oauth2/authorize?client_id=706494061976092693&permissions=1543535712&scope=bot)📫\n🎮[깃허브봇 포털](https://discord.gg/QgGPby)🎮")
                await message.channel.send(embed=embed)

            if message.content.startswith("깃도움"):
                embed = discord.Embed(title="깃허브 봇 명령어", description="``깃허브 명령어``\n---------------------\n``깃사이트``\n깃허브 사이트를 알려줍니다\n\n``깃검색 <깃허브 검색어>``\n깃허브에서 검색어를 검색하여 알려줍니다\n\n``깃마켓``\n준비중.....\n\n``봇 명령어``\n---------------------\n``깃초대``\n깃허브 봇 초대링크입니다\n\n``깃도움``\n깃허브 봇 명령어입니다")
                await message.channel.send(embed=embed)

            if message.content.startswith("깃소개"):
                embed = discord.Embed(title="깃허브 봇 소개", description="github serching bot은 github에 검색할수 있게 도와주는 봇입니다\n여기서 깃허브란 일종의 프로그래머들의 sns같은것 입니다 깃허브에서는 여러 사람들과 코드를 공유하며 수정할 내용 또는 같이 봇을 만들수 있습니다 또는 헤로쿠를 이용하여 봇을 24시간 무료로 돌릴수 있습니다\n자세한 내용은:[깃허브 위키백과](https://ko.wikipedia.org/wiki/깃허브)")
                await message.channel.send(embed=embed)

            if message.content.startswith("깃사이트"):
                embed = discord.Embed(title="깃허브 사이트", description="[깃허브](https://github.com/)")
                await message.channel.send(emned=embed)

            if message.content.startswith("깃마켓"):
                url = "https://github.com/marketplace"
                html = urllib.request.urlopen(url).read()
                soup = BeautifulSoup(html, "html.parser")   

                shop = soup.find(class_="d-md-flex flex-wrap mb-4")
                print(shop)
                embed = discord.Embed(title="깃허브 상점", description="[바로가기](https://github.com/marketplace)")

                for i in shop:
                    url = i.find("a")[0]["href"]
                    print(url)
                    url = f"https://github.com{url}"
                    print(url)
                    name = i.find("h3").text
                    print(name)
                    subtitle = i.find("p").text
                    print(subtitle)
                    embed.add_field(name=f"{name}\n{url}", value=f"{subtitle}\n", inline=False)
                await message.channel.send(embed=embed)
            






            if message.content.startswith("깃검색"):
                count = message.content.split(" ")
                print(int(len(count)))
                if int(len(count)) >= 2:
                    rsearch = message.content[4:].replace(" ", '+')
                else:
                    rsearch = count[1]

                
                url = "https://github.com/search?q=" + urllib.parse.quote_plus(rsearch)
                html = urllib.request.urlopen(url).read()
                

                soup = BeautifulSoup(html, "html.parser")

                embed = discord.Embed(title=f"{message.content[4:]}의 검색 결과", description=f"[검색]({url})    ", colour=discord.Colour.dark_grey())
                
                first = soup.find_all(class_="repo-list-item hx_hit-repo d-flex flex-justify-start py-4 public source")

                for i in first:
                    title = i.find(class_="f4 text-normal").find("a")["href"]
                    subtitle = i.find(class_="f4 text-normal").find("a")["href"]
                    code = i.find(class_="mt-n1").find("span").text
                    des = i.find(class_="mt-n1").find("p").text
                    
                    giturl = f"https://github.com{title}"
                    if "Python" in code:
                        code = "파이썬"
                    elif "Javascript" in code:
                        code = "자바스크립트"
                    elif "Java" in code:
                        code = "자바"
                    elif "C#" in code:
                        code = "C#"
                    elif "PHP" in code:
                        code = "php"
                    elif "TypeScript" in code:
                        code = "TypeScript"
                    elif "C++" in code:
                        code = "C++"
                    elif "Go" in code:
                        code = "go"
                    elif "HTML" in code:
                        code = "HTML"
                    elif "Objective-C" in code:
                        code = "Objective-C"
                    elif "Common Lisp" in code:
                        code = "Common Lisp"
                    elif "Clojure" in code:
                        code = "Clojure" 
                    elif "Ruby" in code:
                        code = "Ruby"
                    elif "Haskell" in code:
                        code = "Haskell"
                    elif "Rascal" in code:
                        code = "Rascal"
                    elif "Jupyter Notebook" in code:
                        code = "Jupyter Notebook"
                    elif "Starlark" in code:
                        code = "Starlark"
                    elif "R" in code:
                        code = "R"
                    else:
                        code = "잘 모르겠음"
                    
                    embed.add_field(name=f"{giturl}", value=f"{des}``{code}``", inline=False)
                
                await message.channel.send(embed=embed)


                    
            if message.content.startswith("깃봇도움"):
                count = message.content.split(" ")
                print(int(len(count)))
                if int(len(count)) >= 2:
                    rsearch = message.content[5:].replace(" ", '+')
                else:
                    rsearch = count[1]

                
                url = "https://discordpy.readthedocs.io/en/latest/search.html?q=" + urllib.parse.quote_plus(rsearch)
                print(url)
                html = urllib.request.urlopen(url).read()
                

                soup = BeautifulSoup(html, "html.parser")

                embed = discord.Embed(title=f"{message.content[4:]}의 도큐검색 결과", description=f"[검색]({url})    ", colour=discord.Colour.dark_grey())
                
                first = soup.find_all("li")

                for i in first:
                    boturl = i.find("a")["href"]
                    title = i.find("a").text
                    des = i.find("span").text
                    embed.add_field(name=f"{title}\n{des}", value=f"{boturl}\n", inline=False)
                
                await message.channel.send(embed=embed)


            
        except:
            embed = discord.Embed(title="Error", description=f"```{traceback.format_exc()}```", colour=discord.Colour.red())
            await message.channel.send(embed=embed)
            print(traceback.format_exc())





client.run(os.environ['token'])
