from PIL import Image,ImageDraw,ImageFont
from discord.ext import commands
import subprocess
import requests
import datetime
import discord
import asyncio
import server
import random
import json
import os
import re

server.start()

bot = discord.Bot(
  intents=discord.Intents.all(),
  activity=discord.Game("/help｜ハムたん#3859"))

class HelpMenu(discord.ui.View):
    @discord.ui.select(placeholder="メニュー", options=[
        discord.SelectOption(label="ホーム", emoji="🏠", description="helpの最初の画面に戻ります。", value="Home"),
        discord.SelectOption(label="便利", emoji="💡", description="便利コマンドを表示します。", value="Tool"), discord.SelectOption(label="パネル", emoji="🖥", description="パネル作成コマンドを表示します。", value="Panel"), discord.SelectOption(label="サーバー管理", emoji="⚒️", description="サーバー管理コマンドを表示します。", value="Moderate"), discord.SelectOption(label="遊び・ネタ", emoji="🎮", description="遊び・ネタコマンドを表示します。", value="Fun"), discord.SelectOption(label="情報", emoji="ℹ️", description="情報コマンドを表示します。", value="Info")
    ])
    async def select_menu(self, select: discord.ui.Select, interaction: discord.Interaction):
        if select.values[0] == "Home":
          await interaction.response.edit_message(embed=discord.Embed(title="help", description="**PoLab** - 便利で使いやすい多機能bot\n\n📮 » お問い合わせや要望は`ハムたん#3859`にお願いします\n\n🔗｜PoLabを導入する\n[管理者権限](https://discord.com/oauth2/authorize?client_id=1106830543699583027&scope=bot+applications.commands&permissions=8)\n[権限なし](https://discord.com/oauth2/authorize?client_id=1106830543699583027&scope=bot+applications.commands)", color=0xadb8cb).set_image(url="https://media.discordapp.net/attachments/1114573511642591272/1114573537542414367/20230604_000735.gif"))
        if select.values[0] == "Tool":
          await interaction.response.edit_message(embed=discord.Embed(title="help", description="**💡便利コマンド**\n\n```/alarm [時間]```アラームをセットします。\n\n```/avatar [ユーザー]```指定したユーザーのアイコンを取得します。\n\n```/botinv [ボット]```指定したbotの招待を作成します。\n\n```/calc [計算式]```計算を行います。\n\n```/memo [操作] (メモ)```メモを保存、読み込みします。\n\n```/poll [タイトル] [選択肢1] [選択肢2] (選択肢3) (選択肢4) (選択肢5) (選択肢6) (選択肢7)```投票を行います。\n\n```/shorten [url]```短縮URLを作成します。\n\n```/translate [テキスト] [翻訳先]```翻訳を行います。\n\n```/weather [地域]```天気予報を表示します。\n\n```/wpoll [タイトル]```自由記述式の投票を行います。", color=0xadb8cb))
        if select.values[0] == "Panel":
          await interaction.response.edit_message(embed=discord.Embed(title="help", description="**🖥パネル作成コマンド**\n\n```/ticket [タイトル] [メッセージ]```チケットパネルを配置します。\n\n```/top [ラベル]```チャンネルの１番上に飛ぶボタンを配置します。\n\n```/verify [ロール] [タイトル] [メッセージ]```認証パネルを配置します。", color=0xadb8cb))
        if select.values[0] == "Info":
          await interaction.response.edit_message(embed=discord.Embed(title="help", description="**ℹ️情報コマンド**\n\n```/help```helpを表示します。\n\n```/ping```botの遅延を計測します。", color=0xadb8cb))
        if select.values[0] == "Moderate":
          await interaction.response.edit_message(embed=discord.Embed(title="help", description="**⚒️サーバー管理コマンド**\n\n```/clear [数] (メンバー)```メッセージを一括削除します。\n\n```/log [対象] [チャンネル]```ログチャンネルを設定します。\n\n```/setup```サーバーセットアップを行います。\n\n```/welcome [メッセージ] [チャンネル]```入室メッセージを設定します。", color=0xadb8cb))
        if select.values[0] == "Fun":
          await interaction.response.edit_message(embed=discord.Embed(title="help", description="**🎮遊び・ネタコマンド**\n\n```/5000 [上のテキスト] [下のテキスト]```5000兆円欲しい！の画像を生成します。\n\n```/minesweeper```マインスイーパーをプレイします。\n\n```/miq [メッセージ]```Make it a Quoteを生成します。\n\n```/python [コード]```pythonのコードを実行します。", color=0xadb8cb))

class TicketButton(discord.ui.View):
  def __init__(self):
    super().__init__(timeout=None)
  @discord.ui.button(label="🎫", style=discord.ButtonStyle.gray, custom_id="ticket_btn")
  async def ticket_button(self, button: discord.ui.Button, interaction: discord.Interaction):
    for channel in interaction.guild.channels:
      if channel.name == f"🎫ticket-{interaction.user.name}":
        return await interaction.response.send_message(embed=discord.Embed(title="<:error:1112400450101186622>｜エラー", description="あなたは既にチケットを作成しています。", color=0xff0000), ephemeral=True)
    overwrites = {
                interaction.guild.default_role: discord.PermissionOverwrite(view_channel = False),
                interaction.user: discord.PermissionOverwrite(view_channel = True, read_message_history = True, send_messages = True, attach_files = True, embed_links = True),
         interaction.guild.me: discord.PermissionOverwrite(view_channel = True, send_messages = True, read_message_history = True)
    }
    ticket_channel = await interaction.guild.create_text_channel(f"🎫ticket-{interaction.user.name}", overwrites=overwrites)
    await ticket_channel.send(embed=discord.Embed(title="<:ticket:1112400556774932542>｜チケット", description="管理者が来るまでお待ちください。", color=0xadb8cb), view=TicketDelete())
    await interaction.response.send_message(content=f"<:ticket:1112400556774932542> » チケットを作成しました。\n{ticket_channel.mention}", ephemeral=True)

class TicketDelete(discord.ui.View):
  def __init__(self):
    super().__init__(timeout=None)
  @discord.ui.button(label="🗑閉じる", style=discord.ButtonStyle.danger, custom_id="ticket_delete_btn")
  async def delete_ticket(self, button: discord.ui.Button, interaction: discord.Interaction):
    await interaction.channel.delete()

class VerifyButton(discord.ui.View):
  def __init__(self):
    super().__init__(timeout=None)
  @discord.ui.button(label="認証", style=discord.ButtonStyle.green, custom_id="verify_btn")
  async def verify(self, button: discord.ui.Button, interaction: discord.Interaction):
    verified_role = interaction.message.embeds[0].footer.text
    try:
      if discord.utils.get(interaction.guild.roles, id=int(verified_role)) in interaction.user.roles:
        await interaction.response.send_message("あなたは既に認証しています。", ephemeral=True)
      else:
        await interaction.user.add_roles(discord.utils.get(interaction.guild.roles, id=int(verified_role)))
        await interaction.response.send_message("<:check:1112400403850600468> » 認証が完了しました。", ephemeral=True)
    except:
      await interaction.response.send_message("<:error:1112400450101186622> » \n認証に失敗しました。\nbotの権限やロールの順位を確認してください。", ephemeral=True)

class SetupButton(discord.ui.View):
  def __init__(self):
    super().__init__(timeout=None)
  @discord.ui.button(label="✅", style=discord.ButtonStyle.gray)
  async def verify(self, button: discord.ui.Button, interaction: discord.Interaction):
    permissions = discord.Permissions()
    permissions.mention_everyone = False
    permissions.view_channel = True
    permissions.read_message_history = True
    permissions.create_public_threads = True
    permissions.send_messages_in_threads = True
    permissions.send_messages = True
    permissions.add_reactions = True
    permissions.attach_files = True
    permissions.embed_links = True
    permissions.use_application_commands = True
    permissions.use_external_emojis = True
    permissions.use_external_stickers = True
    permissions.connect = True
    permissions.speak = True
    permissions.stream = True
    permissions.create_instant_invite = True
    permissions.change_nickname = True
    await interaction.guild.default_role.edit(permissions=permissions)
    overwrites = {
                interaction.guild.default_role: discord.PermissionOverwrite(send_messages = False)}
    await interaction.guild.create_text_channel("📗ルール", overwrites=overwrites)
    await interaction.guild.create_text_channel("🔔お知らせ", overwrites=overwrites)
    verify_ch = await interaction.guild.create_text_channel("✅認証", overwrites=overwrites)
    ticket_ch = await interaction.guild.create_text_channel("📮お問い合わせ", overwrites=overwrites)
    permissions = discord.Permissions()
    permissions.administrator = True
    await interaction.guild.create_role(name="🛡管理者", permissions=permissions, hoist=True)
    await interaction.guild.create_role(name="🤖bot", permissions=permissions, hoist=True)
    permissions = discord.Permissions()
    permissions.mention_everyone = False
    permissions.view_channel = True
    permissions.read_message_history = True
    permissions.create_public_threads = True
    permissions.send_messages_in_threads = True
    permissions.send_messages = True
    permissions.add_reactions = True
    permissions.attach_files = True
    permissions.embed_links = True
    permissions.use_application_commands = True
    permissions.use_external_emojis = True
    permissions.use_external_stickers = True
    permissions.connect = True
    permissions.speak = True
    permissions.stream = True
    permissions.create_instant_invite = True
    permissions.change_nickname = True
    member_role = await interaction.guild.create_role(name="👤メンバー", permissions=permissions, hoist=True)
    
    await verify_ch.send(embed=discord.Embed(title="<:check:1112400403850600468>認証", description="下のボタンを押して認証してください。", color=0xadb8cb).set_footer(text=member_role.id), view=VerifyButton())
    await ticket_ch.send(embed=discord.Embed(title="<:ticket:1112400556774932542>｜お問い合わせ", description="お問い合わせはこちらからお願いします。", color=0xadb8cb), view=TicketButton())
    link = await interaction.channel.create_invite(max_age = 0, max_uses = 0)
    await interaction.channel.send(embed=discord.Embed(title="サーバーセットアップ", description=f"<:check:1112400403850600468> » サーバーセットアップが完了しました。\n🔗 » {link}", color=0xadb8cb), view=None)

class wpollModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.add_item(discord.ui.InputText(label="回答"))
        
    async def callback(self, interaction: discord.Interaction):
      await interaction.message.edit(embed=discord.Embed(title=interaction.message.embeds[0].title, description=f"{interaction.message.embeds[0].description}\n▷{self.children[0].value} - {interaction.user.name}#{interaction.user.discriminator}".replace("Embed.Empty", ""), color=0xadb8cb))
      await interaction.response.send_message("<:check:1112400403850600468> » 回答を送信しました。", ephemeral=True)
      
class wpollButton(discord.ui.View):
  def __init__(self):
    super().__init__(timeout=None)
  @discord.ui.button(label="回答する", style=discord.ButtonStyle.gray)
  async def verify(self, button: discord.ui.Button, interaction: discord.Interaction):
    modal = wpollModal(title=interaction.message.embeds[0].title)
    await interaction.response.send_modal(modal)

@bot.event
async def on_ready():
  bot.add_view(TicketButton())
  bot.add_view(TicketDelete())
  bot.add_view(VerifyButton())

@bot.command(name="help", description="helpを表示します。")
async def help(ctx: discord.ApplicationContext):
  await ctx.respond(embed=discord.Embed(title="help", description="**PoLab** - 便利で使いやすい多機能bot\n\n📮 » お問い合わせや要望は`ハムたん#3859`にお願いします\n\n🔗｜PoLabを導入する\n[管理者権限](https://discord.com/oauth2/authorize?client_id=1106830543699583027&scope=bot+applications.commands&permissions=8)\n[権限なし](https://discord.com/oauth2/authorize?client_id=1106830543699583027&scope=bot+applications.commands)", color=0xadb8cb).set_image(url="https://media.discordapp.net/attachments/1114573511642591272/1114573537542414367/20230604_000735.gif"), view=HelpMenu())

@bot.command(name="ping", description="botの遅延を計測します。")
async def ping(ctx: discord.ApplicationContext):
    await ctx.respond(embed=discord.Embed(title="ping", description=f"**Latency**\n{round(bot.latency * 1000)}ms", color=0xadb8cb))

@bot.command(name="botinv", description="指定したbotの招待を作成します。")
async def botinv(ctx: discord.ApplicationContext, ボット: discord.Option(discord.Member, "botを指定してください。")):
  await ctx.respond(embed=discord.Embed(title=f"<@{ボット.id}>の招待", description=f"**管理者権限**\nhttps://discord.com/oauth2/authorize?client_id={ボット.id}&scope=bot+applications.commands&permissions=8\n\n**権限なし**\nhttps://discord.com/oauth2/authorize?client_id={ボット.id}&scope=bot+applications.commands", color=0xadb8cb))

@bot.command(name="calc", description="計算を行います。")
async def calc(ctx: discord.ApplicationContext, 計算式: discord.Option(str, "計算式を入力してください。")):
  ngchars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
  for ngchar in ngchars:
    if ngchar in 計算式:
      return await ctx.respond(embed=discord.Embed(title="<:error:1112400450101186622>｜エラー", description="計算式を入力してください。", color=0xff0000), ephemeral=True)
      break
    else:
      continue
  try:
    await ctx.respond(embed=discord.Embed(title="<:calc:1112400493180887060>｜計算", description=f"{計算式} = {eval(計算式)}", color=0xadb8cb).set_thumbnail(url="https://i.ibb.co/BK6QYF0/3d-calculator.png"))
  except:
    await ctx.respond(embed=discord.Embed(title="<:error:1112400450101186622>｜エラー", description="計算式を入力してください。", color=0xff0000), ephemeral=True)

@bot.command(name="poll", description="投票を行います。")
async def poll(ctx: discord.ApplicationContext, タイトル: discord.Option(str, "投票のタイトルを入力してください。"), 選択肢1: discord.Option(str, "1つ目の選択肢を入力してください。"), 選択肢2: discord.Option(str, "2つ目の選択肢を入力してください。"), 選択肢3: discord.Option(str, "3つ目の選択肢を入力してください。", required=False), 選択肢4: discord.Option(str, "4つ目の選択肢を入力してください。", required=False), 選択肢5: discord.Option(str, "5つ目の選択肢を入力してください。", required=False), 選択肢6: discord.Option(str, "6つ目の選択肢を入力してください。", required=False), 選択肢7: discord.Option(str, "7つ目の選択肢を入力してください。", required=False)):
  if 選択肢3 == None:
    message = await ctx.respond(embed=discord.Embed(title=タイトル, description=f"1️⃣ » {選択肢1}\n2️⃣ » {選択肢2}", color=0xadb8cb).set_thumbnail(url="https://i.ibb.co/3BH8Ckd/Image-Titan-2023-05-20-15-33-09.png"))
    msg = await message.original_message()
    await msg.add_reaction("1️⃣")
    await msg.add_reaction("2️⃣")
  elif 選択肢4 == None:
    message = await ctx.respond(embed=discord.Embed(title=タイトル, description=f"1️⃣ » {選択肢1}\n2️⃣ » {選択肢2}\n3️⃣ » {選択肢3}", color=0xadb8cb).set_thumbnail(url="https://i.ibb.co/3BH8Ckd/Image-Titan-2023-05-20-15-33-09.png"))
    msg = await message.original_message()
    await msg.add_reaction("1️⃣")
    await msg.add_reaction("2️⃣")
    await msg.add_reaction("3️⃣")
  elif 選択肢5 == None:
    message = await ctx.respond(embed=discord.Embed(title=タイトル, description=f"1️⃣ » {選択肢1}\n2️⃣ » {選択肢2}\n3️⃣ » {選択肢3}\n4️⃣ » {選択肢4}", color=0xadb8cb).set_thumbnail(url="https://i.ibb.co/3BH8Ckd/Image-Titan-2023-05-20-15-33-09.png"))
    msg = await message.original_message()
    await msg.add_reaction("1️⃣")
    await msg.add_reaction("2️⃣")
    await msg.add_reaction("3️⃣")
    await msg.add_reaction("4️⃣")
  elif 選択肢6 == None:
    message = await ctx.respond(embed=discord.Embed(title=タイトル, description=f"1️⃣ » {選択肢1}\n2️⃣ » {選択肢2}\n3️⃣ » {選択肢3}\n4️⃣ » {選択肢4}\n5️⃣ » {選択肢5}", color=0xadb8cb).set_thumbnail(url="https://i.ibb.co/3BH8Ckd/Image-Titan-2023-05-20-15-33-09.png"))
    msg = await message.original_message()
    await msg.add_reaction("1️⃣")
    await msg.add_reaction("2️⃣")
    await msg.add_reaction("3️⃣")
    await msg.add_reaction("4️⃣")
    await msg.add_reaction("5️⃣")
  elif 選択肢7 == None:
    message = await ctx.respond(embed=discord.Embed(title=タイトル, description=f"1️⃣ » {選択肢1}\n2️⃣ » {選択肢2}\n3️⃣ » {選択肢3}\n4️⃣ » {選択肢4}\n5️⃣ » {選択肢5}\n6️⃣ » {選択肢6}", color=0xadb8cb).set_thumbnail(url="https://i.ibb.co/3BH8Ckd/Image-Titan-2023-05-20-15-33-09.png"))
    msg = await message.original_message()
    await msg.add_reaction("1️⃣")
    await msg.add_reaction("2️⃣")
    await msg.add_reaction("3️⃣")
    await msg.add_reaction("4️⃣")
    await msg.add_reaction("5️⃣")
    await msg.add_reaction("6️⃣")
  else:
    message = await ctx.respond(embed=discord.Embed(title=タイトル, description=f"1️⃣ » {選択肢1}\n2️⃣ » {選択肢2}\n3️⃣ » {選択肢3}\n4️⃣ » {選択肢4}\n5️⃣ » {選択肢5}\n6️⃣ » {選択肢6}\n7️⃣ » {選択肢7}", color=0xadb8cb).set_thumbnail(url="https://i.ibb.co/3BH8Ckd/Image-Titan-2023-05-20-15-33-09.png"))
    msg = await message.original_message()
    await msg.add_reaction("1️⃣")
    await msg.add_reaction("2️⃣")
    await msg.add_reaction("3️⃣")
    await msg.add_reaction("4️⃣")
    await msg.add_reaction("5️⃣")
    await msg.add_reaction("6️⃣")
    await msg.add_reaction("7️⃣")

@bot.command(name="ticket", description="チケットパネルを配置します。")
async def ticket(ctx: discord.ApplicationContext, タイトル: discord.Option(str, "チケットパネルのタイトルを入力してください。"), メッセージ: discord.Option(str, "チケットパネルに表示するメッセージを入力してください。")):
  if ctx.author.guild_permissions.manage_channels:
    await ctx.respond(embed=discord.Embed(title=タイトル, description=メッセージ, color=0xadb8cb).set_thumbnail(url="https://i.ibb.co/BrQvZ8w/Microsoft-Fluentui-Emoji-3d-Ticket-3d-512.png"), view=TicketButton())
  else:
    await ctx.respond(embed=discord.Embed(title="エラー", description="<:error:1112400450101186622>｜チケットパネルを作成するには`チャンネル管理`の権限が必要です。", color=0xff0000), ephemeral=True)

