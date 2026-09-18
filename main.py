import asyncio
from aiogram import Bot, Dispatcher, types
API_TOKEN = '8677878265:AAFJ2GMXaDerzMzaR6dzgwk-fhDslWvxTa0'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    
    button_buy = types.InlineKeyboardButton(text="Buy Now", callback_data="menu_shop", style="danger")
    button_update = types.InlineKeyboardButton(text="Check Update", callback_data="menu_update", style="danger")
    button_balance = types.InlineKeyboardButton(text="Add Balance", callback_data="menu_add_balance", style="danger")
    button_profile = types.InlineKeyboardButton(text="My Profile", callback_data="menu_profile", style="danger")
    button_refer = types.InlineKeyboardButton(text="Refer And Earn", callback_data="menu_refer", style="danger")
    button_help = types.InlineKeyboardButton(text="How To Use Bot", callback_data="menu_help", style="danger")
    button_support = types.InlineKeyboardButton(text="Support", callback_data="menu_support", style="danger")
    button_gift = types.InlineKeyboardButton(text="Daily Gift", callback_data="menu_gift", style="danger")
    
    keyboard.add(button_buy, button_update, button_balance, button_profile, button_refer, button_help, button_support, button_gift)
    await message.reply("SAHIL BHAI STORE.", reply_markup=keyboard)
@dp.callback_query_handler(lambda call: True)
async def callback_handler(call: types.CallbackQuery):
    await call.answer(f"You clicked: {call.data}")
    await call.message.answer(f"You selected: {call.data}")
    ADMIN_ID = 8395533259  # यहाँ अपनी Telegram ID डालें

@dp.message_handler(commands=['admin'])
async def admin_command(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        await message.reply("Welcome, Admin! You can now manage your bot.")
    else:
        await message.reply("You are not authorized to use this command.")

@dp.message_handler(commands=['broadcast'])
async def broadcast_command(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        # यहाँ ब्रॉडकास्ट लॉजिक आएगा
        await message.reply("Broadcast functionality is being implemented.")
if __name__ == '__main__': from aiogram import executor; executor.start_polling(dp, skip_updates=True)
