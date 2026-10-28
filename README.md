# Empacotamento bidimensional de retângulos com Algoritmo Genético

Algoritmo Genético (AG) para o problema de empacotamento bidimensional de
retângulos (peças orientadas, sem rotação), aplicado a instâncias do conjunto
CLASS da 2DPackLib. O método, a representação e os resultados estão descritos
no relatório vinculado à entrega do trabalho da disciplina.

## Requisitos

- Python 3.8 ou superior (testado com Python 3.13).
- O AG e os experimentos usam apenas a biblioteca padrão do Python.
- Os gráficos e o desenho da solução precisam do matplotlib.

## Como executar

Todos os comandos são executados **dentro da pasta do projeto**.

### 1. Reproduzir os resultados do relatório

```
python experimentos.py
python graficos.py
```

- `experimentos.py` roda o AG 10 vezes (sementes 0 a 9) em cada uma das 6
  instâncias e leva alguns minutos (a depender da configuração da máquina). Para outro número de execuções: `python experimentos.py 5`.
- `graficos.py` lê os CSV e gera as figuras. Precisa rodar depois de `experimentos.py`.

Arquivos gerados em `resultados/`:

| Arquivo | Conteúdo |
|---|---|
| `resultados.csv` | uma linha por execução: instância, LB e UB publicados, semente, nº de chapas, aptidão e tempo (s) |
| `resumo.csv` | por instância: LB, UB, melhor, média, pior e desvio-padrão do AG, execuções que atingiram o UB e tempo médio |
| `convergencia.csv` | melhor aptidão de cada geração, em cada execução |
| `comparacao.png` | AG em relação ao UB publicado |
| `convergencia.png` | evolução da aptidão ao longo das gerações |
| `solucao.png` | uma solução desenhada (gerada por `desenhar_solucao.py`) |

### 2. Rodar o AG em uma instância

```
python ag.py dados/cl_01_040_01.ins2D 3
```

O primeiro argumento é o arquivo da instância e o segundo (opcional) é a semente
do gerador de números aleatórios. Sem semente, cada execução dá um resultado
diferente. Imprime a melhor aptidão a cada 10 gerações e a melhor solução.

### 3. Desenhar uma solução

```
python desenhar_solucao.py [instância] [semente]
python desenhar_solucao.py cl_05_040_01 9
```

Roda o AG, confere que a solução é válida (cada peça uma vez, dentro da chapa,
sem sobreposição) e grava `resultados/solucao.png`. Sem argumentos, usa
`cl_05_040_01` com a semente 9.

## Reprodutibilidade

Cada execução do AG usa uma semente (0 a 9 nos experimentos). A mesma semente
reproduz exatamente a mesma solução e a mesma aptidão. Só o tempo de execução
varia de uma máquina para outra.

## Parâmetros do AG

Definidos em `PARAMS`, no início de `experimentos.py`:

| Parâmetro | Valor |
|---|---|
| Tamanho da população | 50 |
| Número de gerações | 100 |
| Taxa de cruzamento | 0,9 |
| Taxa de mutação (por filho) | 0,2 |
| Tamanho do torneio | 3 |
| Elitismo | 1 |

Cada execução avalia 50 x 101 = 5050 soluções.

## Dados

As instâncias são do conjunto CLASS da biblioteca 2DPackLib (Universidade de
Bolonha): https://site.unibo.it/operations-research/en/research/2dpacklib

Formato de cada arquivo `.ins2D`: a primeira linha traz o número de peças, a
segunda traz a largura e a altura da chapa, e cada linha seguinte traz o índice,
a largura e a altura de uma peça (as demais colunas não são usadas). O nome
`cl_05_040_01` significa classe 5, 40 peças, instância 01.

Para trocar as instâncias do experimento, edite o dicionário `PUBLICADO` em
`experimentos.py`. Cada entrada traz o nome da instância e os limites (LB, UB)
publicados por Blum et al. (2012), Apêndice A, Tabelas 6, 10 e 14.

## Referências

- C. Blum, V. Schmid e L. Baumgartner. *On solving the oriented two-dimensional
  bin packing problem under free guillotine cutting: exploiting the power of
  probabilistic solution construction.* arXiv:1209.0880, 2012.
- M. Iori, V. L. de Lima, S. Martello e M. Monaci. *2DPackLib: a two-dimensional
  cutting and packing library.* Optimization Letters, 16:471-480, 2022.