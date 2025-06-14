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
    try:
        clicar_quando_nao_interceptado(driver, By.ID, "enviar")
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.ID, "step4-tab")))
        driver.find_element(By.ID, "step4-tab").click()
    except ElementClickInterceptedException:
        curso = Curso(nome_curso, nome_unidade, 0, 0, 0)
        clicar_quando_nao_interceptado(driver, By.XPATH, "/html/body/div[7]/div[3]/div/button/span")
        return False, curso, None

    time.sleep(0.1)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    try:
        duracaoIdeal = soup.find('span', class_='duridlhab').text
        duracaoMinima = soup.find('span', class_='durminhab').text
        duracaoMaxima = soup.find('span', class_='durmaxhab').text
    except Exception:
        return False, None, (nome_unidade, nome_curso)

    curso = Curso(nome_curso, nome_unidade, duracaoIdeal, duracaoMinima, duracaoMaxima)
    tabelas = soup.find('div', id="gradeCurricular").find_all('table')

    if not tabelas:
        return True, curso, (nome_unidade, nome_curso)

    for tabela in tabelas:
        tipo_tabela = tabela.find('td').text
        disciplinas = tabela.find_all('tr', {'style': 'height: 20px;'})

        tipo = None
        if tipo_tabela == "Disciplinas Obrigatórias":
            tipo = "obrigatoria"
        elif tipo_tabela == "Disciplinas Optativas Eletivas":
            tipo = "optativa_eletiva"
        elif tipo_tabela == "Disciplinas Optativas Livres":
            tipo = "optativa_livre"

        if tipo:
            for disciplina in disciplinas:
                infos = disciplina.find_all('td')
                d = Disciplina(*[i.text for i in infos])
                curso.adicionar_disciplina(d, tipo)

    clicar_quando_nao_interceptado(driver, By.ID, "step1-tab")
    return True, curso, None

def disciplinas_em_varios_cursos(lista_unidades):
    # Aqui você pode colocar seu código para análise posterior se quiser
    pass
