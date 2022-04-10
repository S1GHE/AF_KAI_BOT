from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

status_menu = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton(text="Я студент 👨‍🎓"),
            KeyboardButton(text="Я преподаватель 👨‍🏫")
        ]
    ], resize_keyboard=True
)
confirmation_menu = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton(text="Да ✅"),
            KeyboardButton(text="Нет ❌")
        ]
    ], resize_keyboard=True
)
les_menu = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton(text="Ваше расписание")
        ],
        [
            KeyboardButton(text="Расписание преподавателя")
        ],
        [
            KeyboardButton(text="Расписание по номеру группы")
        ],
        [
            KeyboardButton(text="Выйти")
        ]
    ], resize_keyboard=True
)
your_less_menu = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton(text="Вчера")
        ],
        [
            KeyboardButton(text="Сегодня")
        ],
        [
            KeyboardButton(text="Завтра")
        ],
        [
            KeyboardButton(text="Назад")
        ]
    ], resize_keyboard=True
)
