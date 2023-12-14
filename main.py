import pandas as pd
import numpy as np
from dataclasses import dataclass

players = {
    # "Martin Fulier": 100,
    "Максим Франчук": 90,
    "Alexey Kalinin": 90,
    "Pavlo": 85,
    # "Misha Liamtsau": 90,
    "Артем": 85,
    "Alex Dyachkov": 80,
    "Stepan": 75,
    "Vlad Goenko": 70,
    "Андрей Ладутько": 70,
    # "alext tro": 70,
    # "likato": 70,
    # "Roman Tyan": 70,
    "Влад": 70,
    "Evgeny": 65,
    "Alex": 65,
    "Nishan": 65,
    # "Kirill B": 55,
    "Bitcoin Garant": 30,
    "Роман": 30,
    # "Yury S": 30,
    # "Hayyim Vital": 30,
    "Yaugen": 70,
    "Aleksanrd": 100,
    "Сергей": 70,
    "Всеволод": 70,
}

to_df = []
for player, score in players.items():
    noise_degree = 0.07
    noise = np.random.uniform(1-noise_degree, 1+noise_degree)
    to_df.append({"name": player, "score": score * noise})
df = pd.DataFrame(to_df).sort_values(by="score", ascending=False)

@dataclass
class Player:
    name: str
    score: float


class Team:
    def __init__(self, team_name: str):
        self._team_name = team_name
        self._players: list[Player] = []

    def add_player(self, player: Player):
        self._players.append(player)

    @property
    def score(self):
        if not self._players:
            return 0
        return sum([player.score for player in self._players]) / len(self._players)

    @property
    def players(self):
        return self._players

    @property
    def size(self):
        return len(self._players)

    def __repr__(self):
        player_names = [player.name for player in self._players]
        players_str = "\n\t".join(player_names)
        return f"\t {players_str} \n"


n_teams = 3
teams = [Team(f"Team {i+1}") for i in range(n_teams)]

rounds = df.shape[0] / n_teams
for round in range(int(np.ceil(rounds))):
    team_scores = [(num, team.score) for num, team in enumerate(teams)]
    current_round_choice_order = sorted(team_scores, key=lambda x: x[1])
    for round_pick in range(n_teams):
        player_num = round * n_teams + round_pick
        if player_num >= df.shape[0]:
            break
        player = Player(name=df.iloc[player_num]["name"], score=df.iloc[player_num]["score"])
        team = teams[current_round_choice_order[round_pick][0]]
        print(f"Round {round+1}, pick {round_pick+1}: {player} -> {team._team_name}")
        team.add_player(player)

for num, team in enumerate(teams):
    print(f"Team {num+1}:")
    print(team)