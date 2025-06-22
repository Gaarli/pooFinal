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
            time.sleep(0.1)
    
# Função para verificar se ocorreu o erro de dados não encontrados
def erro_dados_nao_encontrados(driver):
    try:
        # Procura a mensagem de erro e retorna se ela está visível na tela
        caixa = driver.find_element(By.XPATH, "//div[@id='err']//p[contains(text(), 'Dados não encontrados')]")
        return caixa.is_displayed()
    except:
        # Caso dê algum erro na procura, retorna False
        return False


# Função que verifica o tipo de situação na busca das informações do curso (erro ou 
# grade horária disponível) e retorna uma string descritiva da situação.
def condicao_erro_ou_aba(driver):
    # Verifica se o overlay sumiu
    try:
        overlay = driver.find_element(By.CLASS_NAME, "blockUI")
        if overlay.is_displayed():
            return False  # Ainda carregando, não tenta clicar
    except:
        pass  # Overlay não existe, seguimos

    # Tenta clicar na aba com segurança
    try:
        aba = driver.find_element(By.ID, "step4-tab")
        if aba.is_displayed() and aba.is_enabled():
            try:
                aba.click()
                return "grade"
            except ElementClickInterceptedException:
                pass  # Ainda tem algo bloqueando
    except:
        pass

    # Verifica se apareceu a caixa de erro
    try:
        if erro_dados_nao_encontrados(driver):
            return "erro"
    except:
        pass

    return False  # Continua esperando