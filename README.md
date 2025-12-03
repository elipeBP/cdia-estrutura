# Trabalho Final: Análise de Dados de Futebol com Estruturas de Dados

Este repositório contém o trabalho final da Unidade Curricular de **Estrutura de Dados** do curso de Bacharelado em Ciência de Dados e Inteligência Artificial do **Centro Universitário SENAI (UniSENAI)**, Santa Catarina.

O projeto consiste no processamento de um dataset histórico de partidas internacionais de futebol, implementando manualmente diversas estruturas de dados fundamentais e algoritmos de ordenação/busca para gerar estatísticas e rankings.

---

## Informações Gerais

* **Instituição:** UniSENAI - Centro Universitário SENAI Santa Catarina
* **Curso:** Ciência de Dados e Inteligência Artificial
* **Disciplina:** Estrutura de Dados
* **Docente:** Paulo Felipe Salviano Brandt
* **Linguagem:** Python 3
* **Dataset:** [Global Football Goalscorers Dataset (Kaggle)](https://www.kaggle.com/) - Arquivo `results.csv`

---

## Funcionalidades e Etapas do Projeto

O desenvolvimento foi dividido em etapas focadas na manipulação eficiente de dados e análise de complexidade (Big O):

### 1. Modelagem de Dados
Definição de classes heterogêneas para representar os dados:
* **Classe `Team`:** Representa uma seleção (Nome, Score/Pontos).
* **Classe `Match`:** Representa uma partida (Data, Times, Placar, Torneio, Localização).

### 2. Leitura e Estruturas Básicas
* Leitura do arquivo `data/results.csv`.
* Tratamento de dados e limpeza (remoção de linhas com dados faltantes).
* Armazenamento inicial dos objetos `Match` em uma estrutura linear (Lista/Fila/Pilha).

### 3. Árvores Binárias de Busca (BST)
Implementação de BSTs para agrupar Seleções por Gols Marcados:
* **BST 1:** Ordenada alfabeticamente pelo nome da seleção.
* **BST 2:** Ordenada pela quantidade total de gols (construída a partir de uma lista pré-processada).

### 4. Algoritmos de Ordenação
Implementação de dois algoritmos de ordenação (um $O(n \log n)$ e um $O(n^2)$) para criar um ranking de seleções baseado em **Pontos**:
* Vitória: 3 pontos.
* Empate: 1 ponto.
* Derrota: 0 pontos.
* **Saída:** Top 10 melhores e Top 10 piores seleções.

### 5. Árvore AVL (Balanceada)
Implementação de uma árvore AVL para organizar as partidas/seleções por Pontos, garantindo busca eficiente através de rotações (Left, Right, LR, RL) e controle de altura.

### 6. Exportação de Dados
Geração automática do arquivo `output/matches_summary.csv` contendo o resumo processado:
`year, country, home_team, away_team, score`

---

## Estrutura do Projeto

A organização de diretórios segue o padrão solicitado:

```text
project/
├─ data/
│  └─ results.csv           # Dataset de entrada (não incluído no git ignore se for grande)
├─ output/
│  └─ matches_summary.csv   # Arquivo gerado pelo programa
├─ src/
│  ├─ data_structs.py       # Definição das Classes Match e Team
│  ├─ bst.py                # Implementação da Binary Search Tree
│  ├─ avl.py                # Implementação da AVL Tree
│  ├─ sorting.py            # Algoritmos de ordenação (Bubble/Insertion e Merge/Quick)
│  ├─ search.py             # Algoritmos de busca (Linear e Binária)
│  └─ main.py               # Ponto de entrada e orquestrador
└─ report.md (ou .pdf)      # Relatório de arquitetura e análise assintótica
