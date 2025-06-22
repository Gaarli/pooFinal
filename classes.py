'''
O módulo 'classes.py' implementa as classes que representam as disciplinas, cursos e unidades.
'''

# Classe para representar uma disciplina
class Disciplina:
    def __init__(self, codigo, nome, creditos_aula, creditos_trabalho,
                 carga_horaria, carga_estagio, carga_praticas, carga_atividades):
        # Inicializa os atributos
        self.codigo = codigo
        self.nome = nome
        self.creditos_aula = creditos_aula
        self.creditos_trabalho = creditos_trabalho
        self.carga_horaria = carga_horaria
        self.carga_estagio = carga_estagio
        self.carga_praticas = carga_praticas
        self.carga_atividades = carga_atividades

    # Função para imprimir as informações da Disciplinas na tela
    def mostrar(self):
        print(f"    • {self.codigo} - {self.nome}")
        print(f"          Créditos Aula: {self.creditos_aula} | Créditos Trabalho: {self.creditos_trabalho} | CH: {self.carga_horaria} | Estágio: {self.carga_estagio} | Práticas: {self.carga_praticas} | Atividades: {self.carga_atividades}")

# Classe para representar um curso
class Curso:
    def __init__(self, nome, unidade, duracao_ideal=0, duracao_minima=0, duracao_maxima=0, info_disponivel = True):
        # Inicializa os atributos
        self.info_disponivel = info_disponivel # indica se as informações do curso foi fornecida (está disponível)
        self.nome = nome
        self.unidade = unidade
        self.duracao_ideal = duracao_ideal
        self.duracao_minima = duracao_minima
        self.duracao_maxima = duracao_maxima
        self.obrigatorias = []
        self.optativas_livres = []
        self.optativas_eletivas = []
    
    # Função para adicionar uma disciplina no curso, de acordo com o seu tipo
    def adicionar_disciplina(self, disciplina, tipo):
        if tipo == "Disciplinas Obrigatórias":
            self.obrigatorias.append(disciplina)
        elif tipo == "Disciplinas Optativas Livres":
            self.optativas_livres.append(disciplina)
        elif tipo == "Disciplinas Optativas Eletivas":
            self.optativas_eletivas.append(disciplina)

    # Função para imprimir as informações do curso na tela
    def mostrar(self):
        print("\n" + "=" * 80)
        print(f'Curso: {self.nome}')
        print("=" * 80)
        print(f"  Duração Ideal: {self.duracao_ideal} | Mínima: {self.duracao_minima} | Máxima: {self.duracao_maxima}")
        print("\n  Disciplinas Obrigatórias:")
        for d in self.obrigatorias:
            d.mostrar()
        print("\n  Disciplinas Optativas Eletivas:")
        for d in self.optativas_eletivas:
            d.mostrar()
        print("\n  Disciplinas Optativas Livres:")
        for d in self.optativas_livres:
            d.mostrar()


# Classe para representar uma unidade
class Unidade:
    def __init__(self, nome):
        # Definição dos atributos
        self.nome = nome
        self.cursos = []

    # O método a seguir adiciona um curso à unidade
    def adicionar_curso(self, curso):
        self.cursos.append(curso)

    # O método a seguir imprime as informações da unidade, como seus cursos
    # Quando é chamado 'curso.mostrar()' as disciplinas também
    # são mostradas
    def mostrar(self):
        print(f"Unidade: {self.nome}")
        print(f"Total de cursos: {len(self.cursos)}")
        for curso in self.cursos:
            curso.mostrar()
            print("\n" + "=" * 80)
    
