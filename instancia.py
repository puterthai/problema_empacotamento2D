"""Cod01: leitura de uma instância da 2DPackLib (classe CLASS).

Formato do arquivo .ins2D:
  linha 1: m                      (número de peças)
  linha 2: W H                    (largura e altura da chapa)
  m linhas: índice, largura, altura, demanda, máx_cópias, lucro

Observação: só usamos largura e altura. As três últimas colunas
            valem sempre 1, 1 e 0 nesta classe e são ignoradas.
------------------------------------------------------------"""
import math

""" Lê um arquivo .ins2D e devolve (W, H, pecas).
    pecas é uma lista de tuplas (largura, altura), na ordem do arquivo.
"""
def ler_instancia(caminho):
    with open(caminho) as arq:
        linhas = []
        for l in arq:
            if l.strip():
                linhas.append(l.split())

    m = int(linhas[0][0])
    W = int(linhas[1][0])
    H = int(linhas[1][1])

    pecas = []
    for l in linhas[2:2 + m]:
            pecas.append((int(l[1]), int(l[2])))

    if not (len(pecas) == m):
        raise AssertionError("Número de peças diferente do informado")

    for w, h in pecas:
        # Verifica se a largura da peça (w) é menor ou igual a largura da chapa (W);
        # e se a altura da peça (h) é menor ou igual a altura da chapa (H).
        if not (w <= W and h <= H):
            raise AssertionError("A peça é maior que a chapa")
    
    return W, H, pecas

"""Menor número de chapas que a área total já exige.

    É um piso: nenhuma solução usa menos que isso, mas nem sempre
    dá para atingi-lo, por causa do formato das peças.
"""
def limite_inferior(W, H, pecas):
    area_total = 0
    # Soma a área de todas as peças
    for w, h in pecas:
        area_total = area_total + w * h

    area_chapa = W * H
    chapas_necessarias = area_total / area_chapa
    return math.ceil(chapas_necessarias)

if __name__ == "__main__":
    import sys
    caminho = sys.argv[1]
    W, H, pecas = ler_instancia(caminho)
    print(f"Chapa: {W}x{H}\nQtd de peças: {len(pecas)}\nPrimeiras peças: {pecas[:4]}")
    print(f"Limite inferior (por área): {limite_inferior(W, H, pecas)} chapas")