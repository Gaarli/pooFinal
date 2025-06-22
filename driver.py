'''
O módulo 'driver.py' implementa as funções responsáveis pela manipulação do driver.
ex.: abrir página, ir para grade curricular, clicar em botões, etc
'''

# Importa as bibliotecas
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
import time

# Função para inicializar o driver
def iniciar_driver():
    # Inicializa o driver
    driver = webdriver.Chrome()
    driver.get("https://uspdigital.usp.br/jupiterweb/jupCarreira.jsp?codmnu=8275")

    # Espera até que o menu de unidades esteja carregado para prosseguir
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'comboUnidade'))
    )
    return driver

# Função para selecionar uma unidade na lista de opções
def selecionar_unidade(select_unidade, unidade):
    select_unidade.select_by_value(unidade.get_attribute('value'))
    time.sleep(0.5)

# Função para selecionar um curso na lista de opções
def selecionar_curso(select_curso, curso):
    select_curso.select_by_value(curso.get_attribute('value'))
    time.sleep(0.2)

# Função para clicar em um elemento bloqueado momentanemente por um overlay de carregamento
def clicar_quando_nao_interceptado(driver, by, value):
    while True:
        try:
            elemento = driver.find_element(by, value)
            elemento.click()
            # deu certo, sai do loop
            break  
        except ElementClickInterceptedException as e:
            # Ainda está bloqueado: espera 0.1s e continua a tentar
            time.sleep(0.1)
