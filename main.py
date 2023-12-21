import pandas as pd
import numpy as np
from dataclasses import dataclass

players_dict = {
    # "Martin Fulier": 100,
    "Aleksanrd": 100,
    "kirill s": 100,
    "Максим Франчук": 90,
    "Alexey Kalinin": 90,
    # "Pavlo": 85,
    # "Yaugen": 80,
    "Misha Liamtsau": 80,
    "Артем": 80,
    # "Alex Dyachkov": 85,
    # "Stepan": 75,
    "Vlad Goenko": 70,
    "Андрей Ладутько": 70,
    # "alext tro": 70,
    # "likato": 70,
    # "Roman Tyan": 70,
    "Влад": 70,
    "Evgeny": 65,
    "Alex": 65,
    "bitdrop228": 60,
    # "Nishan": 60,
    # "baitman": 70,
    # "Kirill B": 55,
    "Bitcoin Garant": 30,
    "Роман": 35,
    # "Yury S": 30,
    # "Hayyim Vital": 30,
    # "Сергей": 70,
    # "Всеволод": 70,
}

to_df = []
for player, score in players_dict.items():
    noise_degree = 0.03
    noise = np.random.uniform(1-noise_degree, 1+noise_degree)
    to_df.append({"name": player, "score": score * noise})
df = pd.DataFrame(to_df).sort_values(by="score", ascending=False)


@dataclass
class Player:
    name: str
    score: float

    def __gt__(self, other) -> bool:
        return self.score > other.score

    def __repr__(self):
        return f"{self.name}: {self.score:.2f}"


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

    def __repr__(self):
        player_names = [player.name for player in self._players]
        players_str = "\n\t".join(player_names)
        return f"{self._team_name}:\n\t{players_str} \n"


class Round:
    def __init__(self, round_name: str, players: list[Player], n_teams: int):
        self._round_name = round_name
        self._players = sorted(players)
        self.n_teams = n_teams

    def is_round_incomplete(self) -> bool:
        return len(self._players) < self.n_teams

    def __bool__(self):
        return bool(self._players)

    def round_best_player_score(self) -> float:
        if self._players:
            return self._players[0].score
        return 0

    def pick(self, strongest_first: bool = True):
        if self._players:
            return self._players.pop(-1 if strongest_first else 0)
        else:
            raise IndexError("No players left in the round")

    def __repr__(self):
        players = [str(player) for player in self._players]
        players_str = "\n\t".join(players)
        return f"{self._round_name}:\n\t{players_str} \n"


def break_into_rounds(df: pd.DataFrame, n_teams: int) -> list[Round]:
    df = df.sort_values(by="score", ascending=False)
    n_rounds = int(np.ceil(df.shape[0] / n_teams))
    rounds = []
    for n_round in range(n_rounds):
        round_name = f"Round {n_round + 1}"
        round_players = []
        for i in range(n_teams):
            player_num = n_round * n_teams + i
            if player_num >= df.shape[0]:
                break
            player = Player(name=df.iloc[player_num]["name"], score=df.iloc[player_num]["score"])
            round_players.append(player)
        rounds.append(Round(round_name, round_players, n_teams=n_teams))
    return rounds


def break_into_teams(df: pd.DataFrame, n_teams: int) -> list[Team]:
    teams = [Team(f"Team {i + 1}") for i in range(n_teams)]
    rounds = break_into_rounds(df, n_teams)
    for round in rounds:
        team_scores = [(num, team.score) for num, team in enumerate(teams)]
        min_team_score = min(team_scores, key=lambda x: x[1])[1]
        strongest_first = True
        if round.round_best_player_score() < min_team_score and round.is_round_incomplete():
            strongest_first = False
        # sort reverse by default bc we pop from the end (the strongest player to the weakest team)
        current_round_choice_order = sorted(team_scores, key=lambda x: x[1], reverse=strongest_first)
        while round:
            # pop the team from the end of the list. If strongest_first — pop the weakest team
            team_num, _ = current_round_choice_order.pop()
            # if strongest_first — pop the strongest player
            teams[team_num].add_player(round.pick(strongest_first=strongest_first))
    return teams


teams = break_into_teams(df, n_teams=3)

for num, team in enumerate(teams):
    print(team)