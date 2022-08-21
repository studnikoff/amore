import emoji
import logging
import datetime
from telegram import Update, Bot
from telegram.ext import Updater, Filters
from telegram.ext import CallbackContext, CommandHandler, MessageHandler
from telegram.error import Unauthorized

from amore.generator import Generator
from amore.compliments_db import Chat, get_chats, save_chat, check_chat_existence
import amore.utility as util

logging.basicConfig(level=logging.DEBUG,
                    format='[%(asctime)s]  %(name)s  %(levelname)s: %(message)s',
                    filename='data/amore.log')

TOKEN = '5135529791:AAH-fYwE0F467F2oUOdcoRbtHk2bN8Idrz0'
URL = 'https://api.telegram.org/bot{token}/{method}'

updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher


def message_for_her(*args, **kwargs):
    bot = Bot(TOKEN)

    chat_ids = get_chats()
    if len(chat_ids) == 0:
        return 0

    
    gen = Generator(scale=0.3)
    try:
        cmpl = gen.choose_compliment()
    except:
        cmpl = None
        text = "Просто не существует слов, чтобы описать тебя (ошибка или бд пустая) :heart:"
        logging.exception("Fill database with compliments".upper())
    if cmpl is None:
        text = "Просто не существует слов, чтобы описать тебя (база данных пустая просто) :heart:"
    elif cmpl.rarity == 1:
        text = f'Обычный комплимент\n{util.SUN*5}\n{cmpl.value}'
    elif cmpl.rarity == 2:
        text = f'Необычный комплимент\n{util.HEART*5}\n{cmpl.value}'
    elif cmpl.rarity == 3:
        text = f'Редкий комплимент\n{util.GEM*5}\n{cmpl.value}'
    elif cmpl.rarity == 4:
        text = f'Вероятность этого комплимента буквально 0 -__-\n{util.RING*5}\n{cmpl.value}'

    msg = emoji.emojize(text, language='alias')

    for chat_id in chat_ids:
        try:
            bot.send_message(chat_id=chat_id, text=msg)
        except Unauthorized:
            logging.exception(f"Bot has been blocked by {chat_id}")

def start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    logging.debug(f'Update: {update}, {type(update)}')
    logging.debug(f'Context: {context}, {type(context)}')

    chat = update.message.chat.to_dict()
    chat.pop('type')
    chat['chat_id'] = chat.pop('id')
    chat = Chat(**chat)
    save_chat(chat)
    
    text = emoji.emojize("Мммм, да это же самая красивая девушка на свете пишет :heart:",
                         language='alias')
    context.bot.send_message(chat_id=chat.chat_id, 
                             text=text)

def chats_stat(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    chats = get_chats()
    text = f"Всего чатов создано: {str(len(chats))}. Их id: {str(chats)}"
    context.bot.send_message(chat_id=chat_id, 
                             text=text)

def send_answer(update: Update, context: CallbackContext):
    text = "К сожалению, я пока ещё не умею отвечать :cry: \nНо в будущем возможно научусь! :smile:"
    context.bot.send_message(chat_id=update.effective_chat.id, 
                             text=emoji.emojize(text, language='alias'))

def start_bot():
    logging.info("Bot start")

    logging.info("start handler")
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    logging.info("chats_stat handler")
    chats_stat_handler = CommandHandler('chats_stat', chats_stat)
    dispatcher.add_handler(chats_stat_handler)

    logging.info("force_send_message handler")
    force_send_message = CommandHandler('force_send_message', message_for_her)
    dispatcher.add_handler(force_send_message)

    logging.info("answer handler")
    send_answer_handler = MessageHandler(Filters.text & (~Filters.command), send_answer)
    dispatcher.add_handler(send_answer_handler)

    job = updater.job_queue
    logging.debug("Set schedule")
    # Moscow: UTC+3:00, TODO: tzinfo
    job.run_daily(message_for_her, datetime.time(4, 0, 0, tzinfo=None)) # Time in UTC

    updater.start_polling()

    