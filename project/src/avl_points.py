# src/avl_points.py
"""
Árvore AVL (balanceada) para armazenar seleções por pontos.
Cada nó guarda payload = {'name':..., 'points':..., ...} e a chave usada para ordenar
é (points, name) — points primário (descendente quando necessário), name secundário.

Fornece:
- AVLNode: nó com altura armazenada
- AVL: insert, root, height, inorder (retorna valores em ordem crescente da chave)
- build_avl_from_stats(stats_list): constroi AVL a partir da lista de stats (qualquer ordem)
"""

from typing import Any, Optional, List, Tuple, Dict

class AVLNode:
    def __init__(self, key: Tuple[int, str], value: Dict[str, Any]):
        self.key = key
        self.value = value
        self.left: Optional['AVLNode'] = None
        self.right: Optional['AVLNode'] = None
        self.height: int = 1  # nó folha tem altura 1

    def __repr__(self):
        return f"AVLNode(key={self.key}, h={self.height}, val={self.value['name']})"

class AVL:
    def __init__(self):
        self.root: Optional[AVLNode] = None
        self._size = 0

    # ---------- helpers ----------
    def _node_height(self, node: Optional[AVLNode]) -> int:
        return node.height if node else 0

    def _update_height(self, node: AVLNode):
        node.height = 1 + max(self._node_height(node.left), self._node_height(node.right))

    def _balance_factor(self, node: Optional[AVLNode]) -> int:
        if not node:
            return 0
        return self._node_height(node.left) - self._node_height(node.right)

    # ---------- rotations ----------
    def _rotate_right(self, y: AVLNode) -> AVLNode:
        x = y.left
        T2 = x.right
        # rotate
        x.right = y
        y.left = T2
        # update heights
        self._update_height(y)
        self._update_height(x)
        return x

    def _rotate_left(self, x: AVLNode) -> AVLNode:
        y = x.right
        T2 = y.left
        # rotate
        y.left = x
        x.right = T2
        # update heights
        self._update_height(x)
        self._update_height(y)
        return y

    # ---------- insertion (recursivo) ----------
    def _insert_node(self, node: Optional[AVLNode], key: Tuple[int, str], value: Dict[str, Any]) -> AVLNode:
        # BST insert by key
        if node is None:
            self._size += 1
            return AVLNode(key, value)
        if key < node.key:
            node.left = self._insert_node(node.left, key, value)
        elif key > node.key:
            node.right = self._insert_node(node.right, key, value)
        else:
            # chave igual: atualizamos o payload (substituição)
            node.value = value
            return node

        # atualizar altura e balancear
        self._update_height(node)
        bf = self._balance_factor(node)

        # Left Left
        if bf > 1 and key < node.left.key:
            return self._rotate_right(node)
        # Right Right
        if bf < -1 and key > node.right.key:
            return self._rotate_left(node)
        # Left Right
        if bf > 1 and key > node.left.key:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
        # Right Left
        if bf < -1 and key < node.right.key:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node

    def insert(self, value: Dict[str, Any]):
        """
        value deve conter 'name' e 'points' (inteiro).
        A chave usada será (points, name).
        Observação: para ordenar por pontos decrescentes, a construção da chave/uso do inorder
        será invertida no consumo; aqui mantemos (points, name) para ordenação natural ascendente.
        """
        key = (value.get("points", 0), value.get("name", ""))
        self.root = self._insert_node(self.root, key, value)

    def root_value(self):
        return self.root.value if self.root else None

    def height(self) -> int:
        return self._node_height(self.root)

    def size(self) -> int:
        return self._size

    def inorder(self) -> List[Dict[str, Any]]:
        """Retorna lista de valores em ordem ascendente da chave (points asc, name asc)."""
        res: List[Dict[str, Any]] = []
        def _in(n: Optional[AVLNode]):
            if n is None:
                return
            _in(n.left)
            res.append(n.value)
            _in(n.right)
        _in(self.root)
        return res

# ---------- utilitário de construção ----------
def build_avl_from_stats(stats_list: List[Dict[str, Any]]) -> AVL:
    """
    Constrói AVL inserindo cada estatística.
    Complexidade: cada inserção O(log T), total O(T log T) para T seleções.
    """
    avl = AVL()
    for s in stats_list:
        avl.insert(s)
    return avl

# ---------- exemplo rápido ----------
if __name__ == "__main__":
    sample = [
        {"name": "A", "points": 10},
        {"name": "B", "points": 5},
        {"name": "C", "points": 12},
        {"name": "D", "points": 7},
    ]
    tree = build_avl_from_stats(sample)
    print("height:", tree.height())
    print("inorder (asc points):", tree.inorder())
