LEXICON: dict[str, str] = {

    'not_found': 'Бот не знает таокой кмоанды, также режиме общение из группы доступно только поиск и просмотр напитков!',
    'already_authorized': 'Вы уже авторизованы 🥳',
    'not_user': 'Вы не авторизованы нажмите пожалуйста /start',
    'input_password': 'Введите пароль администратора:',
    'admin_successful': 'Вы стали администратором',
    'wrong_password': 'Пароль не верный',
    'admin': 'Вы уже являетесь администратором',

    'view_beer': 'Просмотр пива 🍻',
    'search': 'Поиск пива 🔎',
    'add_beer': 'Добавить пиво 🥳',

    'search_name': 'Введите название напитка:',
    'not_search': 'Поиск не дал результатов',

    'list_beer': 'Список пивных напитков:\n\n',

    'delete': 'Удалить',
    'del': '🗑️️',

    'cancel_null': 'Отменять нечего',
    'cancel_add_beer': 'Вы вышли из меню добавления пива\n\n',

    'add_name': 'Пожалуйста, введите название пиво:',
    'upload_photo': 'Пожалуйста, добавьте изображение пиво:',

    'sort_beer': 'Пожалуйста, введите сорт пива:',

    'comment': 'Пожалуйста, напишите краткий коментарий к напитку:',

    'rating': 'Пожалуйста, укажите рейтинг пива от 0 до 10:',
    'price': 'Пожалуйста, укажите цену:',

    'not_beer': 'Нет добавленых напитко :(',

    'save_beer': 'Напиток добавлен!\n\n',

    'edit': 'Редактировать',
    'cancel': 'Отмена',
    'warning_rating': 'Рейтинг должен быть целым числом от 0 до 10\n'
                      'Попробуйте еще раз :)\nЕсли вы хотите прервать '
                      '- отправьте команду /cancel',
    'warning_price': 'Цена должен быть целым числом, без приставки "руб", Максимальная цена 10000\n'
                     'Попробуйте еще раз :)\nЕсли вы хотите прервать '
                     '- отправьте команду /cancel',

}

LEXICON_TEXT: dict[str, str] = {
    '/start': '<b>Привет, мой друг!</b>\n\nЭто пивной бот, в котором '
              'ты можешь просмотреть пиво своих друзей, оценить раличные марки пиво'
              ' и оставить свое мнение.\n\n'
              'Чтобы посмотреть список доступных '
              'команд - нажми --> /help',
    '/help': '<b>Это пивной-бот</b>\n\nДоступные команды:\n\n/start - '
             'начать использование бота\n'
             '/help - справка по работе бота\n\n'
             'Пользователь может удалять только свои заметки о пиве,'
             ' администратор может это делать за всех пользователей. \n\n'
             'Обратите внимание что у БОТ-а в режиме общение из группы доступен только поиск и просмотр напитков, '
             'для добавленеи напитков обращаться боту нужно в личные сообщения'
             '\n<b>Приятного испозования!</b>',
}

LEXICON_MENU: dict[str, str] = {
    '/start': 'Запустить пивного бота',
    '/help': 'Вызвать справка по работе с ботом',
    '/admin': 'Авторизоваться администратором бота',
    '/cancel': 'Отмена'
}
