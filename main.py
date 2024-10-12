import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, ReplyFilter
from aiogram.types import ChatPermissions
from aiogram import F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.enums import ChatMemberStatus
import os

API_TOKEN = 'your bot token' 
PHOTO_PATH = 'image.jpg'  

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

async def is_admin(chat_id: int, user_id: int) -> bool:
    member = await bot.get_chat_member(chat_id, user_id)
    return member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]

@dp.message(F.new_chat_members)
async def welcome_new_member(message: types.Message):
    for new_member in message.new_chat_members:
        with open(PHOTO_PATH, 'rb') as image:
            await bot.send_photo(message.chat.id, image, caption="{new_member.first_name}, дарова чувачок")

@dp.message(Command('ban'), F.reply_to_message)
async def ban_user(message: types.Message):
    if not await is_admin(message.chat.id, message.from_user.id):
        await message.answer("куда мы лезем")
        return
    
    target_user = message.reply_to_message.from_user
    reason = message.text.split(' ', 1)[1] if len(message.text.split()) > 1 else "причина не указана"
    
    await bot.kick_chat_member(message.chat.id, target_user.id)
    await message.answer(f"чувак {target_user.first_name} был забанен.\nПричина: {reason}")
    
    try:
        await bot.send_message(target_user.id, f"ты был забанен в чате {message.chat.title}.\nпричина: {reason}")
    except Exception as e:
        logging.error(f"Не удалось отправить сообщение пользователю {target_user.id}: {e}")
      
@dp.message(Command('unban'), F.reply_to_message)
async def unban_user(message: types.Message):
    if not await is_admin(message.chat.id, message.from_user.id):
        await message.answer("куда мы лезем")
        return

    target_user = message.reply_to_message.from_user
    await bot.unban_chat_member(message.chat.id, target_user.id)
    await message.answer(f"чувак {target_user.first_name} был разбанен.")
  
@dp.message(Command('mute'), F.reply_to_message)
async def mute_user(message: types.Message):
    if not await is_admin(message.chat.id, message.from_user.id):
        await message.answer("куда мы лезем")
        return
    
    target_user = message.reply_to_message.from_user
    reason = message.text.split(' ', 1)[1] if len(message.text.split()) > 1 else "причина не указана"
    
    mute_permissions = ChatPermissions(can_send_messages=False)
    await bot.restrict_chat_member(message.chat.id, target_user.id, permissions=mute_permissions)
    await message.answer(f"чувак {target_user.first_name} был замучен.\nПричина: {reason}")
    
    try:
        await bot.send_message(target_user.id, f"ты был замучен в чате {message.chat.title}.\nпричина: {reason}")
    except Exception as e:
        logging.error(f"Не удалось отправить сообщение пользователю {target_user.id}: {e}")

@dp.message(Command('kick'), F.reply_to_message)
async def kick_user(message: types.Message):
    if not await is_admin(message.chat.id, message.from_user.id):
        await message.answer("куда мы лезем")
        return
    
    target_user = message.reply_to_message.from_user
    reason = message.text.split(' ', 1)[1] if len(message.text.split()) > 1 else "причина не указана"
    
    await bot.kick_chat_member(message.chat.id, target_user.id)
    await message.answer(f"чувак {target_user.first_name} был кикнут.\nПричина: {reason}")
    
    try:
        await bot.send_message(target_user.id, f"ты был кикнут из чата {message.chat.title}.\nпричина: {reason}")
    except Exception as e:
        logging.error(f"Не удалось отправить сообщение пользователю {target_user.id}: {e}")

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
