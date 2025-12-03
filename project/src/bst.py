# src/bst.py
"""
BST simples (não balanceada) para o trabalho de Estrutura de Dados.

Fornece:
- BSTNode: nó genérico com chave (string ou int) e payload (por exemplo, {'name':..., 'goals':...})
- BST: insert, find, inorder
- Construtores utilitários que recebem a lista de Match (do src.data_structs) e geram:
    * BST ordenada por nome da seleção (alfabética)
    * BST ordenada por total de gols da seleção (numérale)
"""

from typing import Any, Callable, List, Optional, Tuple, Dict

class BSTNode:
    def __init__(self, key: Any, value: Any):
        self.key = key
        self.value = value
        self.left: Optional['BSTNode'] = None
        self.right: Optional['BSTNode'] = None

    def __repr__(self):
        return f"BSTNode(key={self.key}, value={self.value})"

class BST:
    def __init__(self, key_func: Callable[[Any], Any] = lambda x: x):
        """
        key_func: função que extrai a chave de comparação a partir de 'value'.
                  Quando inserir, passe o payload como value e a BST usa key_func(value).
        """
        self.root: Optional[BSTNode] = None
        self.key_func = key_func
        self.size = 0

    def insert(self, value: Any):
        """Insere value; chave usada é key_func(value). Se chave já existe, atualiza o nodo (merge opcional)."""
        key = self.key_func(value)
        if self.root is None:
            self.root = BSTNode(key, value)
            self.size = 1
            return

        cur = self.root
        parent = None
        while cur:
            parent = cur
            if key < cur.key:
                cur = cur.left
            elif key > cur.key:
                cur = cur.right
            else:
                # chave igual: aqui escolhemos atualizar o payload —
                # como usamos BST para seleções, o value pode ser dicionário e faremos merge conforme necessidade.
                # O comportamento padrão: substituir.
                cur.value = value
                return

        node = BSTNode(key, value)
        if key < parent.key:
            parent.left = node
        else:
            parent.right = node
        self.size += 1

    def find(self, key: Any) -> Optional[Any]:
        cur = self.root
        while cur:
            if key == cur.key:
                return cur.value
            elif key < cur.key:
                cur = cur.left
            else:
                cur = cur.right
        return None

    def inorder(self) -> List[Any]:
        """Retorna lista de valores em ordem crescente da chave."""
        res: List[Any] = []
        def _in(n: Optional[BSTNode]):
            if n is None:
                return
            _in(n.left)
            res.append(n.value)
            _in(n.right)
        _in(self.root)
        return res

    def inorder_with_keys(self) -> List[Tuple[Any, Any]]:
        """Retorna lista de (key, value) em ordem."""
        res: List[Tuple[Any, Any]] = []
        def _in(n: Optional[BSTNode]):
            if n is None:
                return
            _in(n.left)
            res.append((n.key, n.value))
            _in(n.right)
        _in(self.root)
        return res

# ---------- utilitários específicos para o dataset ----------

def _accumulate_goals(matches) -> Dict[str, int]:
    """
    Recebe lista de Match e retorna dict {team_name: total_gols}.
    Complexidade: O(N) onde N = número de partidas.
    """
    totals: Dict[str, int] = {}
    for m in matches:
        # cada Match tem home_team.name e away_team.name e os gols no próprio match
        hname = m.home_team.name
        aname = m.away_team.name
        totals[hname] = totals.get(hname, 0) + m.home_score
        totals[aname] = totals.get(aname, 0) + m.away_score
    return totals

def build_bst_by_name(matches) -> BST:
    """
    Constroi uma BST ordenada por nome da seleção (chave = nome).
    Inserção em ordem alfabética é pedida: para obedecer ao enunciado,
    vamos primeiro obter a lista de nomes única e ordenada, e inserir nessa ordem.
    """
    # 1) coletar nomes e gols totais (para payload informativo)
    totals = _accumulate_goals(matches)
    # 2) criar lista de payloads (nome, gols)
    payloads = []
    for name, goals in totals.items():
        payloads.append({"name": name, "goals": goals})
    # 3) ordenar alfabeticamente por name
    payloads.sort(key=lambda x: x["name"])
    # 4) inserir na BST (chave será name)
    bst = BST(key_func=lambda v: v["name"])
    for p in payloads:
        bst.insert(p)
    return bst

def build_bst_by_goals(matches) -> BST:
    """
    Constrói uma BST onde a chave é a soma de gols da seleção (int).
    Atenção: múltiplas seleções podem ter o mesmo total de gols — para manter unicidade da chave,
    combinamos a chave (goals, name) ou transformamos payload para incluir name e usar tupla como chave.
    Aqui usaremos chave = (goals, name) para ordenação por gols primário e name secundário.
    """
    totals = _accumulate_goals(matches)
    payloads = []
    for name, goals in totals.items():
        # payload contém name e goals
        payloads.append({"name": name, "goals": goals})
    # construir BST com chave tuple (goals, name)
    bst = BST(key_func=lambda v: (v["goals"], v["name"]))
    for p in payloads:
        bst.insert(p)
    return bst

# ---------- funções auxiliares de conveniência ----------

def top_k_by_inorder_goals(bst: BST, k: int = 10, reverse: bool = True):
    """
    Retorna top-k seleções por gols usando inorder + seleção.
    Se reverse=True, retornamos do maior para o menor (inorder asc -> reverse).
    Complexidade: inorder O(T) onde T = número de seleções, slicing O(k).
    """
    items = bst.inorder()  # ordenados por (goals, name) ascendente
    if reverse:
        items = list(reversed(items))
    return items[:k]

# ---------- exemplo de uso rápido (quando rodar como script) ----------
if __name__ == "__main__":
    # pequeno teste manual se quiser executar diretamente.
    class M:
        def __init__(self, hname, aname, hs, as_):
            from types import SimpleNamespace
            self.home_team = SimpleNamespace(name=hname)
            self.away_team = SimpleNamespace(name=aname)
            self.home_score = hs
            self.away_score = as_

    sample = [
        M("Brazil", "Argentina", 2, 1),
        M("Argentina", "Chile", 1, 1),
        M("Brazil", "Chile", 3, 0),
        M("Peru", "Brazil", 0, 2)
    ]
    bname = build_bst_by_name(sample)
    bgoals = build_bst_by_goals(sample)
    print("Inorder by name (asc):")
    for v in bname.inorder():
        print(v)
    print("\nInorder by goals (asc):")
    for k, v in bgoals.inorder_with_keys():
        print(k, v)
    print("\nTop 2 by goals (desc):", top_k_by_inorder_goals(bgoals, 2))
