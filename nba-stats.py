import pandas as pd
from nba_api.stats.endpoints import ScoreboardV2, LeagueDashPlayerStats
from nba_api.stats.static import teams
from datetime import datetime
from pprint import PrettyPrinter
import sys
sys.stdout.reconfigure(encoding='utf-8')


# Today's Scoreboard
def get_scoreboard():
    today = datetime.today()
    score = ScoreboardV2(game_date=today.strftime("%Y-%m-%d"))
    games = score.get_data_frames()[0]

    if games.empty:
        print("No NBA games today.")
        return

    for _, game in games.iterrows():
        print(f"{game['VISITOR_TEAM_ABBREVIATION']} @ {game['HOME_TEAM_ABBREVIATION']}")
        print(f"{game['VISITOR_TEAM_SCORE']} - {game['HOME_TEAM_SCORE']}")
        print(f"Status: {game['GAME_STATUS_TEXT']}")
        print("--------------------")


def get_top_players(stat='PTS', top_n=10):
    # Fetching per-game stats for all players
    leaders = LeagueDashPlayerStats(per_mode_detailed='PerGame')
    leaders_df = leaders.get_data_frames()[0]

    if stat not in leaders_df.columns:
        print(f"Stat '{stat}' not found in player stats.")
        return

    # Sorting players by the selected stat
    leaders_df = leaders_df.sort_values(by=stat, ascending=False)
    print(f"\nTop {top_n} players by {stat}:")
    print(leaders_df[['PLAYER_NAME', 'TEAM_ABBREVIATION', stat]].head(top_n))


get_scoreboard()
get_top_players('PTS')
get_top_players('REB')
get_top_players('AST')
