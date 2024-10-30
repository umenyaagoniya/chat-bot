import os
import sys
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

API_TOKEN = 'YOUR_BOT_TOKEN'
ADMIN_ID = 123456789  # Замените на ваш Telegram ID (ID создателя бота)

# Настройка бота
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['restart'])
async def restart(message: types.Message):
    # Проверка, является ли пользователь администратором
    if message.from_user.id != ADMIN_ID:
        await message.reply("У вас нет доступа к этой команде.")
        return
    
    await message.reply("Бот перезапускается...")
    
    # Перезапуск бота
    os.execv(sys.executable, [sys.executable] + sys.argv)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
