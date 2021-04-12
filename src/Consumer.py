import pika
import time
import json

import os
import subprocess
import pathlib

# from bot_login_google import Login


# file path in python
FILEBROWSER_PATH = os.path.join(os.getenv('WINDIR'), 'explorer.exe')


direct = pathlib.Path(__file__).parent.absolute().parent.absolute() / "config.json"
direct_read = open(direct, 'r')
direct_data = json.load(direct_read)
url = direct_data['dicts']['amqp']

# Parametros para buscar dados do docker
parameter = pika.URLParameters(url)
connection = pika.BlockingConnection(parameter)
channel = connection.channel()

try:
        
    channel.queue_declare(queue='hello', durable=False)
    print(' [*] Esperando mensagens. Para sair pressione CTRL+C')

    def callback(ch, method, properties, body):
        # print(" [x] Recebidos %r" % body.decode())
        dados = body.decode()
        dados = json.loads(dados)

        print(json.dumps(dados, indent=4, sort_keys=False))

        # robo = dados['Bot']
        # if robo == 1: Login.executar_login_google()
        
        time.sleep(body.count(b'.'))
        print(" [x] Processado")
        ch.basic_ack(delivery_tag=method.delivery_tag)


    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='hello', on_message_callback=callback)

    channel.start_consuming()

except KeyboardInterrupt:
    print('...Task interrompida...')

    