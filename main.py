import json
import os
import requests
from data import TOKEN, token, admin_id
import vk_api
import datetime as dt

api_version = '5.52'
vk_session = vk_api.VkApi(token=TOKEN)
vk_session1 = vk_api.VkApi(token=token)
vk = vk_session.get_api()


def get_but(text, color):
    return {
        "action": {
            "type": "text",
            "payload": "{\"button\": \"" + "1" + "\"}",
            "label": f"{text}"
        },
        "color": f"{color}"
    }


main_keyboard = {
    "one_time": False,
    "buttons": [
        [get_but('😍Получить посты', 'default'), get_but('🤑Получить оплату', 'default')],
        [get_but('📈Топ админов', 'default'), get_but('🤩Посчитать охват', 'default')]
    ]
}
main_keyboard = json.dumps(main_keyboard, ensure_ascii=False).encode('utf-8')
main_keyboard = str(main_keyboard.decode('utf-8'))

payment_keyboard = {
    "one_time": True,
    "buttons": [
        [get_but('◀Назад', 'default')]
    ]
}
payment_keyboard = json.dumps(payment_keyboard, ensure_ascii=False).encode('utf-8')
payment_keyboard = str(payment_keyboard.decode('utf-8'))

payment2_keyboard = {
    "one_time": True,
    "buttons": [
        [get_but('🤑Получить оплату', 'default')]
    ]
}
payment2_keyboard = json.dumps(payment2_keyboard, ensure_ascii=False).encode('utf-8')
payment2_keyboard = str(payment2_keyboard.decode('utf-8'))

yes_or_no_keyboard = {
    "one_time": True,
    "buttons": [
        [get_but('✅Да', 'positive'), get_but('◀Назад', 'default')]
    ]
}
yes_or_no_keyboard = json.dumps(yes_or_no_keyboard, ensure_ascii=False).encode('utf-8')
yes_or_no_keyboard = str(yes_or_no_keyboard.decode('utf-8'))

admin_panel_keyboard = {
    "one_time": False,
    "buttons": [
        [get_but('💰Входящие оплаты', 'default'), get_but('😍Добавить оплаченные посты', 'default')],
        [get_but('🤩Посчитать охват', 'default'), get_but('⛔Заблокировать паблик', 'default')],
        [get_but('✏Ручная рассылка', 'default'), get_but('🔗Добавить посты для закупов', 'default')],
        [get_but('📈Топ админов', 'default'), get_but('⚒Разблокировать паблик', 'default')]
    ]
}

admin_panel_keyboard = json.dumps(admin_panel_keyboard, ensure_ascii=False).encode('utf-8')
admin_panel_keyboard = str(admin_panel_keyboard.decode('utf-8'))

admin_yes_or_no_keyboard = {
    "one_time": True,
    "buttons": [
        [get_but('✅Да', 'positive'), get_but('🚫Нет', 'negative')]
    ]
}
admin_yes_or_no_keyboard = json.dumps(admin_yes_or_no_keyboard, ensure_ascii=False).encode('utf-8')
admin_yes_or_no_keyboard = str(admin_yes_or_no_keyboard.decode('utf-8'))

admin_yes_or_no_keyboard2 = {
    "one_time": True,
    "buttons": [
        [get_but('✅Оплачено', 'positive'), get_but('⛔Заблокировать посты', 'negative')]
    ]
}
admin_yes_or_no_keyboard2 = json.dumps(admin_yes_or_no_keyboard2, ensure_ascii=False).encode('utf-8')
admin_yes_or_no_keyboard2 = str(admin_yes_or_no_keyboard2.decode('utf-8'))


