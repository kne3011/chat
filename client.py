from Socket import Socket
from datetime import datetime
from os import system
import asyncio

import mysql.connector as msql

conn = msql.connect(host='localhost', \
                    database='python', \
                    port=3306, \
                    user='root', \
                    password='')
cursor = conn.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS message(\
                m_id int(16) NOT NULL AUTO_INCREMENT,\
                message TEXT,\
                user VARCHAR(64),\
                PRIMARY KEY (m_id)\
                );")

conn.commit()
name = input("Enter your name:")

def als():
    text = input()
    return text

class Client(Socket):
    def __init__(self):
        super(Client, self).__init__()
        self.messages = ""

    def set_up(self):
        try:
            self.socket.connect(
                ("127.0.0.1", 1234)
            )
        except ConnectionRefusedError:
            print("Sorry, server is offline")
            exit(0)

        self.socket.setblocking(False)

    async def listen_socket(self, listened_socket=None):
        while True:
            data = await self.main_loop.sock_recv(self.socket, 2048)
            self.messages += f"{datetime.now().date()}: {data.decode('utf-8')}\n"

            system("cls")
            print(self.messages)

    async def send_data(self, data=None):
        while True:
            data = await self.main_loop.run_in_executor(None, input)
            message = name + ":" + data
            if data == "history":
                cursor.execute("SELECT * from message")
                history = cursor.fetchall()
                print(history)
            else:
                sql = "insert into message(message, user) values (%s , %s)"
                val = (data, name)
                cursor.execute(sql, val)
                conn.commit()
            await self.main_loop.sock_sendall(self.socket, message.encode("utf-8"))

    async def main(self):
        await asyncio.gather(

            self.main_loop.create_task(self.listen_socket()),
            self.main_loop.create_task(self.send_data())

        )


if __name__ == '__main__':

    client = Client()
    client.set_up()
    client.start()
    conn.close()