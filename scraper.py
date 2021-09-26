from pyrogram import Client
from datetime import datetime

MAX_SEEN_DATE = 4

def is_user(member_log):
    is_bot = member_log.is_bot
    if(is_bot):
        return False
    status = member_log.status
    if(not(status == 'offline' or status == 'recently')):
        return False
    last_online_date = member_log.last_online_date
    if(last_online_date): ##age moshakhas bood
        last_seen = datetime.fromtimestamp(last_online_date)
        now = datetime.now()
        delta_days = (now - last_seen).days
        if(delta_days > MAX_SEEN_DATE):
            return False


    return True
    

FROM_GROUP = input('id adadi ya username grouhe morede nazar ra vard konid: ')
SESSION_NAME = input('name accounte morede nazar ra az account haye mojood entekhab konid: ')

with Client(SESSION_NAME) as app:
    group_members = app.iter_chat_members(FROM_GROUP)



with open('raw_user_names.txt' , 'a') as f:
    for member in group_members:
        member_log = member.user
        user_name = member_log.username
        if(is_user(member_log) and user_name):
            f.write(user_name+'\n')