def sender(user_id, text, key):
    if key == 0:
        vk_session.method('messages.send', {'user_id': user_id, 'message': text, 'random_id': 0,
                                            'keyboard': main_keyboard})
    if key == 1:
        vk_session.method('messages.send',
                          {'user_id': user_id, 'message': text, 'random_id': 0, 'keyboard': payment_keyboard})
    if key == 2:
        vk_session.method('messages.send',
                          {'user_id': user_id, 'message': text, 'random_id': 0, 'keyboard': yes_or_no_keyboard})
    if key == 3:
        vk_session.method('messages.send',
                          {'user_id': user_id, 'message': text, 'random_id': 0, 'keyboard': payment2_keyboard})
    if key == 'admin_rules':
        vk_session.method('messages.send',
                          {'user_id': user_id, 'message': text, 'random_id': 0, 'keyboard': admin_panel_keyboard})
    if key == 'admin_yes_or_no':
        vk_session.method('messages.send',
                          {'user_id': user_id, 'message': text, 'random_id': 0, 'keyboard': admin_yes_or_no_keyboard})
    if key == 'admin_yes':
        vk_session.method('messages.send',
                          {'user_id': user_id, 'message': text, 'random_id': 0, 'keyboard': admin_yes_or_no_keyboard2})
    if key == '666':
        vk_session.method('messages.send', {'user_id': user_id, 'message': text, 'random_id': 0})


def main():
    global vk_session, vk_session1, vk
    try:
        while True:
            messages = vk_session.method('messages.getConversations', {'count': 200, 'filter': 'unanswered'})
            # time.sleep(1)
            if messages['count'] != 0:
                with open('dialog_state.json') as dial:
                    dialogs = json.load(dial)
                user_id = str(messages['items'][0]['last_message']['from_id'])
                msg = messages['items'][0]['last_message']['text']
                if user_id not in dialogs:
                    dialogs[user_id] = 'main'
                    sender(user_id, 'Приветствую тебя', 0)
                    with open('dialog_state.json', 'w') as file:
                        json.dump(dialogs, file)
                elif user_id in admin_id or dialogs[user_id] == 'admin_rules':
                    admin_dialog(user_id, msg)
                else:
                    user_dialog(user_id, msg)
    except vk_api.exceptions.ApiError:
        vk_session = vk_api.VkApi(token=TOKEN)
        vk_session1 = vk_api.VkApi(token=token)
        vk = vk_session.get_api()
        main()
    except requests.exceptions.ConnectionError:
        vk_session = vk_api.VkApi(token=TOKEN)
        vk_session1 = vk_api.VkApi(token=token)
        vk = vk_session.get_api()
        main()


