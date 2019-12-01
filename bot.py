from secret import TOKEN
from config import *
from telebot import types
import telebot
from UseDB import opendb as db


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start_handler(message):
    if db().check_user(message.chat.id):
        answr = bot.send_message(message.chat.id, Welcome)
        bot.register_next_step_handler(answr, registration)
    else:
        bot.send_message(message.chat.id, WelcomeAgain)
        menu_handler(message)


def regestration(message):

    db().ins_user(message)
    gr_failture = bot.send_message(message.chat.id, config.completef)
    bot.register_next_step_handler(gr_failture, change_gr)



@bot.message_handler(commands=['help', 'menu'])
def menu_handler(message):
    if !db().check_user(message.chat.id):
        bot.send_message(message.chat.id, not_registered)
        start_handler(message)
    else:
        answ = 'Меню:'

        markup.telebot.typesReplyKeyboardMarkup()

        markup.row('Тесты')
        markup.row('Результаты')

        bot.send_message(message.chat.id, answ, reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == 'Тесты')
def test_choise(call):
    answ = 'Выберите тест:'
    markup = telebot.types.InlineKeyboardMarkup()

    frst_test = types.InlineKeyboardButton(text='Тест 1', callback_data='test1')
    scnd_test = types.InlineKeyboardButton(text='Тест 2', callback_data='test2')
    thrd_test = types.InlineKeyboardButton(text='Тест 3', callback_data='test3')

    markup.add(frst_test, scnd_test, thrd_test)

    bot.send_message(call.message.chat.id, answ, reply_markup=markup)


# Возвращает пользователю тест. Далее при ответе принимаем ответ в формате
# t%номер-теста%_%номер_вопроса%_%1/0%_%Всего баллов%
@bot.callback_query_handler(func=lambda call: 'test' in call.data)
def give_test(call):
    t_nmbr = call.data[0] + call.data[-1]
    markup = telebot.types.InlineKeyboardMarkup()

    question = tests[t_nmbr].keys()[0]
    answrs = tests[t_nmbr].keys()[0].keys()

    frst_answr = types.inlineKeyboard Button(text=answrs[0],
                        callback_data=f'{t_nmbr}_{1}_{tests[t_nmbr][answrs[0]]}_0')
    secnd_answr = types.inlineKeyboard Button(text=answrs[1],
                        callback_data=f'{t_nmbr}_{1}_{tests[t_nmbr][answrs[1]]}_0')
    thrd_answr = types.inlineKeyboard Button(text=answrs[2],
                        callback_data=f'{t_nmbr}_{1}_{tests[t_nmbr][answrs[2]]}_0')

    markup.add(frst_answr, secnd_answr, thrd_answr)

    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=question, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: 't1' in call.data or 't2' in call.data or 't3' in call.data)
def test_continue(call):
    t_nmbr, ask_nmbr, last_answ, right_answrs = call.data.split('_')
    right_answrs = int(right_answrs) + int(last_answ)

    question = tests[t_nmbr].keys()[int(ask_nmbr)]
    answrs = tests[t_nmbr].keys()[int(ask_nmbr)].keys()

    markup = telebot.types.InlineKeyboardMarkup()
    frst_answr = types.inlineKeyboard Button(text=answrs[0],
                        callback_data=f'{t_nmbr}_{int(ask_nmbr)+1}_{tests[t_nmbr][answrs[0]]}_{right_answrs}')
	secnd_answr = types.inlineKeyboard Button(text=answrs[1],
                        callback_data=f'{t_nmbr}_{int(ask_nmbr)+1}_{tests[t_nmbr][answrs[1]]}_{right_answrs}')
	thrd_answr = types.inlineKeyboard Button(text=answrs[2],
                        callback_data=f'{t_nmbr}_{int(ask_nmbr)+1}_{tests[t_nmbr][answrs[2]]}_{right_answrs}')

	bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=question, reply_markup=markup)

if __name__ == "__main__":
    bot.pooling(non_stop=True)
