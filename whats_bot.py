from selenium import webdriver
import os
from time import sleep
import requests
import json


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

    def consultarPedido(self, pedido):
        payload = {'VendaId': pedido, 'Integrador': 'SAV'}

        headers = {'content-type': 'application/json'}
        r = requests.post('http://localhost:5000/Status/ConsultaPedido',
                          data=json.dumps(payload), headers=headers)
        r.encoding = 'ISO-8859-1'
        if r.status_code == 200:
          bot.envia_msg(r.text)
        else:
          bot.envia_msg("Ocorreu um erro ao consulta o pedido")
        


    def reprocessaPedido(self, pedido):
        payload = {'CodigoWooza': pedido}

        headers = {'content-type': 'application/json'}
        r = requests.post('http://localhost:5000/Status/ReprocessarPedido',
                          data=json.dumps(payload), headers=headers)
        r.encoding = 'ISO-8859-1'
        bot.envia_msg(r.text)

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
            sleep(2)
            # Seleciona acaixa de mensagem
            self.caixa_de_mensagem = self.driver.find_element_by_class_name(
                "DuUXI")
            # Digita a mensagem
            self.caixa_de_mensagem.send_keys(msg)
            sleep(10)
            # Seleciona botão enviar
            self.botao_enviar = self.driver.find_element_by_xpath(
                "//span[@data-icon='send']")
            # Envia msg
            self.botao_enviar.click()
            sleep(2)
        except Exception as e:
            print("Erro ao enviar msg", e)

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

    def abre_conversa(self, contato):
        """ Abre a conversa com um contato especifico """
        try:
            # //self.grupos_ou_pessoas = [contato]

            # Seleciona a caixa de pesquisa de conversa
            # self.caixa_de_pesquisa = self.driver.find_element_by_class_name("jN-F5")
            # Digita o nome ou numero do contato
            # self.caixa_de_pesquisa.send_keys(contato)
            sleep(10)
            # Seleciona o contato
            # self.contato = self.driver.find_element_by_xpath("//span[@title = '{}']".format(contato))
            self.contato = self.driver.find_element_by_xpath(
                f"//span[@title='{contato}']")
            sleep(2)

            # Entra na conversa
            self.contato.click()
        except Exception as e:
            raise e


bot = zapbot()
bot.abre_conversa("WoozaHelp")
# bot.consultarPedido("SA385199")
# bot.envia_msg("Olá, sou o bot whatsapp! Para receber ajuda digite: /help")
imagem = bot.dir_path + "/imagem.jpg"
msg = ""
while msg != "/quit":
    try:
     sleep(1)
     msg = bot.ultima_msg()
     msgsplit = msg.split()
     if msgsplit[0] == "Consultar" :
        bot.consultarPedido(msgsplit[1])
        # bot.envia_msg("""Bot: Esse é um texto com os comandos válidos:
        #     /help (para ajuda)
        #     /mais (para saber mais)
        #     /quit (para sair)
        #     """)
     elif msgsplit[0] == "Reprocessar":
        bot.reprocessaPedido(msgsplit[1])
     elif msg == "/quit":
        bot.envia_msg("Bye bye!")
    except Exception as e:
      raise e
