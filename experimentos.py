"""Cod06 (parte 1): experimentos (várias instâncias x várias execuções).

Para cada instância roda:
  - o AG, N_EXECUCOES vezes (sementes 0, 1, 2, ...);
  - a busca aleatória, com o mesmo número de avaliações e as mesmas sementes;
  - a ordem por área decrescente (determinística, uma vez só).

Uso:  python experimentos.py [número de execuções]
Lê as instâncias da pasta dados/ e grava, na pasta resultados/:
resultados.csv, convergencia.csv e resumo.csv (e imprime o resumo).
"""
import csv
import os
import random
import statistics
import sys
import time

from instancia import ler_instancia, limite_inferior
from aptidao import avaliar
from ag import executar_ag

# Pastas relativas a este arquivo, para funcionar de qualquer diretório
BASE = os.path.dirname(os.path.abspath(__file__))
PASTA_DADOS = os.path.join(BASE, "dados")            # arquivos .ins2D
PASTA_RESULTADOS = os.path.join(BASE, "resultados")  # CSVs de saída

# Instâncias do experimento (classe_nº de peças_instância). Edite à vontade.
INSTANCIAS = [
    "cl_01_040_01", "cl_01_060_01",
    "cl_05_040_01", "cl_05_060_01",
    "cl_09_040_01", "cl_09_060_01",
]

N_EXECUCOES = 10

# Parâmetros do AG (os mesmos valores vão para o relatório)
PARAMS = dict(tam_pop=50, geracoes=100,
              taxa_cruzamento=0.9, taxa_mutacao=0.2,
              k_torneio=3, elitismo=1)


def busca_aleatoria(pecas, W, H, avaliacoes, semente):
    """Sorteia `avaliacoes` ordens e guarda a melhor. Devolve (aptidão, chapas)."""
    rng = random.Random(semente)
    n = len(pecas)
    melhor = None
    for _ in range(avaliacoes):
        ordem = list(range(n))
        rng.shuffle(ordem)
        nota, chapas = avaliar(ordem, pecas, W, H)
        if melhor is None or nota < melhor[0]:
            melhor = (nota, chapas)
    return melhor


def estatisticas(valores):
    """(melhor, média, pior, desvio padrão) de uma lista; menor é melhor."""
    dp = statistics.stdev(valores) if len(valores) > 1 else 0.0
    return min(valores), statistics.mean(valores), max(valores), dp


def main():
    n_exec = int(sys.argv[1]) if len(sys.argv) > 1 else N_EXECUCOES
    linhas, convergencia, resumo = [], [], []

    for nome in INSTANCIAS:
        W, H, pecas = ler_instancia(os.path.join(PASTA_DADOS, nome + ".ins2D"))
        piso = limite_inferior(W, H, pecas)
        print(f"\n{nome}: chapa {W}x{H}, {len(pecas)} peças, piso {piso}", flush=True)

        # referência simples: peças maiores primeiro
        ordem = sorted(range(len(pecas)),
                       key=lambda i: -pecas[i][0] * pecas[i][1])
        nota_ad, chapas_ad = avaliar(ordem, pecas, W, H)
        linhas.append([nome, len(pecas), piso, "AreaDecrescente", 0,
                       chapas_ad, round(nota_ad, 4), 0.0])

        chapas_ag, chapas_al, tempos_ag, tempos_al = [], [], [], []
        for semente in range(n_exec):
            r = executar_ag(pecas, W, H, semente=semente, **PARAMS)
            chapas_ag.append(r["melhor_chapas"])
            tempos_ag.append(r["tempo"])
            linhas.append([nome, len(pecas), piso, "AG", semente,
                           r["melhor_chapas"], round(r["melhor_aptidao"], 4),
                           round(r["tempo"], 2)])
            for g, (nota, ch) in enumerate(r["historico"]):
                convergencia.append([nome, semente, g, round(nota, 4), ch])

            t0 = time.time()
            nota_al, ch_al = busca_aleatoria(pecas, W, H, r["avaliacoes"], semente)
            t_al = time.time() - t0
            chapas_al.append(ch_al)
            tempos_al.append(t_al)
            linhas.append([nome, len(pecas), piso, "Aleatoria", semente,
                           ch_al, round(nota_al, 4), round(t_al, 2)])
            print(f"  execução {semente + 1}/{n_exec}: AG {r['melhor_chapas']} | "
                  f"aleatória {ch_al}", flush=True)

        resumo.append([nome, len(pecas), piso, chapas_ad,
                       *estatisticas(chapas_ag), *estatisticas(chapas_al),
                       round(statistics.mean(tempos_ag), 1),
                       round(statistics.mean(tempos_al), 1)])

    os.makedirs(PASTA_RESULTADOS, exist_ok=True)
    with open(os.path.join(PASTA_RESULTADOS, "resultados.csv"), "w",
              newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["instancia", "n_pecas", "piso", "metodo", "semente",
                    "chapas", "aptidao", "tempo_s"])
        w.writerows(linhas)
    with open(os.path.join(PASTA_RESULTADOS, "convergencia.csv"), "w",
              newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["instancia", "semente", "geracao", "aptidao", "chapas"])
        w.writerows(convergencia)
    cab = ["instancia", "n_pecas", "piso", "area_decrescente",
           "ag_melhor", "ag_media", "ag_pior", "ag_dp",
           "alea_melhor", "alea_media", "alea_pior", "alea_dp",
           "ag_tempo_medio_s", "alea_tempo_medio_s"]
    with open(os.path.join(PASTA_RESULTADOS, "resumo.csv"), "w",
              newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(cab)
        w.writerows([[*l[:4], *[round(x, 2) for x in l[4:12]], l[12], l[13]]
                     for l in resumo])

    print(f"\nResumo ({n_exec} execuções; número de chapas, menor é melhor)")
    print(f"{'instância':14s}{'piso':>5s}{'área↓':>7s} | "
          f"{'AG: melhor':>10s}{'média':>7s}{'pior':>6s}{'dp':>6s} | "
          f"{'Aleat: melhor':>13s}{'média':>7s}{'pior':>6s}{'dp':>6s}")
    for l in resumo:
        print(f"{l[0]:14s}{l[2]:5d}{l[3]:7d} | "
              f"{l[4]:10d}{l[5]:7.1f}{l[6]:6d}{l[7]:6.2f} | "
              f"{l[8]:13d}{l[9]:7.1f}{l[10]:6d}{l[11]:6.2f}")
    print("\nArquivos gerados em resultados/: resultados.csv, convergencia.csv, resumo.csv")


if __name__ == "__main__":
    main()