import sqlite3
sqlite3.connect = (lambda orig: lambda *a, **kw: orig(*a, **{**kw, 'timeout': 30}))(sqlite3.connect)

import socket
orig_getaddrinfo = socket.getaddrinfo
def getaddrinfo_ipv4_only(host, port, family=0, type=0, proto=0, flags=0):
    return orig_getaddrinfo(host, port, socket.AF_INET, type, proto, flags)
socket.getaddrinfo = getaddrinfo_ipv4_only

import asyncio
import random
import time
from pyrogram import Client, filters, enums

API_ID = 8163218
API_HASH = "045afe51dbc99792313002b5c211b8c5"

BOT_NAME = "🔱ঔৣ𝐑𝐎𝐇𝐈𝐓⃝⚜️𝐂𝐇𝐀𝐔𝐇𝐀𝐍ঔৣI🔱"
OWNER_PROFILE = "https://t.me/itz_rohit_rss"
ALIVE_PHOTO = "https://telegra.ph/file/0c9a6d89280d90d8a5624.jpg"

app = Client("rohit_userbot", api_id=API_ID, api_hash=API_HASH, ipv6=False)

is_afk = False
afk_reason = ""
approved_users = set()
quiz_pending = {}
tag_running = {}

@app.on_message(filters.me, group=-1)
async def auto_unafk_handler(client, message):
    global is_afk
    if is_afk and message.text and not message.text.startswith((".afk", ".unafk")):
        is_afk = False
        try:
            m = await client.send_message(message.chat.id, "🔥 **Master Rohit is Back Online!** 🔱")
            await asyncio.sleep(3)
            await m.delete()
        except Exception:
            pass

@app.on_message(filters.me & filters.command("help", prefixes="."))
async def help_cmd(client, message):
    help_text = f"""
💀 **{BOT_NAME} - COMMAND MENU** 💀

🛡️ **PM Protection:**
• `.a` / `.approve` - Whitelist DM / Bot
• `.da` / `.disapprove` - Block DM / Bot

⚡ **System & Status:**
• `.alive` - Dark royal photo card
• `.ping` - Core speed test
• `.afk [reason]` | `.unafk`

👥 **Group Controls:**
• `.tagall [msg]` - Single user tag
• `.cancel` - Stop tagall instantly
• `.vcinvite` - Admin VC alert

🔥 **Animations & Specials:**
• `.hack` - Terminal hack sequence
• `.spam [count] [text]` - Burst messages (Max 10)
• `.propose` - Fixed shayari with changing emojis
• `.love` - Emoji story animation
• `.kiss` - Romantic kiss animation sequence
• `😡` - Angry rage transition
• `🥲 😭 🥺 💔` - Auto Sad Emoji Transition
• `❤️ 💖 😘 🥰` - Auto Love Emoji Transition
• `.roast` - High-attitude warning

🎭 **Fun & Games:**
• `.toss` | `.dice`
"""
    await message.edit_text(help_text)

@app.on_message(filters.me & filters.command("afk", prefixes="."))
async def set_afk(client, message):
    global is_afk, afk_reason
    is_afk = True
    afk_reason = message.text.split(None, 1)[1] if len(message.command) > 1 else "Busy / Offline"
    await message.edit_text(f"💤 **AFK ENGAGED!**\n💀 Reason: `{afk_reason}`")

@app.on_message(filters.me & filters.command("unafk", prefixes="."))
async def unset_afk(client, message):
    global is_afk
    is_afk = False
    await message.edit_text("🔥 **MASTER ROHIT IS BACK ONLINE!** 🔱")

@app.on_message(filters.me & filters.command("cancel", prefixes="."))
async def cancel_tag(client, message):
    cid = message.chat.id
    if tag_running.get(cid, False):
        tag_running[cid] = False
        await message.edit_text("🛑 **Tagall Process Cancelled!**")
    else:
        await message.edit_text("`Koi tagall process active nahi hai.`")