@bot.command(name="translate", description="翻訳を行います。")
async def translate(ctx: discord.ApplicationContext, テキスト: discord.Option(str, "翻訳するテキストを入力してください。"), 翻訳先: discord.Option(str, "翻訳先の言語を指定してください。", choices=["🇯🇵日本語", "🇺🇸英語", "🇨🇳中国語", "🇮🇳ヒンディー語"])):
  if 翻訳先 == "🇯🇵日本語":
    response = requests.get(f"https://script.google.com/macros/s/AKfycbwDZ5mESQpMLLT-efxT0oyXn69n7q_ZzTzD4orm3l640QmtNTR_QlP4PWfQMGrgr9k0sA/exec?text={テキスト}&target=ja").text
    await ctx.respond(embed=discord.Embed(title="<:translate:1112400678552342579>｜翻訳", description=f"📄 » {テキスト}\n\n🇯🇵 » {response}", color=0xadb8cb).set_thumbnail(url="https://i.ibb.co/hLmZYFB/Image-Titan-2023-05-20-15-31-24.png"))
  if 翻訳先 == "🇺🇸英語":
    response = requests.get(f"https://script.google.com/macros/s/AKfycbwDZ5mESQpMLLT-efxT0oyXn69n7q_ZzTzD4orm3l640QmtNTR_QlP4PWfQMGrgr9k0sA/exec?text={テキスト}&target=en").text
    await ctx.respond(embed=discord.Embed(title="<:translate:1112400678552342579>｜翻訳", description=f"📄 » {テキスト}\n\n🇺🇸 » {response}", color=0xadb8cb).set_thumbnail(url="https://i.ibb.co/hLmZYFB/Image-Titan-2023-05-20-15-31-24.png"))
  if 翻訳先 == "🇨🇳中国語":
    response = requests.get(f"https://script.google.com/macros/s/AKfycbwDZ5mESQpMLLT-efxT0oyXn69n7q_ZzTzD4orm3l640QmtNTR_QlP4PWfQMGrgr9k0sA/exec?text={テキスト}&target=zh-CN").text
    await ctx.respond(embed=discord.Embed(title="<:translate:1112400678552342579>｜翻訳", description=f"📄 » {テキスト}\n\n🇨🇳 » {response}", color=0xadb8cb).set_thumbnail(url="https://i.ibb.co/hLmZYFB/Image-Titan-2023-05-20-15-31-24.png"))
  if 翻訳先 == "🇮🇳ヒンディー語":
    response = requests.get(f"https://script.google.com/macros/s/AKfycbwDZ5mESQpMLLT-efxT0oyXn69n7q_ZzTzD4orm3l640QmtNTR_QlP4PWfQMGrgr9k0sA/exec?text={テキスト}&target=hi").text
    await ctx.respond(embed=discord.Embed(title="<:translate:1112400678552342579>｜翻訳", description=f"📄 » {テキスト}\n\n🇮🇳 » {response}", color=0xadb8cb).set_thumbnail(url="https://i.ibb.co/hLmZYFB/Image-Titan-2023-05-20-15-31-24.png"))

@bot.command(name="5000", description="5000兆円欲しい！の画像を生成します。")
async def choyen(ctx: discord.ApplicationContext, 上のテキスト: discord.Option(str, "上に表示するテキストを入力してください。"), 下のテキスト: discord.Option(str, "下に表示するテキストを入力してください。")):
  await ctx.respond(f"https://gsapi.cbrx.io/image?top={上のテキスト}&bottom={下のテキスト}")

@bot.command(name="minesweeper", description="マインスイーパーをプレイします。")
async def minesweeper(ctx: discord.ApplicationContext):
  panels = ["""||:zero:||||:zero:||||:one:||||:one:||||:one:||||:one:||||:bomb:||||:one:||||:zero:||
||:one:||||:one:||||:two:||||:bomb:||||:one:||||:one:||||:one:||||:one:||||:zero:||
||:one:||||:bomb:||||:two:||||:one:||||:one:||||:one:||||:one:||||:two:||||:one:||
||:one:||||:one:||||:one:||||:zero:||||:zero:||||:one:||||:bomb:||||:two:||||:bomb:||
||:zero:||||:zero:||||:zero:||||:one:||||:one:||||:two:||||:two:||||:three:||||:two:||
||:one:||||:one:||||:zero:||||:one:||||:bomb:||||:one:||||:one:||||:bomb:||||:one:||
||:bomb:||||:two:||||:zero:||||:one:||||:one:||||:two:||||:two:||||:two:||||:one:||
||:bomb:||||:two:||||:zero:||||:zero:||||:zero:||||:one:||||:bomb:||||:one:||||:zero:||
||:one:||||:one:||||:zero:||||:zero:||||:zero:||||:one:||||:one:||||:one:||||:zero:||""", """||:bomb:||||:two:||||:bomb:||||:one:||||:zero:||||:one:||||:bomb:||||:one:||||:zero:||
||:one:||||:two:||||:one:||||:two:||||:one:||||:two:||||:one:||||:one:||||:zero:||
||:zero:||||:zero:||||:zero:||||:one:||||:bomb:||||:one:||||:zero:||||:zero:||||:zero:||
||:zero:||||:one:||||:one:||||:two:||||:one:||||:two:||||:one:||||:two:||||:one:||
||:one:||||:two:||||:bomb:||||:one:||||:zero:||||:one:||||:bomb:||||:three:||||:bomb:||
||:one:||||:bomb:||||:three:||||:two:||||:one:||||:one:||||:two:||||:bomb:||||:two:||
||:one:||||:one:||||:two:||||:bomb:||||:one:||||:zero:||||:one:||||:one:||||:one:||
||:zero:||||:zero:||||:one:||||:one:||||:one:||||:zero:||||:zero:||||:zero:||||:zero:||
||:zero:||||:zero:||||:zero:||||:zero:||||:zero:||||:zero:||||:zero:||||:zero:||||:zero:||
""", """||:one:||||:one:||||:two:||||:one:||||:one:||||:zero:||||:zero:||||:zero:||||:zero:||
||:two:||||:bomb:||||:three:||||:bomb:||||:one:||||:one:||||:two:||||:three:||||:two:||
||:two:||||:bomb:||||:three:||||:one:||||:one:||||:one:||||:bomb:||||:bomb:||||:bomb:||
||:one:||||:one:||||:two:||||:one:||||:one:||||:one:||||:three:||||:four:||||:three:||
||:zero:||||:zero:||||:one:||||:bomb:||||:one:||||:zero:||||:one:||||:bomb:||||:one:||
||:zero:||||:one:||||:two:||||:two:||||:two:||||:one:||||:two:||||:one:||||:one:||
||:zero:||||:one:||||:bomb:||||:one:||||:one:||||:bomb:||||:one:||||:zero:||||:zero:||
||:zero:||||:one:||||:one:||||:one:||||:one:||||:one:||||:one:||||:zero:||||:zero:||
||:zero:||||:zero:||||:zero:||||:zero:||||:zero:||||:zero:||||:zero:||||:zero:||||:zero:||
""", """||:zero:||||:zero:||||:zero:||||:zero:||||:one:||||:bomb:||||:one:||||:zero:||||:zero:||
||:zero:||||:zero:||||:zero:||||:zero:||||:one:||||:one:||||:one:||||:zero:||||:zero:||
||:zero:||||:one:||||:one:||||:one:||||:zero:||||:zero:||||:one:||||:one:||||:one:||
||:zero:||||:two:||||:bomb:||||:two:||||:zero:||||:zero:||||:one:||||:bomb:||||:one:||
||:zero:||||:two:||||:bomb:||||:three:||||:one:||||:one:||||:one:||||:one:||||:one:||
||:zero:||||:one:||||:one:||||:two:||||:bomb:||||:one:||||:zero:||||:zero:||||:zero:||
||:one:||||:one:||||:one:||||:two:||||:two:||||:two:||||:zero:||||:zero:||||:zero:||
||:one:||||:bomb:||||:one:||||:one:||||:bomb:||||:two:||||:two:||||:three:||||:two:||
||:one:||||:one:||||:one:||||:one:||||:one:||||:two:||||:bomb:||||:bomb:||||:bomb:||
""", """||:zero:||||:zero:||||:zero:||||:zero:||||:two:||||:bomb:||||:three:||||:bomb:||||:one:||
||:one:||||:one:||||:one:||||:zero:||||:two:||||:bomb:||||:four:||||:two:||||:one:||
||:one:||||:bomb:||||:one:||||:zero:||||:one:||||:two:||||:bomb:||||:one:||||:zero:||
||:two:||||:two:||||:one:||||:zero:||||:zero:||||:one:||||:one:||||:one:||||:zero:||
||:bomb:||||:one:||||:zero:||||:zero:||||:zero:||||:zero:||||:zero:||||:zero:||||:zero:||
||:two:||||:two:||||:one:||||:one:||||:one:||||:zero:||||:zero:||||:zero:||||:zero:||
||:bomb:||||:one:||||:one:||||:bomb:||||:one:||||:zero:||||:one:||||:one:||||:one:||
||:one:||||:one:||||:two:||||:two:||||:two:||||:zero:||||:one:||||:bomb:||||:one:||
||:zero:||||:zero:||||:one:||||:bomb:||||:one:||||:zero:||||:one:||||:one:||||:one:||
""", """||:two:||||:bomb:||||:one:||||:one:||||:one:||||:one:||||:zero:||||:zero:||||:zero:||
||:bomb:||||:two:||||:two:||||:two:||||:bomb:||||:two:||||:one:||||:two:||||:one:||
||:one:||||:one:||||:one:||||:bomb:||||:two:||||:two:||||:bomb:||||:two:||||:bomb:||
||:zero:||||:zero:||||:one:||||:two:||||:two:||||:two:||||:one:||||:two:||||:one:||
||:zero:||||:zero:||||:zero:||||:one:||||:bomb:||||:one:||||:one:||||:one:||||:one:||
||:one:||||:one:||||:one:||||:one:||||:one:||||:one:||||:one:||||:bomb:||||:one:||
||:one:||||:bomb:||||:one:||||:zero:||||:zero:||||:zero:||||:two:||||:two:||||:two:||
||:one:||||:one:||||:one:||||:zero:||||:zero:||||:zero:||||:one:||||:bomb:||||:one:||
||:zero:||||:zero:||||:zero:||||:zero:||||:zero:||||:zero:||||:one:||||:one:||||:one:||
""", """||:bomb:||||:one:||||:zero:||||:zero:||||:zero:||||:zero:||||:one:||||:bomb:||||:one:||
||:one:||||:one:||||:zero:||||:zero:||||:zero:||||:one:||||:two:||||:two:||||:one:||
||:zero:||||:zero:||||:one:||||:one:||||:one:||||:one:||||:bomb:||||:one:||||:zero:||
||:zero:||||:one:||||:two:||||:bomb:||||:one:||||:one:||||:one:||||:one:||||:zero:||
||:zero:||||:one:||||:bomb:||||:three:||||:two:||||:zero:||||:zero:||||:zero:||||:zero:||
||:zero:||||:two:||||:three:||||:bomb:||||:two:||||:one:||||:zero:||||:zero:||||:zero:||
||:zero:||||:one:||||:bomb:||||:three:||||:bomb:||||:two:||||:one:||||:one:||||:one:||
||:zero:||||:one:||||:one:||||:two:||||:two:||||:bomb:||||:one:||||:one:||||:bomb:||
||:zero:||||:zero:||||:zero:||||:zero:||||:one:||||:one:||||:one:||||:one:||||:one:||
""", """||:zero:||||:zero:||||:one:||||:one:||||:two:||||:one:||||:one:||||:zero:||||:zero:||
||:zero:||||:zero:||||:one:||||:bomb:||||:two:||||:bomb:||||:two:||||:one:||||:zero:||
||:zero:||||:zero:||||:one:||||:one:||||:two:||||:two:||||:bomb:||||:one:||||:zero:||
||:zero:||||:zero:||||:zero:||||:zero:||||:zero:||||:two:||||:two:||||:two:||||:zero:||
||:one:||||:one:||||:one:||||:zero:||||:zero:||||:one:||||:bomb:||||:one:||||:zero:||
||:one:||||:bomb:||||:one:||||:zero:||||:one:||||:two:||||:three:||||:two:||||:one:||
||:one:||||:two:||||:two:||||:one:||||:two:||||:bomb:||||:three:||||:bomb:||||:one:||
||:zero:||||:one:||||:bomb:||||:two:||||:three:||||:bomb:||||:three:||||:one:||||:one:||
||:zero:||||:one:||||:two:||||:bomb:||||:two:||||:one:||||:one:||||:zero:||||:zero:||
""", """||:two:||||:bomb:||||:two:||||:zero:||||:zero:||||:zero:||||:zero:||||:zero:||||:zero:||
||:two:||||:bomb:||||:two:||||:one:||||:one:||||:one:||||:one:||||:one:||||:one:||
||:one:||||:one:||||:one:||||:one:||||:bomb:||||:one:||||:one:||||:bomb:||||:one:||
||:zero:||||:zero:||||:zero:||||:one:||||:one:||||:one:||||:one:||||:one:||||:one:||
||:zero:||||:zero:||||:zero:||||:zero:||||:zero:||||:zero:||||:zero:||||:zero:||||:zero:||
||:zero:||||:zero:||||:zero:||||:zero:||||:zero:||||:zero:||||:one:||||:one:||||:one:||
||:two:||||:two:||||:one:||||:zero:||||:zero:||||:zero:||||:one:||||:bomb:||||:one:||
||:bomb:||||:bomb:||||:two:||||:two:||||:two:||||:one:||||:two:||||:two:||||:two:||
||:two:||||:two:||||:two:||||:bomb:||||:bomb:||||:one:||||:one:||||:bomb:||||:one:||
""", """||:zero:||||:one:||||:bomb:||||:one:||||:one:||||:one:||||:one:||||:zero:||||:zero:||
||:zero:||||:one:||||:one:||||:one:||||:one:||||:bomb:||||:one:||||:zero:||||:zero:||
||:zero:||||:zero:||||:zero:||||:zero:||||:one:||||:one:||||:one:||||:zero:||||:zero:||
||:zero:||||:zero:||||:zero:||||:zero:||||:one:||||:one:||||:two:||||:one:||||:one:||
||:zero:||||:zero:||||:zero:||||:zero:||||:one:||||:bomb:||||:two:||||:bomb:||||:two:||
||:zero:||||:zero:||||:zero:||||:zero:||||:two:||||:two:||||:three:||||:two:||||:bomb:||
||:one:||||:one:||||:one:||||:one:||||:two:||||:bomb:||||:two:||||:two:||||:two:||
||:bomb:||||:one:||||:one:||||:bomb:||||:two:||||:two:||||:three:||||:bomb:||||:one:||
||:one:||||:one:||||:one:||||:one:||||:one:||||:one:||||:bomb:||||:two:||||:one:||
"""]
  await ctx.respond(embed=discord.Embed(title="マインスイーパー", description=random.choice(panels), color=0xadb8cb).set_footer(text="9x9｜💣x10"))