def admin_dialog(user_id, msg):
    dialogs, checker, done, req, top, descript, ban = open_json()
    if 'Посчитать охват' in msg:
        sender(user_id, '😎Укажите ссылки на посты, каждый пост с новой строчки', 1)
        dialogs[user_id] = 'checker'
    elif 'wall' in msg and dialogs[user_id] == 'checker':
        pay = get_views(msg, False, user_id)
        sender(user_id, pay[0], 1)
    elif 'Назад' in msg:
        dialogs[user_id] = 'admin_rules'
        sender(user_id, '😍🤑', 'admin_rules')
    elif 'Добавить оплаченные посты' in msg:
        dialogs[user_id] = 'pay_post'
        sender(user_id, '😎Укажите ссылки на посты, каждый пост с новой строчки', 1)
    elif dialogs[user_id] == 'pay_post' and 'wall' in msg:
        posts = msg.split('\n')
        for elem in posts:
            done = append_doned(elem, admin_id, 'payed')
        sender(user_id, 'Успешно', 'admin_rules')
    elif '✅Да' in msg:
        send_payment()
    elif '💰Входящие оплаты' in msg:
        send_payment()
    elif '✅Оплачено' in msg:
        sender(admin_id, 'Введите номер оплаты:', '666')
        dialogs[user_id] = 'number_of_pay'
    elif dialogs[user_id] == 'number_of_pay':
        checker, done, top, text = send_grate_payment(msg)
        sender(user_id, text, '666')
        dialogs[user_id] = 'admin_rules'
        send_payment()
    elif 'Заблокировать паблик' in msg:
        sender(user_id, 'Укажите ссылку на пост или группу', 1)
        dialogs[user_id] = 'block_group'
    elif dialogs[user_id] == 'block_group':
        url = msg.split('\n')
        for msg in url:
            if 'wall' in msg:
                group = msg.split('wall')[1].split('_')[0]
            elif 'group' in msg:
                group = '-' + msg.split('public')[1]
            else:
                info = vk_session1.method('groups.getById', {'group_id': msg.split('com/')[1]})
                group = '-' + str(info[0]['id'])
            if group not in ban['groups']:
                ban['groups'].append(group)
                sender(user_id, f'Группа {msg} забанена', 'admin_rules')
            else:
                sender(user_id, f'Группа {msg} уже в бане', 'admin_rules')
        dialogs[user_id] = 'admin_rules'
    elif 'Добавить посты для закупов' in msg:
        sender(user_id, 'Пришлите фото', 1)
        dialogs[user_id] = 'add_post_photo'
    elif dialogs[user_id] == 'add_post_photo':
        save_photo()
        dialogs[user_id] = 'add_post_copyright'
    elif dialogs[user_id] == 'add_post_copyright':
        name = os.listdir(path="data")[-1]
        descript[name] = [msg]
        dialogs[user_id] = 'add_post_date'
        sender(user_id, 'Успешно, пришлите дату в формате ДД.ММ.ГГГГ', '666')
    elif dialogs[user_id] == 'add_post_date':
        name = os.listdir(path="data")[-1]
        descript[name].append(msg)
        sender(user_id, 'Успешно', 'admin_rules')
        dialogs[user_id] = 'admin_rules'
    elif 'Ручная рассылка' in msg:
        sender(user_id, 'Введите сообщение:', 1)
        dialogs[user_id] = 'spam'
    elif dialogs[user_id] == 'spam':
        names = list(dialogs.keys())
        for name in names:
            if name != admin_id:
                sender(name, msg, 0)
            else:
                sender(name, 'Успешно', 'admin_rules')
        dialogs[user_id] = 'admin_rules'
    elif msg == '📈Топ админов':
        admins = list(top['all'].keys())
        admins.sort(key=lambda x: -int(top['all'][x][0]))
        text = f'Админы заработали с нами: {top["sum"]}₽\n'
        k = len(admins)
        if len(admins) >= 10:
            k = 11
        for i in range(k):
            text += f'\n{i + 1}) {admins[i]} - {top["all"][admins[i]][0]}₽, ' \
                    f'опубликовано {top["all"][admins[i]][1]} постов'
        sender(user_id, text, 'admin_rules')
    elif 'Разблокировать паблик' in msg:
        dialogs[user_id] = 'unban'
        sender(user_id, 'Укажите ссылку на пост или группу', 1)
    elif dialogs[user_id] == 'unban':
        url = msg.split('\n')
        for msg in url:
            if 'wall' in msg:
                group = msg.split('wall')[1].split('_')[0]
            elif 'group' in msg:
                group = '-' + msg.split('public')[1]
            else:
                info = vk_session1.method('groups.getById', {'group_id': msg.split('com/')[1]})
                group = '-' + str(info[0]['id'])
            if group in ban['groups']:
                id = ban['groups'].index(group)
                del ban['groups'][id]
                sender(user_id, f'Группа {msg} разбанена', 'admin_rules')
            else:
                sender(user_id, f'Группа {msg} не в бане', 'admin_rules')
        dialogs[user_id] = 'admin_rules'
    else:
        dialogs[user_id] = 'admin_rules'
        sender(user_id, '😍🤑', 'admin_rules')
    save_json(dialogs, checker, done, req, top, descript, ban)


