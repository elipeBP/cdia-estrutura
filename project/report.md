# Relatório do Trabalho Final — Estrutura de Dados

### Curso: Ciência de Dados e Inteligência Artificial

### Disciplina: Estrutura de Dados

### Docente: Paulo Felipe Salviano Brandt

---

# 1. Arquitetura do Projeto

A seguinte estrutura de pastas foi utilizada conforme solicitado no enunciado:

```
project/
├─ data/
│  └─ results.csv
├─ output/
│  └─ matches_summary.csv
├─ src/
│  ├─ data_structs.py
│  ├─ bst.py
│  ├─ sorting.py
│  ├─ avl_points.py
│  ├─ search.py
│  └─ main.py
└─ report.md
```

Cada módulo possui responsabilidade clara:

* **data_structs.py**: Classes `Team` e `Match`.
* **bst.py**: Implementação das árvores binárias de busca por nome e por gols.
* **sorting.py**: Implementação de Insertion Sort (O(n²)) e Merge Sort (O(n log n)) + cálculo de pontos.
* **avl_points.py**: Implementação da AVL para armazenar seleções por pontos.
* **search.py**: Busca linear e binária.
* **main.py**: Orquestra todo o fluxo do projeto.

---

# 2. Etapa 1 — Modelagem

### Estruturas criadas

* Classe **Team** contendo nome e gols/pontos.
* Classe **Match** contendo todos os atributos do arquivo CSV.
* Métodos importantes:

  * `total_goals()` → soma dos gols.
  * `to_list()` → linha formatada para o CSV final.

### Complexidade

* Criação de cada Match: **O(1)**.
* Armazenamento em lista: append amortizado **O(1)**.

---

# 3. Etapa 2 — Leitura do CSV

### Detalhes da Implementação

* Leitura via `csv.DictReader`.
* Linhas com dados faltantes foram **descartadas**.
* O tratamento de datas usa múltiplos formatos.

### Saída

* Impressão da quantidade de linhas lidas e válidas.
* Geração do arquivo **matches_summary.csv**.

### Complexidade

* Leitura total: **O(N)**.

---

# 4. Etapa 3 — Implementação das BSTs

### BST por Nome

* Ordenada alfabeticamente.
* Inserção em ordem **causa árvore degenerada**, conforme exigido.

### BST por Gols

* Chave → `(total_gols, nome)`.

### Complexidade

* Construção da BST por nome: **O(T²)** no pior caso.
* Construção da BST por gols: **O(T log T)** em média.

### Saída

* Top 10 seleções com mais gols.

---

# 5. Etapa 4 — Ordenações

### Algoritmos Implementados

* **Insertion Sort** — O(n²), estável.
* **Merge Sort** — O(n log n), estável.

### Cálculo de Pontos

Regras:

* Vitória = 3 pontos
* Empate = 1 ponto
* Derrota = 0

### Saídas

* Top 10 seleções com mais pontos (merge sort)
* Bottom 10 seleções com menos pontos (insertion sort)

---

# 6. Etapa 5 — Implementação da AVL

### Características

* Armazena seleções ordenadas por `(pontos, nome)`.
* Alturas atualizadas dinamicamente.
* Implementadas rotações: `LL`, `RR`, `LR`, `RL`.

### Complexidade

* Inserção: **O(log T)**.
* Construção da árvore: **O(T log T)**.

---

# 7. Etapa 6 — Geração do matches_summary.csv

Formato correto:

```
year,country,home_team,away_team,score
```

Complexidade de escrita: **O(N)**.

---

# 8. Etapa 7 — Métodos de Busca

### Busca Linear (stats)

* Predicado flexível.
* Complexidade: **O(T)**.

### Busca Binária

* Baseada em lista ordenada.
* Complexidade: **O(log T)**.

---

# 9. Análise Assintótica Geral do Projeto

| Etapa | Estrutura / Algoritmo | Complexidade |
| ----- | --------------------- | ------------ |
| 1     | Criação dos objetos   | O(N)         |
| 2     | Leitura e filtragem   | O(N)         |
| 3     | BST (nome)            | O(T²)        |
| 3     | BST (gols)            | O(T log T)   |
| 4     | Insertion Sort        | O(T²)        |
| 4     | Merge Sort            | O(T log T)   |
| 5     | AVL                   | O(T log T)   |
| 6     | Escrita CSV           | O(N)         |
| 7     | Busca Linear          | O(T)         |
| 7     | Busca Binária         | O(log T)     |

---

# 10. Considerações Finais

O trabalho cobre integralmente as estruturas pedidas: listas, BSTs, AVL, ordenações, busca e manipulação de arquivos. A arquitetura foi separada em módulos para organização e clareza.

O arquivo `main.py` executa todas as etapas de forma sequencial, permitindo reprodução fácil dos resultados.

---

# 11. Contribuição dos Integrantes (modelo)

*(Ajuste com os nomes dos membros do grupo)*

* **Aluno 1:** Implementação das classes `Match` e `Team`, leitura CSV.
* **Aluno 2:** Implementação das BSTs e acúmulo de gols.
* **Aluno 3:** Implementação do Merge Sort e cálculo de pontos.
* **Aluno 4:** Implementação da AVL.
* **Aluno 5:** Busca linear/binária, integração e geração do relatório.
* **Aluno 6:** Implementação da AVL.
---

Fim do relatório.
