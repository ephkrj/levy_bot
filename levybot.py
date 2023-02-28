import logging
from telegram import Update
from telegram.ext import filters, ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler
import datetime

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Hi " + update.message.from_user.first_name + "! I'm a bot service to update you on the issues regarding migrant domestic worker levies.")

async def outstanding(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Reveals how much levy is left outstanding for the employer."""
    await update.message.reply_text("As of "+datetime.datetime.now().strftime("%Y-%m-%d %H:%M")+", there is currently $200 outstanding in your account.")

async def history(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends out message about the payment history over the past 6 months."""
    await update.message.reply_text("#############################\n Month: Jan 2023\n Status: Levy paid. \n Payment Amt: $200 \n Payment Mode: Giro\n#############################\n" + 
                                    " Month: Feb 2023\n Status: Levy paid. \n Payment Amt: $200 \n Payment Mode: Giro\n#############################\n" +
                                    " Month: Mar 2023\n Status: Levy paid. \n Payment Amt: $200 \n Payment Mode: Giro\n#############################\n" )

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

async def phone_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Please call +6564385122 to speak to our friendly officers for further enquires. \n Alternatively, you could visit https://www.mom.gov.sg/passes-and-permits/work-permit-for-foreign-domestic-worker/foreign-domestic-worker-levy/paying-levy for more information about the levy payment process.")

if __name__ == '__main__':
    application = ApplicationBuilder().token('6039231535:AAHdtbOOWGuuV3EioWZlYc9O0GuZldgnIo0').build()
    
    start_handler = CommandHandler('start', start)
    out_handler = CommandHandler('payment_due', outstanding)
    hist_handler = CommandHandler('history', history)
    phone_handler = CommandHandler('enquiry', phone_number)
    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    application.add_handler(start_handler)
    application.add_handler(out_handler)
    application.add_handler(hist_handler)
    application.add_handler(phone_handler)
    application.add_handler(unknown_handler)
    
    application.run_polling()