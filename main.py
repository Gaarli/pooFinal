# NOME: Gabriel de Araujo Lima - NUSP: 14571376
# NOME: Beatriz Alves dos Santos - NUSP: 15588630

# BIBLIOTECAS UTILIZADAS: SELENIUM; BEAUTIFULSOUP4
# IMPORTANTE: PRECISA BAIXAR CADA BIBLIOTECA UTILIZANDO pip install nomeBiblioteca no terminal
# pip install selenium
# pip install beautifulsoup4

# Importa os módulos
from driver import *    # Módulo responsável pela manipulação da web
from extrai import *    # Módulo responsável por extrair os dados
from consulta import *  # Módulo responsável pelas consultas dos dados
from imprime import *   # Módulo responsável por imprimir os dados

import sys  # Biblioteca para leitura direto do terminal, conforme solicitado no pdf

# Função principal, que lê do usuário a quantidade de unidades, extrai os dados e solicita as consultas
def main():
    quantidade_unidades = int(sys.argv[1])  # Lê a quantidade de unidades diretamente do terminal
    # Foi utilizado leitura com sys para poder escrever 'python3 main.py 3' diretamente
    # Ou seja, o '3', por exemplo, pode ser escrito na frente de main.py

    lista_de_unidades = extrair_todos_dados(quantidade_unidades) # Extrai os dados e guarda em lista_unidades
    print("\n---------- Extração finalizada ----------")
    
    # Entra no loop das consultas
    while True:
        # Imprime a interface no terminal
        print("\n0 - FINALIZAR CONSULTAS ")
        print("1 - Lista de cursos por unidade ")
        print("2 - Dados de um determinado curso ")
        print("3 - Dados de todos os cursos ")
        print("4 - Dados de uma disciplina, inclusive quais cursos ela faz parte ")
        print("5 - Disciplinas que são usadas em mais de um curso ")
        print("6 - Busca de cursos por filtros ")

        codigo = input("\nDigite o código: ") # Lê o código do usuário

        if codigo == '0':   # Encerra o programa
            print("\nPROGRAMA FINALIZADO\n")
            break

        elif codigo == '1': # Consulta 1. Lista de cursos por unidades
            imprimir_primeira_consulta(listar_cursos_por_unidade(lista_de_unidades)) # Chama e imprime a consulta

        elif codigo == '2': # Consulta 2. Dados de um determinado curso
            nome = input("Digite o nome do curso: ")
            imprimir_segunda_consulta(buscar_curso_por_nome(lista_de_unidades, nome))  # Chama e imprime a consulta

        elif codigo == '3': # Consulta 3. Dados de todos os cursos 
            imprimir_terceira_consulta(listar_dados_de_todos_os_cursos(lista_de_unidades))  # Chama e imprime a consulta

        elif codigo == '4': # Consulta 4. Dados de uma disciplina, inclusive quais cursos ela faz parte
            termo = input("Digite o nome (completo) ou código da disciplina: ")
            imprimir_quarta_consulta(buscar_disciplina(lista_de_unidades, termo))   # Chama e imprime a consulta

        elif codigo == '5': # Consulta 5. Disciplinas que são usadas em mais de um curso
            imprimir_quinta_consulta(disciplinas_em_varios_cursos(lista_de_unidades))   # Chama e imprime a consulta
        
        elif codigo == '6': # Consulta 6. Filtro customizável de cursos
            filtros = solicitar_filtros_do_usuario()    # Solicita os filtros do usuário
            imprimir_sexta_consulta(filtrar_cursos_funcional(lista_de_unidades,**filtros))  # Chama e imprime a consulta

        else:   # Caso seja um código que não esteja de 1 a 6
            print("Código inválido. Tente novamente.")
    
    quit()  # Encerra o programa

# Chama a função main
if __name__ == "__main__":
    main()
