import requests as req
import socket
import emoji
import telegram


TOKEN = '5135529791:AAH-fYwE0F467F2oUOdcoRbtHk2bN8Idrz0'
URL = 'https://api.telegram.org/bot{token}/{method}'

class Server():
    def __init__(self) -> None:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('', 1666))

    def get_addr(self) -> None:
        self.connection, _ = self.socket.accept()
    
    def send_message(self, msg: str) -> None:

        params = {
            'chat_id':133926322,
            'text': msg
        }
        bot = telegram.Bot(token=TOKEN)
        print(f'Message configuration: {params}')
        bot.send_message(params['chat_id'], emoji.emojize(params['text'], language='alias'))

    def run(self) -> None:
        self.socket.listen()
        while True:
            self.get_addr()
            with self.connection as con:
                msg = con.recv(1024)
                print(f'Raw mwg:\n{msg}')
                msg = msg.decode('utf-8')
                print(msg)
                self.send_message(msg)



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

    # bot = telegram.Bot(token=TOKEN)
    # print(bot.get_me())
    server = Server()
    print('Server starting...')
    server.run()

    