def user_dialog(user_id, msg):
    dialogs, checker, done, req, top, descript, ban = open_json()
    if msg == '/+admin':
        dialogs[user_id] = 'admin_rules'
        sender(user_id, 'Вы получили права администратора', 'admin_rules')
    elif 'Получить оплату' in msg:
        if dialogs[user_id] == 'payment1':
            dialogs[user_id] = 'payment2'
            sender(user_id, 'Укажите номер киви в формате +79000000000', 1)
        else:
            dialogs[user_id] = 'payment1'
            sender(user_id, '😎Укажите ссылки на посты, каждый пост с новой строчки', 1)
    elif 'Получить посты' in msg:
        names = os.listdir(path="data")
        if len(names) == 0:
            sender(user_id, 'Закупов на данный момент нет', 0)
        else:
            for name in names:
                if 'unactive' not in descript[name]:
                    date = descript[name][1]
                    copy = descript[name][0]
                    print(str(dt.date.today())[-5:-2], date[-5:-2])
                    if int(str(dt.date.today())[-2:]) - int(date[-2:]) >= 0 and str(dt.date.today())[-5:-2] == date[-5:-2]:
                        descript[name].append('unactive')
                        continue
                    upload = vk_api.VkUpload(vk_session)
                    photo = upload.photo_messages(f'data\{name}', user_id)
                    owner_id = photo[0]['owner_id']
                    photo_id = photo[0]['id']
                    access_key = photo[0]['access_key']
                    attachment = f'photo{owner_id}_{photo_id}_{access_key}'
                    sender(user_id, f'На {date} \n'
                                    f'Исток: {copy}', 0)
                    vk.messages.send(peer_id=user_id, random_id=0, attachment=attachment)
    elif 'Посчитать охват' in msg:
        sender(user_id, '😎Укажите ссылки на посты, каждый пост с новой строчки', 1)
        dialogs[user_id] = 'checker'
    elif 'wall' in msg and dialogs[user_id] == 'checker':
        pay = get_views(msg, False, user_id)
        sender(user_id, pay[0], 1)
    elif dialogs[user_id] == 'payment1' and 'wall' in msg:
        pay = get_views(msg, True, user_id)
        req[user_id] = [pay[1], msg.split('\n')]
        sender(user_id, pay[0], 3)
        if pay[-1]:
            sender(user_id, '\n'.join(pay[-1]), 3)
        if pay[1] == 0:
            dialogs[user_id] = 'main'
            sender(user_id, '😍🤑', 0)
    elif '+79' in msg and dialogs[user_id] == 'payment2':
        dialogs[user_id] = 'payment3'
        sender(user_id, f'Оплачиваем {req[user_id][0]}₽ на киви {msg} \nВсе верно?', 2)
        req[user_id].append(msg)
    elif 'Назад' in msg:
        dialogs[user_id] = 'main'
        sender(user_id, '😍🤑', 0)
    elif msg == '✅Да' and dialogs[user_id] == 'payment3':
        sender(user_id, '✅Оплата успешно запрошена! \n‼НЕ удаляйте посты до получения оплаты!', 0)
        last = int(checker['last'])
        checker['last'] = last + 1
        checker[last] = req[user_id]
        checker[last].append(f'vk.com/id{user_id}')
        dialogs[user_id] = 'main'
        for elem in req[user_id][1]:
            done = append_doned(elem, user_id, 'requested')
        send_noutification()
    elif msg == '📈Топ админов':
        admins = list(top['all'].keys())
        admins.sort(key=lambda x: -int(top['all'][x][0]))
        text = f'Админы заработали с нами: {top["sum"]}₽\n'
        k = len(admins)
        if len(admins) >= 10:
            k = 11
        for i in range(k):
            text += f'\n{i + 1}) https://{admins[i]} - {top["all"][admins[i]][0]}₽, ' \
                    f'опубликовано {top["all"][admins[i]][1]} постов'
        sender(user_id, text, 0)
    else:
        sender(user_id, '😍🤑', 0)
        dialogs[user_id] = 'main'
    save_json(dialogs, checker, done, req, top, descript, ban)


def send_noutification():
    post = 1
    dialogs, checker, done, req, top, descript, ban = open_json()
    last = checker['last']
    for i in range(last + 1, 100000000, -1):
        if str(i) in checker:
            post += 1
    sender(admin_id, f'{post} постов ожидают оплаты. \nПросмотреть?', 'admin_yes_or_no')


