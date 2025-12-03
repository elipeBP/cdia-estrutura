# src/data_structs.py
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Team:
    name: str
    score: int = 0   # uso genérico; pode representar gols ou pontos conforme etapa

    def __repr__(self):
        return f"Team(name='{self.name}', score={self.score})"

class Match:
    def __init__(self, date: datetime, home_team: Team, away_team: Team,
                 tournament: str, city: str, country: str, neutral: bool,
                 home_score: int, away_score: int):
        self.date = date
        self.home_team = home_team
        self.away_team = away_team
        self.tournament = tournament
        self.city = city
        self.country = country
        self.neutral = neutral
        self.home_score = home_score
        self.away_score = away_score

    def total_goals(self) -> int:
        """Retorna a soma dos gols da partida."""
        return self.home_score + self.away_score

    def score_str(self) -> str:
        """Retorna 'home-away'."""
        return f"{self.home_score}-{self.away_score}"

    def to_list(self):
        """
        Retorna linha para gravação CSV no formato exigido:
        year,country,home_team,away_team,score
        """
        year = self.date.year
        return [str(year), self.country, self.home_team.name, self.away_team.name, self.score_str()]

    def __repr__(self):
        d = self.date.strftime("%Y-%m-%d")
        return (f"Match(date={d}, {self.home_team.name} {self.home_score} x "
                f"{self.away_score} {self.away_team.name}, country={self.country})")
