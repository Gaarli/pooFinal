# extrai.py

from bs4 import BeautifulSoup
from driver import clicar_quando_nao_interceptado
from classes import Curso, Disciplina
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
import time

# Importa classes
from classes import Unidade
from classes import Disciplina
from classes import Curso

from driver import *

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

# Função para verificar se ocorreu o erro de dados não encontrados
def erro_dados_nao_encontrados(driver):
    try:
        caixa = driver.find_element(By.XPATH, "//div[@id='err']//p[contains(text(), 'Dados não encontrados')]")
        return caixa.is_displayed()
    except:
        return False


def extrair_todos_dados(quantidade_unidades):
    lista_unidades = []

    try:
        driver = iniciar_driver()

        # Espera até que o select tenha mais de uma opção (excluindo a primeira "Selecione")
        WebDriverWait(driver, 10).until(
            lambda d: len(Select(d.find_element(By.ID, "comboUnidade")).options) > 1
        )
        select_unidade = Select(driver.find_element(By.ID, "comboUnidade"))

        # Para cada unidade no range especificado pelo usuário
        for unidade in select_unidade.options[1:(quantidade_unidades+1)]:
            # Seleciona a unidade
            selecionar_unidade(select_unidade, unidade)
            
            # Cria uma instância da unidade atual
            nomeUnidade = unidade.get_attribute('text')
            unidade_instancia = Unidade(nomeUnidade)
            
            print(f"\n***** UNIDADE SELECIONADA: {nomeUnidade} *****")
            
            # Espera as opções de curso ser clicável
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "comboCurso")))

            select_curso = Select(driver.find_element(By.ID, "comboCurso"))
            
            # Para cada curso na unidade
            for curso in select_curso.options[2:]:
                # Seleciona o curso
                selecionar_curso(select_curso, curso)
                nomeCurso = curso.get_attribute('text')
                
                print(f"\n***** CURSO SELECIONADO: {nomeCurso} *****")

                # Tenta buscar as informações do curso, clicando no botão "Buscar"
                clicar_quando_nao_interceptado(driver, By.ID, "enviar")
                try:

                    # Tenta clicar na aba de "Grade Curricular"
                    WebDriverWait(driver,3).until(EC.element_to_be_clickable((By.ID,"step4-tab")))
                    driver.find_element(By.ID,"step4-tab").click()
                
                # Tratamento de erro - curso sem informações disponíveis
                except ElementClickInterceptedException as e:
                    # Adiciona na lista apenas com o nome do curso e da unidade
                    curso_instancia = Curso(nomeCurso, nomeUnidade, info_disponivel=False)
                    unidade_instancia.adicionar_curso(curso_instancia)      

                    # Clica para fechar a mensagem de erro          
                    clicar_quando_nao_interceptado(driver, By.XPATH, "/html/body/div[7]/div[3]/div/button/span")
                    
                    continue    # Segue para o próximo curso
                
                curso_instancia = extrair_dados_do_curso(driver,nomeCurso,nomeUnidade)
                unidade_instancia.adicionar_curso(curso_instancia)
                
                print(f"***** DADOS EXTRAIDOS *****")
                # curso_instancia.mostrar()

                clicar_quando_nao_interceptado(driver, By.ID, "step1-tab")


            lista_unidades.append(unidade_instancia)

    except Exception as e:
        print("Erro durante execução:", type(e).__name__, e)
        driver.quit()

    return lista_unidades