import telebot
from telebot import types
from cryptography.fernet import Fernet
import logging
import os

# Проврека верности пути файла
log_path = "YOUR LOG FILE"
os.makedirs(os.path.dirname(log_path), exist_ok=True)


# Функция логирования
logging.basicConfig(level=logging.INFO, filename=log_path,
                    format="%(asctime)s - %(name)s - %(message)s")
logger = logging.getLogger()

# Отвечает за запуск и апи
API_TOKEN = '[YOU API KEY]'
bot = telebot.TeleBot(API_TOKEN)

# Генерация ключа для шифрования
key = Fernet.generate_key()
fernet = Fernet(key)

# все текстовые кнопки
def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Шифрование текста")
    btn2 = types.KeyboardButton("Дешифрование текста")
    markup.add(btn1, btn2)
    return markup

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Добро пожаловать! Выберите действие:", reply_markup=main_menu())

# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text == "Шифрование текста":
        msg = bot.reply_to(message, "Введите текст для шифрования:")
        bot.register_next_step_handler(msg, encrypt_text)
    elif message.text == "Дешифрование текста":
        msg = bot.reply_to(message, "Введите зашифрованный текст:")
        bot.register_next_step_handler(msg, decrypt_text)
    else:
        bot.reply_to(message, "Неверный выбор. Пожалуйста попробуйте снова.", reply_markup=main_menu())

# Функция шифрования текста
def encrypt_text(message):
    try:
        encrypted_message = fernet.encrypt(message.text.encode())
        bot.reply_to(message, f"Зашифрованный текст: {encrypted_message.decode()}", reply_markup=main_menu())
        logger.info(f"User: {message.from_user.username}, Encrypted: {message.text}, Result: {encrypted_message.decode()}")
    except Exception as e:
        bot.reply_to(message, "Произошла ошибка при шифровании текста.", reply_markup=main_menu())
        logger.error(f"User: {message.from_user.username}, Error: {str(e)}")

# Функция дешифрования текста
def decrypt_text(message):
    try:
        decrypted_message = fernet.decrypt(message.text.encode()).decode()
        bot.reply_to(message, f"Дешифрованный текст: {decrypted_message}", reply_markup=main_menu())
        logger.info(f"User: {message.from_user.username}, Decrypted: {message.text}, Result: {decrypted_message}")
    except Exception as e:
        bot.reply_to(message, "Произошла ошибка при дешифровании текста.", reply_markup=main_menu())
        logger.error(f"User: {message.from_user.username}, Error: {str(e)}")

bot.polling()
