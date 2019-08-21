# -- coding: utf8 --
from vk_api import VkUpload
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import vk_api
import psycopg2

vk = vk_api.VkApi(token="6b70a77a629a560c597473fdd178e4589dacc2425d61f5d749120d597f3e60fc81fede865fe96b6f93768")
longpoll = VkBotLongPoll(vk, 185672476)
vk2 = vk.get_api()
upload = VkUpload(vk)


def database():
    con = psycopg2.connect(
        database='d4glhqs3332p6a',
        user='cfueissddpyojd',
        password='100991e74074f1cb5693f454aaa6f9f71868a4df450327a3314ed66a8dbba6fe',
        host='ec2-54-247-96-169.eu-west-1.compute.amazonaws.com',
        port='5432')
    q = con.cursor()
    return con, q


def messages_send(peer_id, message):
    vk2.messages.send(
        random_id=0,
        peer_id=peer_id,
        message=message)


for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW:
        text = event.object.text.lower()
        peer_id = event.object.peer_id
        user_id = event.object.from_id
        if peer_id == user_id:
            con, q = database()
            q.execute("SELECT * FROM user_inform WHERE User_ID = '%s'" % (user_id))
            result = q.fetchall()
            con.close()
            print(result)
            if len(result) == 0:
                if text == "маг":
                    con, q = database()
                    q.execute(
                            "INSERT INTO user_inform (Name, Clas, User_ID, Balance, Atack1, Atack2) VALUES ('%s', '%s', '%s', '%s', '%s', '%s')" % (' ', 1, user_id, 0, 1, 2))
                    con.commit()
                    con.close()
                    messages_send(user_id, 'Теперь введи свой ник')
                elif text == "воин":
                    con, q = database()
                    q.execute(
                        "INSERT INTO user_inform (Name, Clas, User_ID, Balance, Atack1, Atack2) VALUES ('%s', '%s', '%s', '%s', '%s', '%s')" % (' ', 2, user_id, 0, 3, 4))
                    con.commit()
                    con.close()
                    messages_send(user_id, 'Теперь введи свой ник')
                elif text == "стрелок":
                    con, q = database()
                    q.execute(
                            "INSERT INTO user_inform (Name, Clas, User_ID, Balance, Atack1, Atack2) VALUES ('%s', '%s', '%s', '%s', '%s', '%s')" % (' ', 3, user_id, 0, 5, 6))
                    con.commit()
                    con.close()
                    messages_send(user_id, 'Теперь введи свой ник')
                else:
                    messages_send(peer_id, 'Ты не выбрал класс')
            else:
                if result[0][0] == ' ':
                    names = []
                    con, q = database()
                    q.execute("SELECT * FROM user_inform")
                    result2 = q.fetchall()
                    for res in result2:
                        if res != ' ':
                            names.append(res)
                    if len(text) <= 15:
                        if ' ' not in text:
                            if text not in names:
                                q.execute("UPDATE user_inform SET Name = '%s' WHERE User_ID = '%s'" % (text, user_id))
                                con.commit()
                                con.close()
                                messages_send(user_id, 'Вы успешно создали аккаунт!\nВремя играть!')
                            else:
                                messages_send(user_id, 'Ник занят!')
                        else:
                            messages_send(user_id, 'Нельзя использовать пробел в нике!')
                    else:
                        messages_send(user_id, 'Длинна ника должна быть меньше 15 символов!')


