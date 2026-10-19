"""Cod06 (parte 2): gráficos a partir de resultados.csv e convergencia.csv.

Uso:  python graficos.py
Lê os CSVs da pasta resultados/ e grava lá: convergencia.png e comparacao.png
Precisa do matplotlib:  pip install matplotlib
"""
import csv
import os
import statistics
from collections import defaultdict

import matplotlib.pyplot as plt

# Pasta de resultados, relativa a este arquivo (funciona de qualquer diretório)
PASTA_RESULTADOS = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "resultados")

# Cores (paleta validada para daltonismo): AG = azul, aleatória = laranja
COR_AG = "#2a78d6"
COR_AL = "#eb6834"
COR_PISO = "#52514e"
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
    gerações (média das execuções e faixa do melhor ao pior). A linha
    laranja é a média da busca aleatória, que não tem gerações."""
    ncols = 2
    nrows = -(-len(instancias) // ncols)
    fig, eixos = plt.subplots(nrows, ncols, figsize=(9, 3.2 * nrows),
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
                        linewidth=0)
        ax.plot(ger, media, color=COR_AG, linewidth=2, label="AG (média das execuções)")

        al = [float(r["aptidao"]) for r in resultados
              if r["instancia"] == nome and r["metodo"] == "Aleatoria"]
        ax.axhline(statistics.mean(al), color=COR_AL, linewidth=2,
                   linestyle="--", label="Busca aleatória (média)")

        n_pecas = next(r["n_pecas"] for r in resultados if r["instancia"] == nome)
        ax.set_title(f"{nome}  ({n_pecas} peças)", fontsize=10, loc="left")
        ax.set_xlabel("Geração")
        ax.set_ylabel("Aptidão (menor é melhor)")
    for ax in list(eixos.flat)[len(instancias):]:
        ax.axis("off")
    h, l = eixos.flat[0].get_legend_handles_labels()
    fig.legend(h, l, loc="upper center", ncol=2, frameon=False,
               bbox_to_anchor=(0.5, 1.0))
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    fig.savefig(os.path.join(PASTA_RESULTADOS, "convergencia.png"), dpi=160)
    plt.close(fig)


def grafico_comparacao(resultados, instancias):
    """Barras: número médio de chapas de cada método, com traço do melhor
    ao pior resultado nas execuções. O traço cinza é o piso por área."""
    fig, ax = plt.subplots(figsize=(11, 4.6))
    larg = 0.36
    for k, (metodo, cor, rotulo) in enumerate(
            [("AG", COR_AG, "AG"), ("Aleatoria", COR_AL, "Busca aleatória")]):
        xs, medias, abaixo, acima = [], [], [], []
        for i, nome in enumerate(instancias):
            v = [int(r["chapas"]) for r in resultados
                 if r["instancia"] == nome and r["metodo"] == metodo]
            m = statistics.mean(v)
            xs.append(i + (k - 0.5) * (larg + 0.03))
            medias.append(m)
            abaixo.append(m - min(v))
            acima.append(max(v) - m)
        ax.bar(xs, medias, width=larg, color=cor, label=rotulo,
               edgecolor=FUNDO, linewidth=1)
        ax.errorbar(xs, medias, yerr=[abaixo, acima], fmt="none",
                    ecolor=TEXTO, elinewidth=1, capsize=3)
    for i, nome in enumerate(instancias):
        piso = int(next(r["piso"] for r in resultados if r["instancia"] == nome))
        ax.plot([i - 0.42, i + 0.42], [piso, piso], color=COR_PISO, linewidth=2,
                label="Piso por área" if i == 0 else None)
    ax.set_xticks(range(len(instancias)))
    ax.set_xticklabels(instancias, rotation=20, ha="right")
    ax.set_ylabel("Número de chapas (menor é melhor)")
    ax.set_title("Chapas usadas: média de cada método e variação entre execuções",
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