@bot.command(name="verify", description="認証パネルを配置します。")
async def verify(ctx: discord.ApplicationContext, ロール: discord.Option(discord.Role, "認証時に付与するロールを選択してください。"), タイトル: discord.Option(str, "認証パネルのタイトルを入力してください。"), メッセージ: discord.Option(str, "認証パネルに表示するメッセージを入力してください。")):
  if ctx.author.guild_permissions.manage_roles:
    await ctx.respond(embed=discord.Embed(title=タイトル, description=メッセージ, color=0xadb8cb).set_footer(text=ロール.id).set_thumbnail(url="https://i.ibb.co/2ypgMfW/Polish-20230519-223024918.png"), view=VerifyButton())
  else:
    await ctx.respond(embed=discord.Embed(title="<:error:1112400450101186622>｜エラー", description="認証パネルを作成するには`ロール管理`の権限が必要です。", color=0xff0000), ephemeral=True)

@bot.command(name="shorten", description="短縮URLを作成します。")
async def shorten(ctx: discord.ApplicationContext, url: discord.Option(str, "短縮するURLを入力してください。")):
  response = requests.get(f"https://is.gd/create.php?format=json&url={url}")
  try:
    shortened_url = response.json()["shorturl"]
    await ctx.respond(embed=discord.Embed(title="短縮URL", description=f"<:check:1112400403850600468> » 短縮URLを作成しました。\n{shortened_url}", color=0xadb8cb))
  except:
    await ctx.respond(embed=discord.Embed(title="<:error:1112400450101186622>｜エラー", description="URLを入力してください。", color=0xff0000), ephemeral=True)

