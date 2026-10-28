"""Cod04: operadores do AG (seleção, cruzamento e mutação).

Um indivíduo é uma ordem das peças: uma lista de índices sem repetição,
por exemplo [1, 3, 2, 0]. Todos os operadores devolvem uma lista nova e
sempre uma permutação válida (cada peça aparece uma única vez).
------------------------------------------------------------------"""
import random

# Sorteia k indivíduos e devolve (cópia do) que tiver a menor nota.
def selecao_torneio(populacao, notas, k=3, rng=random):
    l_sorteados = rng.sample(range(len(populacao)), k)   # Ex.: [17, 4, 42]
    vencedor = l_sorteados[0]       # Inicializa com o primeiro sendo o melhor
    for i in l_sorteados:
        if notas[i] < notas[vencedor]:    # Menor fitness é melhor
            vencedor = i
    return list(populacao[vencedor])      # Devolve uma cópia do vencedor

"""Cruzamento de ordem (OX):
    1. Copia para o filho um trecho do pai1, nas mesmas posições;
    2. Preenche as posições vazias, da esquerda para a direita, com as
       peças que faltam, na ordem em que aparecem no pai2.

    cortes=(a, b) fixa o trecho [a, b) (útil para testar).
    Se None, sorteia.
"""
def cruzamento_ox(pai1, pai2, rng=random, cortes=None):
    n = len(pai1)
    if cortes is None:
        a, b = sorted(rng.sample(range(n + 1), 2))
    else:
        a, b = cortes
    filho = [None] * n
    filho[a:b] = pai1[a:b]     # Copia do pai1 as posições de a até b-1
    ja_no_filho = set(pai1[a:b])    # Anota quais peças já estão no filho
    faltam = iter(p for p in pai2 if p not in ja_no_filho)
    for i in range(n):
        if filho[i] is None:
            filho[i] = next(faltam)
    return filho

# Com probabilidade `taxa`, troca duas peças de posição.
# posicoes=(i, j) fixa as posições trocadas
def mutacao_troca(individuo, taxa, rng=random, posicoes=None):
    novo = list(individuo)
    if rng.random() < taxa:
        if posicoes is None:
            i, j = rng.sample(range(len(novo)), 2)
        else:
            i, j = posicoes
        novo[i], novo[j] = novo[j], novo[i]
    return novo

if __name__ == "__main__":
    nomes = "ABCDEF"
    def txt(ordem):
        return " ".join(nomes[i] for i in ordem)

    # --- Seleção por torneio ---
    # Três indivíduos com notas 1.45, 1.80 e 2.10. Como k = 3,
    # os três são sorteados e a nota 1.45 tem de vencer.
    populacao = [[0, 1, 2], [2, 1, 0], [1, 0, 2]]
    notas = [1.45, 1.80, 2.10]
    print("Torneio entre notas", notas)
    print("Vencedor:", selecao_torneio(populacao, notas, k=3),
          "(deve ser a primeira ordem, nota 1.45)")
    print()

    # --- Cruzamento OX (exemplo do tópico 4) ---
    pai1 = [0, 1, 2, 3, 4, 5]          # A B C D E F
    pai2 = [3, 5, 1, 0, 4, 2]          # D F B A E C
    filho = cruzamento_ox(pai1, pai2, cortes=(2, 4))   # trecho C D
    print("Cruzamento OX")
    print("  pai 1:", txt(pai1))
    print("  pai 2:", txt(pai2))
    print("  trecho do pai 1: posições 3 e 4 (C D)")
    print("  filho:", txt(filho))
    print()

    # --- Mutação por troca (exemplo do tópico 4) ---
    antes = filho
    depois = mutacao_troca(antes, taxa=1.0, posicoes=(0, 4))
    print("Mutação por troca (1ª com a 5ª posição)")
    print("  antes: ", txt(antes))
    print("  depois:", txt(depois))
    print()

    # --- Teste de segurança: nunca pode sair ordem inválida ---
    random.seed(0)
    for _ in range(10000):
        p1 = random.sample(range(30), 30)
        p2 = random.sample(range(30), 30)
        f = mutacao_troca(cruzamento_ox(p1, p2), taxa=0.5)
        assert sorted(f) == list(range(30))
    print("10000 cruzamentos + mutações aleatórios: todos os filhos são ordens válidas.")