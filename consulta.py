# O módulo 'consulta.py' implementa as funções que realizam os filtros
# dos dados passados em formato de lista de unidades e retorna
# os dados coletados em dicionários

# A impressão dos dados retornados é realizada pelas funções
# de impressão, localizadas no módulo 'imprime.py'

# Importa os módulos e bibliotecas utilizados
import unicodedata # Importa a biblioteca para comparar sem acentos nas letras
from collections import defaultdict

# A função a seguir implementa a funcionalidade 1. Lista de cursos por unidades
# Define a função 'listar_cursos_por_unidade', que recebe uma lista de objetos de unidade como argumento.
def listar_cursos_por_unidade(lista_unidades):
    # Cria um dicionário vazio para armazenar a relação entre unidades e seus cursos.
    resultado = {}
    # Inicia um laço de repetição para processar cada 'unidade' dentro da 'lista_unidades'.
    for unidade in lista_unidades:
        # Obtém o nome da unidade atual e o armazena na variável 'nome_unidade'.
        nome_unidade = unidade.nome
        # Cria uma lista contendo os nomes de todos os cursos pertencentes à unidade atual.
        cursos = [curso.nome for curso in unidade.cursos]
        # Adiciona ao dicionário 'resultado' o nome da unidade como chave e a lista de cursos como valor.
        resultado[nome_unidade] = cursos
    # Retorna o dicionário 'resultado' preenchido.
    return resultado

# A função a seguir é auxiliar para remover os acentos durante a comparação
def remover_acentos(texto):
    # Normaliza a string para a forma NFKD, que separa os caracteres base dos seus acentos.
    nfkd = unicodedata.normalize('NFKD', texto)
    # Reconstrói a string, mantendo apenas os caracteres que não são acentos (combining chars).
    return "".join([c for c in nfkd if not unicodedata.combining(c)])

# A função a seguir implementa a funcionalidade 2. Dados de um determinado curso
def buscar_curso_por_nome(lista_unidades, nome_curso_busca):
    # Normaliza o termo de busca (minúsculas, sem acentos e espaços extras)
    termo = remover_acentos(nome_curso_busca.strip().lower())

    # Acumula cursos encontrados como tuplas (curso, unidade)
    cursos_encontrados = []

    for unidade in lista_unidades:
        for curso in unidade.cursos:
            nome_normalizado = remover_acentos(curso.nome.lower())
            if termo in nome_normalizado:
                cursos_encontrados.append((curso, unidade))

    if not cursos_encontrados:
        print("Nenhum curso encontrado com esse nome.")
        return

    # Se houver mais de um curso (ex.: turnos diferentes), peça para escolher
    if len(cursos_encontrados) > 1:
        print(f"\nForam encontrados {len(cursos_encontrados)} cursos com esse nome:")
        for i, (curso, unidade) in enumerate(cursos_encontrados, 1):
            print(f"{i} - {curso.nome} ({unidade.nome})")

        while True:
            try:
                escolha = int(input("Digite o número correspondente ao curso desejado: "))
                if 1 <= escolha <= len(cursos_encontrados):
                    curso, unidade = cursos_encontrados[escolha - 1]
                    print(f"\nCurso selecionado: {curso.nome} ({unidade.nome})\n")
                    curso.mostrar()
                    return
                else:
                    print("Número fora do intervalo. Tente novamente.")
            except ValueError:
                print("Entrada inválida. Digite apenas um número.")
    else:
        # Apenas um curso encontrado – mostra diretamente
        curso, unidade = cursos_encontrados[0]
        print(f"\nCurso encontrado: {curso.nome} ({unidade.nome})\n")
        curso.mostrar()

# A função a seguir implementa a funcionalidade 3. Dados de todos os cursos
def listar_dados_de_todos_os_cursos(lista_de_unidades):
    # Cria um dicionário vazio para armazenar os dados.
    resultado = {}
    # Itera sobre cada objeto 'unidade' na lista de unidades.
    for unidade in lista_de_unidades:
        # Associa o nome da unidade à sua lista completa de objetos de curso.
        resultado[unidade.nome] = unidade.cursos  # lista de objetos Curso
    # Retorna o dicionário preenchido com todas as unidades e seus cursos.
    return resultado

