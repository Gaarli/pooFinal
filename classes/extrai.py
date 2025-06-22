'''
O módulo 'extrai.py' implementa as funções principais e auxiliares relativas à extração de dados 
do website e à criação e inicialização dos objetos dos tipos Unidade, Curso e Disciplina.
'''

# Importação de bibliotecas e funções
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
import time
from driver import *

# Importa classes
from classes import Curso, Disciplina, Unidade

# --------------------------- FUNÇÕES PRINCIPAIS --------------------------

# Função que extrai todas as disciplinas de um curso, cria os
# objetos que as representam e retorna uma lista com todos eles.
def extrair_disciplinas(soup):
    # Resgata as tabelas que dividem as disciplinas por tipo
    tabelas = soup.find('div', id="gradeCurricular").find_all('table')

    # Lista para adicionar as disciplinas
    lista_disciplinas=[]

    for tabela in tabelas:
        # Tipo da tabela (obrigatória, optativa livre ou optativa eletiva)
        tipo_tabela = tabela.find('td').text

        # Resgata os elementos html das disciplinas
        disciplinas = tabela.find_all('tr',{'style': 'height: 20px;'})

        for disciplina in disciplinas:
            # Extrai as informações separadas da disciplina, cria um objeto e adiciona-o na lista
            infos = disciplina.find_all('td')
            disciplina_instancia = Disciplina(infos[0].text,infos[1].text,infos[2].text,infos[3].text,infos[4].text,infos[5].text,infos[6].text,infos[7].text)
            lista_disciplinas.append((disciplina_instancia, tipo_tabela))

    # Retorna a lista com todas as disciplinas
    return lista_disciplinas


# Função para extrair os dados de um curso e retornar um objeto do tipo Curso que o representa.
def extrair_dados_do_curso(driver, nome_curso, nome_unidade):
    time.sleep(0.5)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    # Busca as informações de duração do curso
    duracaoIdeal = soup.find('span', class_='duridlhab').text
    duracaoMinima = soup.find('span', class_='durminhab').text
    duracaoMaxima = soup.find('span', class_='durmaxhab').text

    # Inicializa uma instância de Curso
    curso_instancia = Curso(nome_curso, nome_unidade, duracaoIdeal, duracaoMinima, duracaoMaxima)

    # Busca todas as disciplinas do curso
    lista_disciplinas = extrair_disciplinas(soup)
    
    # Adicionas as disciplinas na instância do curso
    for disciplina,tipo in lista_disciplinas:
        curso_instancia.adicionar_disciplina(disciplina,tipo)

    lista_disciplinas.clear() 
    # Retorna a instância atualizada do curso
    return curso_instancia

# Função principal que extrai todos os dados de cada unidade e retorna uma lista
# com todas elas. A quantidade de unidades é dada pelo parâmetro.
def extrair_todos_dados(quantidade_unidades):
    # Lista para adicionar as unidades
    lista_unidades = []

    try:
        driver = iniciar_driver()

        # Espera até que o select tenha mais de uma opção (excluindo a primeira "Selecione")
        WebDriverWait(driver, 10).until(
            lambda d: len(Select(d.find_element(By.ID, "comboUnidade")).options) > 1
        )
        select_unidade = Select(driver.find_element(By.ID, "comboUnidade"))

        # Para cada unidade no range especificado pelo usuário
        for unidade in select_unidade.options[1:]:
            # Seleciona a unidade
            selecionar_unidade(select_unidade, unidade)
            
            # Cria uma instância da unidade atual
            nomeUnidade = unidade.get_attribute('text')
            unidade_instancia = Unidade(nomeUnidade)
            
            print(f"\nUNIDADE SELECIONADA: {nomeUnidade}")
            
            # Espera as opções de curso ser clicável
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "comboCurso")))

            select_curso = Select(driver.find_element(By.ID, "comboCurso"))
            
            # Para cada curso na unidade
            for curso in select_curso.options[1:]:

                # Seleciona o curso
                selecionar_curso(select_curso, curso)
                nomeCurso = curso.get_attribute('text')
                
                print(f"\nCURSO SELECIONADO: {nomeCurso}")

                # Tenta buscar as informações do curso, clicando no botão "Buscar"
                clicar_quando_nao_interceptado(driver, By.ID, "enviar")


                # Verifica se houve erro de informações não disponíveis
                resultado = WebDriverWait(driver, 10).until(condicao_erro_ou_aba)
                if resultado == "erro":

                    # Adiciona na lista apenas com o nome do curso e da unidade
                    curso_instancia = Curso(nomeCurso, nomeUnidade, info_disponivel=False)
                    unidade_instancia.adicionar_curso(curso_instancia)      

                    # Clica para fechar a mensagem de erro
                    clicar_quando_nao_interceptado(driver, By.XPATH, "/html/body/div[7]/div[3]/div/button/span")
                    
                    continue  # Segue para o próximo curso

                # Tenta clicar na aba de "Grade Curricular" até o overlay de carregamento sumir
                clicar_quando_nao_interceptado(driver, By.ID, "step4-tab")

                # Cria uma instância do curso e adiciona-o na instância da unidade
                curso_instancia = extrair_dados_do_curso(driver,nomeCurso,nomeUnidade)
                unidade_instancia.adicionar_curso(curso_instancia)
                
                # DEBUG
                print(f"*** DADOS EXTRAIDOS ***\n")
                # curso_instancia.mostrar()

                # Voltar para o menu de escolha do curso
                clicar_quando_nao_interceptado(driver, By.ID, "step1-tab")


            # Adiciona a unidade atualizada na lista de unidades
            lista_unidades.append(unidade_instancia)

    except Exception as e:
        print("Erro durante execução:", type(e).__name__, e)
        driver.quit()

    # Retorna a lista com todas as unidades, de acordo com a quantidade especificada
    return lista_unidades