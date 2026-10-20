"""Cod05: laço principal do Algoritmo Genético.

Obs: usar python ag.py caminho/da/instancia.ins2D [semente]
---------------------------------------------------------"""
import random
import sys
import time

from instancia import ler_instancia, limite_inferior
from aptidao import avaliar
from operadores import selecao_torneio, cruzamento_ox, mutacao_troca

"""Roda o AG uma vez e devolve um dicionário com o resultado.
    Parâmetros:
      tam_pop -> quantos indivíduos (ordens) há em cada geração
      geracoes -> quantas gerações são produzidas
      taxa_cruzamento -> chance de um par de pais cruzar (senão o filho é cópia do pai 1)
      taxa_mutacao -> chance de um filho sofrer a troca de duas peças
      k_torneio -> quantos indivíduos disputam cada torneio
      elitismo -> quantos melhores passam direto para a próxima geração
      semente -> fixa o sorteio: mesma semente, mesmo resultado
-------------------------------------------------------------------------------------"""
def executar_ag(pecas, W, H, tam_pop=50, geracoes=100,
                taxa_cruzamento=0.9, taxa_mutacao=0.2,
                k_torneio=3, elitismo=1,
                semente=None, verbose=False):
    
    rng = random.Random(semente)
    n = len(pecas)
    inicio = time.time()

    # 1. população inicial: ordens aleatórias
    populacao = []
    for _ in range(tam_pop):
        ordem = list(range(n))
        rng.shuffle(ordem)
        populacao.append(ordem)

    historico = []   # (melhor aptidão, chapas do melhor) ao fim de cada geração
    for g in range(geracoes + 1):
        
        # 2. nota de cada indivíduo
        avaliacoes = [avaliar(ordem, pecas, W, H) for ordem in populacao]
        notas = [a[0] for a in avaliacoes]

        melhor = min(range(tam_pop), key=lambda i: notas[i])
        historico.append((notas[melhor], avaliacoes[melhor][1]))

        if verbose and g % 10 == 0:
            print(f"  geração {g:3d} | melhor aptidão {notas[melhor]:.3f} "
                  f"| {avaliacoes[melhor][1]} chapas")
        if g == geracoes:
            break

        # 3. nova geração: elite + filhos
        l_ordenados = sorted(range(tam_pop), key=lambda i: notas[i])  # coloca as posições
                                                                    #  dos indivíduos em ordem,
                                                                    # da menor nota para a maior
        l_nova_geracao = [list(populacao[i]) for i in l_ordenados[:elitismo]]

        while len(l_nova_geracao) < tam_pop:
            pai1 = selecao_torneio(populacao, notas, k_torneio, rng)
            pai2 = selecao_torneio(populacao, notas, k_torneio, rng)

            if rng.random() < taxa_cruzamento:
                filho = cruzamento_ox(pai1, pai2, rng)
            else:
                filho = list(pai1)

            filho = mutacao_troca(filho, taxa_mutacao, rng)
            l_nova_geracao.append(filho)

        populacao = l_nova_geracao

    return {
        "melhor_ordem": list(populacao[melhor]),
        "melhor_aptidao": notas[melhor],
        "melhor_chapas": avaliacoes[melhor][1],
        "historico": historico,
        "avaliacoes": tam_pop * (geracoes + 1),
        "tempo": time.time() - inicio,
    }

if __name__ == "__main__":
    caminho = sys.argv[1]
    semente = int(sys.argv[2]) if len(sys.argv) > 2 else None

    W, H, pecas = ler_instancia(caminho)
    piso = limite_inferior(W, H, pecas)
    print(f"{caminho}: chapa {W}x{H}; {len(pecas)} peças; piso = {piso} chapas\n")

    res = executar_ag(pecas, W, H, semente=semente, verbose=True)
    print(f"\nMelhor solução: {res['melhor_chapas']} chapas "
          f"(piso {piso}) | aptidão {res['melhor_aptidao']:.3f} "
          f"| {res['tempo']:.1f} s")