@bot.command(name="weather", description="天気予報を表示します。")
async def weather(ctx: discord.ApplicationContext, 地域: discord.Option(str, "地域を選択してください。", choices=["東京", "神奈川 / 横浜", "大阪", "愛知 / 名古屋", "埼玉 / さいたま", "千葉", "兵庫 / 神戸", "北海道 / 札幌", "福岡", "静岡", "茨城 / 水戸", "広島", "京都", "宮城 / 仙台"])):
  if 地域 == "東京":
    response = requests.get("https://weather.tsukumijima.net/api/forecast/city/130010")
    today_weather = response.json()["forecasts"][0]["telop"]
    today_temperature_min = response.json()["forecasts"][0]["temperature"]["min"]["celsius"]
    today_temperature_max = response.json()["forecasts"][0]["temperature"]["max"]["celsius"]
    tomorrow_weather = response.json()["forecasts"][1]["telop"]
    tomorrow_temperature_min = response.json()["forecasts"][1]["temperature"]["min"]["celsius"]
    tomorrow_temperature_max = response.json()["forecasts"][1]["temperature"]["max"]["celsius"]
    await ctx.respond(embed=discord.Embed(title="<:weather:1112400730498793482>｜天気予報", description=f"東京の天気予報です。\n\n**今日**\n{str(today_weather)}\n最高気温{str(today_temperature_max)}℃\n最低気温{str(today_temperature_min)}℃\n\n**明日**\n{str(tomorrow_weather)}\n最高気温{str(tomorrow_temperature_max)}℃\n最低気温{str(tomorrow_temperature_min)}℃", color=0xadb8cb).set_thumbnail(url="https://i.ibb.co/xjj4sm6/Polish-20230520-144515175.png"), ephemeral=True)
  if 地域 == "神奈川 / 横浜":
    response = requests.get("https://weather.tsukumijima.net/api/forecast/city/140010")
    today_weather = response.json()["forecasts"][0]["telop"]
    today_temperature_min = response.json()["forecasts"][0]["temperature"]["min"]["celsius"]
    today_temperature_max = response.json()["forecasts"][0]["temperature"]["max"]["celsius"]
    tomorrow_weather = response.json()["forecasts"][1]["telop"]
    tomorrow_temperature_min = response.json()["forecasts"][1]["temperature"]["min"]["celsius"]
    tomorrow_temperature_max = response.json()["forecasts"][1]["temperature"]["max"]["celsius"]
    await ctx.respond(embed=discord.Embed(title="<:weather:1112400730498793482>｜天気予報", description=f"神奈川 / 横浜の天気予報です。\n\n**今日**\n{str(today_weather)}\n最高気温{str(today_temperature_max)}℃\n最低気温{str(today_temperature_min)}℃\n\n**明日**\n{str(tomorrow_weather)}\n最高気温{str(tomorrow_temperature_max)}℃\n最低気温{str(tomorrow_temperature_min)}℃", color=0xadb8cb).set_thumbnail(url="https://i.ibb.co/xjj4sm6/Polish-20230520-144515175.png"), ephemeral=True)
  if 地域 == "大阪":
    response = requests.get("https://weather.tsukumijima.net/api/forecast/city/270000")
    today_weather = response.json()["forecasts"][0]["telop"]
    today_temperature_min = response.json()["forecasts"][0]["temperature"]["min"]["celsius"]
    today_temperature_max = response.json()["forecasts"][0]["temperature"]["max"]["celsius"]
    tomorrow_weather = response.json()["forecasts"][1]["telop"]
    tomorrow_temperature_min = response.json()["forecasts"][1]["temperature"]["min"]["celsius"]
    tomorrow_temperature_max = response.json()["forecasts"][1]["temperature"]["max"]["celsius"]
    await ctx.respond(embed=discord.Embed(title="<:weather:1112400730498793482>｜天気予報", description=f"大阪の天気予報です。\n\n**今日**\n{str(today_weather)}\n最高気温{str(today_temperature_max)}℃\n最低気温{str(today_temperature_min)}℃\n\n**明日**\n{str(tomorrow_weather)}\n最高気温{str(tomorrow_temperature_max)}℃\n最低気温{str(tomorrow_temperature_min)}℃", color=0xadb8cb).set_thumbnail(url="https://i.ibb.co/xjj4sm6/Polish-20230520-144515175.png"), ephemeral=True)
  if 地域 == "愛知 / 名古屋":
    response = requests.get("https://weather.tsukumijima.net/api/forecast/city/230010")
    today_weather = response.json()["forecasts"][0]["telop"]
    today_temperature_min = response.json()["forecasts"][0]["temperature"]["min"]["celsius"]
    today_temperature_max = response.json()["forecasts"][0]["temperature"]["max"]["celsius"]
    tomorrow_weather = response.json()["forecasts"][1]["telop"]
    tomorrow_temperature_min = response.json()["forecasts"][1]["temperature"]["min"]["celsius"]
    tomorrow_temperature_max = response.json()["forecasts"][1]["temperature"]["max"]["celsius"]
    await ctx.respond(embed=discord.Embed(title="<:weather:1112400730498793482>｜天気予報", description=f"愛知 / 名古屋の天気予報です。\n\n**今日**\n{str(today_weather)}\n最高気温{str(today_temperature_max)}℃\n最低気温{str(today_temperature_min)}℃\n\n**明日**\n{str(tomorrow_weather)}\n最高気温{str(tomorrow_temperature_max)}℃\n最低気温{str(tomorrow_temperature_min)}℃", color=0xadb8cb).set_thumbnail(url="https://i.ibb.co/xjj4sm6/Polish-20230520-144515175.png"), ephemeral=True)
  if 地域 == "埼玉 / さいたま":
    response = requests.get("https://weather.tsukumijima.net/api/forecast/city/110010")
    today_weather = response.json()["forecasts"][0]["telop"]
    today_temperature_min = response.json()["forecasts"][0]["temperature"]["min"]["celsius"]
    today_temperature_max = response.json()["forecasts"][0]["temperature"]["max"]["celsius"]
    tomorrow_weather = response.json()["forecasts"][1]["telop"]
    tomorrow_temperature_min = response.json()["forecasts"][1]["temperature"]["min"]["celsius"]
    tomorrow_temperature_max = response.json()["forecasts"][1]["temperature"]["max"]["celsius"]
    await ctx.respond(embed=discord.Embed(title="<:weather:1112400730498793482>｜天気予報", description=f"埼玉 / さいたまの天気予報です。\n\n**今日**\n{str(today_weather)}\n最高気温{str(today_temperature_max)}℃\n最低気温{str(today_temperature_min)}℃\n\n**明日**\n{str(tomorrow_weather)}\n最高気温{str(tomorrow_temperature_max)}℃\n最低気温{str(tomorrow_temperature_min)}℃", color=0xadb8cb).set_thumbnail(url="https://i.ibb.co/xjj4sm6/Polish-20230520-144515175.png"), ephemeral=True)
  if 地域 == "千葉":
    response = requests.get("https://weather.tsukumijima.net/api/forecast/city/120010")
    today_weather = response.json()["forecasts"][0]["telop"]
    today_temperature_min = response.json()["forecasts"][0]["temperature"]["min"]["celsius"]
    today_temperature_max = response.json()["forecasts"][0]["temperature"]["max"]["celsius"]
    tomorrow_weather = response.json()["forecasts"][1]["telop"]
    tomorrow_temperature_min = response.json()["forecasts"][1]["temperature"]["min"]["celsius"]
    tomorrow_temperature_max = response.json()["forecasts"][1]["temperature"]["max"]["celsius"]
    await ctx.respond(embed=discord.Embed(title="<:weather:1112400730498793482>｜天気予報", description=f"千葉の天気予報です。\n\n**今日**\n{str(today_weather)}\n最高気温{str(today_temperature_max)}℃\n最低気温{str(today_temperature_min)}℃\n\n**明日**\n{str(tomorrow_weather)}\n最高気温{str(tomorrow_temperature_max)}℃\n最低気温{str(tomorrow_temperature_min)}℃", color=0xadb8cb).set_thumbnail(url="https://i.ibb.co/xjj4sm6/Polish-20230520-144515175.png"), ephemeral=True)
  if 地域 == "兵庫 / 神戸":
    response = requests.get("https://weather.tsukumijima.net/api/forecast/city/280010")
    today_weather = response.json()["forecasts"][0]["telop"]
    today_temperature_min = response.json()["forecasts"][0]["temperature"]["min"]["celsius"]
    today_temperature_max = response.json()["forecasts"][0]["temperature"]["max"]["celsius"]
    tomorrow_weather = response.json()["forecasts"][1]["telop"]
    tomorrow_temperature_min = response.json()["forecasts"][1]["temperature"]["min"]["celsius"]
    tomorrow_temperature_max = response.json()["forecasts"][1]["temperature"]["max"]["celsius"]
    await ctx.respond(embed=discord.Embed(title="<:weather:1112400730498793482>｜天気予報", description=f"兵庫 / 神戸の天気予報です。\n\n**今日**\n{str(today_weather)}\n最高気温{str(today_temperature_max)}℃\n最低気温{str(today_temperature_min)}℃\n\n**明日**\n{str(tomorrow_weather)}\n最高気温{str(tomorrow_temperature_max)}℃\n最低気温{str(tomorrow_temperature_min)}℃", color=0xadb8cb).set_thumbnail(url="https://i.ibb.co/xjj4sm6/Polish-20230520-144515175.png"), ephemeral=True)
  if 地域 == "北海道 / 札幌":
    response = requests.get("https://weather.tsukumijima.net/api/forecast/city/016010")
    today_weather = response.json()["forecasts"][0]["telop"]
    today_temperature_min = response.json()["forecasts"][0]["temperature"]["min"]["celsius"]
    today_temperature_max = response.json()["forecasts"][0]["temperature"]["max"]["celsius"]
    tomorrow_weather = response.json()["forecasts"][1]["telop"]
    tomorrow_temperature_min = response.json()["forecasts"][1]["temperature"]["min"]["celsius"]
    tomorrow_temperature_max = response.json()["forecasts"][1]["temperature"]["max"]["celsius"]
    await ctx.respond(embed=discord.Embed(title="<:weather:1112400730498793482>｜天気予報", description=f"北海道 / 札幌の天気予報です。\n\n**今日**\n{str(today_weather)}\n最高気温{str(today_temperature_max)}℃\n最低気温{str(today_temperature_min)}℃\n\n**明日**\n{str(tomorrow_weather)}\n最高気温{str(tomorrow_temperature_max)}℃\n最低気温{str(tomorrow_temperature_min)}℃", color=0xadb8cb).set_thumbnail(url="https://i.ibb.co/xjj4sm6/Polish-20230520-144515175.png"), ephemeral=True)
  if 地域 == "福岡":
    response = requests.get("https://weather.tsukumijima.net/api/forecast/city/400010")
    today_weather = response.json()["forecasts"][0]["telop"]
    today_temperature_min = response.json()["forecasts"][0]["temperature"]["min"]["celsius"]
    today_temperature_max = response.json()["forecasts"][0]["temperature"]["max"]["celsius"]
    tomorrow_weather = response.json()["forecasts"][1]["telop"]
    tomorrow_temperature_min = response.json()["forecasts"][1]["temperature"]["min"]["celsius"]
    tomorrow_temperature_max = response.json()["forecasts"][1]["temperature"]["max"]["celsius"]
    await ctx.respond(embed=discord.Embed(title="<:weather:1112400730498793482>｜天気予報", description=f"福岡の天気予報です。\n\n**今日**\n{str(today_weather)}\n最高気温{str(today_temperature_max)}℃\n最低気温{str(today_temperature_min)}℃\n\n**明日**\n{str(tomorrow_weather)}\n最高気温{str(tomorrow_temperature_max)}℃\n最低気温{str(tomorrow_temperature_min)}℃", color=0xadb8cb).set_thumbnail(url="https://i.ibb.co/xjj4sm6/Polish-20230520-144515175.png"), ephemeral=True)
  if 地域 == "静岡":
    response = requests.get("https://weather.tsukumijima.net/api/forecast/city/220010")
    today_weather = response.json()["forecasts"][0]["telop"]
    today_temperature_min = response.json()["forecasts"][0]["temperature"]["min"]["celsius"]
    today_temperature_max = response.json()["forecasts"][0]["temperature"]["max"]["celsius"]
    tomorrow_weather = response.json()["forecasts"][1]["telop"]
    tomorrow_temperature_min = response.json()["forecasts"][1]["temperature"]["min"]["celsius"]
    tomorrow_temperature_max = response.json()["forecasts"][1]["temperature"]["max"]["celsius"]
    await ctx.respond(embed=discord.Embed(title="<:weather:1112400730498793482>｜天気予報", description=f"静岡の天気予報です。\n\n**今日**\n{str(today_weather)}\n最高気温{str(today_temperature_max)}℃\n最低気温{str(today_temperature_min)}℃\n\n**明日**\n{str(tomorrow_weather)}\n最高気温{str(tomorrow_temperature_max)}℃\n最低気温{str(tomorrow_temperature_min)}℃", color=0xadb8cb).set_thumbnail(url="https://i.ibb.co/xjj4sm6/Polish-20230520-144515175.png"), ephemeral=True)
  if 地域 == "茨城 / 水戸":
    response = requests.get("https://weather.tsukumijima.net/api/forecast/city/080010")
    today_weather = response.json()["forecasts"][0]["telop"]
    today_temperature_min = response.json()["forecasts"][0]["temperature"]["min"]["celsius"]
    today_temperature_max = response.json()["forecasts"][0]["temperature"]["max"]["celsius"]
    tomorrow_weather = response.json()["forecasts"][1]["telop"]
    tomorrow_temperature_min = response.json()["forecasts"][1]["temperature"]["min"]["celsius"]
    tomorrow_temperature_max = response.json()["forecasts"][1]["temperature"]["max"]["celsius"]
    await ctx.respond(embed=discord.Embed(title="<:weather:1112400730498793482>｜天気予報", description=f"茨城 / 水戸の天気予報です。\n\n**今日**\n{str(today_weather)}\n最高気温{str(today_temperature_max)}℃\n最低気温{str(today_temperature_min)}℃\n\n**明日**\n{str(tomorrow_weather)}\n最高気温{str(tomorrow_temperature_max)}℃\n最低気温{str(tomorrow_temperature_min)}℃", color=0xadb8cb).set_thumbnail(url="https://i.ibb.co/xjj4sm6/Polish-20230520-144515175.png"), ephemeral=True)
  if 地域 == "広島":
    response = requests.get("https://weather.tsukumijima.net/api/forecast/city/340010")
    today_weather = response.json()["forecasts"][0]["telop"]
    today_temperature_min = response.json()["forecasts"][0]["temperature"]["min"]["celsius"]
    today_temperature_max = response.json()["forecasts"][0]["temperature"]["max"]["celsius"]
    tomorrow_weather = response.json()["forecasts"][1]["telop"]
    tomorrow_temperature_min = response.json()["forecasts"][1]["temperature"]["min"]["celsius"]
    tomorrow_temperature_max = response.json()["forecasts"][1]["temperature"]["max"]["celsius"]
    await ctx.respond(embed=discord.Embed(title="<:weather:1112400730498793482>｜天気予報", description=f"広島の天気予報です。\n\n**今日**\n{str(today_weather)}\n最高気温{str(today_temperature_max)}℃\n最低気温{str(today_temperature_min)}℃\n\n**明日**\n{str(tomorrow_weather)}\n最高気温{str(tomorrow_temperature_max)}℃\n最低気温{str(tomorrow_temperature_min)}℃", color=0xadb8cb).set_thumbnail(url="https://i.ibb.co/xjj4sm6/Polish-20230520-144515175.png"), ephemeral=True)
  if 地域 == "京都":
    response = requests.get("https://weather.tsukumijima.net/api/forecast/city/260010")
    today_weather = response.json()["forecasts"][0]["telop"]
    today_temperature_min = response.json()["forecasts"][0]["temperature"]["min"]["celsius"]
    today_temperature_max = response.json()["forecasts"][0]["temperature"]["max"]["celsius"]
    tomorrow_weather = response.json()["forecasts"][1]["telop"]
    tomorrow_temperature_min = response.json()["forecasts"][1]["temperature"]["min"]["celsius"]
    tomorrow_temperature_max = response.json()["forecasts"][1]["temperature"]["max"]["celsius"]
    await ctx.respond(embed=discord.Embed(title="<:weather:1112400730498793482>｜天気予報", description=f"京都の天気予報です。\n\n**今日**\n{str(today_weather)}\n最高気温{str(today_temperature_max)}℃\n最低気温{str(today_temperature_min)}℃\n\n**明日**\n{str(tomorrow_weather)}\n最高気温{str(tomorrow_temperature_max)}℃\n最低気温{str(tomorrow_temperature_min)}℃", color=0xadb8cb).set_thumbnail(url="https://i.ibb.co/xjj4sm6/Polish-20230520-144515175.png"), ephemeral=True)
  if 地域 == "宮城 / 仙台":
    response = requests.get("https://weather.tsukumijima.net/api/forecast/city/040010")
    today_weather = response.json()["forecasts"][0]["telop"]
    today_temperature_min = response.json()["forecasts"][0]["temperature"]["min"]["celsius"]
    today_temperature_max = response.json()["forecasts"][0]["temperature"]["max"]["celsius"]
    tomorrow_weather = response.json()["forecasts"][1]["telop"]
    tomorrow_temperature_min = response.json()["forecasts"][1]["temperature"]["min"]["celsius"]
    tomorrow_temperature_max = response.json()["forecasts"][1]["temperature"]["max"]["celsius"]
    await ctx.respond(embed=discord.Embed(title="<:weather:1112400730498793482>｜天気予報", description=f"宮城 / 仙台の天気予報です。\n\n**今日**\n{str(today_weather)}\n最高気温{str(today_temperature_max)}℃\n最低気温{str(today_temperature_min)}℃\n\n**明日**\n{str(tomorrow_weather)}\n最高気温{str(tomorrow_temperature_max)}℃\n最低気温{str(tomorrow_temperature_min)}℃", color=0xadb8cb).set_thumbnail(url="https://i.ibb.co/xjj4sm6/Polish-20230520-144515175.png"), ephemeral=True)

