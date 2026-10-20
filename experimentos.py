"""Cod06 (parte 1): experimentos (várias instâncias x várias execuções).
 
Para cada instância roda o AG N_EXECUCOES vezes (sementes 0, 1, 2, ...) e
compara o número de chapas com os limites publicados por Blum et al. (2012),
Apêndice A: LB (limite inferior) e UB (melhor solução conhecida).
 
Uso:  python experimentos.py [número de execuções]
Lê as instâncias da pasta dados/ e grava, na pasta resultados/:
resultados.csv, convergencia.csv e resumo.csv (e imprime o resumo).
-----------------------------------------------------------------------"""
import csv
import os
import statistics
import sys
 
from instancia import ler_instancia, limite_inferior
from ag import executar_ag
 
# Pastas relativas a este arquivo, para funcionar de qualquer diretório
BASE = os.path.dirname(os.path.abspath(__file__))
PASTA_DADOS = os.path.join(BASE, "dados")            # arquivos .ins2D
PASTA_RESULTADOS = os.path.join(BASE, "resultados")  # CSVs de saída
 
# Instâncias do experimento e seus limites publicados: nome -> (LB, UB).
# Fonte: Blum, Schmid e Baumgartner (2012), Apêndice A, Tabelas 6, 10 e 14
# (instâncias numeradas de 1 a 500; aqui: linhas 11, 21, 211, 221, 411 e 421).
PUBLICADO = {
    "cl_01_040_01": (10, 10),
    "cl_01_060_01": (22, 23),
    "cl_05_040_01": (8, 8),
    "cl_05_060_01": (20, 20),
    "cl_09_040_01": (25, 25),
    "cl_09_060_01": (46, 46),
}
INSTANCIAS = list(PUBLICADO)
 
N_EXECUCOES = 10

# Parâmetros do AG (os mesmos valores vão para o relatório)
PARAMS = dict(tam_pop=50, geracoes=100, taxa_cruzamento=0.9,
              taxa_mutacao=0.2, k_torneio=3, elitismo=1)

def estatisticas(valores):
    """(melhor, média, pior, desvio padrão) de uma lista; menor é melhor."""
    dp = statistics.stdev(valores) if len(valores) > 1 else 0.0
    return min(valores), statistics.mean(valores), max(valores), dp
 
def main():
    n_exec = int(sys.argv[1]) if len(sys.argv) > 1 else N_EXECUCOES
    linhas, convergencia, resumo = [], [], []
 
    for nome in INSTANCIAS:
        W, H, pecas = ler_instancia(os.path.join(PASTA_DADOS, nome + ".ins2D"))
        lb, ub = PUBLICADO[nome]
 
        # Verificação: o limite inferior por área nunca pode passar do LB
        # publicado. Se passar, a instância foi associada à linha errada.
        piso = limite_inferior(W, H, pecas)
        assert piso <= lb, f"{nome}: piso por área {piso} > LB publicado {lb}"
        print(f"\n{nome}: chapa {W}x{H}, {len(pecas)} peças, "
              f"piso por área {piso}, publicado LB {lb} / UB {ub}", flush=True)
 
        chapas_ag, tempos_ag = [], []
        for semente in range(n_exec):
            r = executar_ag(pecas, W, H, semente=semente, **PARAMS)
            chapas_ag.append(r["melhor_chapas"])
            tempos_ag.append(r["tempo"])
            linhas.append([nome, len(pecas), lb, ub, semente,
                           r["melhor_chapas"], round(r["melhor_aptidao"], 4),
                           round(r["tempo"], 2)])
            for g, (nota, ch) in enumerate(r["historico"]):
                convergencia.append([nome, semente, g, round(nota, 4), ch])
            print(f"  execução {semente + 1}/{n_exec}: AG {r['melhor_chapas']} "
                  f"chapas (UB publicado: {ub})", flush=True)
 
        n_ub = sum(1 for c in chapas_ag if c <= ub)  # execuções que atingiram o UB
        resumo.append([nome, len(pecas), lb, ub, *estatisticas(chapas_ag),
                       n_ub, round(statistics.mean(tempos_ag), 1)])
 
    os.makedirs(PASTA_RESULTADOS, exist_ok=True)
    with open(os.path.join(PASTA_RESULTADOS, "resultados.csv"), "w",
              newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["instancia", "n_pecas", "lb_pub", "ub_pub", "semente",
                    "chapas", "aptidao", "tempo_s"])
        w.writerows(linhas)
    with open(os.path.join(PASTA_RESULTADOS, "convergencia.csv"), "w",
              newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["instancia", "semente", "geracao", "aptidao", "chapas"])
        w.writerows(convergencia)
    cab = ["instancia", "n_pecas", "lb_pub", "ub_pub",
           "ag_melhor", "ag_media", "ag_pior", "ag_dp",
           "execucoes_com_ub", "ag_tempo_medio_s"]
    with open(os.path.join(PASTA_RESULTADOS, "resumo.csv"), "w",
              newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(cab)
        w.writerows([[*l[:4], l[4], round(l[5], 2), l[6], round(l[7], 2),
                      l[8], l[9]] for l in resumo])
 
    print(f"\nResumo ({n_exec} execuções; número de chapas, menor é melhor)")
    print(f"{'instância':14s}{'LB':>4s}{'UB':>4s} | "
          f"{'AG: melhor':>10s}{'média':>7s}{'pior':>6s}{'dp':>6s} | "
          f"{'com UB':>7s}{'tempo(s)':>9s}")
    for l in resumo:
        print(f"{l[0]:14s}{l[2]:4d}{l[3]:4d} | "
              f"{l[4]:10d}{l[5]:7.1f}{l[6]:6d}{l[7]:6.2f} | "
              f"{l[8]:3d}/{n_exec:<3d}{l[9]:9.1f}")
    print("\nArquivos gerados em resultados/: resultados.csv, convergencia.csv, resumo.csv")
 
if __name__ == "__main__":
    main()
