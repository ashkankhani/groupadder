from pyrogram import Client
from pyrogram.errors import FloodWait,BadRequest,Forbidden
from time import sleep
import sqlite3
import re


def get_session_list():
    session_list = list()
    connection = sqlite3.connect('database.db')

    cursor = connection.cursor()

    cursor.execute('''select session_name
    from sessions
    ''')

    session_tuples = cursor.fetchall()


    for tup in session_tuples:
        session_list.append(tup[0])

    return session_list

    

session_list = get_session_list()
print(session_list)

def join_chat(session_list,link):
    
    res = re.findall(r'^.*t\.me/(\w*)$',link)

    if(len(res)):
        link = res[0]
    

    for session in session_list:
        with Client(session) as app:
            try:
                join = app.join_chat(link)
            except BadRequest as e:
                e_id = e.ID
                if(e_id == 'USERNAME_INVALID'):
                    print('link eshtebah ast!')
                elif(e_id == 'USER_ALREADY_PARTICIPANT'):
                    print(f'karbare {session} dar grouh az ghabl bood!')
            except FloodWait as e:
                sleep_time = e.x
                print(f'{session} bayad {sleep_time} sanie esterahat kone!')
                sleep(sleep_time)
            except:
                print('error')
            else:
                print(f'{session} be grouh join shod!')

GROUP = input('id ya username grouhe maghsad ra vared konid: ')
TEDAD = int(input('tedade add ra moshakhas konid: '))


join_chat(session_list,GROUP)



added = 0
mojaz = True
for session in session_list:
    if(mojaz):
        with Client(session) as app:
            with open('user_names.txt' , 'r+') as f:
                lines = f.readlines()
                tedad = 0
                for user_name in lines:
                    try:
                        app.add_chat_members(GROUP ,user_name.replace('\n',''))
                    except Forbidden as e:
                        id = e.ID
                        if(id == 'USER_PRIVACY_RESTRICTED'):
                            print(user_name,'ghofl karde add ro!')
                        elif(id == 'CHAT_WRITE_FORBIDDEN'):
                            print(f'robote {session} dar grouhe maghsad nist!in robot ro dar grouh add karde va dobare talash konid!')
                            sleep(100000000)
                    except BadRequest as e:
                        if(e.ID == 'PEER_FLOOD'):
                            print(f'accounte {session} report shod!')
                            break
                    except FloodWait as e:
                        sleep_time = e.x
                        if(sleep_time > 600):
                                print(f'{sleep_time} sanie mahdood shodim!:( korooj...')
                                break
                        print(f'{sleep_time} sanie esterahat!')
                        sleep(sleep_time)
                    except:
                        print('errore na maloom!')
                    else:
                        print(user_name,'be gap add shod!')
                        added += 1
                        if(added == TEDAD):
                            mojaz = False
                            break

                    tedad += 1

                f.seek(0)
                f.truncate()
                f.writelines(lines[tedad:])

            

input(f'tamam!be tedade {added} user add kardim!,agar barname be moshkel khord va account report nashod,username {user_name} ra az file usernames hazf konid!')