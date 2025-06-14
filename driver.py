# O módulo 'driver.py' implementa as funções responsáveis pela manipulação do driver
# ex.: abrir página, ir para grade curricular, clicar em botões, etc

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
import time

def iniciar_driver():
    driver = webdriver.Chrome()
    driver.get("https://uspdigital.usp.br/jupiterweb/jupCarreira.jsp?codmnu=8275")
    wait = WebDriverWait(driver, 10)
    return driver

def selecionar_unidade(select_unidade, unidade):
    select_unidade.select_by_value(unidade.get_attribute('value'))
    time.sleep(0.5)

def selecionar_curso(select_curso, curso):
    select_curso.select_by_value(curso.get_attribute('value'))
    time.sleep(0.2)

def clicar_quando_nao_interceptado(driver, by, value):
    while True:
        try:
            elemento = driver.find_element(by, value)
            elemento.click()
            break  # deu certo, saiu do loop
        except ElementClickInterceptedException as e:
            time.sleep(0.1)
