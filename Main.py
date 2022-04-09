try:
    from pyrogram import Client, idle
    from pyrogram.types import Message, InlineKeyboardMarkup as inMarkup, InlineKeyboardButton as button
    from pyrogram.filters import edited, command, private, text
    from pyrogram.errors.exceptions.forbidden_403 import RightForbidden
    from pyrogram.errors.exceptions.bad_request_400 import ChatAdminRequired, UserAdminInvalid, UserNotParticipant, UsernameInvalid, UsernameNotOccupied, PeerIdInvalid, BadRequest, UserIsBlocked
except ImportError:
    from os import system
    print("Wait For Install Madules")
    system("python3 -m pip install pyrogram")
    exit("Installed...")
myDict = {} 
from re import match
from dictdb import db; steps = db("steps")
from get_config import get; config = get()
app = Client(session_name="myBot", api_id=config.api_id, api_hash=config.api_hash, bot_token=config.bot_token)
with app: mbot = app.get_me(); botU = mbot.username; botI = mbot.id
# #BUTTONS
mainMenu = inMarkup([
        [button("( افزودن ادمین )", callback_data="addAdmin")],
        [button("( بستن منو )", callback_data="closeMenu")]
        ])
goMain = inMarkup([
        [button("( بستن منو )", callback_data="closeMenu"), button("( منوی اصلی )", callback_data="mainMenu")]
        ])
def check(texts: tuple or list, x):
    for text in texts:
        if text in x:
            return True
    return False
def get_creator(chat_id):
    for admin in app.get_chat_members(chat_id, filter='administrators'):
        if match(r"^creator$", admin.status):
            return admin
def get_my_per(app, chat):
    mymy = app.get_chat_member(chat, 'me')
    text = ""
    if mymy.is_anonymous: text += '`anonymous` - `ناشناس بودن`\n'
    if mymy.can_manage_chat: text += '`can manage chat` - `مدیریت چت`\n'
    if mymy.can_change_info: text += '`can change info` - `تغییر اطلاعات چت`\n'
    if mymy.can_post_messages: text += '`can post messages` - `پست کردن پیام`\n'
    if mymy.can_edit_messages: text += '`can edit messages` - `تغییر  در پست`\n'
    if mymy.can_delete_messages: text += '`can delete messages` - `حذف پست`\n'
    if mymy.can_restrict_members: text += '`can restrict members` - `تغییر قابلیت های اعضا`\n'
    if mymy.can_invite_users: text += '`can invite users` - `دعوت کردن کاربر`\n'
    if mymy.can_pin_messages: text += '`can pin messages` - `سنجاق کردن پست ها`\n'
    if mymy.can_promote_members: text += '`can promote members` - `افزودن ادمین جدید`\n'
    if mymy.can_manage_voice_chats: text += '`can manage voice chats` - `مدیریت ویس چت`\n'
    return text
@app.on_message(edited)
def edited(_, __):
    pass
@app.on_message(private&command(['start']))
def start(app, m: Message):
    steps.set_data(m.chat.id, "Home")
    m.reply("( __**منوی اصلی\nCoder: @Dev_moon**__ )", reply_markup=mainMenu)