@app.on_message(filters.me & filters.command("tagall", prefixes="."))
async def tagall_run(client, message):
    cid = message.chat.id
    tag_running[cid] = True
    custom = message.text.split(None, 1)[1] if len(message.command) > 1 else "Active ho jao sabhi!"
    await message.delete()

    async for member in client.get_chat_members(cid):
        if not tag_running.get(cid, False):
            break
        if member.user.is_bot:
            continue
        try:
            await client.send_message(cid, f"📢 {custom}\n👤 {member.user.mention}")
            await asyncio.sleep(1.3)
        except Exception:
            pass
    tag_running[cid] = False

@app.on_message(filters.me & filters.command(["a", "approve"], prefixes="."))
async def approve_pm(client, message):
    cid = message.chat.id
    approved_users.add(cid)
    if cid in quiz_pending:
        del quiz_pending[cid]
    try:
        await client.unblock_user(cid)
    except Exception:
        pass
    await message.edit_text(f"✅ **APPROVED BY MASTER!**\n\nAb baat kar sakte hain! ✨\n🔱 [ROHIT CHAUHAN]({OWNER_PROFILE})")

@app.on_message(filters.me & filters.command(["da", "disapprove"], prefixes="."))
async def disapprove_pm(client, message):
    cid = message.chat.id
    if cid in approved_users:
        approved_users.remove(cid)
    await message.edit_text("⛔ **Disapproved!** Blocked.")
    try:
        await client.block_user(cid)
    except Exception:
        pass

@app.on_message(filters.private & ~filters.me)
async def pm_security_quiz(client, message):
    global is_afk, afk_reason
    if message.from_user and message.from_user.is_bot:
        return

    uid = message.chat.id
    if uid in approved_users:
        if is_afk:
            try:
                await message.reply_text(f"💤 **Master Rohit is AFK!**\nReason: `{afk_reason}`")
            except Exception:
                pass
        return

    if uid not in quiz_pending:
        quiz_pending[uid] = 1
        quiz_card = (
            f"⚠️ **{BOT_NAME} PM SECURITY** ⚠️\n\n"
            f"𝐀𝐚𝐩 𝐦𝐚𝐬𝐭𝐞𝐫 𝐬𝐞 𝐤𝐲𝐮 𝐛𝐚𝐚𝐭 𝐤𝐚𝐫𝐧𝐚 𝐜𝐡𝐚𝐡𝐭𝐞 𝐡𝐚𝐢𝐧 ?\n\n"
            f"𝐎𝐩𝐭𝐢𝐨𝐧𝐬:\n"
            f"𝟏. 𝐝𝐨𝐬𝐭 𝐡𝐨\n"
            f"𝟐. 𝐤𝐚𝐚𝐦 𝐭𝐡𝐚\n"
            f"𝟑. 𝐛𝐚𝐚𝐭 𝐤𝐚𝐫𝐧𝐢 𝐡𝐚𝐢\n"
            f"𝟒. 𝐟𝐢𝐠𝐡𝐭 𝐤𝐚𝐫𝐧𝐢 𝐡𝐚𝐢 😡\n\n"
            f"👉 *Kripya option choose karein.*"
        )
        try:
            await message.reply_text(quiz_card)
        except Exception:
            pass
        return

    ans = message.text.lower() if message.text else ""

    if "4" in ans or "fight" in ans:
        del quiz_pending[uid]
        try:
            await message.reply_text("⚔️ **Aukaat me rehkar baat kar!** Direct BLOCK. 💀")
            await client.block_user(uid)
        except Exception:
            pass
        return

    if any(k in ans for k in ["1", "2", "3", "dost", "kaam", "baat"]):
        del quiz_pending[uid]
        try:
            await message.reply_text("✅ **Verification Received!** Master Rohit ke approve karne ka intezaar karein.")
        except Exception:
            pass
    else:
        del quiz_pending[uid]
        try:
            await message.reply_text("⛔ **FAILED VERIFICATION!** Sahi option choose nahi kiya. Direct BLOCK.")
            await client.block_user(uid)
        except Exception:
            pass

