import json

about_fuckology = (
    '<b>Что такое #нахуйлогия?</b>\n\n'

    'Это не волшебная таблетка, не коучинговая сессия, не сессия у психотерапевта.\n\n'

    'А авторский разъеб-вебинар Марии Милерюс. Для тех, у кого не хватает энергии на новые рывки, и тех, '
    'кто реально хочет изменений и готов работать.\n\n'

    '<b>Вебинар для вас, если в вашей голове есть эти мысли:</b>\n'
    '— не понимаю, чего я, блять, хочу\n'
    '— нет энергии хуярить\n'
    '— почему действия есть, а толку ноль\n'
    '— хочу, мечтаю, всем завидую, но начать не могу\n'
    '— меня окружают долбоебы, и я не понимаю, почему\n\n'

    '<b>Старт #нахуйлогии – 15 декабря.</b>\n\n'

    'Attention! Вебинар будет продаваться в 3 окна продаж, и цена будет только повышаться.'
)

about_blogger = (
    'Мария Милерюс – хозяйка одного из самых популярных и бодрых бьюти-каналов в телеге, бывший бьюти-журналист и '
    'обладательница самого дорогого лица телеграма (с недавнего времени и самых красивых сисек). '
    'Маша понимает, как найти врача, который не изуродует, топит за грамотный улучшайзинг и триггерит на то, '
    'чтобы жить без оглядки на окружающих.'
)

rate1 = (
    'Доступ к вебинару (1,5 часа вебинар и полчаса сессия вопрос-ответ) и к материалам.'
)

rate2 = (
    'Доступ к вебинару, материалам и мастер-майндам в малых группах, где мы будем намечать план '
    'действий вместе с Машей. А также доступ к чатам малых групп, где еще 2 месяца мы будем на '
    'связи и поддерживать друг друга.'
)

rate3 = (
    'Доступ к вебинару, материалам и личная работа с Машей в течение 2-х месяцев. Общение в чате, '
    '4 индивидуальных сессии-звонка с Машей.'
)

data = {
    '1': about_fuckology,
    '2': about_blogger,
    '3': rate1,
    '4': rate2,
    '5': rate3,
    'rates': [
        {
            'description': rate1,
            'prices': [
                5_000,
                7_000,
                10_000
            ],
            'final_price': 10_000
        },
        {
            'description': rate2,
            'prices': [
                20_000,
                25_000,
                30_000
            ],
            'final_price': 30_000
        },
        {
            'description': rate3,
            'prices': [
                70_000,
                80_000,
                100_000
            ],
            'final_price': 100_000
        }
    ],
    'invoice_id': 1,
    'reg_users': [],
    'open_sells': True,
    'sells_closed_text': 'Продажи закрыты!'
}

if __name__ == "__main__":
    with open('messages.json', 'w') as file:
        json.dump(data, file, indent=4)