# A função a seguir implementa a funcionalidade 4. Dados de uma disciplina, inclusive quais cursos ela faz parte
def buscar_disciplina(lista_unidades, termo_busca):
    # Normaliza o termo de busca para minúsculas, sem espaços extras e sem acentos.
    termo_busca = remover_acentos(termo_busca.lower().strip())
    # Cria uma lista vazia para armazenar os resultados encontrados.
    resultados = []

    # Itera sobre cada unidade na lista de unidades.
    for unidade in lista_unidades:
        # Dentro de cada unidade, itera sobre seus respectivos cursos.
        for curso in unidade.cursos:
            # Junta todas as disciplinas (obrigatórias e optativas) do curso em uma lista única.
            todas = (
                [(d, "Obrigatória") for d in curso.obrigatorias] + # Adiciona as disciplinas obrigatórias.
                [(d, "Optativa Eletiva") for d in curso.optativas_eletivas] + # Adiciona as optativas eletivas.
                [(d, "Optativa Livre") for d in curso.optativas_livres] # Adiciona as optativas livres.
            )
            # Itera sobre a lista unificada de disciplinas para realizar a busca.
            for disciplina, tipo in todas:
                # Verifica se o termo de busca está no nome ou no código da disciplina.
                if termo_busca == remover_acentos(disciplina.nome.lower()) or termo_busca in disciplina.codigo.lower():
                    # Se encontrar, adiciona uma tupla com os dados da ocorrência aos resultados.
                    resultados.append((disciplina, curso.nome, unidade.nome, tipo))

    # Após a busca, verifica se nenhum resultado foi encontrado.
    if not resultados:
        return {}  # Nenhum resultado encontrado

    # Cria um dicionário para agrupar os resultados por disciplina.
    disciplinas_agrupadas = {}
    # Itera sobre a lista de resultados para organizá-los.
    for d, curso_nome, unidade_nome, tipo in resultados:
        # Verifica se a disciplina (pelo código) ainda não foi adicionada ao dicionário.
        if d.codigo not in disciplinas_agrupadas:
            # Se for a primeira ocorrência, cria a estrutura base para agrupar os dados.
            disciplinas_agrupadas[d.codigo] = {
                "disciplina": d, # Armazena o objeto da disciplina.
                "ocorrencias": [] # Cria uma lista para as ocorrências em diferentes cursos/unidades.
            }
        # Adiciona os detalhes da ocorrência atual (onde ela foi encontrada).
        disciplinas_agrupadas[d.codigo]["ocorrencias"].append({
            "curso": curso_nome, # O nome do curso onde a disciplina é ofertada.
            "unidade": unidade_nome, # A unidade responsável pelo curso.
            "tipo": tipo # O tipo da disciplina naquele curso (Obrigatória, Optativa, etc).
        })

    # Retorna o dicionário com as disciplinas encontradas e todas as suas ocorrências agrupadas.
    return disciplinas_agrupadas
  

# A função a seguir implementa a funcionalidade 5. Disciplinas que são usadas em mais de um curso
def disciplinas_em_varios_cursos(lista_unidades):
    # Cria uma lista única contendo todos os objetos de curso de todas as unidades.
    cursos = sum(map(lambda u: u.cursos, lista_unidades), [])

    # Mapeia: código da disciplina → conjunto de cursos onde aparece
    # Inicializa um dicionário especial onde cada novo item é um conjunto (set) vazio.
    disciplinas_por_curso = defaultdict(set)

    # Itera sobre cada curso da lista unificada.
    for curso in cursos:
        # Junta todas as disciplinas do curso (obrigatórias e optativas) em uma lista só.
        todas = curso.obrigatorias + curso.optativas_eletivas + curso.optativas_livres
        # Itera sobre cada disciplina encontrada no curso.
        for d in todas:
            # Adiciona o nome do curso ao conjunto de cursos que oferecem esta disciplina.
            disciplinas_por_curso[f"({d.codigo}) " + d.nome].add(curso.nome)

    # Filtro: apenas disciplinas que aparecem em 2 ou mais cursos
    # Converte os itens do dicionário em uma lista, mantendo apenas aqueles com mais de um curso associado.
    return list(filter(lambda item: len(item[1]) > 1, disciplinas_por_curso.items()))

