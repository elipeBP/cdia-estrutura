# src/main.py
import csv
import os
from datetime import datetime
from src.data_structs import Team, Match

DATA_PATHS = [
    os.path.join("data", "results.csv"),
    os.path.join("project", "data", "results.csv"),
    os.path.join("..", "data", "results.csv")
]

def find_csv():
    for p in DATA_PATHS:
        if os.path.exists(p):
            return p
    # fallback: try absolute /mnt/data (quando for o ambiente do avaliador)
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
            # validações básicas: campos obrigatórios
            date_s = row.get("date", "").strip()
            home = row.get("home_team", "").strip()
            away = row.get("away_team", "").strip()
            home_score_s = row.get("home_score", "").strip()
            away_score_s = row.get("away_score", "").strip()
            country = row.get("country", "").strip()
            # descarta linhas com campos faltando
            if not (date_s and home and away and home_score_s != "" and away_score_s != ""):
                # Aqui optamos por descartar linhas incompletas.
                # Poderíamos também imputar, mas o enunciado pede que expliquemos no relatório.
                continue
            # parse date - o dataset costuma usar ISO (YYYY-MM-DD)
            parsed_date = None
            for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%Y-%m-%d %H:%M:%S"):
                try:
                    parsed_date = datetime.strptime(date_s, fmt)
                    break
                except Exception:
                    pass
            if parsed_date is None:
                # se não conseguiu parse, pula linha
                continue
            home_score = safe_int(home_score_s)
            away_score = safe_int(away_score_s)
            if home_score is None or away_score is None:
                continue
            tournament = row.get("tournament", "").strip()
            city = row.get("city", "").strip()
            neutral = parse_bool(row.get("neutral", "").strip())
            # criar objetos Team (ainda não somamos gols aqui; apenas encapsulamos)
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
    # decisão de estrutura (Etapa 2): usamos lista Python (array dinámico) para armazenar Match.
    # Justificativa: acesso sequencial, ordenação e iteração são necessárias nas etapas seguintes.
    # Complexidade: append é O(1) amortizado.
    # Exemplo rápido: print 5 primeiras partidas
    for i, m in enumerate(matches[:5], start=1):
        print(f"{i}. {m}")
    # gerar output/matches_summary.csv
    out_file = os.path.join("output", "matches_summary.csv")
    write_summary(matches, out_file)
    print(f"Arquivo gerado: {out_file} (total {len(matches)} linhas)")

if __name__ == "__main__":
    main()
