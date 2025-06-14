# extrai.py

from bs4 import BeautifulSoup
from driver import clicar_quando_nao_interceptado
from classes import Curso, Disciplina
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
import time

def extrair_dados_do_curso(driver, nome_curso, nome_unidade):
    time.sleep(0.5)

    lista_disciplinas=[]

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    duracaoIdeal = soup.find('span', class_='duridlhab').text
    duracaoMinima = soup.find('span', class_='durminhab').text
    duracaoMaxima = soup.find('span', class_='durmaxhab').text

    curso_instancia = Curso(nome_curso, nome_unidade, duracaoIdeal, duracaoMinima, duracaoMaxima)
    
    tabelas = soup.find('div', id="gradeCurricular").find_all('table')

    for tabela in tabelas:
        tipo_tabela = tabela.find('td').text
        disciplinas = tabela.find_all('tr',{'style': 'height: 20px;'})
        if(tipo_tabela=="Disciplinas Obrigatórias"):
            for disciplina in disciplinas:
                infos = disciplina.find_all('td')
                disciplina_instancia = Disciplina(infos[0].text,infos[1].text,infos[2].text,infos[3].text,infos[4].text,infos[5].text,infos[6].text,infos[7].text)
                lista_disciplinas.append((disciplina_instancia,"obrigatoria"))
            continue
        if(tipo_tabela=="Disciplinas Optativas Eletivas"):
            for disciplina in disciplinas:
                infos = disciplina.find_all('td')
                disciplina_instancia = Disciplina(infos[0].text,infos[1].text,infos[2].text,infos[3].text,infos[4].text,infos[5].text,infos[6].text,infos[7].text)
                lista_disciplinas.append((disciplina_instancia,"optativa_eletiva"))
            continue
        if(tipo_tabela=="Disciplinas Optativas Livres"):
            for disciplina in disciplinas:
                infos = disciplina.find_all('td')
                disciplina_instancia = Disciplina(infos[0].text,infos[1].text,infos[2].text,infos[3].text,infos[4].text,infos[5].text,infos[6].text,infos[7].text)
                lista_disciplinas.append((disciplina_instancia,"optativa_livre"))
            continue
    
    for disciplina,tipo in lista_disciplinas:
        curso_instancia.adicionar_disciplina(disciplina,tipo)

    lista_disciplinas.clear()
    return curso_instancia