# A função a seguir implementa a funcionalidade 6. Outras consultas que você ache relevantes.
def filtrar_cursos_funcional(lista_unidades, **filtros):
    # Coletar todos os cursos
    cursos = sum(map(lambda u: u.cursos, lista_unidades), [])

    def normalizar(texto):
        return texto.strip().lower() if isinstance(texto, str) else texto

    def get_todas_disciplinas(curso):
        return curso.obrigatorias + curso.optativas_eletivas + curso.optativas_livres

    def atende_filtros(curso):
        checks = []

        # unidade
        if "nome_unidade" in filtros and filtros["nome_unidade"]:
            checks.append(normalizar(filtros["nome_unidade"]) in normalizar(curso.unidade))

        # nome do curso
        if "nome_curso" in filtros and filtros["nome_curso"]:
            checks.append(normalizar(filtros["nome_curso"]) in normalizar(curso.nome))

        # duração mínima
        if "min_duracao" in filtros and filtros["min_duracao"] is not None:
            checks.append(int(curso.duracao_minima) >= int(filtros["min_duracao"]))

        # duração máxima
        if "max_duracao" in filtros and filtros["max_duracao"] is not None:
            checks.append(int(curso.duracao_maxima) <= int(filtros["max_duracao"]))

        # duração ideal
        if "ideal_duracao" in filtros and filtros["ideal_duracao"] is not None:
            checks.append(int(curso.duracao_ideal) == int(filtros["ideal_duracao"]))

        # disciplina por código
        if "codigo_disciplina" in filtros and filtros["codigo_disciplina"]:
            codigo_filtro = normalizar(filtros["codigo_disciplina"])
            disciplinas = get_todas_disciplinas(curso)
            checks.append(any(codigo_filtro in normalizar(d.codigo) for d in disciplinas))

        # disciplina por nome
        if "nome_disciplina" in filtros and filtros["nome_disciplina"]:
            nome_filtro = normalizar(filtros["nome_disciplina"])
            disciplinas = get_todas_disciplinas(curso)
            checks.append(any(nome_filtro in normalizar(d.nome) for d in disciplinas))

        return all(checks)

    # Aplicar filtros
    cursos_filtrados = list(filter(atende_filtros, cursos))

    return cursos_filtrados

# Função auxiliar da sexta consulta (filtro customizável)
# para ler os inputs do usuário
def solicitar_filtros_do_usuario():
    print("\nVamos coletar alguns filtros para buscar cursos:")
    print("Deixe em branco (aperte <enter>) caso não queira filtrar por um item.\n")

    filtros = {}

    filtros["nome_unidade"] = input("Nome da Unidade: ").strip() or None
    filtros["nome_curso"] = input("Nome do Curso: ").strip() or None

    try:
        filtros["min_duracao"] = int(input("Duração mínima (em semestres): ").strip() or 0)
    except ValueError:
        filtros["min_duracao"] = None

    try:
        filtros["max_duracao"] = int(input("Duração máxima (em semestres): ").strip() or 0)
    except ValueError:
        filtros["max_duracao"] = None

    try:
        filtros["ideal_duracao"] = int(input("Duração ideal (exata, em semestres): ").strip() or 0)
    except ValueError:
        filtros["ideal_duracao"] = None

    filtros["codigo_disciplina"] = input("Código da Disciplina: ").strip() or None
    filtros["nome_disciplina"] = input("Nome da Disciplina: ").strip() or None

    # Limpa filtros vazios
    filtros = {k: v for k, v in filtros.items() if v not in [None, '', 0]}

    return filtros