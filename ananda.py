import time
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer

import wikipedia
wikipedia.set_lang('pt')

#INSTANCIAR CHATBOT
chatbot = ChatBot('Arcanjo')
trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train('chatterbot.corpus.portuguese')
trainerer = ListTrainer(chatbot)
# ARMAZENAR DIRETORIO PRINCIPAL EM VARIAVEL
dir_path = os.getcwd()
# INICIAR APLICAÇÃO
driver = webdriver.Chrome(dir_path+'/chromedriver.exe') 
driver.get('https://web.whatsapp.com/')
driver.implicitly_wait(15)
# FUNÇÕES BÁSICAS DE COMUNICAÇÃO
def pegaConversa():
	try:
		post = driver.find_elements_by_class_name("_3zb-j")
		ultimo = len(post) - 1
		texto = post[ultimo].find_element_by_css_selector("span.selectable-text").text
		return texto
	except:
		pass
def enviaMensagem(mensagem):
	caixa_de_texto = driver.find_element_by_class_name('_1Plpp')
	valor = "*Arcanjo:* "+str(mensagem)
	for part in valor.split("\n"):
		caixa_de_texto.send_keys(part)
		ActionChains(driver).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.SHIFT).perform()
	time.sleep(0.5)
	botao_enviar = driver.find_element_by_class_name('_35EW6')
	botao_enviar.click()
def treinar(mensagem):
	resposta = 'Como respondo isso? me ensina, por favor...? utilize ;"'+str(mensagem)+'"'
	enviaMensagem(resposta)
	novo = []
	try:
		while True:
			ultima = pegaConversa()
			if ultima == "!":
				enviaMensagem("Você desativou meu aprendizado.")
				break
			elif ultima.replace(';','') != '' and ultima != mensagem and ultima[0] == ";" :
				auxiliar = ultima
				print(mensagem.lower().strip())
				print(ultima.replace(';','').lower().strip())
				novo.append(mensagem.lower().strip())
				novo.append(ultima.replace(';','').lower().strip())
				trainerer.train(novo)
				enviaMensagem("Pronto, aprendi! Obrigada <3")
				break
	except:
		pass
# WIKIPEDIA
def wiki():
  try:
    busca = str(pegaConversa().strip().lower()[2:])
    mensagem = '{}'.format(wikipedia.summary(busca))
    enviaMensagem(mensagem)
  except:
    enviaMensagem('Não encontrei nada relevante para "{}" na Wikipedia em português.'.format(busca))
# NOTÍCIAS
import json
import requests
def noticias():
	try:
		req = requests.get('https://newsapi.org/v2/top-headlines?country=br&category=technology&apiKey=')
		noticias = json.loads(req.text)
		for news in noticias['articles']:
			titulo = news['title']
			link = news['url']
			desc = news['description']
			mensagem = "{}\n{}\n{}".format(titulo,desc,link)
			enviaMensagem(mensagem)
			time.sleep(1)
	except:
		enviaMensagem("agora não...")
		pass
# BLOCO PRINCIPAL DE EXECUÇÃO
salva = pegaConversa()
while True:
	try:
		if pegaConversa() != "" and pegaConversa()[:9] != "Arcanjo: " and pegaConversa()[:9] != "arcanjo: " and pegaConversa() != salva and pegaConversa().strip() != "!" and pegaConversa().strip() != ";" and pegaConversa().strip().lower()[:2] != "w:" and pegaConversa().strip().lower() != "noticias" and pegaConversa().strip().lower() != "notícias" and pegaConversa().strip().lower() != "visão computacional" and pegaConversa().strip().lower() != "email":
			texto = str(pegaConversa().strip().lower())
			response = chatbot.get_response(texto)
			print(texto)
			print(response)
			if float(response.confidence) < 0.2:
				treinar(pegaConversa())
			else:
				enviaMensagem(response)
		elif pegaConversa().strip().lower()[:2] == "w:":
			wiki()
		elif pegaConversa().strip().lower() == "noticias" or pegaConversa().strip().lower() == "notícias":
			noticias()
		elif pegaConversa().strip().lower() == "visão computacional":
			enviaMensagem("Aguardando envio da imagem...")
			time.sleep(15)
			visa()
			pass
		elif pegaConversa().strip().lower() == "email":
			try:
				email()
				enviaMensagem("Enviado!")
			except Exception as aiaiai:
				enviaMensagem("Ainda não realizado...")
				print(aiaiai)
				pass
		else:
			pass
	except Exception as ok:
		print(ok)
		pass
