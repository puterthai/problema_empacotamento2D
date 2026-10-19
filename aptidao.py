"""Cod03: aptidão (fitness) de uma ordem de peças.

    aptidão = (nº de chapas - 1) + aproveitamento da chapa menos cheia

Menor é melhor. O aproveitamento de uma chapa é a área ocupada pelas
peças dividida pela área da chapa (vale entre 0 e 1).
------------------------------------------------------------"""
from decodificador import decodificar

def aproveitamentos(chapas, W, H):
    # Aproveitamento (0 a 1) de cada chapa.
    area_chapa = W * H
    return [sum(w * h for _, _, _, w, h in chapa) / area_chapa
            for chapa in chapas]

def calcular_aptidao(chapas, W, H):
    # Retorna a nota de um conjunto de chapas já montadas (menor é melhor)
    return (len(chapas) - 1) + min(aproveitamentos(chapas, W, H))

def avaliar(ordem, pecas, W, H):
    # Decodifica a ordem e devolve (aptidão, número de chapas)
    chapas = decodificar(ordem, pecas, W, H)
    return calcular_aptidao(chapas, W, H), len(chapas)

if __name__ == "__main__":
    # Exemplo dos tópicos 2 e 3: chapa 10 x 4, peças A, B, C, D
    W, H = 10, 4
    pecas = [(6, 3), (4, 2), (4, 2), (6, 1)]
    nomes = "ABCD"

    for ordem in ([0, 1, 2, 3], [1, 3, 2, 0]):
        chapas = decodificar(ordem, pecas, W, H)
        aprov = aproveitamentos(chapas, W, H)
        nota = calcular_aptidao(chapas, W, H)
        print("Ordem:", ", ".join(nomes[i] for i in ordem))
        print(f"  chapas: {len(chapas)}")
        print("  aproveitamento de cada chapa:",
              ", ".join(f"{a:.2f}" for a in aprov))
        print(f"  aptidão = ({len(chapas)} - 1) + {min(aprov):.2f} = {nota:.2f}")
        print()