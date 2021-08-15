from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import json
import csv
from fetch_form import search_someone

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
  
f = open('config.json',)
data = json.load(f)
f.close()

wa_links_file = open("gruplar.csv",encoding='utf-8')
wa_links = list(csv.reader(wa_links_file,delimiter=','))
wa_links_file.close()

token = data["telegram_token"]

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def groups(update, context):
    chat_data = update["message"]["from_user"]
    try:
        result = search_someone(chat_data["username"])
        if(result):
            for i in wa_links:
                if(i[0] == result[7]):
                    message = "{} için aşağıdaki bölüm gruplarına katılabilirsin!\n\n {}\n\nFakülte grupları için de aşağıdaki bağlantıları kullanabilirsin!\n\n{}\n\nGenel okul gruplarına katılmayı da unutma ;)\n\n{}".format(i[0],i[1].replace(" ","\n"),i[2].replace(" ","\n"),f"{i[3]}\nhttps://t.me/ytu2021girisliler")
                    update.message.reply_text(message)
                    return 
            update.message.reply_text("Bölümün için kurulmuş grup bulamadık! Bizimle sosyal medya hesaplarımı üzerinden iletişime geç!")
        else:
            update.message.reply_text(f"Üzgünüm {chat_data.first_name} ama adına bir başvuru bulamadık. Formu tekrar doldurur musun?\n\nhttps://forms.gle/4C24TSRFMSBRLRoAA")
    except NameError as e:
        update.message.reply_text(f"Bir sorunla karşılaştık :'( en kısa zamanda çözmeye çalışacağız")

def commands(update,context):
     update.message.reply_text(f"Bot ile kullanabileceğin komutlar şu şekilde:\n /gruplar => Bölümünle ilgili gruplara girmeni sağlar\n /komutlar => Bot ile kullanabileceğin komutları görmeni sağlar\n /linkler => Okul hayatında yardımcı olabilecek linkleri görebilirsin")
    
def links(update,context):
    update.message.reply_text(f"Bizi sosyal medya hesaplarımızdan takip edebilirsin:\nhttps://www.instagram.com/ytu2021giris/\nhttps://twitter.com/ytu2021giris/\n\nBölüm hakkında sorularını Pusulam Yıldız'a iletebilirsin:\nhttps://bit.ly/3yOV4mM\n\nYıldızlıların mobil uygulaması, Yıldız Cep!\nhttps://yildizcep.com")

def start(update, context):
    first_name = update["message"]["from_user"]["first_name"]
    update.message.reply_text(f"Merhaba {first_name}!\nGruplara katılabilmen için https://forms.gle/4C24TSRFMSBRLRoAA formu doldurmalısın! Sonrasında /gruplar komutu ile katılabileceğin Whatsapp ve Telegram gruplarının bağlantılarını alabilirsin!\n\n Kullanabileceğin diğer komutlar için /komutlar")


def main():
    updater = Updater(token, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("gruplar", groups))
    dp.add_handler(CommandHandler("komutlar", commands))
    dp.add_handler(CommandHandler("linkler", links))
    dp.add_handler(CommandHandler("help",commands))

    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()