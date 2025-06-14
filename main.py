### BIBLIOTECAS UTILIZADAS: SELENIUM; BEAUTIFULSOUP4; TIME
### IMPORTANTE: PRECISA BAIXAR CADA BIBLIOTECA UTILIZANDO pip install nomeBiblioteca no terminal
### ex.: pip install selenium

# Importa bibliotecas
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.common.exceptions import *

from extrai import *
from driver import *

from bs4 import BeautifulSoup
import time

# Importa classes
from classes import Unidade
from classes import Disciplina
from classes import Curso

# Função principal
def main():

    lista_unidades = []

    driver = iniciar_driver()

    select_unidade = Select(driver.find_element(By.ID, "comboUnidade"))

    for unidade in select_unidade.options[1:]:
        select_unidade.select_by_value(unidade.get_attribute('value'))

        nomeUnidade = unidade.get_attribute('text')
        
        unidade_instancia = Unidade(nomeUnidade)

        select_curso = Select(driver.find_element(By.ID, "comboCurso"))
        
        for curso in select_curso.options[1:]:
            select_curso.select_by_value(curso.get_attribute('value'))
            nomeCurso = curso.get_attribute('text')
            
            clicar_quando_nao_interceptado(driver, By.ID, "enviar")

            try:
                WebDriverWait(driver,3).until(EC.element_to_be_clickable((By.ID,"step4-tab")))
                driver.find_element(By.ID,"step4-tab").click()
            except ElementClickInterceptedException as e:
                curso_instancia = Curso(nomeCurso,nomeUnidade,0,0,0)
                unidade_instancia.adicionar_curso(curso_instancia)                
                clicar_quando_nao_interceptado(driver, By.XPATH, "/html/body/div[7]/div[3]/div/button/span")
                continue
            
            curso_instancia = extrair_dados_do_curso(driver,nomeCurso,nomeUnidade)
            unidade_instancia.adicionar_curso(curso_instancia)
            
            clicar_quando_nao_interceptado(driver, By.ID, "step1-tab")

        lista_unidades.append(unidade_instancia)

# Chama a função principal
main()