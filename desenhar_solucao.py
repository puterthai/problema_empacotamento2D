"""Passo 7: desenha uma solução encontrada pelo AG (figura do relatório).

Uso:  python desenhar_solucao.py [instância] [semente]
      python desenhar_solucao.py cl_05_040_01 9      (valores padrão)

O que faz:
  1. roda o AG uma vez, com os mesmos parâmetros do experimento;
  2. decodifica a melhor ordem encontrada em chapas (Bottom-Left);
  3. confere que a solução é válida (toda peça uma vez, sem sobreposição);
  4. desenha uma chapa por quadro e grava resultados/solucao.png.
Precisa do matplotlib:  pip install matplotlib
"""
import os
import sys

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from instancia import ler_instancia
from decodificador import decodificar
from aptidao import aproveitamentos
from ag import executar_ag
# Importa os parâmetros e as pastas de experimentos.py para que a figura use
# exatamente as mesmas configurações da tabela de resultados.
# (o main() de experimentos.py só roda se o arquivo for executado direto)
from experimentos import PARAMS, PASTA_DADOS, PASTA_RESULTADOS

# Cores: peça em azul, parte vazia da chapa em cinza claro, borda em preto
COR_PECA = "#4a89d8"
COR_VAZIO = "#ebe9e5"
COR_BORDA_PECA = "white"
COLUNAS = 4            # quantas chapas por linha na figura
LIMIAR_ROTULO = 0.10   # só escreve o número se a peça tiver pelo menos 10% da
                       # chapa nas duas dimensões (peça fina não comporta texto)


def validar(chapas, pecas, W, H):
    """Confere a solução. Se algo estiver errado, o programa para (assert)."""
    # (a) toda peça aparece exatamente uma vez, no total das chapas
    usadas = sorted(i for chapa in chapas for i, *_ in chapa)
    assert usadas == list(range(len(pecas))), "peça faltando ou repetida"
    for chapa in chapas:
        for a, (i, x, y, w, h) in enumerate(chapa):
            # (b) a peça cabe inteira dentro da chapa
            assert x >= 0 and y >= 0 and x + w <= W and y + h <= H, "peça fora"
            # (c) não se sobrepõe a nenhuma outra peça da mesma chapa
            for j, px, py, pw, ph in chapa[a + 1:]:
                sobrepoe = x < px + pw and px < x + w and y < py + ph and py < y + h
                assert not sobrepoe, f"peças {i + 1} e {j + 1} se sobrepõem"


def desenhar(chapas, aproveit, W, H, caminho):
    """Desenha cada chapa em um quadro e salva a imagem em `caminho`."""
    n = len(chapas)
    linhas = -(-n // COLUNAS)       # divisão para cima: quantas linhas de quadros
    fig, eixos = plt.subplots(linhas, COLUNAS, figsize=(12, 3.2 * linhas),
                              squeeze=False)
    for k, ax in enumerate(eixos.flat):
        if k >= n:                  # sobrou quadro vazio na última linha
            ax.axis("off")
            continue
        # fundo da chapa (o que não for coberto por peça fica cinza)
        ax.add_patch(Rectangle((0, 0), W, H, facecolor=COR_VAZIO,
                               edgecolor="black", linewidth=0.8))
        for i, x, y, w, h in chapas[k]:
            ax.add_patch(Rectangle((x, y), w, h, facecolor=COR_PECA,
                                   edgecolor=COR_BORDA_PECA, linewidth=1.2))
            if w / W >= LIMIAR_ROTULO and h / H >= LIMIAR_ROTULO:
                # i + 1: o arquivo da instância numera as peças a partir de 1
                ax.text(x + w / 2, y + h / 2, str(i + 1), color="white",
                        ha="center", va="center", fontsize=8)
        ax.set_xlim(0, W)
        ax.set_ylim(0, H)
        ax.set_aspect("equal")      # 1 unidade em x = 1 unidade em y
        ax.set_xticks([])
        ax.set_yticks([])
        for lado in ax.spines.values():
            lado.set_visible(False)
        ax.set_title(f"Chapa {k + 1}: {aproveit[k] * 100:.0f}% ocupada",
                     fontsize=10)
    fig.tight_layout()
    fig.savefig(caminho, dpi=160)
    plt.close(fig)


if __name__ == "__main__":
    nome = sys.argv[1] if len(sys.argv) > 1 else "cl_05_040_01"
    semente = int(sys.argv[2]) if len(sys.argv) > 2 else 9

    W, H, pecas = ler_instancia(os.path.join(PASTA_DADOS, nome + ".ins2D"))
    res = executar_ag(pecas, W, H, semente=semente, **PARAMS)

    chapas = decodificar(res["melhor_ordem"], pecas, W, H)
    validar(chapas, pecas, W, H)
    aproveit = aproveitamentos(chapas, W, H)

    os.makedirs(PASTA_RESULTADOS, exist_ok=True)
    caminho = os.path.join(PASTA_RESULTADOS, "solucao.png")
    desenhar(chapas, aproveit, W, H, caminho)

    print(f"{nome}, semente {semente}: {len(chapas)} chapas, "
          f"aptidão {res['melhor_aptidao']:.4f}")
    print("ocupação de cada chapa (%):",
          [round(a * 100) for a in aproveit])
    for k, chapa in enumerate(chapas, start=1):
        print(f"  chapa {k}: peças {sorted(i + 1 for i, *_ in chapa)}")
    print(f"solução válida (sem sobreposição) | figura salva em {caminho}")