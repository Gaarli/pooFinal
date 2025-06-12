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
# from selenium.common.exceptions import TimeoutException
# from selenium.common.exceptions import NoSuchElementException
# from selenium.common.exceptions import StaleElementReferenceException

from bs4 import BeautifulSoup
import time

# Importa classes
from classes import Unidade
from classes import Disciplina
from classes import Curso

# Funções
def esperar_overlay_sumir(driver, timeout=10):
    wait = WebDriverWait(driver, timeout)
    try:
        # Espera overlay aparecer (caso ainda não esteja visível)
        #wait.until(EC.presence_of_element_located((By.CLASS_NAME, "blockUI")))
        # Espera overlay desaparecer
        wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "blockUI")))
    except:
        pass  # se não aparecer, segue em frente


def clicar_quando_nao_interceptado(driver, by, value, timeout=10):
    while True:
        try:
            elemento = driver.find_element(by, value)
            elemento.click()
            break  # deu certo, saiu do loop
        except ElementClickInterceptedException as e:
            pass

def buscar_cursos_por_nome(lista_unidades, palavra):
    return list(filter(
        lambda curso: palavra.lower() in curso.nome.lower(),
        sum(map(lambda u: u.cursos, lista_unidades), [])
    ))

def todas_obrigatorias(lista_unidades):
    return list(
        map(lambda d: d,
            sum(map(lambda curso: curso.obrigatorias,
                    sum(map(lambda u: u.cursos, lista_unidades), [])
                ), [])
        )
    )

def flatten(lista_de_listas):
    return sum(lista_de_listas, [])

def todos_cursos(lista_unidades):
    return flatten(map(lambda u: u.cursos, lista_unidades))

def dados_curso(lista_unidades, nome_curso):
    cursos = flatten(map(lambda u: u.cursos, lista_unidades))
    return next(filter(lambda c: c.nome == nome_curso, cursos), None)

def disciplinas_em_varios_cursos(lista_unidades):
    cursos = todos_cursos(lista_unidades)

    dicionario = defaultdict(set)

    for curso in cursos:
        todas = curso.obrigatorias + curso.optativas_eletivas + curso.optativas_livres
        for d in todas:
            dicionario[d.codigo].add(curso.nome)

    return list(filter(lambda item: len(item[1]) > 1, dicionario.items()))


# Função principal
def main():
    # Abrir o navegador
    driver = webdriver.Chrome()
    driver.get("https://uspdigital.usp.br/jupiterweb/jupCarreira.jsp?codmnu=8275")
    wait = WebDriverWait(driver, 10)

    select_unidade = Select(driver.find_element(By.ID, "comboUnidade"))

    contador = 0
    contador2=0
    contador3=0
    lista_unidades = []
    lista_disciplinas = []

    lista_debug=[]
    for unidade in select_unidade.options[1:]:
        select_unidade.select_by_value(unidade.get_attribute('value'))

        nomeUnidade = unidade.get_attribute('text')
        unidade_instancia = Unidade(nomeUnidade)
        # Espera até que comboCurso seja carregado com mais de 1 opção
        # WebDriverWait(driver, 10).until(
        #     lambda d: len(Select(d.find_element(By.ID, "comboCurso")).options) > 1
        # )

        select_curso = Select(driver.find_element(By.ID, "comboCurso"))

        # print(nomeUnidade)
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
                contador+=1
                
                clicar_quando_nao_interceptado(driver, By.XPATH, "/html/body/div[7]/div[3]/div/button/span")
                continue

            time.sleep(0.1)
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')

            # print(f"soup: {soup}")
            
            duracaoIdeal = soup.find_all('span', class_='duridlhab')[0].text
            duracaoMinima = soup.find_all('span', class_='durminhab')[0].text
            duracaoMaxima = soup.find_all('span', class_='durmaxhab')[0].text

            # print(duracaoIdeal,duracaoMinima,duracaoMaxima)
            
            curso_instancia = Curso(nomeCurso, nomeUnidade, duracaoIdeal, duracaoMinima, duracaoMaxima) # cria o curso

            tabelas = soup.find('div',id="gradeCurricular").find_all('table')
            if(not tabelas):
                lista_debug.append((nomeUnidade, nomeCurso))
                contador3+=1
            else:
                contador2+=1
            
            numeroTabela = 0

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
            unidade_instancia.adicionar_curso(curso_instancia)
            
            clicar_quando_nao_interceptado(driver, By.ID, "step1-tab")
            
            contador += 1
        lista_unidades.append(unidade_instancia)

    print(contador)

    disciplinas_em_varios_cursos(lista_unidades)

# Chama a função principal
main()