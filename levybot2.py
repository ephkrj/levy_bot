import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import filters, ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, CallbackQueryHandler, CallbackContext
import datetime
import openai

openai.api_key = "api-token"
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("Outstanding", callback_data='outstanding')],
                [InlineKeyboardButton("History", callback_data='history')],
                [InlineKeyboardButton("Phone number", callback_data='phone_number')],
                [InlineKeyboardButton("Chat", callback_data='chat')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Hi " + update.message.from_user.first_name + "! I'm a bot service to update you on the issues regarding migrant domestic worker levies.")
    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text="You have just renewed your work permit for your existing migrant domestic worker. Please note that late payment of your foreign worker levy will result in a late payment penalty. For more information about the penalties, please see https://www.mom.gov.sg/passes-and-permits/work-permit-for-foreign-worker/foreign-worker-levy/paying-the-levy.",
        reply_markup=reply_markup
    )

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("Outstanding", callback_data='outstanding')],
                [InlineKeyboardButton("History", callback_data='history')],
                [InlineKeyboardButton("Phone number", callback_data='phone_number')],
                [InlineKeyboardButton("Chat", callback_data='chat')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(chat_id=update.effective_chat.id, text='Menu', reply_markup=reply_markup)


async def test_notice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="10 March 2023: 7 days until your foreign worker levy is due.")
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Amount due: $300\n Payment due date: 17 March 2023\n Your bill will be deducted from OCBC account XXX-XXX-XXX-123 via GIRO payment.")
    await context.bot.send_message(chat_id=update.effective_chat.id, text="To avoid payment failure and a $20 dollar penalty please ensure sufficient balance in your account. Thank you!")

async def nomoney(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="18 March 2023: Your payment transaction of $300 via GIRO was unsuccessful. Please review your outstanding payment at https://www.mom.gov.sg/eservices/services/check-and-pay-levy and make payment immediately to avoid legal action.")

async def outstanding(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Reveals how much levy is left outstanding for the employer."""
    keyboard = [[InlineKeyboardButton("Back to menu", callback_data='menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="As of "+datetime.datetime.now().strftime("%Y-%m-%d %H:%M")+", there is currently $200 outstanding in your account.", reply_markup=reply_markup)

async def history(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends out message about the payment history over the past 6 months."""
    keyboard = [[InlineKeyboardButton("Back to menu", callback_data='menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="#############################\n Month: Jan 2023\n Status: Levy paid. \n Payment Amt: $200 \n Payment Mode: Giro\n#############################\n" + 
                                    " Month: Feb 2023\n Status: Levy paid. \n Payment Amt: $200 \n Payment Mode: Giro\n#############################\n" +
                                    " Month: Mar 2023\n Status: Levy paid. \n Payment Amt: $200 \n Payment Mode: Giro\n#############################\n", reply_markup=reply_markup)

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

async def phone_number(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends out message about the payment history over the past 6 months."""
    keyboard = [[InlineKeyboardButton("Back to menu", callback_data='menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Please contact MOM at 1800-233-6688 for any enquiries regarding your levy payments.", reply_markup=reply_markup
    )

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends out message about the payment history over the past 6 months."""
    keyboard = [[InlineKeyboardButton("Back to menu", callback_data='menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    start_message = "Hi I'm Ah Girl, how can I help you today?"
    # Get previous user input from context.user_data
    convo = context.user_data.get('previous_input', '')
    if len(convo) == 0:
        convo = "The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly. AI: " + start_message + " Human: "
    elif len(convo) >= 1000:
        convo = "The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly." + convo[-500:]

    if update.message and update.message.text:
        prompt = convo + update.message.text + " AI: "
        print('prompt: ', prompt)
        response = openai.Completion.create(
                    model="text-davinci-003",
                    prompt=prompt,
                    temperature=0.9,
                    max_tokens=150,
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0.6,
                    stop=[" Human:", " AI:"]
                )
        print('response: ', response)
        await update.message.reply_text(response.choices[0].text.strip(), reply_markup=reply_markup)
        
        convo = convo + update.message.text + " AI: " + response.choices[0].text.strip() + " Human: "
        context.user_data['previous_input'] = convo

    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=start_message, 
            reply_markup=reply_markup
        )
        


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    if query.data == "outstanding":
        await outstanding(update, context)
    elif query.data == "history":
        await history(update, context)
    elif query.data == "phone_number":
        await phone_number(update, context)
    elif query.data == "chat":
        await chat(update, context)
    elif query.data == "menu":
        await menu(update, context)


if __name__ == '__main__':
    application = ApplicationBuilder().token('telegram.bot.token').build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("test_notice", test_notice))
    application.add_handler(CommandHandler("nomoney", nomoney))
    application.add_handler(MessageHandler(filters.TEXT, chat))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.COMMAND, unknown))
    application.add_handler(CommandHandler('simulation1', test_notice))
    application.add_handler(CommandHandler('simulation2', nomoney))
    application.run_polling()

    
