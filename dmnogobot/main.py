#!/usr/bin/python3.4
# -*- coding: utf-8 -*-

import telebot
import cherrypy
import numpy as np
import os
from PIL import Image, ImageFont, ImageDraw

WEBHOOK_HOST = '127.0.0.1'
WEBHOOK_PORT = 7772
WEBHOOK_LISTEN = '127.0.0.1'
WEBHOOK_ROUTE = 'dmnogobot'

WEBHOOK_URL = 'https://{}/{}/'.format(WEBHOOK_HOST, WEBHOOK_ROUTE)

BOT_TOKEN = 'INSERT-YOUR-TOKEN-HERE'

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


@bot.message_handler(commands=['dd'])
def get_random_answer(message):
    if len(message.text.split()) != 2:
        bot.reply_to(message, "Too few arguments")
        return
    arg = message.text.split()[1]
    try:
        arg = int(arg)
    except ValueError:
        bot.reply_to(message, "Not a number")
        return
    rand = np.random.randint(1, arg)
    if arg > 99999:
        bot.reply_to(message, "Argument too big. Maximum value: 99999")
        return

    font_size = 80

    img = Image.open('img/base_img.jpg')
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("font.ttf", font_size)

    character_size = font_size / 2.3
    space_size = font_size / 5.714

    draw.text((img.width / 2 - (character_size * len(str(rand)) + space_size * len(str(rand))) / 2 + 3,
               img.height / 2 - font.size / 2), str(rand), (0, 0, 0), font=font)
    img.save("img/new_img.jpg", 'JPEG')
    photo = open('img/new_img.jpg', 'rb')
    bot.send_photo(message.chat.id, photo)
    photo.close()
    # os.remove('img/new_img.jpg')

bot.remove_webhook()

bot.set_webhook(url=WEBHOOK_URL)

cherrypy.config.update({
    'server.socket_host': WEBHOOK_LISTEN,
    'server.socket_port': WEBHOOK_PORT,
    'server.ssl_module': 'builtin',
})

cherrypy.quickstart(WebhookServer(), '/', {'/': {}})
