# src/main.py
import csv
import os
from datetime import datetime

from src.data_structs import Team, Match
from src.bst import build_bst_by_name, build_bst_by_goals, top_k_by_inorder_goals
from src.sorting import accumulate_points, top_k_by_points, bottom_k_by_points, merge_sort, insertion_sort
from src.avl_points import build_avl_from_stats
from src.search import linear_search, binary_search

# caminhos possíveis para facilitar execução em diferentes ambientes
DATA_PATHS = [
    os.path.join("data", "results.csv"),
    os.path.join("project", "data", "results.csv"),
    os.path.join("..", "data", "results.csv")
]

def find_csv():
    for p in DATA_PATHS:
        if os.path.exists(p):
            return p
    if os.path.exists("/mnt/data/results.csv"):
        return "/mnt/data/results.csv"
    raise FileNotFoundError("results.csv não encontrado. Coloque em project/data/results.csv")

def parse_bool(value: str) -> bool:
    if value is None:
        return False
    v = value.strip().lower()
    return v in ("1", "true", "yes", "y", "t")

def safe_int(value: str):
    try:
        return int(value)
    except Exception:
        return None

def read_matches(csv_path: str):
    matches = []
    total_read = 0
    total_valid = 0
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            total_read += 1
            date_s = row.get("date", "").strip()
            home = row.get("home_team", "").strip()
            away = row.get("away_team", "").strip()
            home_score_s = row.get("home_score", "").strip()
            away_score_s = row.get("away_score", "").strip()
            country = row.get("country", "").strip()
            if not (date_s and home and away and home_score_s != "" and away_score_s != ""):
                continue
            parsed_date = None
            for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%Y-%m-%d %H:%M:%S"):
                try:
                    parsed_date = datetime.strptime(date_s, fmt)
                    break
                except Exception:
                    pass
            if parsed_date is None:
                continue
            home_score = safe_int(home_score_s)
            away_score = safe_int(away_score_s)
            if home_score is None or away_score is None:
                continue
            tournament = row.get("tournament", "").strip()
            city = row.get("city", "").strip()
            neutral = parse_bool(row.get("neutral", "").strip())
            home_team = Team(name=home, score=home_score)
            away_team = Team(name=away, score=away_score)
            m = Match(parsed_date, home_team, away_team,
                      tournament, city, country, neutral, home_score, away_score)
            matches.append(m)
            total_valid += 1
    return matches, total_read, total_valid

def write_summary(matches, out_path):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    header = ["year", "country", "home_team", "away_team", "score"]
    with open(out_path, "w", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for m in matches:
            writer.writerow(m.to_list())

def demonstrate_searches(stats_list, sorted_by_name):
    print("\n--- Exemplos de buscas ---")
    # busca linear: encontrar seleção que comece com 'Brazil' (exemplo)
    idx = linear_search(stats_list, lambda s: s["name"].lower() == "brazil")
    if idx is not None:
        print("Linear search: encontrado Brazil nos stats (índice):", idx, stats_list[idx])
    else:
        print("Linear search: Brazil não encontrado nos stats.")

    # busca binária: precisa de lista ordenada por name asc
    # preparar lista ordenada por name (tupla key)
    names_sorted = merge_sort(sorted_by_name, key=lambda s: s["name"], reverse=False)
    bidx = binary_search(names_sorted, key_fn=lambda s: s["name"], target="Brazil")
    if bidx is not None:
        print("Binary search: encontrado Brazil em lista ordenada por nome (índice):", bidx, names_sorted[bidx])
    else:
        print("Binary search: Brazil não encontrado (lista ordenada por nome).")

def main():
    try:
        csv_path = find_csv()
    except FileNotFoundError as e:
        print(str(e))
        return
    print("Lendo CSV em:", csv_path)
    matches, total_read, total_valid = read_matches(csv_path)
    print(f"Linhas lidas: {total_read}")
    print(f"Partidas válidas processadas: {total_valid}")

    # salva resumo CSV (Etapa 6)
    out_file = os.path.join("output", "matches_summary.csv")
    write_summary(matches, out_file)
    print(f"Arquivo gerado: {out_file} (total {len(matches)} linhas)")

    # ---------- BSTs (Etapa 3) ----------
    bst_name = build_bst_by_name(matches)
    bst_goals = build_bst_by_goals(matches)
    print("\nBSTs construídas:")
    print("Total seleções na BST (nome):", bst_name.size)
    print("Total seleções na BST (gols):", bst_goals.size)

    top10_goals = top_k_by_inorder_goals(bst_goals, 10)
    print("\nTop 10 por gols (maiores):")
    for i, p in enumerate(top10_goals, 1):
        print(f"{i}. {p['name']} — {p['goals']} gols")

    # ---------- Pontos e Ordenação (Etapa 4) ----------
    stats = accumulate_points(matches)
    print(f"\nTotal seleções com estatísticas: {len(stats)}")

    print("\nTop 10 - por pontos (merge sort):")
    for i, s in enumerate(top_k_by_points(stats, 10, use_merge=True), 1):
        gd = s["goals_for"] - s["goals_against"]
        print(f"{i}. {s['name']} — {s['points']} pts (W{s['wins']} D{s['draws']} L{s['losses']}), GD={gd}")

    print("\nBottom 10 - por pontos (insertion sort):")
    for i, s in enumerate(bottom_k_by_points(stats, 10, use_merge=False), 1):
        gd = s["goals_for"] - s["goals_against"]
        print(f"{i}. {s['name']} — {s['points']} pts (W{s['wins']} D{s['draws']} L{s['losses']}), GD={gd}")

    # ---------- AVL por pontos (Etapa 5) ----------
    avl = build_avl_from_stats(stats)
    print("\nAVL construída por pontos:")
    print("Altura da AVL:", avl.height())
    print("Raiz (valor):", avl.root_value())
    print("Total de nós (seleções):", avl.size())

    vals_asc = avl.inorder()
    vals_desc = list(reversed(vals_asc))
    print("\nTop 10 por pontos (usando AVL inorder):")
    for i, s in enumerate(vals_desc[:10], 1):
        print(f"{i}. {s['name']} — {s['points']} pts")

    # ---------- Buscas (Etapa 5/Extra) ----------
    # Para busca binária por nome precisamos de lista ordenada por name asc
    demonstrate_searches(stats, stats)

    print("\nFinalizado. Verifique output/matches_summary.csv e os prints acima para incluir no relatório.")

if __name__ == "__main__":
    main()