def send_payment():
    dialogs, checker, done, req, top, descript, ban = open_json()
    payment_id = checker['last'] - 1
    while str(payment_id) not in checker:
        payment_id -= 1
        if payment_id < 100000000:
            sender(admin_id, 'Входящих оплат нет', 'admin_rules')
            return True
    sender(admin_id, 'ОПЛАТА 💰', '666')
    sender(admin_id, f'{str(payment_id)}', '666')
    sender(admin_id, f'🧛‍♂админ: {checker[str(payment_id)][3]}\n' +
           '😍 посты:' + str('\n'.join(checker[str(payment_id)][1])) +
           f'\n💵сумма: {checker[str(payment_id)][0]}\n'
           f'Qiwi: {checker[str(payment_id)][2]}', 'admin_yes')


def send_grate_payment(payment_id):
    dialogs, checker, done, req, top, descript, ban = open_json()
    if payment_id in checker:
        sender(checker[payment_id][3][9:],
               f'✅Вы получили оплату за посты. '
               f'\nНомер киви: {checker[payment_id][2]} '
               f'\nСумма: {checker[payment_id][0]}₽'
               f'\nСтатус: Оплачено✅ '
               f'\nОставьте отзыв, чтобы другие админы не просили предоплату: '
               f'\nhttps://vk.com/topic-203281870_47417826',
               0)
        top['sum'] += checker[payment_id][0]
        if checker[payment_id][3] not in top['all']:
            top['all'][checker[payment_id][3]] = [0, 0]
        top['all'][checker[payment_id][3]][0] += checker[payment_id][0]
        for url in checker[payment_id][1]:
            user_id = url.split('wall')[1]
            group_id = user_id.split('_')[0]
            post_id = user_id.split('_')[1]
            top['all'][checker[payment_id][3]][1] += 1
            done[group_id][post_id][1] = 'payed'
        del checker[payment_id]
        text = 'Успешно оплачено'
    else:
        text = 'Входящих оплат нет'
    return checker, done, top, text


def block_payment(payment_id):
    dialogs, checker, done, req, top, descript, ban = open_json()
    sender(checker[payment_id][3][7:], f'😳Ваша оплата №{payment_id} была отклонена. '
                                       f'За подробностями к vk.com/id{admin_id}', 0)
    for url in checker[payment_id][1]:
        user_id = url.split('wall')[1]
        group_id = user_id.split('_')[0]
        post_id = user_id.split('_')[1]
        done[group_id][post_id][1] = 'banned'
    del checker[payment_id]
    return done, checker


def open_json():
    with open('dialog_state.json') as dial:
        dialogs = json.load(dial)
    with open('checker.json') as dial:
        checker = json.load(dial)
    with open('doned.json') as dial:
        done = json.load(dial)
    with open('requests.json') as dial:
        req = json.load(dial)
    with open('top_of_all.json') as dial:
        top = json.load(dial)
    with open('post_description.json') as dial:
        descript = json.load(dial)
    with open('banned.json') as dial:
        ban = json.load(dial)
    return dialogs, checker, done, req, top, descript, ban


def save_json(dialogs, checker, done, req, top, descript, ban):
    with open('dialog_state.json', 'w') as file:
        json.dump(dialogs, file)
    with open('checker.json', 'w') as file:
        json.dump(checker, file)
    with open('doned.json', 'w') as file:
        json.dump(done, file)
    with open('requests.json', 'w') as file:
        json.dump(req, file)
    with open('top_of_all.json', 'w') as file:
        json.dump(top, file)
    with open('post_description.json', 'w') as file:
        json.dump(descript, file)
    with open('banned.json', 'w') as file:
        json.dump(ban, file)


def check_copypaste(copy):
    dialogs, checker, done, req, top, descript, ban = open_json()
    names = os.listdir(path="data")
    for name in names:
        if copy == descript[name][0]:
            return True
    return False


def check_contacts(group_id, user_id):
    info = vk_session1.method('groups.getById', {'group_id': group_id[1:], 'fields': 'contacts'})
    state = False
    for i in range(len(info[0]['contacts'])):
        if int(info[0]['contacts'][i]['user_id']) == int(user_id):
            state = True
            break
    return state


def check_doned(user_id):
    dialogs, checker, done, req, top, descript, ban = open_json()
    group_id = user_id.split('_')[0]
    post_id = user_id.split('_')[1]
    if group_id in done:
        if post_id in done[group_id]:
            return done[group_id][post_id][1]
    return False