@app.on_message(filters.me & filters.command("alive", prefixes="."))
async def alive_cmd(client, message):
    caption = (
        f"☠️ **[ {BOT_NAME} ]** ☠️\n\n"
        f"⚔️ **Imperial Rule**: Active & Dominating\n"
        f"🩸 **Master Control**: [ROHIT CHAUHAN]({OWNER_PROFILE})\n"
        f"⚡ **System Status**: 100% Lethal Overclocked\n"
        f"🛡️ **Defense Layer**: Kurigram Anti-Ban Active\n\n"
        f"👑 *Jhukte wo hain jinke me dum nahi hota, Rohit wahan khada hota hai jahan faisla hota hai.*"
    )
    chat_id = message.chat.id
    await message.delete()
    try:
        await client.send_photo(chat_id, photo=ALIVE_PHOTO, caption=caption)
    except Exception:
        await client.send_message(chat_id, caption)


# ================= LIVE COMMANDS (ALIVE MATCHED) =================
import asyncio

ANIMATED_FRAMES = [
    ("⚡✨", "✨⚡"),
    ("🔥💫", "💫🔥"),
    ("👑💎", "💎👑"),
    ("🌹💖", "💖🌹"),
    ("🔱✨", "✨🔱")
]

@app.on_message(filters.me & filters.command(["hii", "hello"], prefixes="."))
async def animated_hello_cmd(client, message):
    frames = [
        "👋 <i>H</i>",
        "👋 <i>He</i>",
        "👋 <i>Hel</i>",
        "👋 <i>Hell</i>",
        "👋 <i>Hello!</i> ✨",
        "🌟 <b>Hello Ji! Kaise ho aap sab?</b> 💖",
        "🔱👑 <b>Hello Everyone! Rohit Chauhan is Here!</b> ✨💫"
    ]
    for frame in frames:
        try:
            await message.edit_text(frame)
            await asyncio.sleep(0.7)
        except Exception:
            break

@app.on_message(filters.me & filters.command(["gm", "goodmorning"], prefixes="."))
async def animated_gm_cmd(client, message):
    frames = [
        "🌅 <i>Good</i>",
        "☕ <i>Good Morning...</i>",
        "🌻 <b>Good Morning Ji! Have a wonderful day!</b> ☀️",
        "🔱✨ <b>Suprabhat! A fresh day, full of energy!</b> 🌸👑"
    ]
    for frame in frames:
        try:
            await message.edit_text(frame)
            await asyncio.sleep(0.7)
        except Exception:
            break

@app.on_message(filters.me & filters.command(["gn", "goodnight"], prefixes="."))
async def animated_gn_cmd(client, message):
    frames = [
        "🌙 <i>Good</i>",
        "🌌 <i>Good Night...</i>",
        "✨ <b>Shubh Ratri! Sweet dreams!</b> 😴💤",
        "🔱💫 <b>Good Night! Take rest, meet you tomorrow!</b> 🌟👑"
    ]
    for frame in frames:
        try:
            await message.edit_text(frame)
            await asyncio.sleep(0.7)
        except Exception:
            break

@app.on_message(filters.me & filters.text)
async def dynamic_dot_animator_cmd(client, message):
    txt = message.text or ""
    if txt.startswith(".") and not txt.startswith(".."):
        first_word = txt.split()[0].lower().lstrip(".")
        if first_word in ["alive", "help", "ping", "restart", "repo", "hello", "hii", "gm", "gn", "goodmorning", "goodnight"]:
            return

        body = txt[1:].strip()
        if not body:
            return

        for left, right in ANIMATED_FRAMES:
            try:
                await message.edit_text(f"{left} {body} {right}")
                await asyncio.sleep(0.9)
            except Exception:
                break
        try:
            await message.edit_text(f"🔱✨ {body} ✨🔱")
        except Exception:
            pass
# =================================================================


