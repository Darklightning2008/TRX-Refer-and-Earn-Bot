import json
import telebot

## TOKEN DETAILS
TOKEN = "Credit"

BOT_TOKEN = "6311818634:AAEnyN8OPYmwwOWNVk4B_KvBL7XR72Le8tE"
PAYMENT_CHANNEL = "@payout22234"  # add payment channel here including the '@' sign
OWNER_ID = 6097439527  # write owner's user id here.. get it from @MissRose_Bot by /id
Per_Refer = 0.5  # add per refer bonus here

bot = telebot.TeleBot(BOT_TOKEN)


def menu(id):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('🆔 Account')
    keyboard.row('🙌🏻 Referrals', '💸 Withdraw')
    keyboard.row('📊 Statistics')
    bot.send_message(id, "*🏡 Home*", parse_mode="Markdown", reply_markup=keyboard)


@bot.message_handler(commands=['start'])
def start(message):
    try:
        user = str(message.chat.id)
        data = json.load(open('users.json', 'r'))

        if user not in data['referred']:
            data['referred'][user] = 0
            data['total'] = data['total'] + 1

        if user not in data['referby']:
            data['referby'][user] = user

        # Add more initialization checks here...

        json.dump(data, open('users.json', 'w'))
        menu(message.chat.id)
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, "An error occurred. Please try again later.")
        bot.send_message(OWNER_ID, "Your bot encountered an error on command: /start")


@bot.message_handler(content_types=['text'])
def send_text(message):
    try:
        if message.text == '💸 Withdraw':
            user_id = message.chat.id
            user = str(user_id)

            data = json.load(open('users.json', 'r'))

            if user not in data['balance']:
                data['balance'][user] = 0

            json.dump(data, open('users.json', 'w'))

            bal = data['balance'][user]

            markup = telebot.types.InlineKeyboardMarkup()
            markup.row(telebot.types.InlineKeyboardButton('Crunchyroll bin - 3 credits', callback_data='bin'),
                       telebot.types.InlineKeyboardButton('Crunchyroll account (1 month) - 5 credits', callback_data='account'))

            bot.send_message(user_id,
                             f"Hello {message.from_user.first_name}!\n\nAvailable credits: {bal}\n\nWithdrawal:",
                             reply_markup=markup)

        # Add more message handlers for other commands...
        elif message.text == '🆔 Account':
            data = json.load(open('users.json', 'r'))
            accmsg = '*👮 User : {}\n\n⚙️ Wallet : *`{}`*\n\n💸 Balance : *`{}`* {}*'
            user_id = message.chat.id
            user = str(user_id)

            if user not in data['balance']:
                data['balance'][user] = 0

            json.dump(data, open('users.json', 'w'))

            balance = data['balance'][user]
            msg = accmsg.format(message.from_user.first_name,
                                "N/A", balance, TOKEN)
            bot.send_message(message.chat.id, msg, parse_mode="Markdown")

        elif message.text == '🙌🏻 Referrals':
            data = json.load(open('users.json', 'r'))
            ref_msg = "*⏯️ Total Invites : {} Users\n\n👥 Referrals System\n\n1 Level:\n🥇 Level°1 - {} {}\n\n🔗 Referral Link ⬇️\n{}*"

            bot_name = bot.get_me().username
            user_id = message.chat.id
            user = str(user_id)

            if user not in data['referred']:
                data['referred'][user] = 0

            json.dump(data, open('users.json', 'w'))

            ref_count = data['referred'][user]
            ref_link = 'https://telegram.me/{}?start={}'.format(
                bot_name, message.chat.id)
            msg = ref_msg.format(ref_count, Per_Refer, TOKEN, ref_link)
            bot.send_message(message.chat.id, msg, parse_mode="Markdown")

        elif message.text == "📊 Statistics":
            user_id = message.chat.id
            user = str(user_id)
            data = json.load(open('users.json', 'r'))
            msg = "*📊 Total members : {} Users\n\n🥊 Total successful Withdraw : {} {}*"
            msg = msg.format(data['total'], data['totalwith'], TOKEN)
            bot.send_message(user_id, msg, parse_mode="Markdown")
            return

    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, "An error occurred. Please try again later.")
        bot.send_message(OWNER_ID, "Your bot encountered an error on command: " + message.text)


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    try:
        user_id = call.message.chat.id
        user = str(user_id)
        data = json.load(open('users.json', 'r'))

        if user not in data['balance']:
            data['balance'][user] = 0

        if call.data == 'bin':
            if data['balance'][user] >= 3:
                data['balance'][user] -= 3
                json.dump(data, open('users.json', 'w'))
                bot.send_message(user_id, "Crunchyroll bin requested.",
                                 reply_markup=telebot.types.ReplyKeyboardRemove())
                bot.send_message(PAYMENT_CHANNEL,
                                 f"New Crunchyroll bin requested\nUser - {user_id}\nPowered by - @{bot.get_me().username}")
            else:
                bot.send_message(user_id, "You don't have required credits, Kindly refer and earn more.")
        elif call.data == 'account':
            if data['balance'][user] >= 5:
                data['balance'][user] -= 5
                json.dump(data, open('users.json', 'w'))
                bot.send_message(user_id, "Crunchyroll account (1 month) requested.",
                                 reply_markup=telebot.types.ReplyKeyboardRemove())
                bot.send_message(PAYMENT_CHANNEL,
                                 f"New Crunchyroll account (1 month) requested\nUser - {user_id}\nPowered by - @{bot.get_me().username}")
            else:
                bot.send_message(user_id, "You don't have required credits, Kindly refer and earn more.")
    except Exception as e:
        print(e)
        bot.send_message(user_id, "An error occurred. Please try again later.")
        bot.send_message(OWNER_ID, "Your bot encountered an error in callback handler.")


print("BOT IS ALIVE")

if __name__ == '__main__':
    bot.polling(none_stop=True)
