import datetime
import discord
import sqlite3
import asyncio
from discord.ext import commands
from datetime import datetime
from pytz import timezone

import requests
import json

url1 = 'https://solved.ac/api/v3/coins/exchange_rate'
header1 = {'Content-Type' : 'application/json'}

response = requests.get(url1,headers=header1)
data_json = json.loads(response.content)
coinp = int(data_json['rate'])
coin2p = coinp

intents = discord.Intents.all()
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

con = sqlite3.connect("userdata.db", isolation_level = None)
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS User_Info(id INTEGER PRIMARY KEY, coinA INTEGER, coinB INTEGER, money INTEGER)")

arr = []
brr = []
ttt = []
cntk = 0
moneyhave = 10000000
coint = 0
coint2 = 0
coinhave = 0
flag = True

token = ''

def checkuser(id):
    alr_exist = []
    con = sqlite3.connect(r'userdata.db', isolation_level = None)
    cur = con.cursor()
    cur.execute("SELECT id FROM User_Info WHERE id = ?", (id,))
    rows = cur.fetchall()
    for i in rows:
        alr_exist.append(i[0])

    if id not in alr_exist:
        return 0
    elif id in alr_exist:
        return 1
    con.close()


@bot.event
async def on_message(msg):
    if(msg.author.bot): return None
    await bot.process_commands(msg)

@bot.event
async def on_ready():
    global arr, cntk, ttt, prevvi
    global coinp, coin2p
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('Solved Coin! (by haru_101)'))
    print('[DEBUG]=================\nbot status : on\n=================')
    while(True):
        response = requests.get(url1, headers=header1)
        data_json = json.loads(response.content)
        coinp = int(data_json['rate'])
        if(len(arr)==0):
            arr.append(coinp)
        else:
            if(arr[0]!=coinp):
                coin2p += (coinp - arr[0])*2
                coin2p = max(0, coin2p)
                arr[0]=coinp
            else:
                pass
        await asyncio.sleep(300)


@bot.command()
async def 가입신청(ctx):
    id = ctx.author.id
    con = sqlite3.connect(r'userdata.db', isolation_level=None)
    cur = con.cursor()
    chk = checkuser(id)
    if(chk==0):
        cur.execute("INSERT INTO User_Info VALUES(?, ?, ?, ?)", (id, 0, 0, 10000000))
        await ctx.channel.send(f'{ctx.message.author.mention} 가입완료')
    elif(chk==1):
        await ctx.channel.send(f'{ctx.message.author.mention} 이미 가입되어 있습니다.')
    con.close()

@bot.command()
async def 탈퇴(ctx):
    id = ctx.author.id
    con = sqlite3.connect(r'userdata.db', isolation_level=None)
    cur = con.cursor()
    chk = checkuser(id)
    if(chk==0):
        pass
    elif(chk==1):
        cur.execute("DELETE FROM User_Info WHERE id = ?", (id,))
    con.close()

@bot.command()
async def 지갑(ctx):
    global coint, coint2, coinp, coin2p
    await ctx.channel.send(f'{ctx.message.author.mention}')
    tid = ctx.author.id
    con = sqlite3.connect(r'userdata.db', isolation_level=None)
    cur = con.cursor()
    chk = checkuser(tid)
    if (chk == 0):
        embed = discord.Embed(title='솔브닥 코인 가상 거래소',
                              description=f'{ctx.message.author.mention}님의 지갑현황을 조회할 수 없습니다.',
                              colour=0xFA5858)
        embed.add_field(name='> 실패사유', value='DB에 정보가 없습니다.\n!가입신청 을 입력해주세요.')
        await ctx.channel.send(embed=embed)
    elif (chk == 1):
        cur.execute("SELECT money FROM User_Info WHERE id = ?", (tid, ))
        k1 = int(cur.fetchone()[0])
        cur.execute("SELECT coinA FROM User_Info WHERE id = ?", (tid, ))
        k2 = int(cur.fetchone()[0])
        cur.execute("SELECT coinB FROM User_Info WHERE id = ?", (tid,))
        k3 = int(cur.fetchone()[0])
        embed = discord.Embed(title='솔브닥 코인 가상 거래소',
                              description=f'{ctx.message.author.mention}님의 지갑현황입니다.',
                              colour=0xD0F5A9)
        embed.add_field(name='> 지갑현황', value='솔브닥 코인 : {}개\n솔브닥 코인 2x 레버리지 : {}개\n잔고 : {}원\n추정자산 : {}원'.format(format(k2, ","), format(k3, ","), format(k1, ","), format(k2*coinp + k3*coin2p + k1, ",")))
        await ctx.channel.send(embed=embed)
    con.close()

