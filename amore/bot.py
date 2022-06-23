import requests as req
import telegram

TOKEN = '5135529791:AAH-fYwE0F467F2oUOdcoRbtHk2bN8Idrz0'

url = 'https://api.telegram.org/bot{token}/{method}'

if __name__ == '__main__':
    # url_req = url.format(token=TOKEN, method='sendMessage')
    # print(url_req)


    # msg = str(input())
    # params = {
    #     'chat_id':133926322,
    #     'text': msg
    # }
    # response = req.get(url_req, params=params)
    # print(response.content)

    bot = telegram.Bot(token=TOKEN)
    print(bot.get_me())

    