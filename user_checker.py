from pyrogram import Client
from pyrogram.errors import FloodWait,BadRequest
from time import sleep


TO_GROUP = input('id adadi ya username grouhe maghsad ra vard konid: ')
MAX_SEARCH = int(input('saghfe barasie username ha ra tayin konid: '))



def get_bot_tokens():
    token_list = list()
    with open('api_bots.txt' , 'r') as f:
        for token in f:
            token_list.append(token.replace('\n' ,''))

    return token_list

token_list = get_bot_tokens()
shomare = 1
mojaz = True
for token in token_list:
    if(mojaz):
        print(f'robote shomare {shomare}')
        with Client(f'bot{shomare}',bot_token=token) as bot:
            add_shomar = 0 #===> add shomar
            barasi = 0
            with open('user_names.txt' , 'a') as f2:
                with open('raw_user_names.txt' , 'r+') as f:
                    lines = f.readlines() #mabda
                    for user_name in lines:
                        barasi+=1
                        print('barasi',user_name.replace('\n',''),'....')
                        try :
                            bot.get_chat_member(chat_id =  TO_GROUP, user_id = user_name)
                        except FloodWait as e:
                            sleep_time = e.x
                            if(sleep_time > 600):
                                print(f'{sleep_time} sanie mahdood shodim!:( korooj...')
                                shomare += 1
                                break
                            print(f'{sleep_time} sanie esterahat...')
                            sleep(sleep_time)
                        except BadRequest as e:
                            #user dar gape maghsad nabood
                            f2.write(user_name)
                            print(user_name.replace('\n',''),'=========> bayad add she')
                            add_shomar += 1
                        except:
                            print('error na maloom!')

                        if(barasi == MAX_SEARCH):
                            mojaz = False
                            break
                        
                            

                    f.seek(0)
                    f.truncate()
                    f.writelines(lines[barasi:])



input('tamam')