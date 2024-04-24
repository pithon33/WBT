import logging
from strings import RESPONSE_MSG, HELP_MSG, HELLO_MSG, NOT_WORD_MSG, START_MSG
from word import Word
from config import BOT_TOKEN
from telegram import ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def start(update, context) -> None:
    """Обработчик /start"""
    first_name = update.effective_user.first_name
    update.message.reply_text(START_MSG.format(first_name),
                              parse_mode=ParseMode.HTML)


def hi(update, context) -> None:
    """Обработчик /hi"""
    update.message.reply_text(HELLO_MSG)


def help_(update, context) -> None:
    """Обработчик /help """
    update.message.reply_text(HELP_MSG)


def analyse(update, context) -> None:
    """Анализ сообщений"""
    my_word = Word(update.message.text)


    unique_letters_string = ''
    for key in my_word.unique_letters:
        unique_letters_string += ("%d x %s, " % (my_word.unique_letters[key], key))
    unique_letters_string = unique_letters_string.rstrip(', ')

    if len(my_word.most_frequent_letters) > 1:
        frequent_letters_string = ("буквы - это %s с вхождениями %d в каждой" % (
            ' и '.join(my_word.most_frequent_letters), my_word.most_frequent_letters_count))
    else:
        frequent_letters_string = ("буква %s с вхождениями %d" % (
            ''.join(my_word.most_frequent_letters), my_word.most_frequent_letters_count))

    update.message.reply_text(RESPONSE_MSG.format(my_word.word,
                                                  my_word.length,
                                                  my_word.vowels_count,
                                                  my_word.consonants_count,
                                                  len(my_word.unique_letters),
                                                  unique_letters_string,
                                                  frequent_letters_string
                                                  ))


def error(update, context) -> None:
    """Логирование ошибок"""
    logger.warning('Обновление "%s" вызвало ошибку "%s"', update, context.error)


def main():
    """Запуск бота"""

    updater = Updater(BOT_TOKEN, use_context=True)

    # Диспетчер
    dp = updater.dispatcher

    # Команды
    dp.add_handler(CommandHandler("hi", hi))
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_))

    dp.add_handler(MessageHandler(Filters.text, analyse))

    # log
    dp.add_error_handler(error)

    # Start
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
