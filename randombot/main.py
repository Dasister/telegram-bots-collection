#!/usr/bin/python3.4
# -*- coding: utf-8 -*-

import telebot
import cherrypy
import numpy as np

WEBHOOK_HOST = '127.0.0.1'
WEBHOOK_PORT = 7771
WEBHOOK_LISTEN = '127.0.0.1'
WEBHOOK_ROUTE = 'randombot'

WEBHOOK_URL = 'https://{}/{}/'.format(WEBHOOK_HOST, WEBHOOK_ROUTE)

BOT_TOKEN = 'INSERT-YOUR-TOKEN-HERE'

answers = [
    'YES',
    'NO',
    'Pishov nahooy! Ya tebe ne bot!',
    'Maybe YES',
    'Maybe NO',
    'Definitely YES',
    'Definitely NO',
    'Ask later'
]
bot = telebot.TeleBot(BOT_TOKEN)


class WebhookServer(object):
    @cherrypy.expose
    def index(self):
        if 'content-length' in cherrypy.request.headers and \
                        'content-type' in cherrypy.request.headers and \
                        cherrypy.request.headers['content-type'] == 'application/json':
            length = int(cherrypy.request.headers['content-length'])
            json_string = cherrypy.request.body.read(length).decode("utf-8")
            update = telebot.types.Update.de_json(json_string)
            # Эта функция обеспечивает проверку входящего сообщения
            bot.process_new_updates([update])
            return ''
        else:
            raise cherrypy.HTTPError(403)


@bot.message_handler(commands=['random'])
def get_random_answer(message):
    bot.send_message(message.chat.id, np.random.choice(answers, p=[0.25, 0.25, 0.01, 0.10, 0.10, 0.10, 0.10, 0.09]))

bot.remove_webhook()
bot.set_webhook(url=WEBHOOK_URL)

cherrypy.config.update({
    'server.socket_host': WEBHOOK_LISTEN,
    'server.socket_port': WEBHOOK_PORT,
    'server.ssl_module': 'builtin',
})

cherrypy.quickstart(WebhookServer(), '/', {'/': {}})

