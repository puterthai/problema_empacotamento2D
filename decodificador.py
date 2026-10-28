"""Cod02: decodificador Bottom-Left (genótipo -> fenótipo).

Entrada: uma ordem das peças (lista de índices), por exemplo [1, 3, 2, 0].
Saída: as chapas montadas. Cada chapa é uma lista de peças colocadas,
        e cada peça colocada é a tupla (índice, x, y, largura, altura).
        (x, y) é o canto inferior esquerdo; e y cresce para cima.
-----------------------------------------------------------------------"""

# Retorna verdadeiro se o retângulo (x, y, w, h) está dentro da chapa
# e não se sobrepõe a nenhuma peça já colocada.
def cabe(x, y, w, h, l_colocadas, W, H):
    if (x + w > W) or (y + h > H):
        return False

    # _ no começo do laço representa o índice da peça, que não será usado
    for _, px, py, pw, ph in l_colocadas:
        # Há sobreposição quando os intervalos em x e em y se cruzam
        if (x < px + pw) and (px < x + w) and (y < py + ph) and (py < y + h):
            return False
    
    return True

# Procura onde a peça (w x h) deve ficar dentro de UMA chapa.
# Regra Bottom-Left: escolhe a posição mais BAIXA onde ela cabe;
# se houver mais de uma na mesma altura, escolhe a mais à esquerda.
# Devolve (x, y), ou None se a peça não couber em nenhum lugar desta chapa.
def posicao_bottom_left(w, h, l_colocadas, W, H):
    conjunto_x = {0}
    for _, px, _, pw, _ in l_colocadas:
        conjunto_x.add(px + pw)
    xs = sorted(conjunto_x)

    conjunto_y = {0}
    for _, _, py, _, ph in l_colocadas:
        conjunto_y.add(py + ph)
    ys = sorted(conjunto_y)

    for y in ys:          # de baixo para cima
        for x in xs:      # da esquerda para a direita
            if cabe(x, y, w, h, l_colocadas, W, H):
                return x, y

    return None

# Coloca as peças na ordem dada, sempre na primeira chapa onde
# couberem (posição Bottom-Left). Abre chapa nova se não couber.
def decodificar(ordem, pecas, W, H):
    chapas = []
    for i in ordem:
        w, h = pecas[i]
        for chapa in chapas:
            pos = posicao_bottom_left(w, h, chapa, W, H)
            if pos is not None:
                chapa.append((i, pos[0], pos[1], w, h))
                break
        else:                # não coube em nenhuma chapa aberta
            chapas.append([(i, 0, 0, w, h)])
    return chapas

# Desenha cada chapa em texto. Peça i vira a letra A, B, C... (i=0 é A).
def desenhar(chapas, W, H):
    numero_da_chapa = 1
    for chapa in chapas:
        # 1) Cria a grade: H linhas, cada uma com W pontos "."
        grade = []
        for _ in range(H):
            nova_linha = []
            for _ in range(W):
                nova_linha.append(".")
            grade.append(nova_linha)

        # 2) Escreve a letra de cada peça nas células que ela ocupa
        for i, x, y, w, h in chapa:
            if i < 26:
                letra = chr(65 + i)
            else:
                letra = "#"
            for yy in range(y, y + h):
                for xx in range(x, x + w):
                    grade[yy][xx] = letra

        # 3) Imprime de cima para baixo
        print(f"Chapa {numero_da_chapa}")
        for linha in reversed(grade):
            texto = ""
            for caractere in linha:
                texto = texto + caractere
            print(texto)
        print()
        numero_da_chapa = numero_da_chapa + 1

if __name__ == "__main__":
    # Exemplo: chapa 10 x 4
    W, H = 10, 4

    # (largura, altura) das pecas A, B, C, D, respectivamente
    pecas = [(6, 3), (4, 2), (4, 2), (6, 1)]
    nomes = "ABCD"

    for ordem in ([0, 1, 2, 3], [1, 3, 2, 0]):     # A,B,C,D  e  B,D,C,A
        print("Ordem:", ", ".join(nomes[i] for i in ordem))
        chapas = decodificar(ordem, pecas, W, H)
        print(f"-> Resultado: {len(chapas)} chapa(s)\n")
        desenhar(chapas, W, H)