@bot.command()
async def 코인시세(ctx):
    global coint, coint2
    now = datetime.now(timezone('Asia/Seoul'))
    await ctx.channel.send(f'{ctx.message.author.mention}')
    embed = discord.Embed(title='솔브닥 코인 가상 거래소',
                          description='현재 솔브닥 코인 시세를 알려드립니다.',
                          colour=0xD0F5A9)
    embed.add_field(name='> 현재가', value='일반가 : {}원\n레버리지 : {}원'.format(format(coinp,","), format(coin2p,",")))
    embed.add_field(name='> 거래량', value='매수량 : {}개\n매도량 : {}개'.format(format(coint, ","), format(coint2, ",")))
    embed.set_footer(text='기준일시 : {}시 {}분 {}초'.format(now.hour, now.minute, now.second))
    await ctx.channel.send(embed=embed)

@bot.command()
async def admin_change_price(ctx, *input):
    global coint, coint2, coinp, coin2p, arr
    password = int(input[0])
    if(password==??????????):
        arr[0] = int(input[1])
        coinp = arr[0]
        coin2p = int(input[2])
        coint = 0
        coint2 = 0

@bot.command()
async def 코인매수(ctx, *input):
    global coint, coint2, coinp, coin2p
    print(input[0])
    now = datetime.now()
    await ctx.channel.send(f'{ctx.message.author.mention}')
    try:
        tid = ctx.author.id
        con = sqlite3.connect(r'userdata.db', isolation_level=None)
        cur = con.cursor()
        chk = checkuser(tid)
        if (chk == 0):
            embed = discord.Embed(title='솔브닥 코인 가상 거래소',
                                  description=f'{ctx.message.author.mention}님의 거래결과를 알려드립니다.',
                                  colour=0xFA5858)
            embed.add_field(name='> 거래여부', value='실패')
            embed.add_field(name='> 실패사유', value='DB에 정보가 없습니다.\n!가입신청 을 입력해주세요.')
            embed.set_footer(text='거래일시 : {}시 {}분 {}초'.format(now.hour, now.minute, now.second))
            await ctx.channel.send(embed=embed)
        elif (chk == 1):
            cur.execute("SELECT money FROM User_Info WHERE id = ?", (tid, ))
            k = int(cur.fetchone()[0])
            r = int(input[0])
            if(r<=0):
                embed = discord.Embed(title='솔브닥 코인 가상 거래소',
                                      description=f'{ctx.message.author.mention}님의 거래결과를 알려드립니다.',
                                      colour=0xFA5858)
                embed.add_field(name='> 거래여부', value='실패')
                embed.add_field(name='> 실패사유', value='입력에 불필요한 입력이 있습니다.\n숫자 또는 1 이상의 숫자만 입력해주세요.')
                embed.set_footer(text='거래일시 : {}시 {}분 {}초'.format(now.hour, now.minute, now.second))
                await ctx.channel.send(embed=embed)
            elif(k-coinp*r<0):
                embed = discord.Embed(title='솔브닥 코인 가상 거래소',
                                      description=f'{ctx.message.author.mention}님의 거래결과를 알려드립니다.',
                                      colour=0xFA5858)
                embed.add_field(name='> 거래여부', value='실패')
                embed.add_field(name='> 실패사유', value='잔고가 부족합니다.')
                embed.set_footer(text='거래일시 : {}시 {}분 {}초'.format(now.hour, now.minute, now.second))
                await ctx.channel.send(embed=embed)
            else:
                kk = -1*r*coinp
                con.close()
                con = sqlite3.connect(r'userdata.db', isolation_level=None)
                cur = con.cursor()
                cur.execute("UPDATE User_info SET money = money + ? WHERE id = ?", (int(kk),tid,))
                cur.execute("UPDATE User_info SET coinA = coinA + ? WHERE id = ?", (int(r),tid,))
                cur.execute("SELECT money FROM User_Info WHERE id = ?", (tid, ))
                m1 = int(cur.fetchone()[0])
                cur.execute("SELECT coinA FROM User_Info WHERE id = ?", (tid, ))
                c1 = int(cur.fetchone()[0])
                cur.execute("SELECT coinB FROM User_Info WHERE id = ?", (tid,))
                c2 = int(cur.fetchone()[0])
                print(1111)
                embed = discord.Embed(title='솔브닥 코인 가상 거래소',
                                      description=f'{ctx.message.author.mention}님의 거래결과를 알려드립니다.',
                                      colour=0xD0F5A9)
                embed.add_field(name='> 거래여부', value='성공')
                embed.add_field(name='> 현재가', value='{}원'.format(format(coinp, ",")))
                embed.add_field(name='> 거래개수', value='{}개'.format(format(int(input[0]), ",")))
                embed.add_field(name='> 지갑현황', value='솔브닥 코인 : {}개\n솔브닥 코인 2x 레버리지 : {}개\n잔고 : {}원'.format(format(c1, ","), format(c2, ","), format(m1, ",")))
                embed.set_footer(text='거래일시 : {}시 {}분 {}초'.format(now.hour, now.minute, now.second))
                await ctx.channel.send(embed=embed)
                coint += r
    except:
        embed = discord.Embed(title='솔브닥 코인 가상 거래소',
                              description=f'{ctx.message.author.mention}님의 거래결과를 알려드립니다.',
                              colour=0xFA5858)
        embed.add_field(name='> 거래여부', value='실패')
        embed.add_field(name='> 실패사유', value='입력에 불필요한 입력이 있습니다.\n!코인매수 [개수(숫자)] 형식으로 입력해주세요.')
        embed.set_footer(text='거래일시 : {}시 {}분 {}초'.format(now.hour, now.minute, now.second))
        await ctx.channel.send(embed=embed)
    con.close()