def append_doned(url, user_id, text):
    dialogs, checker, done, req, top, descript, ban = open_json()
    try:
        group_id = url.split('wall')[1].split('_')[0]
        post_id = url.split('wall')[1].split('_')[1]
        info = vk_session1.method('wall.getById', {'posts': f"{group_id}_{post_id}"})
        unix = info[0]['date']
        date = unix // 86400
        if group_id not in done:
            done[group_id] = {}
        done[group_id][post_id] = [date, text]
        return done
    except:
        if user_id == admin_id:
            sender(user_id, 'Ошибка', 'admin_rules')
        else:
            sender(user_id, 'Ошибка', 0)
        return done


def data_check(post_id):
    dialogs, checker, done, req, top, descript, ban = open_json()
    group_id = post_id.split('_')[0]
    post_id = post_id.split('_')[1]
    info = vk_session1.method('wall.getById', {'posts': f"{group_id}_{post_id}"})
    unix = info[0]['date']
    date = unix // 86400
    today = dt.datetime.timestamp(dt.datetime.today()) // 86400
    if today - date >= 5:
        return 'long'
    else:
        files = os.listdir(path="data")
        count_files_data = len(files)
        for i in range(count_files_data):
            name = f'img{i}.jpg'
            if name in descript:
                if descript[name][1] == date:
                    return True
        return 'uncorrect'


def banned_public(group_id):
    dialogs, checker, done, req, top, descript, ban = open_json()
    if group_id in ban['groups']:
        return False
    return True


def get_views(urls, state, user_id):
    urls = urls.split('\n')
    counted_urls = []
    deffect_postes = []
    summa_of_views = 0
    for url in urls:
        if 'wall' in url:
            info = vk_session1.method('wall.getById', {'posts': url.split('wall')[1]})
            view = info[0]['views']['count']
            doned = check_doned(url.split('wall')[1])
            try:
                copy = check_copypaste(info[0]['copyright']['link'])
            except KeyError:
                copy = False
            try:
                contact = check_contacts(url.split('wall')[1].split('_')[0], user_id)
            except KeyError:
                contact = False
            if url not in counted_urls:
                if state:
                    if banned_public(url.split('wall')[1].split('_')[1]):
                        if copy:
                            if data_check(url):
                                if contact:
                                    if not doned:
                                        summa_of_views += view
                                    elif doned == 'requested':
                                        deffect_postes.append(f'{url} - Оплата уже запрошена')
                                    elif doned == 'banned':
                                        deffect_postes.append(f'{url} - Оплата за этот пост была отклонена')
                                    elif doned == 'payed':
                                        deffect_postes.append(f'{url} - Пост оплачен')
                                else:
                                    deffect_postes.append(f'{url} - Вас нет в контактах')
                            elif data_check(url) == 'long':
                                deffect_postes.append(f'{url} - Пост был выставлен более 5-ти дней назад')
                            else:
                                deffect_postes.append(f'{url} - Некорректная дата')
                        else:
                            deffect_postes.append(f'{url} - Несовпадение источника')
                    else:
                        deffect_postes.append(f'{url} - Выплаты из этого паблика заблокированы')
                else:
                    summa_of_views += view
                counted_urls.append(url)
    final = f'🤩Общий охват: {summa_of_views} \n Сумма: {summa_of_views * 15 // 1000}₽'
    return [final, summa_of_views * 15 // 1000, deffect_postes]


def save_photo():
    info = vk_session.method('messages.getHistoryAttachments', {'peer_id': admin_id, 'media_type': 'photo', 'count': 1})
    url = info['items'][0]['attachment']['photo']['sizes'][-1]['url']
    files = os.listdir(path="data")
    count_files_data = len(files)
    picture = requests.get(url)
    while f'img{count_files_data}.jpg' in files:
        count_files_data += 1
    with open(f'data\img{count_files_data}.jpg', 'wb') as file:
        file.write(picture.content)
    sender(admin_id, 'Успешно, пришлите источник', '666')


if __name__ == '__main__':
    main()