@bot.command(name="clear", description="メッセージを一括削除します。")
async def clear(ctx: discord.ApplicationContext, 数: discord.Option(int, "削除する数を入力してください。"), メンバー: discord.Option(discord.Member, "対象のメンバーを指定してください。", required=False)):
  if ctx.author.guild_permissions.manage_messages:
    if メンバー == None:
      await ctx.respond(embed=discord.Embed(title="clear", description="<:check:1112400403850600468> » メッセージを一括削除しました。", color=0xadb8cb), ephemeral=True)
      await ctx.channel.purge(limit=数)
    else:
      await ctx.respond(embed=discord.Embed(title="clear", description="<:check:1112400403850600468> » メッセージを一括削除しました。", color=0xadb8cb), ephemeral=True)
      await ctx.channel.purge(limit=数, check=lambda message: message.author == メンバー)
  else:
    await ctx.respond(embed=discord.Embed(title="エラー", description="メッセージの一括削除を行うには`メッセージ管理`の権限が必要です。", color=0xff0000), ephemeral=True)

@bot.command(name="top", description="チャンネルの１番上に飛ぶボタンを配置します。")
async def top(ctx: discord.ApplicationContext, ラベル: discord.Option(str, "ボタンに表示するテキストを入力してください。")):
  msg = [message async for message in ctx.channel.history(limit=1, oldest_first=True)]
  msg_link = msg[0].jump_url
  class TopButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        button = discord.ui.Button(label=ラベル, style=discord.ButtonStyle.url, url=msg_link)
        self.add_item(button)
  await ctx.respond(view=TopButton())

@bot.command(name="avatar", description="指定したユーザーのアイコンを取得します。")
async def avatar(ctx: discord.ApplicationContext, ユーザー: discord.Option(discord.Member, "ユーザーを指定してください。")):
  await ctx.respond(embed=discord.Embed(title=f"{ユーザー.mention}のアイコン", color=0xadb8cb).set_image(url=ユーザー.avatar.url))

@bot.command(name="python", description="pythonのコードを実行します。")
async def python(ctx: discord.ApplicationContext, コード: discord.Option(str, "実行するコードを入力してください。")):
  if "import os" in コード or "import sys" in コード or "from os" in コード or "from sys" in コード:
    return await ctx.respond(embed=discord.Embed(title="エラー", description="`os`と`sys`はインポートできません。", color=0xff0000), ephemeral=True)
  if "open" in コード:
    return await ctx.respond(embed=discord.Embed(title="エラー", description="ファイルの操作はできません。", color=0xff0000), ephemeral=True)
  with open("./temp.py", "w") as f:
    f.write(コード)
  result = subprocess.run(["python", "temp.py"], capture_output=True, text=True)
  await ctx.respond(embed=discord.Embed(title="python", description=f"**コード**```python\n{コード}```\n\n**出力**```{result.stdout}\n{result.stderr}```", color=0xadb8cb))
  os.remove("./temp.py")

@bot.listen("on_message")
async def on_message(message):
  if re.search(r"https://discord.com/channels/[0-9]+/[0-9]+/[0-9]+", message.content):
    try:
      msg_link = re.findall("https://discord.com/channels/[0-9]+/[0-9]+/[0-9]+", message.content)[0]
      channel_id = int(msg_link.split("/")[5])
      channel = message.guild.get_channel(channel_id)
      msg_id = int(msg_link.split("/")[6])
      msg = await channel.fetch_message(msg_id)
      class JumpButton(discord.ui.View):
        def __init__(self):
          super().__init__(timeout=None)
          button = discord.ui.Button(label="メッセージに飛ぶ", style=discord.ButtonStyle.url, url=msg_link)
          self.add_item(button)
      await message.channel.send(embed=discord.Embed(title=f"#{channel.name} でのメッセージ", description=msg.content, color=0xadb8cb).set_author(name=msg.author.name, icon_url=msg.author.avatar.url), view=JumpButton())
    except:
      return