@app.on_message(filters.me & filters.command("ping", prefixes="."))
async def ping_cmd(client, message):
    start = time.time()
    await message.edit_text("⚡ `Checking speed...`")
    delta_ping = round((time.time() - start) * 1000, 2)
    await message.edit_text(f"🔥 **Core Speed:** `{delta_ping}ms`\n🔱 Master: [ROHIT]({OWNER_PROFILE})")

# 6. VC INVITE, HACK, SPAM & ROAST
@app.on_message(filters.me & filters.command("vcinvite", prefixes="."))
async def vcinvite_cmd(client, message):
    await message.delete()
    chat_id = message.chat.id
    admins = []
    try:
        async for m in client.get_chat_members(chat_id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
            if not m.user.is_bot:
                admins.append(m.user.mention)
        if admins:
            await client.send_message(chat_id, f"🚨 **HIGH PRIORITY VC ALERT** 🚨\n\n{' '.join(admins)}\n\n🔱 By {BOT_NAME}")
    except Exception as e:
        await client.send_message(chat_id, f"`Error: {e}`")

@app.on_message(filters.me & filters.command("hack", prefixes="."))
async def super_hack(client, message):
    target = message.reply_to_message.from_user.first_name if message.reply_to_message else "Target"
    logs = [
        f"💀 [INIT] Locating Telegram UID for `{target}`...",
        "🛰️ [PROXY] Routing traffic via Tor network...",
        "⚡ [EXPLOIT] Zero-day payload injected...",
        "🔓 [FIREWALL] Cloud bypass: 80%",
        f"☠️ [100%] Hacking Complete! `{target}` full device hijacked.",
        f"🔥 Dominator: {BOT_NAME}"
    ]
    for step in logs:
        try:
            await message.edit_text(step)
            await asyncio.sleep(1.1)
        except Exception:
            pass

@app.on_message(filters.me & filters.command("spam", prefixes="."))
async def spam_cmd(client, message):
    args = message.text.split(None, 2)
    if len(args) < 3: return
    count = min(int(args[1]), 10)
    await message.delete()
    for _ in range(count):
        try:
            await client.send_message(message.chat.id, args[2])
            await asyncio.sleep(0.4)
        except Exception:
            pass

@app.on_message(filters.me & filters.command("roast", prefixes="."))
async def royal_roast(client, message):
    target = message.reply_to_message.from_user.mention if message.reply_to_message else "Beta"
    frames = [
        f"Aukaat me reh kar baat karna seekh, {target}... 🤫",
        f"Kyunki Rohit ke sheher me shor nahi, faisle hote hain! ⚡",
        f"Aankhein uthane ki koshish bhi mat karna, seedha aukaat dikha denge. ☠️",
        f"🔥 **WARNING DELIVERED!** Now stay silent. 🤫🔥\n🔱 By {BOT_NAME}"
    ]
    for frame in frames:
        try:
            await message.edit_text(frame)
            await asyncio.sleep(1.0)
        except Exception:
            pass

# 7. PROPOSE (FIXED SHAYARI, CHANGING EMOJIS)
@app.on_message(filters.me & filters.command("propose", prefixes="."))
async def propose_cmd(client, message):
    target = message.reply_to_message.from_user.mention if message.reply_to_message else "Meri Jaan"
    emoji_sets = [
        ("🌹", "✨", "💓", "🌙", "💋", "💍", "❤️"),
        ("💖", "💫", "💘", "🍷", "🥀", "👑", "❤️‍🔥"),
        ("💞", "⭐", "💗", "🕯️", "🌹", "💎", "💖"),
        ("💝", "✨", "💓", "🌸", "💋", "💍", "💘"),
        ("❤️‍🔥", "🌟", "💖", "🍷", "🥀", "👑", "💞"),
        ("🌹", "💫", "💘", "🌙", "💋", "💎", "❤️‍🔥"),
        ("✨🌹", "💫", "❤️‍🔥", "🍷🥀", "💋✨", "👑💍", "❤️‍🔥")
    ]
    for e1, e2, e3, e4, e5, e6, e7 in emoji_sets:
        frame_text = (
            f"{e1} **Meri har ek subah aur har ek shaam aapke naam hai...** {e1}\n\n"
            f"{e2} Aapki ek jhalak se meri har raat rangeen aur din roshan hota hai {e3}\n"
            f"{e4} Sirf chahat nahi, meri rooh ki ibadat ban chuke ho aap {e5}\n"
            f"{e6} Kya ye haseen zindagi ka safar mere sath bitaoge? {e6}\n\n"
            f"**I LOVE YOU SO MUCH, {target}!** {e7}\n\n"
            f"🔱 [ROHIT CHAUHAN]({OWNER_PROFILE})"
        )
        try:
            await message.edit_text(frame_text)
            await asyncio.sleep(0.8)
        except Exception:
            pass

# 8. EMOJI STORY ANIMATION (.love)
@app.on_message(filters.me & filters.command("love", prefixes="."))
async def emoji_love_anim(client, message):
    emoji_frames = [
        "👀 ✨",
        "👩‍❤️‍👨 💫",
        "👩‍❤️‍💋‍👨 🍷",
        "💞 🌹",
        "💍 👑",
        "🤰 ✨",
        "🏥 ⏳",
        "👶 🍼",
        "👨‍👩‍👦 🏡",
        "🎈 🧸 👶",
        "👦 🎒 ⚽",
        "👨‍👩‍👧‍👦 ❤️‍🔥"
    ]
    for frame in emoji_frames:
        try:
            await message.edit_text(frame)
            await asyncio.sleep(0.9)
        except Exception:
            pass

# 9. KISS COMMAND (.kiss)
@app.on_message(filters.me & filters.command("kiss", prefixes="."))
async def kiss_anim(client, message):
    target = message.reply_to_message.from_user.mention if message.reply_to_message else "My Love"
    kiss_frames = [
        f"😘 **Come close...** {target}",
        f"💋 Sending sweet kisses for you... ✨",
        f"👩‍❤️‍💋‍👨 **MUAAAHHH!** ❤️‍🔥",
        f"💋💋💋",
        f"💖 **Always yours, {target}!** 🌹\n🔱 By {BOT_NAME}"
    ]
    for f in kiss_frames:
        try:
            await message.edit_text(f)
            await asyncio.sleep(0.9)
        except Exception:
            pass

# 10. AUTO SAD & LOVE EMOJI TRIGGERS
SAD_EMOJIS = ["🥲", "😭", "🥺", "😖", "😔", "😢", "💔", "😞", "😿", "😣", "☹️", "🙁"]
LOVE_EMOJIS = ["❤️", "💖", "💘", "💓", "💞", "💕", "😘", "🥰", "😍", "💋", "❤️‍🔥", "🌹"]

@app.on_message(filters.me & filters.text)
async def auto_emoji_anim(client, message):
    txt = message.text.strip()
    
    if txt in SAD_EMOJIS:
        sad_sequence = ["🥲", "😔", "😞", "😢", "🥺", "😭", "💔", "🥀"]
        for emo in sad_sequence:
            try:
                await message.edit_text(emo)
                await asyncio.sleep(0.5)
            except Exception:
                pass
        return

    if txt in LOVE_EMOJIS:
        love_sequence = ["❤️", "💖", "💘", "💓", "💞", "💕", "😘", "🥰", "❤️‍🔥", "🌹✨"]
        for emo in love_sequence:
            try:
                await message.edit_text(emo)
                await asyncio.sleep(0.5)
            except Exception:
                pass
        return

    if txt == "😡":
        for emo in ["👿", "🤬", "💀", "🔥", "⚡", "💥", "👹", "☠️"]:
            try:
                await message.edit_text(emo)
                await asyncio.sleep(0.5)
            except Exception:
                pass
        return

# 11. GAMES
@app.on_message(filters.me & filters.command("toss", prefixes="."))
async def toss_cmd(client, message):
    await message.edit_text(f"🪙 Coin: **{random.choice(['Heads 🪙', 'Tails 🪙'])}**")

@app.on_message(filters.me & filters.command("dice", prefixes="."))
async def dice_cmd(client, message):
    await message.edit_text(f"🎲 Dice: **{random.randint(1, 6)}**")

print(f"{BOT_NAME} ALL ADVANCED MODULES READY!")
try:
    import signal
    signal.signal = lambda *args, **kwargs: None
except Exception:
    pass
app.run()


import asyncio

ANIMATED_FRAMES = [
    ("⚡✨", "✨⚡"),
    ("🔥💫", "💫🔥"),
    ("👑💎", "💎👑"),
    ("🌹💖", "💖🌹"),
    ("🔱✨", "✨🔱"),
    ("🌟⚡", "⚡🌟")
]

# 1. Custom Dot Magic Animated Text (Runs for 5 Seconds)
# 1. Guaranteed Dot Magic Animated Text (5 Seconds)
@app.on_message(filters.me & filters.text)
async def dynamic_dot_animator(client, message):
    txt = message.text or ""
    
    # Exclude system commands
    existing_cmds = ["alive", "help", "ping", "restart", "repo", "hello", "hii", "gm", "gn", "goodmorning", "goodnight"]
    parts = txt.split()
    if not parts:
        return
    first_word = parts[0].lower().lstrip(".").lstrip("/")
    if first_word in existing_cmds:
        return

    # Trigger strictly when message starts with a single '.'
    if txt.startswith(".") and not txt.startswith(".."):
        actual_text = txt[1:].strip()
        if not actual_text:
            return

        for i in range(5):
            left, right = ANIMATED_FRAMES[i % len(ANIMATED_FRAMES)]
            try:
                await message.edit_text(f"{left} {actual_text} {right}")
                await asyncio.sleep(0.9)
            except Exception:
                break
        
        try:
            await message.edit_text(f"🔱✨ {actual_text} ✨🔱")
        except Exception:
            pass

@app.on_message(filters.me & filters.command(["hello", "hii"], prefixes=["."]))
async def animated_hello(client, message):
    frames = [
        "👋 <i>H</i>",
        "👋 <i>He</i>",
        "👋 <i>Hel</i>",
        "👋 <i>Hell</i>",
        "👋 <i>Hello!</i> ✨",
        "🌟 <b>Hello Ji! Kaise ho aap sab?</b> 💖",
        "🔱👑 <b>Hello Everyone! Rohit Chauhan is Here!</b> ✨💫"
    ]
    for frame in frames:
        try:
            await message.edit(frame)
            await asyncio.sleep(0.7)
        except Exception:
            break

@app.on_message(filters.me & filters.command(["gm", "goodmorning"], prefixes=["."]))
async def animated_gm(client, message):
    frames = [
        "🌅 <i>G</i>",
        "🌅 <i>Good</i>",
        "🌅 <i>Good Mor</i>",
        "☕ <i>Good Morning...</i>",
        "🌻 <b>Good Morning Ji! Have a wonderful day!</b> ☀️",
        "🔱✨ <b>Suprabhat! A fresh day, full of energy!</b> 🌸👑"
    ]
    for frame in frames:
        try:
            await message.edit(frame)
            await asyncio.sleep(0.7)
        except Exception:
            break

@app.on_message(filters.me & filters.command(["gn", "goodnight"], prefixes=["."]))
async def animated_gn(client, message):
    frames = [
        "🌙 <i>G</i>",
        "🌙 <i>Good</i>",
        "🌙 <i>Good Ni</i>",
        "🌌 <i>Good Night...</i>",
        "✨ <b>Shubh Ratri! Sweet dreams!</b> 😴💤",
        "🔱💫 <b>Good Night! Take rest, meet you tomorrow!</b> 🌟👑"
    ]
    for frame in frames:
        try:
            await message.edit(frame)
            await asyncio.sleep(0.7)
        except Exception:
            break
