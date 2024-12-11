from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
import logging
import random

from config import API_TOKEN, CHANNEL_ID

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
router = Router()
dp = Dispatcher()
dp.include_router(router)

# Кнопка "НАЧАТЬ"
start_inline_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="НАЧАТЬ", callback_data="start_interaction")]
    ]
)

@router.message(F.text == "/start")
async def start_command(message: types.Message):
    response1 = "Здравствуйте! Я - бот \"Газпром энергосбыт Тюмень\", ваш надежный помощник в активации услуг. Я готов помочь вам и оперативно решить все возникающие задачи."
    response2 = "Чтобы использовать бот, нажмите здесь:"
    await message.answer(response1)
    await message.answer(response2, reply_markup=start_inline_keyboard)

@router.callback_query(F.data == "start_interaction")
async def handle_start_button(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text("Теперь вы можете отправить фото или файл.")

@router.message(F.content_type.in_({'photo', 'document'}))
async def handle_media(message: types.Message):
    if message.photo:
        file_id = message.photo[-1].file_id
    else:
        file_id = message.document.file_id

    random_code = random.randint(1000, 9999)

    try:
        if message.photo:
            await bot.send_photo(CHANNEL_ID, file_id, caption=f"Новое фото от пользователя. Код: {random_code}")
        else:
            await bot.send_document(CHANNEL_ID, file_id, caption=f"Новый файл от пользователя. Код: {random_code}")

        await message.answer(f"Спасибо, файл был успешно отправлен. Ваш код: {random_code}")
        await message.answer("Хотите отправить еще раз? Нажмите сюда:", reply_markup=start_inline_keyboard)
    except Exception as e:
        logging.error(f"Ошибка при отправке файла в канал: {e}")
        await message.answer("Произошла ошибка при отправке файла. Попробуйте еще раз.", reply_markup=start_inline_keyboard)

@router.message()
async def handle_other_messages(message: types.Message):
    await message.answer("Пожалуйста, отправьте фото или файл.")

async def main():
    await bot.delete_webhook()  # Удаление вебхука
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
