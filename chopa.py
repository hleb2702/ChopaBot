from sqlite3 import connect
from random import randint as r, choice
from traceback import format_exc
from time import sleep
from json import dumps

from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api import VkApi

from config import token, group, STICKERS

def main():
    ss = VkApi(token=token)
    s = ss.method
    db = connect('chopa.db')
    c = db.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS chat(
        peer int,
        shans int,
        words text
    )''')

    while True:
        try:

            def end():
                c.execute(f'UPDATE chat SET shans = {shans}, words = "{words}" WHERE peer = {peer}')
                db.commit()

            def send(txt=None, peer3=None, rep=True, stick=None):
                if peer3 is not None:
                    peer2 = peer3
                else:
                    peer2 = peer
                if rep:
                    jjss = dumps({'peer_id': peer2,
                                   'conversation_message_ids': [msg],
                                   'is_reply': True})
                return s('messages.send', {'random_id': 0, 'peer_id':peer2, 'message':txt, 
                                           'forward':jjss, 'sticker_id':stick, 'disable_mentions':1})

            def trigger(txt):
                a = ['http', 'vk.com', 'vk.cc', 'vk.me', 't.me', '.com', '.onion', '.ru', '.by', '.wb']
                for i in a:
                    if i in txt:
                        return True
                return False

            print('eeee')
            for event in VkBotLongPoll(ss, group).listen():
                if event.type == VkBotEventType.MESSAGE_NEW:
                    info = event.object.message
                    id, peer, txt_txt, msg = info['from_id'], info['peer_id'], info['text'], info['conversation_message_id']
                    text = txt_txt.split()
                    text.append('')
                    txt = text[0].lower()
                    if peer < 2000000000:
                        send('Бот доступен только в беседах')
                        continue
                    if id < 1:
                        continue

                    chat = s('messages.getConversationsById', {'peer_ids':peer})['items'][0]['chat_settings']
                    admins = chat['admin_ids']
                    admins.append(chat['owner_id'])

                    while True:
                        try:
                            c.execute(f'SELECT * FROM chat WHERE peer = {peer}')
                            fet = c.fetchone()
                            shans = fet[1]
                            words = eval(fet[2])
                            break
                        except:
                            c.execute(f'INSERT INTO chat VALUES({peer}, 35, "[]")')
                            db.commit()

                    if txt == '!п':
                        a = '''
📝Список команд:
!п - помощь по командам
!р - бот напишет рандомное сообщение из базы беседы
!т - тех поддержка чопы
!б - краткая инфа о беседе
!д - поддержать чопу

👨‍💻Для администраторов:
!ш от 10-70 - установить вероятность с какой бот будет отвечать (по стандарту 35)
!с - стереть базу ответов
!у ответ на смс чопы - удаляет фразу из базы беседы 
                        '''
                        send(a)

                    elif txt == '!р':
                        if words:
                            send(choice(words))

                    elif txt == '!с':
                        if id in admins:
                            words = []
                            send('готово')
                        else:
                            send('вы не админ')

                    elif txt == '!о':
                        if id in admins:
                            try:
                                shans = int(text[1])
                                if shans > 70:
                                    send('готово, поставлено 70%')
                                    shans = 70
                                else:
                                    send('готово')
                            except:
                                send('!о (число от 0 до 70)')
                        else:
                            send('вы не админ')

                    elif txt == '!б':
                        send(f'Добавлено фраз в этой беседе: {len(words)}\npeer_id: {peer}')

                    elif txt == '!д':
                        send('Вы всегда можете меня поддержать по этой ссылке: https://vk.com/keksikapp?mid=-216021821&ref=group_menu')

                    elif txt == '!т':
                        send('По вопросам: @neatboy\nНашли баг: @idd2702')

                    elif txt == '!у':
                        if id not in admins:
                            send('Вы не админ беседы')
                            continue
                        try:
                            if -info['reply_message']['from_id'] == group:
                                words.remove(info['reply_message']['text'])
                                send('готово')
                            else:
                                send('Команда работает только ответом на смс чопы')
                        except ValueError:
                            send('Данного сообщения нет в базе')
                        except:
                            send('Команда работает только ответом на смс чопы')

                    elif txt_txt not in words and not trigger(txt_txt) and len(txt_txt) > 2:
                        words.append(txt_txt)

                    if r(0, 100) > 5:
                        send(stick=choice(STICKERS))
                    if r(1, 100) <= shans:
                        send(choice(words))

                    end()

        except:
            print(format_exc())
            sleep(3)

if __name__ == '__main__':
    main()


