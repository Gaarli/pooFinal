# O módulo 'classes.py' implementa as classes que representam as disciplinas, cursos e unidades

class Disciplina:
    def __init__(self, codigo, nome, creditos_aula, creditos_trabalho,
                 carga_horaria, carga_estagio, carga_praticas, carga_atividades):
        self.codigo = codigo
        self.nome = nome
        self.creditos_aula = creditos_aula
        self.creditos_trabalho = creditos_trabalho
        self.carga_horaria = carga_horaria
        self.carga_estagio = carga_estagio
        self.carga_praticas = carga_praticas
        self.carga_atividades = carga_atividades

    def mostrar(self):
        print(f"  {self.codigo} - {self.nome}, Créditos Aula: {self.creditos_aula}, Créditos Trabalho: {self.creditos_trabalho}")
        print(f"    CH: {self.carga_horaria}, Estágio: {self.carga_estagio}, Práticas: {self.carga_praticas}, Atividades: {self.carga_atividades}")


class Curso:
    def __init__(self, nome, unidade, duracao_ideal=0, duracao_minima=0, duracao_maxima=0, info_disponivel = True):
        self.info_disponivel = info_disponivel # indica se as informações do curso foi fornecido (está disponível)
        self.nome = nome
        self.unidade = unidade
        self.duracao_ideal = duracao_ideal
        self.duracao_minima = duracao_minima
        self.duracao_maxima = duracao_maxima
        self.obrigatorias = []
        self.optativas_livres = []
        self.optativas_eletivas = []

    def adicionar_disciplina(self, disciplina, tipo):
        if tipo == "Disciplinas Obrigatórias":
            self.obrigatorias.append(disciplina)
        elif tipo == "Disciplinas Optativas Livres":
            self.optativas_livres.append(disciplina)
        elif tipo == "Disciplinas Optativas Eletivas":
            self.optativas_eletivas.append(disciplina)

    def mostrar(self):
        print(f"  Duração Ideal: {self.duracao_ideal} | Mínima: {self.duracao_minima} | Máxima: {self.duracao_maxima}")
        print("\n  Disciplinas Obrigatórias:")
        for disciplina in self.obrigatorias:
            disciplina.mostrar()
        print("\n  Disciplinas Optativas Eletivas:")
        for disciplina in self.optativas_eletivas:
            disciplina.mostrar()
        print("\n  Disciplinas Optativas Livres:")
        for disciplina in self.optativas_livres:
            disciplina.mostrar()


class Unidade:
    def __init__(self, nome):
        self.nome = nome
        self.cursos = []

    def adicionar_curso(self, curso):
        self.cursos.append(curso)

    def mostrar(self):
        print(f"Unidade: {self.nome}")
        print(f"Total de cursos: {len(self.cursos)}")
        for curso in self.cursos:
            print("\n---------------------------")
            curso.mostrar()
    