@bot.command()
async def 코인매도(ctx, *input):
    global coint, coint2, coinp, coin2p
    now = datetime.now(timezone('Asia/Seoul'))
    await ctx.channel.send(f'{ctx.message.author.mention}')
    try:
        tid = ctx.author.id
        con = sqlite3.connect(r'userdata.db', isolation_level=None)
        cur = con.cursor()
        chk = checkuser(tid)
        if (chk == 0):
            embed = discord.Embed(title='솔브닥 코인 가상 거래소',
                                  description=f'{ctx.message.author.mention}님의 거래결과를 알려드립니다.',
                                  colour=0xFA5858)
            embed.add_field(name='> 거래여부', value='실패')
            embed.add_field(name='> 실패사유', value='DB에 정보가 없습니다.\n!가입신청 을 입력해주세요.')
            embed.set_footer(text='거래일시 : {}시 {}분 {}초'.format(now.hour, now.minute, now.second))
            await ctx.channel.send(embed=embed)
        elif (chk == 1):
            cur.execute("SELECT coinA FROM User_Info WHERE id = ?", (tid, ))
            k = int(cur.fetchone()[0])
            r = int(input[0])
            if(r==0):
                embed = discord.Embed(title='솔브닥 코인 가상 거래소',
                                      description=f'{ctx.message.author.mention}님의 거래결과를 알려드립니다.',
                                      colour=0xFA5858)
                embed.add_field(name='> 거래여부', value='실패')
                embed.add_field(name='> 실패사유', value='입력에 불필요한 입력이 있습니다.\n숫자 또는 1 이상의 숫자만 입력해주세요.')
                embed.set_footer(text='거래일시 : {}시 {}분 {}초'.format(now.hour, now.minute, now.second))
                await ctx.channel.send(embed=embed)
            elif(k-r<0 or k==0 or r<0):
                embed = discord.Embed(title='솔브닥 코인 가상 거래소',
                                      description=f'{ctx.message.author.mention}님의 거래결과를 알려드립니다.',
                                      colour=0xFA5858)
                embed.add_field(name='> 거래여부', value='실패')
                embed.add_field(name='> 실패사유', value='잔고가 부족합니다.')
                embed.set_footer(text='거래일시 : {}시 {}분 {}초'.format(now.hour, now.minute, now.second))
                await ctx.channel.send(embed=embed)
            else:
                kk = r*coinp
                con.close()
                con = sqlite3.connect(r'userdata.db', isolation_level=None)
                cur = con.cursor()
                cur.execute("UPDATE User_info SET money = money + ? WHERE id = ?", (int(kk), tid, ))
                cur.execute("UPDATE User_info SET coinA = coinA + ? WHERE id = ?", (int(-r), tid, ))
                cur.execute("SELECT money FROM User_Info WHERE id = ?", (tid, ))
                m1 = int(cur.fetchone()[0])
                cur.execute("SELECT coinA FROM User_Info WHERE id = ?", (tid, ))
                c1 = int(cur.fetchone()[0])
                cur.execute("SELECT coinB FROM User_Info WHERE id = ?", (tid,))
                c2 = int(cur.fetchone()[0])
                embed = discord.Embed(title='솔브닥 코인 가상 거래소',
                                      description=f'{ctx.message.author.mention}님의 거래결과를 알려드립니다.',
                                      colour=0xD0F5A9)
                embed.add_field(name='> 거래여부', value='성공')
                embed.add_field(name='> 현재가', value='{}원'.format(format(coinp, ",")))
                embed.add_field(name='> 거래개수', value='{}개'.format(format(int(input[0]), ",")))
                embed.add_field(name='> 지갑현황', value='솔브닥 코인 : {}개\n솔브닥 코인 2x 레버리지 : {}개\n잔고 : {}원'.format(format(c1, ","), format(c2, ","), format(m1, ",")))
                embed.set_footer(text='거래일시 : {}시 {}분 {}초'.format(now.hour, now.minute, now.second))
                await ctx.channel.send(embed=embed)
                coint2 += r
    except:
        embed = discord.Embed(title='솔브닥 코인 가상 거래소',
                              description=f'{ctx.message.author.mention}님의 거래결과를 알려드립니다.',
                              colour=0xFA5858)
        embed.add_field(name='> 거래여부', value='실패')
        embed.add_field(name='> 실패사유', value='입력에 불필요한 입력이 있습니다.\n!코인매도 [개수(숫자)] 형식으로 입력해주세요.')
        embed.set_footer(text='거래일시 : {}시 {}분 {}초'.format(now.hour, now.minute, now.second))
        await ctx.channel.send(embed=embed)
    con.close()

