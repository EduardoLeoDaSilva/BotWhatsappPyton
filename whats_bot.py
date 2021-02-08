from selenium import webdriver
import os
from time import sleep
import requests
import json
from collections import deque
from threading import Thread
class zapbot:
    # O local de execução do nosso script
    dir_path = os.getcwd()
    # O caminho do chromedriver
    chromedriver = os.path.join(dir_path, "chromedriver.exe")
    # Caminho onde será criada pasta profile
    profile = os.path.join(dir_path, "profile", "wpp")

    def __init__(self):
        self.options = webdriver.ChromeOptions()
        # Configurando a pasta profile, para mantermos os dados da seção
        self.options.add_argument(
            r"user-data-dir={}".format(self.profile))
        # Inicializa o webdriver
        self.driver = webdriver.Chrome(
            self.chromedriver, chrome_options=self.options)
        # Abre o whatsappweb
        self.driver.get("https://web.whatsapp.com/")
        # Aguarda alguns segundos para validação manual do QrCode
        self.driver.implicitly_wait(15)

    def consultarPedido(self):
       while True: 
           try:
              if len(filaConsulta)  > 0 :
                pedido = filaConsulta[0]
                payload = {'VendaId': pedido, 'Integrador': 'SAV'}

                headers = {'content-type': 'application/json'}
                r = requests.post('http://localhost:5000/Status/ConsultaPedido',
                                data=json.dumps(payload), headers=headers)
                r.encoding = 'ISO-8859-1'
                if r.status_code == 200:
                 filaMensagens.append({'demanda': r.text, 'tipo': 'msg'})
                 filaEmEspera.append(pedido)
                #   bot.envia_msg(r.text)
                 filaConsulta.popleft()
                elif r.status_code == 202:
                #   bot.envia_msg("Pedido não encontrado!")
                  filaMensagens.append({'demanda': "Pedido não encontrado!", 'tipo': 'msg'})
                  filaEmEspera.append(pedido)
                  filaConsulta.popleft()
                elif r.status_code == 204:
                #   bot.envia_msg("Pedido sem vendaId!")
                  filaMensagens.append({'demanda': "Pedido sem vendaId!", 'tipo': 'msg'})
                  filaEmEspera.append(pedido)
                  filaConsulta.popleft()
                else:
                #   bot.envia_msg("Ocorreu um erro ao consultar o pedido!")
                  filaMensagens.append({'demanda': "Ocorreu um erro ao consultar o pedido!", 'tipo': 'msg'})
                  filaEmEspera.append(pedido)
                  filaConsulta.popleft()
           except Exception as e:
            print("Erro ao consultar o servidor!")


    def obterLog(self):
       while True: 
           try:
              if len(filaLog)  > 0 :
                pedido = filaLog[0]
                headers = {'content-type': 'application/json'}
                r = requests.get('http://localhost:5000/Log/ObterLog?codigoWooza='+ pedido,headers=headers)
                r.encoding = 'ISO-8859-1'
                if r.status_code == 200:
                 filaMensagens.append({'demanda': "C:/Users/Dud/LogsIziPizi/LogsBot/Log-" + pedido+ ".txt", 'tipo': 'arquivo'})
                #   bot.envia_arquivo("C:/Users/Dud/LogsIziPizi/LogsBot/Log-" + pedido+ ".txt")
                 filaEmEspera.append(pedido)
                 filaLog.popleft()
                elif r.status_code == 202:
                #   bot.envia_msg("Pedido não encontrado!")
                 filaMensagens.append({'demanda': "Pedido não encontrado!", 'tipo': 'msg'})
                 filaEmEspera.append(pedido)
                 filaLog.popleft()
                elif r.status_code == 204:
                #   bot.envia_msg("Pedido sem vendaId!")
                 filaMensagens.append({'demanda': "Pedido sem vendaId!", 'tipo': 'msg'})
                 filaEmEspera.append(pedido)
                 filaLog.popleft()
                else:
                #   bot.envia_msg("Ocorreu um erro ao consultar o pedido!")
                 filaMensagens.append({'demanda': "Ocorreu um erro ao consultar o pedido!", 'tipo': 'msg'})
                 filaEmEspera.append(pedido)
                 filaLog.popleft()
           except Exception as e:
            print("Erro ao consultar o servidor!")              
        


    def reprocessaPedido(self):
        while True:
            if len(filaReprocessa)  > 0 :
               pedido = filaReprocessa[0]
               payload = {'CodigoWooza': pedido}

               headers = {'content-type': 'application/json'}
               r = requests.post('http://localhost:5000/Status/ReprocessarPedido',
                                 data=json.dumps(payload), headers=headers)
               if r.status_code == 200:
                 r.encoding = 'ISO-8859-1'
                 filaMensagens.append({"demanda": r.text , "tipo": "msg"})
                 filaEmEspera.append(pedido)
                #  bot.envia_msg(r.text)
                 filaReprocessa.popleft()
               elif r.status_code == 202:
                #  bot.envia_msg("Pedido não encontrado!")
                 filaEmEspera.append(pedido)
                 filaMensagens.append({'demanda': "Pedido não encontrado!", 'tipo': 'msg'})
                 filaReprocessa.popleft()
               else:
                #  bot.envia_msg("Ocorreu um erro ao reprocessar o pedido")
                 filaEmEspera.append(pedido)
                 filaMensagens.append({'demanda': "Ocorreu um erro ao reprocessar o pedido", 'tipo': 'msg'})
                 filaReprocessa.popleft()                  

    def ultima_msg(self):
        """ Captura a ultima mensagem da conversa """
        try:
            post = self.driver.find_elements_by_class_name("_1wlJG")
            ultimo = len(post) - 1
            # O texto da ultima mensagem
            texto = post[ultimo].find_element_by_css_selector(
                "span.selectable-text").text
            return texto
        except Exception as e:
            print("Erro ao ler msg, tentando novamente!")

    def envia_msg(self, msg):
        """ Envia uma mensagem para a conversa aberta """
        try:
            # sleep(2)
            # Seleciona acaixa de mensagem
            self.caixa_de_mensagem = self.driver.find_element_by_class_name(
                "DuUXI")
            sleep(2)
            # Digita a mensagem
            self.caixa_de_mensagem.send_keys(msg)
            sleep(5)
            # Seleciona botão enviar
            self.botao_enviar = self.driver.find_element_by_xpath(
                "//span[@data-icon='send']")
            # Envia msg
            self.botao_enviar.click()
            sleep(2)
        except Exception as e:
            print("Erro ao enviar msg, tentando novamente", e)
            self.envia_msg(msg)

    def envia_media(self, fileToSend):
        """ Envia media """
        try:
            # Clica no botão adicionar
            self.driver.find_element_by_css_selector(
                "span[data-icon='clip']").click()
            # Seleciona input
            attach = self.driver.find_element_by_css_selector(
                "input[type='file']")
            # Adiciona arquivo
            attach.send_keys(fileToSend)
            sleep(3)
            # Seleciona botão enviar
            send = self.driver.find_element_by_xpath(
                "//div[contains(@class, 'yavlE')]")
            # Clica no botão enviar
            send.click()
        except Exception as e:
            print("Erro ao enviar media", e)

    def envia_arquivo(self, fileToSend):
        """ Envia media """
        try:
            self.envia_msg("Segue o log:")
            # Clica no botão adicionar
            self.driver.find_element_by_css_selector(
                "span[data-icon='clip']").click()
            # Seleciona input
            attach = self.driver.find_element_by_css_selector(
                "input[type='file']")
            # Adiciona arquivo
            attach.send_keys(fileToSend)
            sleep(3)
            # Seleciona botão enviar
            send = self.driver.find_element_by_xpath(
                "//div[contains(@class, '_3ipVb')]")
            # Clica no botão enviar
            send.click()
        except Exception as e:
            print("Erro ao enviar media", e)      


    def enviar_msg_queu(self):
      while True:
        try:
          if len(filaMensagens)  > 0:
            demanda = filaMensagens[0]
            if demanda['tipo']== "msg":
              self.envia_msg(demanda['demanda'])
              if len(filaConsulta) > 0:
                 filaConsulta.popleft()
              if len(filaReprocessa) > 0:      
                 filaReprocessa.popleft()         
            elif demanda['tipo']== "arquivo" :
              self.envia_arquivo(demanda['demanda'])
              filaLog.popleft()
            else:
                print("tipo inválido")
            filaMensagens.popleft()
            filaEmEspera.popleft()    
        except Exception as e:
           print("Erro ao tentar obter filaMensagens")



    def abre_conversa(self, contato):
        """ Abre a conversa com um contato especifico """
        try:
            # //self.grupos_ou_pessoas = [contato]

            # Seleciona a caixa de pesquisa de conversa
            # self.caixa_de_pesquisa = self.driver.find_element_by_class_name("jN-F5")
            # Digita o nome ou numero do contato
            # self.caixa_de_pesquisa.send_keys(contato)
            sleep(1)
            # Seleciona o contato
            # self.contato = self.driver.find_element_by_xpath("//span[@title = '{}']".format(contato))
            self.contato = self.driver.find_element_by_xpath(
                f"//span[@title='{contato}']")
            sleep(2)

            # Entra na conversa
            self.contato.click()
        except Exception as e:
            print("Erro ao tentar abrir contato, tentando novamente")
            self.abre_conversa(contato)
    
    def fluxo_tratamento(self):
       msg = ""
       while msg != "/quit":
         try:
           sleep(0.2)
           msg = bot.ultima_msg()
           msgsplit = msg.split()
           if msgsplit[0] == "Consultar" :
               if msgsplit[1] not in filaConsulta  and msgsplit[1] not in filaEmEspera:
                 filaConsulta.append(msgsplit[1])
              # bot.consultarPedido(msgsplit[1])
              # bot.envia_msg("""Bot: Esse é um texto com os comandos válidos:
              #     /help (para ajuda)
              #     /mais (para saber mais)
              #     /quit (para sair)
              #     """)
           elif msgsplit[0] == "Reprocessar":
               if msgsplit[1] not in filaReprocessa and msgsplit[1] not in filaEmEspera :
                   filaReprocessa.append(msgsplit[1])
                #  bot.reprocessaPedido(msgsplit[1])
           elif msgsplit[0] == "ObterLog":
               if msgsplit[1] not in filaLog and msgsplit[1] not in filaEmEspera:
                  filaLog.append(msgsplit[1])
           elif msg == "/quit":
              bot.envia_msg("Bye bye!")
         except Exception as e:
           print("Erro")  


bot = zapbot()
bot.abre_conversa("Mãe")

# bot.consultarPedido("SA385199")
# bot.envia_msg("Olá, sou o bot whatsapp! Para receber ajuda digite: /help")
imagem = bot.dir_path + "/imagem.jpg"
msg = ""
filaConsulta = deque([])
filaReprocessa = deque([])
filaLog = deque([])
filaMensagens = deque([])
filaEmEspera = deque([])
t = Thread(target=bot.consultarPedido)
t2 = Thread(target=bot.fluxo_tratamento)
t3 = Thread(target=bot.reprocessaPedido)
t4 = Thread(target=bot.obterLog)
t5 = Thread(target=bot.enviar_msg_queu)
t.start()
t2.start()
t3.start()
t4.start()
t5.start()