@bot.event
async def on_reaction_add(reaction, user):
    if reaction.emoji == "🇯🇵":
      response = requests.get(f"https://script.google.com/macros/s/AKfycbwDZ5mESQpMLLT-efxT0oyXn69n7q_ZzTzD4orm3l640QmtNTR_QlP4PWfQMGrgr9k0sA/exec?text={reaction.message.content}&target=ja").text
      class TRJumpButton(discord.ui.View):
        def __init__(self):
          super().__init__(timeout=None)
          button = discord.ui.Button(label="メッセージに飛ぶ", style=discord.ButtonStyle.url, url=reaction.message.jump_url)
          self.add_item(button)
      await reaction.message.channel.send(embed=discord.Embed(title="<:translate:1112400678552342579>｜翻訳", description=f"🇯🇵 » {response}", color=0xadb8cb).set_author(name=reaction.message.author.name, icon_url=reaction.message.author.avatar.url).set_thumbnail(url="https://i.ibb.co/hLmZYFB/Image-Titan-2023-05-20-15-31-24.png"), view=TRJumpButton())

@bot.command(name="setup", description="サーバーセットアップを行います。")
async def setup(ctx: discord.ApplicationContext):
  if ctx.author == ctx.guild.owner:
    await ctx.respond(embed=discord.Embed(title="サーバーセットアップ", description="サーバーセットアップでは、毎回する初期設定を一括で行うことができます。\n━━━━━━━━━━\n▪everyone/hereへのメンションの無効化\n▪永久招待リンクの作成\n▪メインチャンネル(ルールなど)の作成\n▪認証パネル、お問い合わせパネルの配置\n▪メインロール(メンバーなど)の作成\n━━━━━━━━━━\nサーバーセットアップを行いますか？\n行う場合は下の✅ボタンを押してください。**\nこの操作は取り消せません。**", color=0xadb8cb), ephemeral=True, view=SetupButton())
  else:
    await ctx.respond(embed=discord.Embed(title="<:error:1112400450101186622>｜エラー", description="サーバーセットアップはサーバーの所有者のみ行えます。", color=0xff0000), ephemeral=True)

@bot.command(name="log", description="ログチャンネルを設定します。")
async def log(ctx: discord.ApplicationContext, 対象: discord.Option(str, "ログする対象を選択してください。", choices=["メッセージ削除", "メッセージ編集", "参加/退出"]), チャンネル: discord.Option(discord.TextChannel, "ログを送信するチャンネルを選択してください。")):
  if ctx.author.guild_permissions.manage_channels:
    if 対象 == "メッセージ削除":
      await チャンネル.edit(topic=f"{チャンネル.topic}\n\n< message-delete-log >".replace("None", ""))
      await ctx.respond(embed=discord.Embed(title="ログ", description="<:check:1112400403850600468> » メッセージ削除ログチャンネルを設定しました。", color=0xadb8cb))
    if 対象 == "メッセージ編集":
      await チャンネル.edit(topic=f"{チャンネル.topic}\n\n< message-edit-log >".replace("None", ""))
      await ctx.respond(embed=discord.Embed(title="ログ", description="<:check:1112400403850600468> » メッセージ編集ログチャンネルを設定しました。", color=0xadb8cb))
    if 対象 == "参加/退出":
      await チャンネル.edit(topic=f"{チャンネル.topic}\n\n< join-leave-log >".replace("None", ""))
      await ctx.respond(embed=discord.Embed(title="ログ", description="<:check:1112400403850600468> » 参加/退出ログチャンネルを設定しました。", color=0xadb8cb))
  else:
    await ctx.respond(embed=discord.Embed(title="<:error:1112400450101186622>｜エラー", description="ログチャンネルを設定するには`チャンネル管理`の権限が必要です。", color=0xff0000), ephemeral=True)

@bot.event
async def on_message_delete(message):
  for channel in message.guild.text_channels:
    if channel.topic != None:
      if "< message-delete-log >" in channel.topic:
        await channel.send(embed=discord.Embed(title="メッセージ削除ログ", description=f"{message.content}", color=0xadb8cb).set_author(name=message.author.name, icon_url=message.author.avatar.url))

@bot.event
async def on_message_edit(message_before, message_after):
  for channel in message_before.guild.text_channels:
    if channel.topic != None:
      if "< message-edit-log >" in channel.topic:
        await channel.send(embed=discord.Embed(title="メッセージ編集ログ", description=f"```{message_before.content}```⇩```{message_after.content}```", color=0xadb8cb).set_author(name=message_before.author.name, icon_url=message_before.author.avatar.url))

@bot.event
async def on_member_join(member):
  for channel in member.guild.text_channels:
    if channel.topic != None:
      if "< join-leave-log >" in channel.topic:
        await channel.send(embed=discord.Embed(title="参加ログ", description=f"{member.name}#{member.discriminator}が参加しました。", color=0xadb8cb).set_thumbnail(url=member.avatar.url))

@bot.event
async def on_member_remove(member):
  for channel in member.guild.text_channels:
    if channel.topic != None:
      if "< join-leave-log >" in channel.topic:
        await channel.send(embed=discord.Embed(title="退出ログ", description=f"{member.name}#{member.discriminator}が退出しました。", color=0xadb8cb).set_thumbnail(url=member.avatar.url))

@bot.command(name="alarm", description="アラームをセットします。")
async def alarm(ctx: discord.ApplicationContext, 時間: discord.Option(str, "アラームをセットする時間を入力してください。（30s=30秒後、5m=5分後）")):
  if 時間.endswith("s"):
    second = int(時間[:-1])
  elif 時間.endswith("m"):
    second = int(時間[:-1]) * 60
  else:
    return await ctx.respond(embed=discord.Embed(title="<:error:1112400450101186622>｜エラー", description="時間を正しく入力してください。", color=0xff0000), ephemeral=True)
  
  if second > 600:
    return await ctx.respond(embed=discord.Embed(title="<:error:1112400450101186622>｜エラー", description="セットできる時間は最大10分後です。", color=0xff0000), ephemeral=True)

  await ctx.respond(embed=discord.Embed(title="<:alarm:1112400780918542397>｜アラーム", description=f"アラームを{second}秒後に設定しました。", color=0xadb8cb).set_thumbnail(url="https://i.ibb.co/WKDWCx5/3d-alarm.png"))
  await asyncio.sleep(second)
  await ctx.channel.send(f"{ctx.author.mention}", embed=discord.Embed(title="<:alarm:1112400780918542397>｜アラーム", description=f"設定した時間になりました。", color=0xadb8cb).set_thumbnail(url="https://i.ibb.co/WKDWCx5/3d-alarm.png"))

@bot.command(name="welcome", description="入室メッセージを設定します。")
async def welcome(ctx: discord.ApplicationContext, メッセージ: discord.Option(str, "送信するメッセージを入力してください。\n（例：{member}さん、よろしく！）"), チャンネル: discord.Option(discord.TextChannel, "メッセージを送信するチャンネルを選択してください。")):
  if ctx.author.guild_permissions.manage_channels:
    await チャンネル.edit(topic=f"{チャンネル.topic}\n\n< welcome-ch >\n{メッセージ}".replace("None", ""))
    await ctx.respond(embed=discord.Embed(title="入室メッセージ", description="<:check:1112400403850600468> » 入室メッセージの設定が完了しました。", color=0xadb8cb))
  else:
    await ctx.respond(embed=discord.Embed(title="<:error:1112400450101186622>｜エラー", description="入室メッセージを設定するには`チャンネル管理`の権限が必要です。", color=0xff0000), ephemeral=True)

@bot.event
async def on_member_join(member):
  for channel in member.guild.text_channels:
    if channel.topic != None:
      if "< welcome-ch >" in channel.topic:
        await channel.send(f"{channel.topic.split('< welcome-ch >')[1]}".replace("{member}", f"{member.mention}"))

