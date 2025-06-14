# O módulo 'consulta.py' implementa as funções responsáveis pelas consultas do usuário

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