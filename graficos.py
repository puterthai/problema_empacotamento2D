"""Cod06 (parte 2): gráficos a partir de resultados.csv
e convergencia.csv.

Lê os CSVs da pasta resultados/ e envia para ela
    os arquivos convergencia.png e comparacao.png
Precisa do matplotlib:  pip install matplotlib
---------------------------------------------------------"""
import csv
import os
import statistics
from collections import defaultdict

import matplotlib.pyplot as plt

# Pasta de resultados, relativa a este arquivo (funciona de qualquer diretório)
PASTA_RESULTADOS = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "resultados")

# Cores (paleta validada para daltonismo): AG = azul
COR_AG = "#2a78d6"
COR_LB = "#52514e"
TEXTO = "#0b0b0b"
TEXTO_2 = "#52514e"
GRADE = "#e3e2de"
FUNDO = "#fcfcfb"

plt.rcParams.update({
    "figure.facecolor": FUNDO, "axes.facecolor": FUNDO,
    "axes.edgecolor": GRADE, "axes.labelcolor": TEXTO_2,
    "xtick.color": TEXTO_2, "ytick.color": TEXTO_2,
    "text.color": TEXTO, "axes.titlecolor": TEXTO,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.color": GRADE, "grid.linewidth": 0.8,
    "axes.axisbelow": True, "font.size": 10,
})


def ler(caminho):
    with open(caminho, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def grafico_convergencia(conv, resultados, instancias):
    """Uma janela por instância: aptidão do melhor indivíduo ao longo das
    gerações (média das execuções e faixa do melhor ao pior)."""
    ncols = 3
    nrows = -(-len(instancias) // ncols)
    fig, eixos = plt.subplots(nrows, ncols, figsize=(13, 3.4 * nrows),
                              squeeze=False)
    for ax, nome in zip(eixos.flat, instancias):
        por_geracao = defaultdict(list)
        for r in conv:
            if r["instancia"] == nome:
                por_geracao[int(r["geracao"])].append(float(r["aptidao"]))
        ger = sorted(por_geracao)
        media = [statistics.mean(por_geracao[g]) for g in ger]
        minimo = [min(por_geracao[g]) for g in ger]
        maximo = [max(por_geracao[g]) for g in ger]
        ax.fill_between(ger, minimo, maximo, color=COR_AG, alpha=0.15,
                        linewidth=0, label="Melhor e pior execução")
        ax.plot(ger, media, color=COR_AG, linewidth=2,
                label="AG (média das execuções)")

        n_pecas = next(r["n_pecas"] for r in resultados if r["instancia"] == nome)
        ax.set_title(f"{nome}  ({n_pecas} peças)", fontsize=10, loc="left")
        ax.set_xlabel("Geração")
        ax.set_ylabel("Aptidão (menor é melhor)")
    for ax in list(eixos.flat)[len(instancias):]:
        ax.axis("off")
    h, l = eixos.flat[0].get_legend_handles_labels()
    fig.legend(h, l, loc="upper center", ncol=2, frameon=False,
               bbox_to_anchor=(0.5, 1.0))
    fig.tight_layout(rect=(0, 0, 1, 0.92))
    fig.savefig(os.path.join(PASTA_RESULTADOS, "convergencia.png"), dpi=160)
    plt.close(fig)


def grafico_comparacao(resultados, instancias):
    """Diferença entre o AG e o UB publicado (melhor solução conhecida).
    Zero = igual ao melhor conhecido. Ponto: média das execuções; traço
    vertical: do melhor ao pior resultado; traço cinza: LB publicado (a
    faixa entre o LB e o zero é onde o ótimo pode estar)."""
    fig, ax = plt.subplots(figsize=(10, 4.2))
    rotulos = []
    for i, nome in enumerate(instancias):
        linhas = [r for r in resultados if r["instancia"] == nome]
        lb, ub = int(linhas[0]["lb_pub"]), int(linhas[0]["ub_pub"])
        v = [int(r["chapas"]) - ub for r in linhas]
        m = statistics.mean(v)
        ax.errorbar(i, m, yerr=[[m - min(v)], [max(v) - m]], fmt="o",
                    color=COR_AG, ecolor=COR_AG, elinewidth=2, capsize=4,
                    markersize=7, label="AG: média, melhor e pior" if i == 0 else None)
        ax.plot([i - 0.25, i + 0.25], [lb - ub, lb - ub], color=COR_LB,
                linewidth=3, label="LB publicado" if i == 0 else None)
        rotulos.append(f"{nome}\nLB {lb} | UB {ub}")
    ax.axhline(0, color=TEXTO, linewidth=1, label="UB publicado (melhor conhecido)")
    ax.set_xticks(range(len(instancias)))
    ax.set_xticklabels(rotulos, fontsize=8)
    ax.set_ylabel("Chapas a mais que o UB publicado")
    ax.set_ylim(-2, 2)
    ax.set_yticks([-2, -1, 0, 1, 2])
    ax.set_title("AG em relação ao melhor valor conhecido (0 = igual ao UB)",
                 loc="left")
    ax.grid(axis="x", visible=False)
    ax.legend(frameon=False, ncol=3, loc="upper left")
    fig.tight_layout()
    fig.savefig(os.path.join(PASTA_RESULTADOS, "comparacao.png"), dpi=160)
    plt.close(fig)


if __name__ == "__main__":
    resultados = ler(os.path.join(PASTA_RESULTADOS, "resultados.csv"))
    conv = ler(os.path.join(PASTA_RESULTADOS, "convergencia.csv"))
    instancias = list(dict.fromkeys(r["instancia"] for r in resultados))
    grafico_convergencia(conv, resultados, instancias)
    grafico_comparacao(resultados, instancias)
    print("Gráficos gerados em resultados/: convergencia.png, comparacao.png")