@bot.command(name="miq", description="Make it a Quoteを生成します。")
async def miq(ctx: discord.ApplicationContext, メッセージ: discord.Option(str, "対象のメッセージのリンクを入力してください。")):
  message = None
  if re.search(r"https://discord.com/channels/[0-9]+/[0-9]+/[0-9]+", メッセージ):
    try:
      msg_link = re.findall("https://discord.com/channels/[0-9]+/[0-9]+/[0-9]+", メッセージ)[0]
      channel_id = int(msg_link.split("/")[5])
      channel = ctx.guild.get_channel(channel_id)
      msg_id = int(msg_link.split("/")[6])
      msg = await channel.fetch_message(msg_id)
      message = msg
      if message.content == None or message.content == "":
        return await ctx.respond(embed=discord.Embed(title="<:error:1112400450101186622>｜エラー", description="メッセージが空です。\n（画像のみ、embedのみのメッセージは空と判定されます。）", color=0xff0000), ephemeral=True)
    except:
      return await ctx.respond(embed=discord.Embed(title="<:error:1112400450101186622>｜エラー", description="メッセージリンクを指定してください。", color=0xff0000), ephemeral=True)
    respond = await ctx.respond("<:loading:1114471724675764235> » 生成しています...")
    respond_message = await respond.original_message()
    with open("icon.jpeg", "wb") as f:
      f.write(requests.get(message.author.avatar.url).content)
    mestext=""
    if len(message.content) < 20:
      for con in message.content:
        if len(mestext)%10==0 and len(mestext) != 0:
          con+="\n"
        mestext+=con
    elif len(message.content) < 35:
      for con in message.content:
        if len(mestext)%12==0 and len(mestext) != 0:
          con+="\n"
        mestext+=con
    elif len(message.content) < 50:
      for con in message.content:
        if len(mestext)%14==0 and len(mestext) != 0:
          con+="\n"
        mestext+=con
    elif len(message.content) < 70:
      for con in message.content:
        if len(mestext)%18==0 and len(mestext) != 0:
          con+="\n"
        mestext+=con
    else:
      for con in message.content:
        if len(mestext)%21==0 and len(mestext) != 0:
          con+="\n"
        mestext+=con
    icon=Image.open("icon.jpeg")
    haikei=Image.open("grad.png")
    black=Image.open("black.jpeg")
    w,h=(680,370)
    w1,h1=icon.size
    haikei=haikei.resize((w,h))
    haikei=haikei.convert("L")
    black=black.resize((w,h))
    new=Image.new(mode="RGB",size=    (w,h))
    icon=icon.resize((h,h))
    new.paste(icon)
    sa=Image.composite(new,black,haikei)
    draw = ImageDraw.Draw(sa)# im上のImageDrawインスタンスを作る
    if len(mestext) < 20:
      fnt = ImageFont.truetype('font.ttf',30)
    elif len(mestext) < 35:
      fnt = ImageFont.truetype('font.ttf',27)
    elif len(mestext) < 50:
      fnt = ImageFont.truetype('font.ttf',23)
    elif len(mestext) < 70:
      fnt = ImageFont.truetype('font.ttf',21)
    else:
      fnt = ImageFont.truetype('font.ttf',18)
    font = ImageFont.truetype('font.ttf',20)
#ImageFontインスタンスを作る
    draw.text((350,90),mestext,font=fnt,fill='#FFF') #fontを指定
    draw.text((400,270),f"- {message.author.name}#{message.author.discriminator}",font=font,fill="#FFF")
    sa.save("miq.png")
    file = discord.File("miq.png")
    await respond_message.edit(content=f"<:check:1112400403850600468> » \n[元のメッセージ]({メッセージ})", file=file)
    os.remove("./miq.png")
  else:
    await ctx.respond(embed=discord.Embed(title="<:error:1112400450101186622>｜エラー", description="メッセージリンクを指定してください。", color=0xff0000), ephemeral=True)

@bot.message_command(name="Make it a Quote")
async def miq_context(ctx, message: discord.Message):
    if message.content == None or message.content == "":
      return await ctx.respond(embed=discord.Embed(title="<:error:1112400450101186622>｜エラー", description="メッセージが空です。\n（画像のみ、embedのみのメッセージは空と判定されます。）", color=0xff0000), ephemeral=True)
    respond = await ctx.respond("<:loading:1114471724675764235> » 生成しています...")
    respond_message = await respond.original_message()
    with open("icon.jpeg", "wb") as f:
      f.write(requests.get(message.author.avatar.url).content)
    mestext=""
    if len(message.content) < 20:
      for con in message.content:
        if len(mestext)%10==0 and len(mestext) != 0:
          con+="\n"
        mestext+=con
    elif len(message.content) < 35:
      for con in message.content:
        if len(mestext)%12==0 and len(mestext) != 0:
          con+="\n"
        mestext+=con
    elif len(message.content) < 50:
      for con in message.content:
        if len(mestext)%14==0 and len(mestext) != 0:
          con+="\n"
        mestext+=con
    elif len(message.content) < 70:
      for con in message.content:
        if len(mestext)%18==0 and len(mestext) != 0:
          con+="\n"
        mestext+=con
    else:
      for con in message.content:
        if len(mestext)%21==0 and len(mestext) != 0:
          con+="\n"
        mestext+=con
    icon=Image.open("icon.jpeg")
    haikei=Image.open("grad.png")
    black=Image.open("black.jpeg")
    w,h=(680,370)
    w1,h1=icon.size
    haikei=haikei.resize((w,h))
    haikei=haikei.convert("L")
    black=black.resize((w,h))
    new=Image.new(mode="RGB",size=    (w,h))
    icon=icon.resize((h,h))
    new.paste(icon)
    sa=Image.composite(new,black,haikei)
    draw = ImageDraw.Draw(sa)# im上のImageDrawインスタンスを作る
    if len(mestext) < 20:
      fnt = ImageFont.truetype('font.ttf',30)
    elif len(mestext) < 35:
      fnt = ImageFont.truetype('font.ttf',27)
    elif len(mestext) < 50:
      fnt = ImageFont.truetype('font.ttf',23)
    elif len(mestext) < 70:
      fnt = ImageFont.truetype('font.ttf',21)
    else:
      fnt = ImageFont.truetype('font.ttf',17)
    font = ImageFont.truetype('font.ttf',20)
#ImageFontインスタンスを作る
    draw.text((350,90),mestext,font=fnt,fill='#FFF') #fontを指定
    draw.text((400,270),f"- {message.author.name}#{message.author.discriminator}",font=font,fill="#FFF")
    sa.save("miq.png")
    file = discord.File("miq.png")
    await respond_message.edit(content=f"<:check:1112400403850600468> » \n[元のメッセージ]({message.jump_url})", file=file)
    os.remove("./miq.png")

@bot.message_command(name="日本語に翻訳")
async def translate_context(ctx, message: discord.Message):
    response = requests.get(f"https://script.google.com/macros/s/AKfycbwDZ5mESQpMLLT-efxT0oyXn69n7q_ZzTzD4orm3l640QmtNTR_QlP4PWfQMGrgr9k0sA/exec?text={message.content}&target=ja").text
    class TRJumpButton(discord.ui.View):
        def __init__(self):
          super().__init__(timeout=None)
          button = discord.ui.Button(label="メッセージに飛ぶ", style=discord.ButtonStyle.url, url=message.jump_url)
          self.add_item(button)
    await ctx.respond(embed=discord.Embed(title="<:translate:1112400678552342579>｜翻訳", description=f"🇯🇵 » {response}", color=0xadb8cb).set_author(name=message.author.name, icon_url=message.author.avatar.url).set_thumbnail(url="https://i.ibb.co/hLmZYFB/Image-Titan-2023-05-20-15-31-24.png"), view=TRJumpButton())

@bot.command(name="wpoll", description="自由記述式の投票を行います。")
async def wpoll(ctx: discord.ApplicationContext, タイトル: discord.Option(str, "投票のタイトルを入力してください。")):
  await ctx.respond(embed=discord.Embed(title=タイトル, description="", color=0xadb8cb), view=wpollButton())

@bot.event
async def on_application_command_error(ctx: discord.ApplicationContext, error: discord.DiscordException):
  if "Missing Permissions" in str(error):
    await ctx.channel.send(embed=discord.Embed(title="<:error:1112400450101186622>｜エラー", description="botに権限がありません。\n管理者権限をbotに付与してください。", color=0xff0000))
  else:
    await ctx.channel.send(embed=discord.Embed(title="<:error:1112400450101186622>｜エラー", description=f"エラーが発生しました。```{str(error)}```", color=0xff0000))
    log_ch = bot.get_channel(1117476520907243561)
    await log_ch.send("<@730753004738707526>", embed=discord.Embed(title="<:error:1112400450101186622>｜エラー", description=f"/{ctx.command}\n\n```{str(error)}```", color=0xff0000).set_footer(text=f"{ctx.guild.name}｜#{ctx.channel.name}").set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url))

@bot.command(name="memo", description="メモを保存、読み込みします。")
async def memo(ctx: discord.ApplicationContext, 操作: discord.Option(str, "操作を選択してください。", choices=["保存", "読み込み"]), メモ: discord.Option(str, "メモの内容を入力してください。（保存時のみ）", required=False)):
  if 操作 == "保存":
    if メモ == None:
      return await ctx.respond(embed=discord.Embed(title="<:error:1112400450101186622>｜エラー", description="メモの内容を入力してください。", color=0xff0000), ephemeral=True)
    if len(メモ) > 1999:
      return await ctx.respond(embed=discord.Embed(title="<:error:1112400450101186622>｜エラー", description="メモの文字数が多すぎます。", color=0xff0000), ephemeral=True)
    guild = bot.get_guild(1109374064436465684)
    memo_channel = guild.get_channel(1121096053110870058)
    for thread in memo_channel.threads:
      if thread.name == str(ctx.author.id):
        await thread.send(メモ)
        return await ctx.respond(embed=discord.Embed(title="<:memo:1121099972880904203>｜メモ", description="メモを保存しました。", color=0xadb8cb), ephemeral=True)
    thread = await memo_channel.create_thread(name=str(ctx.author.id))
    await thread.send(メモ)
    await ctx.respond(embed=discord.Embed(title="<:memo:1121099972880904203>｜メモ", description="メモを保存しました。", color=0xadb8cb), ephemeral=True)
  if 操作 == "読み込み":
    guild = bot.get_guild(1109374064436465684)
    memo_channel = guild.get_channel(1121096053110870058)
    for thread in memo_channel.threads:
      if thread.name == str(ctx.author.id):
        memo = [mm async for mm in thread.history(limit=1)]
        memotxt = memo[0].content
        return await ctx.respond(embed=discord.Embed(title="<:memo:1121099972880904203>｜メモ", description=f"```{memotxt}```", color=0xadb8cb), ephemeral=True)
    return await ctx.respond(embed=discord.Embed(title="<:error:1112400450101186622>｜エラー", description="メモが保存されていません。", color=0xff0000), ephemeral=True)

bot.run(os.environ['TOKEN'])