@bot.command()
async def 레버코인매수(ctx, *input):
    global coint, coint2, coinp, coin2p
    now = datetime.now(timezone('Asia/Seoul'))
    await ctx.channel.send(f'{ctx.message.author.mention}')
    try:
        tid = ctx.author.id
        con = sqlite3.connect(r'userdata.db', isolation_level=None)
        cur = con.cursor()
        chk = checkuser(tid)
        if (chk == 0):
            embed = discord.Embed(title='솔브닥 코인 가상 거래소',
                                  description=f'{ctx.message.author.mention}님의 거래결과를 알려드립니다.',
                                  colour=0xFA5858)
            embed.add_field(name='> 거래여부', value='실패')
            embed.add_field(name='> 실패사유', value='DB에 정보가 없습니다.\n!가입신청 을 입력해주세요.')
            embed.set_footer(text='거래일시 : {}시 {}분 {}초'.format(now.hour, now.minute, now.second))
            await ctx.channel.send(embed=embed)
        elif (chk == 1):
            cur.execute("SELECT money FROM User_Info WHERE id = ?", (tid, ))
            k = int(cur.fetchone()[0])
            r = int(input[0])
            if(r<=0):
                embed = discord.Embed(title='솔브닥 코인 가상 거래소',
                                      description=f'{ctx.message.author.mention}님의 거래결과를 알려드립니다.',
                                      colour=0xFA5858)
                embed.add_field(name='> 거래여부', value='실패')
                embed.add_field(name='> 실패사유', value='입력에 불필요한 입력이 있습니다.\n숫자 또는 1 이상의 숫자만 입력해주세요.')
                embed.set_footer(text='거래일시 : {}시 {}분 {}초'.format(now.hour, now.minute, now.second))
                await ctx.channel.send(embed=embed)
            elif(k-coin2p*r<0):
                embed = discord.Embed(title='솔브닥 코인 가상 거래소',
                                      description=f'{ctx.message.author.mention}님의 거래결과를 알려드립니다.',
                                      colour=0xFA5858)
                embed.add_field(name='> 거래여부', value='실패')
                embed.add_field(name='> 실패사유', value='잔고가 부족합니다.')
                embed.set_footer(text='거래일시 : {}시 {}분 {}초'.format(now.hour, now.minute, now.second))
                await ctx.channel.send(embed=embed)
            else:
                kk = -r*coin2p
                con.close()
                con = sqlite3.connect(r'userdata.db', isolation_level=None)
                cur = con.cursor()
                cur.execute("UPDATE User_info SET money = money + ? WHERE id = ?", (int(kk),tid,))
                cur.execute("UPDATE User_info SET coinB = coinB + ? WHERE id = ?", (int(r),tid,))
                cur.execute("SELECT money FROM User_Info WHERE id = ?", (tid, ))
                m1 = int(cur.fetchone()[0])
                cur.execute("SELECT coinA FROM User_Info WHERE id = ?", (tid, ))
                c1 = int(cur.fetchone()[0])
                cur.execute("SELECT coinB FROM User_Info WHERE id = ?", (tid,))
                c2 = int(cur.fetchone()[0])
                embed = discord.Embed(title='솔브닥 코인 가상 거래소',
                                      description=f'{ctx.message.author.mention}님의 거래결과를 알려드립니다.',
                                      colour=0xD0F5A9)
                embed.add_field(name='> 거래여부', value='성공')
                embed.add_field(name='> 현재가', value='{}원'.format(format(coin2p, ",")))
                embed.add_field(name='> 거래개수', value='{}개'.format(format(int(input[0]), ",")))
                embed.add_field(name='> 지갑현황', value='솔브닥 코인 : {}개\n솔브닥 코인 2x 레버리지 : {}개\n잔고 : {}원'.format(format(c1, ","), format(c2, ","), format(m1, ",")))
                embed.set_footer(text='거래일시 : {}시 {}분 {}초'.format(now.hour, now.minute, now.second))
                await ctx.channel.send(embed=embed)
                coint += r
    except:
        embed = discord.Embed(title='솔브닥 코인 가상 거래소',
                              description=f'{ctx.message.author.mention}님의 거래결과를 알려드립니다.',
                              colour=0xFA5858)
        embed.add_field(name='> 거래여부', value='실패')
        embed.add_field(name='> 실패사유', value='입력에 불필요한 입력이 있습니다.\n!레버코인매수 [개수(숫자)] 형식으로 입력해주세요.')
        embed.set_footer(text='거래일시 : {}시 {}분 {}초'.format(now.hour, now.minute, now.second))
        await ctx.channel.send(embed=embed)

    con.close()

