# O módulo "imprime.py" imprime os dados retornados por cada consulta
# Esse módulo foi implementado para uma tentativa de separar as funções que filtram
# os dados das funções que imprimem os dados filtrados

# A seguir são implementadas as funções para imprimir as consultas
# A ideia é que as consultas retornem objetos com os dados filtrados
# para manter os dados isolados de prints
# Por isso, são implementadas funções particulares para imprimir
# os dados filtrados

# Função para imprimir a lista retornada pela consulta 1
def imprimir_primeira_consulta(dicionario):
    for unidade, cursos in dicionario.items():
        titulo = f"Unidade: {unidade}"
        linha = "*" * len(titulo)
        print(linha)
        print(titulo)
        print("*" * len(titulo))
        print(f"Possui {len(cursos)} cursos:")
        for curso in cursos:
            print(f"  • {curso}")
        print()  # Linha em branco entre unidades
    
# Função para imprimir o dicionario retornado pela consulta 2
def imprimir_segunda_consulta(dicionario_cursos):
    if not dicionario_cursos or all(len(cursos) == 0 for cursos in dicionario_cursos.values()):
        # print("\nNenhum curso foi encontrado.\n")
        return
        
    print("\n" + "=" * 80)
    print(" " * 25 + "  CURSO(S) ENCONTRADOS")
    print("=" * 80 + "\n")

    for nome_unidade, cursos in dicionario_cursos.items():
        titulo_unidade = f"Unidade: {nome_unidade}"
        print(titulo_unidade)
        print("-" * len(titulo_unidade))

        for curso in cursos:
            curso.mostrar()
            print("\n" + "-" * 60 + "\n")

# Função para imprimir o dicionário retornado pela consulta 3
def imprimir_terceira_consulta(dicionario_cursos):
    if not dicionario_cursos or all(len(cursos) == 0 for cursos in dicionario_cursos.values()):
        print("\nNenhum curso encontrado nas unidades.\n")
        return

    print("\n" + "=" * 80)
    print(" " * 25 + "DADOS DE TODOS OS CURSOS")
    print("=" * 80 + "\n")

    for nome_unidade, cursos in dicionario_cursos.items():
        if not cursos:
            print(f"Unidade: {nome_unidade}")
            print("Nenhum curso disponível nesta unidade.\n")
            continue

        titulo_unidade = f"Unidade: {nome_unidade}"
        print(titulo_unidade)
        print("=" * len(titulo_unidade))

        for curso in cursos:
            curso.mostrar()
            print("-" * 80 + "\n")

# Imprimir quarta consulta
def imprimir_quarta_consulta(disciplinas_agrupadas):
    if not disciplinas_agrupadas:
        print("\nNenhuma disciplina encontrada com o termo buscado.\n")
        return

    print("\n" + "=" * 80)
    print(" " * 25 + "RESULTADO DA BUSCA DE DISCIPLINAS")
    print("=" * 80 + "\n")

    for codigo, info in disciplinas_agrupadas.items():
        disciplina = info["disciplina"]
        ocorrencias = info["ocorrencias"]

        titulo = f"{disciplina.codigo} - {disciplina.nome}"
        print(titulo)
        print("-" * len(titulo))

        print(f"Carga Horária Total: {disciplina.carga_horaria} horas")
        print(f"Créditos Aula: {disciplina.creditos_aula}, Créditos Trabalho: {disciplina.creditos_trabalho}")
        print(f"Estágio: {disciplina.carga_estagio}, Práticas: {disciplina.carga_praticas}, Atividades: {disciplina.carga_atividades}\n")

        print("Presente nos seguintes cursos/unidades e tipos:")
        for oc in ocorrencias:
            print(f" • Curso: {oc['curso']}")
            print(f"   Unidade: {oc['unidade']}")
            print(f"   Tipo: {oc['tipo']}\n")

        print("-" * 60 + "\n")

# Função para imprimir a quinta consulta
def imprimir_quinta_consulta(lista_disciplinas):
    if not lista_disciplinas:
        print("\nNenhuma disciplina aparece em mais de um curso.\n")
        return

    print("\n" + "=" * 80)
    print("DISCIPLINAS QUE APARECEM EM VÁRIOS CURSOS".center(80))
    print("=" * 80 + "\n")

    for codigo, cursos in lista_disciplinas:
        print(f"Disciplina: {codigo}")
        print(f"    • Presente em {len(cursos)} curso(s):")
        for nome_curso in sorted(cursos):
            print(f"      - {nome_curso}")
        print("-" * 80)

# Funcao para imprimir a sexta consulta (filtro customizável)
def imprimir_sexta_consulta(cursos_filtrados):
    if not cursos_filtrados:
        print("\nNehum curso encontrado com os critérios\n")
        return
    
    print("\n" + "=" * 80)
    print("CURSOS COM OS CRITÉRIOS ESCOLHIDOS".center(80))
    print("=" * 80 + "\n")

    # Mostrar os cursos encontrados
    for curso in cursos_filtrados:
        print(f"•{curso.nome}")

    print('\n')
        