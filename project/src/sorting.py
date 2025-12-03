# src/sorting.py
from typing import List, Dict, Callable, Any

def safe_int(x):
    try:
        return int(x)
    except:
        return 0

def accumulate_points(matches):
    """
    Retorna dicionário {team: stats} onde stats = {
        'name','points','wins','draws','losses','goals_for','goals_against'
    }
    Regra: vitória = 3, empate = 1, derrota = 0.
    Complexidade: O(N) onde N = número de partidas.
    """
    stats: Dict[str, Dict] = {}
    def ensure(team):
        if team not in stats:
            stats[team] = {
                "name": team,
                "points": 0,
                "wins": 0,
                "draws": 0,
                "losses": 0,
                "goals_for": 0,
                "goals_against": 0
            }
    for m in matches:
        h = m.home_team.name
        a = m.away_team.name
        hs = safe_int(m.home_score)
        as_ = safe_int(m.away_score)
        ensure(h); ensure(a)
        stats[h]["goals_for"] += hs
        stats[h]["goals_against"] += as_
        stats[a]["goals_for"] += as_
        stats[a]["goals_against"] += hs
        if hs > as_:
            stats[h]["wins"] += 1
            stats[h]["points"] += 3
            stats[a]["losses"] += 1
        elif hs < as_:
            stats[a]["wins"] += 1
            stats[a]["points"] += 3
            stats[h]["losses"] += 1
        else:
            stats[h]["draws"] += 1
            stats[a]["draws"] += 1
            stats[h]["points"] += 1
            stats[a]["points"] += 1
    # transformar em lista
    return list(stats.values())

# ----------------- Sorts -----------------

def insertion_sort(arr: List[Any], key: Callable[[Any], Any] = lambda x: x, reverse: bool = False) -> List[Any]:
    """
    Insertion sort estável. O(n^2) tempo, O(1) espaço extra.
    Retorna nova lista ordenada (faz cópia para não alterar original).
    """
    a = arr[:]  # cópia
    n = len(a)
    for i in range(1, n):
        current = a[i]
        kcur = key(current)
        j = i - 1
        # while and move right
        if not reverse:
            while j >= 0 and key(a[j]) > kcur:
                a[j+1] = a[j]
                j -= 1
        else:
            while j >= 0 and key(a[j]) < kcur:
                a[j+1] = a[j]
                j -= 1
        a[j+1] = current
    return a

def merge_sort(arr: List[Any], key: Callable[[Any], Any] = lambda x: x, reverse: bool = False) -> List[Any]:
    """
    Merge sort estável. O(n log n) tempo, O(n) espaço adicional.
    """
    if len(arr) <= 1:
        return arr[:]
    mid = len(arr) // 2
    left = merge_sort(arr[:mid], key=key, reverse=reverse)
    right = merge_sort(arr[mid:], key=key, reverse=reverse)

    merged = []
    i = j = 0
    while i < len(left) and j < len(right):
        lv = key(left[i])
        rv = key(right[j])
        if not reverse:
            if lv <= rv:
                merged.append(left[i]); i += 1
            else:
                merged.append(right[j]); j += 1
        else:
            if lv >= rv:
                merged.append(left[i]); i += 1
            else:
                merged.append(right[j]); j += 1
    # append rest (mantém estabilidade)
    if i < len(left):
        merged.extend(left[i:])
    if j < len(right):
        merged.extend(right[j:])
    return merged

# ----------------- Helpers -----------------

def top_k_by_points(stats_list: List[Dict], k: int = 10, use_merge: bool = True):
    """
    Retorna top-k melhores (por pontos decrescentes). Se use_merge=True usa merge_sort (O(n log n)),
    caso contrário insertion_sort (O(n^2)).
    Tie-breakers: pontos, depois goal difference (goals_for - goals_against), depois name asc.
    """
    def key_fn(s):
        gd = s["goals_for"] - s["goals_against"]
        # queremos ordenar por: points desc, gd desc, name asc
        # Para usar os sorts que suportam apenas um valor, devolvemos tupla apropriada.
        return (s["points"], gd, -ord(s["name"][0]) if s["name"] else 0)  # name handled later by stable behavior

    # melhor formar key como tuple para ordenar asc/desc via reverse flag:
    # vamos criar wrapper que transforma em valor comparável simples:
    def key_wrapper(s):
        # para ordenação decrescente de points/gd e asc de name, devolvemos tuple: (points, gd, name_neg)
        return (s["points"], s["goals_for"] - s["goals_against"], s["name"])

    if use_merge:
        sorted_all = merge_sort(stats_list, key=key_wrapper, reverse=True)
    else:
        sorted_all = insertion_sort(stats_list, key=key_wrapper, reverse=True)
    topk = sorted_all[:k]
    return topk

def bottom_k_by_points(stats_list: List[Dict], k: int = 10, use_merge: bool = True):
    """
    Retorna k piores por pontos (menores pontos). Usa mesma tie-breaker invertido.
    """
    def key_wrapper(s):
        return (s["points"], s["goals_for"] - s["goals_against"], s["name"])
    if use_merge:
        sorted_all = merge_sort(stats_list, key=key_wrapper, reverse=False)
    else:
        sorted_all = insertion_sort(stats_list, key=key_wrapper, reverse=False)
    return sorted_all[:k]