@bot.command()
async def 레버코인매도(ctx, *input):
    global coint, coint2, coinp, coin2p
    now = datetime.now(timezone('Asia/Seoul'))
    await ctx.channel.send(f'{ctx.message.author.mention}')
    try:
        tid = ctx.author.id
        con = sqlite3.connect(r'userdata.db', isolation_level=None)
        cur = con.cursor()
        chk = checkuser(tid)
        if (chk == 0):
            embed = discord.Embed(title='솔브닥 코인 가상 거래소',
                                  description=f'{ctx.message.author.mention}님의 거래결과를 알려드립니다.',
                                  colour=0xFA5858)
            embed.add_field(name='> 거래여부', value='실패')
            embed.add_field(name='> 실패사유', value='DB에 정보가 없습니다.\n!가입신청 을 입력해주세요.')
            embed.set_footer(text='거래일시 : {}시 {}분 {}초'.format(now.hour, now.minute, now.second))
            await ctx.channel.send(embed=embed)
        elif (chk == 1):
            cur.execute("SELECT coinB FROM User_Info WHERE id = ?", (tid, ))
            k = int(cur.fetchone()[0])
            r = int(input[0])
            if(r<=0):
                embed = discord.Embed(title='솔브닥 코인 가상 거래소',
                                      description=f'{ctx.message.author.mention}님의 거래결과를 알려드립니다.',
                                      colour=0xFA5858)
                embed.add_field(name='> 거래여부', value='실패')
                embed.add_field(name='> 실패사유', value='입력에 불필요한 입력이 있습니다.\n숫자 또는 1 이상의 숫자만 입력해주세요.')
                embed.set_footer(text='거래일시 : {}시 {}분 {}초'.format(now.hour, now.minute, now.second))
                await ctx.channel.send(embed=embed)
            elif(k-r<0 or k==0):
                embed = discord.Embed(title='솔브닥 코인 가상 거래소',
                                      description=f'{ctx.message.author.mention}님의 거래결과를 알려드립니다.',
                                      colour=0xFA5858)
                embed.add_field(name='> 거래여부', value='실패')
                embed.add_field(name='> 실패사유', value='잔고가 부족합니다.')
                embed.set_footer(text='거래일시 : {}시 {}분 {}초'.format(now.hour, now.minute, now.second))
                await ctx.channel.send(embed=embed)
            else:
                kk = r*coin2p
                con.close()
                con = sqlite3.connect(r'userdata.db', isolation_level=None)
                cur = con.cursor()
                cur.execute("UPDATE User_info SET money = money + ? WHERE id = ?", (int(kk), tid, ))
                cur.execute("UPDATE User_info SET coinB = coinB + ? WHERE id = ?", (int(-r), tid, ))
                cur.execute("SELECT money FROM User_Info WHERE id = ?", (tid, ))
                m1 = int(cur.fetchone()[0])
                cur.execute("SELECT coinA FROM User_Info WHERE id = ?", (tid, ))
                c1 = int(cur.fetchone()[0])
                cur.execute("SELECT coinB FROM User_Info WHERE id = ?", (tid,))
                c2 = int(cur.fetchone()[0])
                embed = discord.Embed(title='솔브닥 코인 가상 거래소',
                                      description=f'{ctx.message.author.mention}님의 거래결과를 알려드립니다.',
                                      colour=0xD0F5A9)
                embed.add_field(name='> 거래여부', value='성공')
                embed.add_field(name='> 현재가', value='{}원'.format(format(coin2p, ",")))
                embed.add_field(name='> 거래개수', value='{}개'.format(format(int(input[0]), ",")))
                embed.add_field(name='> 지갑현황', value='솔브닥 코인 : {}개\n솔브닥 코인 2x 레버리지 : {}개\n잔고 : {}원'.format(format(c1, ","), format(c2, ","), format(m1, ",")))
                embed.set_footer(text='거래일시 : {}시 {}분 {}초'.format(now.hour, now.minute, now.second))
                await ctx.channel.send(embed=embed)
                coint2 += r
    except:
        embed = discord.Embed(title='솔브닥 코인 가상 거래소',
                              description=f'{ctx.message.author.mention}님의 거래결과를 알려드립니다.',
                              colour=0xFA5858)
        embed.add_field(name='> 거래여부', value='실패')
        embed.add_field(name='> 실패사유', value='입력에 불필요한 입력이 있습니다.\n!레버코인매도 [개수(숫자)] 형식으로 입력해주세요.')
        embed.set_footer(text='거래일시 : {}시 {}분 {}초'.format(now.hour, now.minute, now.second))
        await ctx.channel.send(embed=embed)
    con.close()

bot.run(token)
