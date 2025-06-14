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

# Importa classes
from classes import Unidade
from classes import Disciplina
from classes import Curso
import sys

# Função principal
def main():

    quantidade_unidades = int(sys.argv[1])

    lista_unidades = []
    lista_unidades = extrair_todos_dados(quantidade_unidades)

    print("*************** EXTRAÇÃO DOS DADOS FINALIZADA ***************")
    print()
    while True:
        print("******************************")
        print("DIGITE A CONSULTA DESEJADA")
        print("******************************")

        print("0 - FINALIZAR CONSULTAS ")
        print("1 - Lista de cursos por unidade ")
        print("2 - Dados de um determinado curso ")
        print("3 - Dados de todos os cursos ")
        print("4 - Dados de uma disciplina, inclusive quais cursos ela faz parte ")
        print("5 - Disciplinas que são usadas em mais de um curso ")
        
        codigo = input()

        if(codigo == '0'):
            print("PROGRAMA FINALIZADO")
            break
        elif(codigo == '1'):
            print('codigo 1')
        elif(codigo == '2'):
            print('codigo 2')
        elif(codigo == '3'): 
            print('codigo 3')
        elif(codigo == '4'): 
            print('codigo 4')
        elif(codigo == '5'): 
            print('codigo 5')
        
    quit()

if __name__ == "__main__":
    # Chama a função principal
    main()