# src/search.py
from typing import List, Callable, Any, Optional

def linear_search(arr: List[Any], predicate: Callable[[Any], bool]) -> Optional[int]:
    """
    Busca linear: retorna índice do primeiro elemento que satisfaz predicate, ou None.
    Complexidade: O(N).
    """
    for i, v in enumerate(arr):
        if predicate(v):
            return i
    return None

def binary_search(arr: List[Any], key_fn: Callable[[Any], Any], target: Any) -> Optional[int]:
    """
    Busca binária iterativa: arr deve estar ordenado pela chave key_fn em ordem ascendente.
    Retorna índice se encontrado, senão None.
    Complexidade: O(log N).
    """
    lo = 0
    hi = len(arr) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        kval = key_fn(arr[mid])
        if kval == target:
            return mid
        elif kval < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return None
