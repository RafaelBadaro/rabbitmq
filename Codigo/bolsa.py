import pika
import sys
import re

exchange_name = 'BOLSADEVALORES'


def enviar_notificacoes(topicos: list[str]):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.exchange_declare(exchange=exchange_name, exchange_type='topic')

    rota = topicos[0]  # operacao.acao
    mensagem = montar_conteudo(topicos) # quant;val;corretora

    channel.basic_publish(exchange=exchange_name, routing_key=rota, body=mensagem)

    print(" [x] Enviado %r:%r" % rota, mensagem)

    connection.close()

def montar_conteudo(topicos):
        return topicos[1] + ';' + topicos[2] + ';' + topicos[3]


def receber_operacoes():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queueDeclare("BROKER", True, False, False, None)
    print("[*] Recebendo operacoes . Para sair pressione CTRL+C'")

    channel.basic_consume(queue='BROKER', on_message_callback=callback)


def callback(ch, method, properties, body):
    print(" [x] Chegou: %r:%r" % (method.routing_key, body))

    topico: list[str] = body.split('-')

    if topico[0].__contains__('info'):
        realizar_info(topico[0], topico[1])
        pass
    else:
        try:
            enviar_notificacoes(topico)
        except Exception as e:
            print(e)
        salvar_operacao(topico[0], topico[1])


# salvar as operacoes feitas
def salvar_operacao(operacao_acao: str, oferta: str):

    operacao = operacao_acao + ';' + oferta
    #TODO - chamar operacao para salvar no livro de ofertas

def realizar_info(operacao_acao: str, data:str):
    consulta = operacao_acao + data

    #TODO - chamar operacao para consultar no livro de ofertas