@app.on_message(private&text)
def Main(app, m: Message):
    global myDict
    text, chat_id = m.text, m.chat.id
    if steps.data_is(chat_id, "getChatUsernameOrId"):
        try:
            get_user = app.get_chat_member(text, chat_id)
        except UsernameNotOccupied:
            m.reply("__**چت وجود ندارد**__", reply_markup=goMain)
        except ChatAdminRequired:
            m.reply(f"__**من در این چنل ادمین نیستم ( `{text}` )**__", reply_markup=goMain)
        except (UsernameInvalid, PeerIdInvalid):
            m.reply("__**یوزرنیم نادرست است**__", reply_markup=goMain)
        except ValueError:
            m.reply("__**این یوزرنیم برای یک کاربر است**__", reply_markup=goMain)
        else:
            if app.get_chat_member(text, 'me').can_promote_members:
                if match(r"^creator$", get_user.status):
                    steps.set_data(chat_id, "getAdminUsernameOrId"); myDict[str(chat_id)] = text
                    get = app.get_chat(text)
                    cr = get_creator(text, app)
                    m.reply(f'''چت یافت شد!
🎗 اسم چت : `{get.title}`
🎗 شناسه چت : {f"@{get.username}" if get.username else f"`{get.id}`"}
🎗 درباره چت : {get.description if get.description else 'ندارد!'}
🎗 سازنده چت :  {cr.user.mention}
''')
                    m.reply("__**شناسه کاربری که میخوای ادمین کنی رو بفرست (Username/id)**__", reply_markup=goMain)
                else:
                    m.reply("__**شما سازنده این کانال یا گروه نیستید**__", reply_markup=goMain)
                    m.reply("__**به منوی اصلی بازگشتید**__", reply_markup=mainMenu)
                    steps.set_data(chat_id, 'Home')
            else:
                m.reply("__**من نمیتونم کسی رو تو چنلت ادمین کنم**__")
                m.reply("__**به منوی اصلی بازگشتید**__", reply_markup=mainMenu)
                steps.set_data(chat_id, "Home")
    elif steps.data_is(chat_id, "getAdminUsernameOrId"):
        if match(r"^me$", text):
            m.reply('😐'); return
        try:
            get_user = app.get_chat_member(myDict[str(chat_id)], text)
        except UsernameNotOccupied:
            m.reply("__**کاربر وجود ندارد**__", reply_markup=goMain)
        except (UsernameInvalid, PeerIdInvalid):
            m.reply("__**یوزرنیم نادرست است**__", reply_markup=goMain)
        except UserNotParticipant:
            m.reply("__**کاربر در چنل عضو نیست**__", reply_markup=goMain)
        else:
            status = get_user.status
            if match(r"^member$", status) or (get_user.promoted_by.username == botU):
                steps.set_data(chat_id, "setChatAdmin"); myDict[str(chat_id)] = f'{myDict[str(chat_id)]}-{text}'
                m.reply(f"{get_user.user.mention} - `{get_user.user.id}` - `{status}` __**یافت شد !**__")
                m.reply(f"""از قابلیت های زیر کدوم رو میخوای که برای این ادمین بزاری؟
هر کدوم که خواستی رو به صورت خط به خط بفرست

{get_my_per(app, myDict[str(chat_id)].split('-')[0])}""", reply_markup=goMain)
            else:
                m.reply(f"`{text}` - {get_user.user.mention} - `{get_user.user.id}`__** is ( `{status}` )**__", reply_markup=goMain)
    elif steps.data_is(chat_id, 'setChatAdmin'):
        info = myDict[str(chat_id)].split('-')
        try:
            app.promote_chat_member(
chat_id=info[0], 
user_id=info[1],
is_anonymous=check(('anonymous‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍', 'ناشناس بودن'), text),
can_manage_chat=check(('can manage chat', 'مدیریت چت'), text),
can_change_info=check(('can change info', 'تغییر اطلاعات چت'), text),
can_post_messages=check(('can post messages', 'پست کردن پیام'), text),
can_edit_messages=check(('can edit messages', 'تغییر  در پست'), text),
can_delete_messages=check(('can delete messages', 'حذف پست'), text),
can_restrict_members=check(('can restrict members', 'تغییر قابلیت های اعضا'), text),
can_invite_users=check(('can invite users', 'دعوت کردن کاربر'), text),
can_pin_messages=check(('can pin messages', 'سنجاق کردن پست ها'), text),
can_promote_members=check(('can promote members', 'افزودن ادمین جدید'), text),
can_manage_voice_chats=check(('can manage voice chats', 'مدیریت ویس چت'), text)); m.reply('کاربر با موفقیت ادمین شد در صورتی که کاربری رو حذف کرد از چت حذفش میکنم خیالت راحت باشه'); steps.set_data(chat_id, "Home")
        except RightForbidden:
            m.reply(f"""ــ**مثل اینکه دسترسی کامل بهم ندادی تو چت
فقط این دسترسی ها رو به من دادی**ــ
{get_my_per(app, info[0])}""")
@app.on_callback_query()
def callback(_, call):
    m ,data = call.message, call.data
    chat_id = m.chat.id
    if match(r"^addAdmin$", data):
        m.edit("__**شناسه چت را بفرستید (username/id)**__", reply_markup=goMain)
        steps.set_data(m.chat.id, "getChatUsernameOrId")
    elif match(r"^closeMenu$", data):
        call.answer("Bye..."), m.delete()
    elif match(r"^mainMenu$", data):
        m.edit("( __**به منوی اصلی بازگشتید**__ )", reply_markup=mainMenu)
        steps.set_data(chat_id, "Home")

@app.on_chat_member_updated()
def Kicked(_, Update):
    try:
        status = Update['new_chat_member' or 'old_chat_member'].status or Update.status
        chat, from_user, kicked = Update.chat, Update.from_user, Update.new_chat_member.user
        chat_id = chat.id; username = chat.username
        if "banned" == status:
            if from_user.id == botI: return
            cc = get_creator(chat_id).user.id
            try: app.unban_chat_member(chat_id, kicked.id)
            except: pass
            try:
                app.ban_chat_member(chat_id, from_user.id)
                app.send_message(cc, f"کاربر {from_user.mention} , {kicked.mention} رو از {f'[{username}](https://t.me/{username})' if username else chat.title} بن کرد")
            except UserIsBlocked: pass
            except (UserAdminInvalid, BadRequest):
                try: app.send_message(cc, f"کاربر {from_user.mention} , {kicked.mention} رو از {f'[{username}](https://t.me/{username})' if username else chat.title} بن کرد\nمن نمی تونم بنش کنم!")
                except UserIsBlocked: pass
    except AttributeError:
        pass
app.start(), print(f'{botU} started'), idle(), app.stop()
