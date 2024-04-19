import os
from dotenv import load_dotenv
import requests
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import poisson

load_dotenv()

API_KEY = os.getenv('API_KEY')
BASE_URL = os.getenv('BASE_URL')
EUROPA_LEAGUE_ID = os.getenv('EUROPA_LEAGUE_ID')

headers = {
    'x-rapidapi-key': API_KEY,
    'x-rapidapi-host': 'api-football-v1.p.rapidapi.com'
}

def fetch_data(endpoint, params=None):
    """Utility function to fetch data from the API."""
    response = requests.get(f"{BASE_URL}{endpoint}", headers=headers, params=params)
    response.raise_for_status()
    return response.json()['response']

def list_countries():
    """Lists all countries available from the API."""
    countries = fetch_data("countries")
    print("Countries Available:")
    for country in countries:
        print(f"{country['name']} (Code: {country['code']})")
    return {country['name']: country['code'] for country in countries}



def list_leagues_by_country(country="Europe"):
    """Lists leagues for a specific country or for Europe."""
    querystring = {"country": country}
    leagues = fetch_data("leagues", params=querystring)
    print("\nLeagues Available:")
    league_dict = {}
    for league in leagues:
        print(f"{league['league']['name']} (ID: {league['league']['id']})")
        league_dict[league['league']['id']] = league['league']['name']
    return league_dict

def fetch_teams(league_id, season):
    """Fetch all teams participating in a league for a given season."""
    endpoint = "teams"
    params = {"league": league_id, "season": season}
    teams = fetch_data(endpoint, params)
    print(f"\nTeams Available:")
    team_dict = {team['team']['id']: team['team']['name'] for team in teams}
    for team_id, team_name in team_dict.items():
        print(f"- {team_name} (ID: {team_id})")
    return team_dict

def fetch_teams_for_europa_league(season):
    """Fetch all teams participating in the Europa League for a given season."""
    return fetch_teams(EUROPA_LEAGUE_ID, season)

def get_team_stats(team_id, league_id, season):
    """Fetch team statistics for a given team and season."""
    endpoint = "teams/statistics"
    params = {"team": team_id, "league": league_id, "season": season}
    stats = fetch_data(endpoint, params)
    goals_for_avg = stats.get('goals', {}).get('for', {}).get('average', {}).get('total', 0)
    goals_against_avg = stats.get('goals', {}).get('against', {}).get('average', {}).get('total', 0)
    return float(goals_for_avg), float(goals_against_avg)

def get_league_average_goals(league_id, season):
    """Calculate the average number of goals per match in a league for a given season."""
    endpoint = "fixtures"
    params = {"league": league_id, "season": season}
    fixtures = fetch_data(endpoint, params)
    total_goals = sum(fixture['goals']['home'] + fixture['goals']['away']
                      for fixture in fixtures if fixture['goals']['home'] is not None and fixture['goals']['away'] is not None)
    num_games = len([1 for fixture in fixtures if fixture['goals']['home'] is not None and fixture['goals']['away'] is not None])
    return total_goals / num_games if num_games > 0 else 2.5  


def plot_probabilities(match_results, home_team_name, away_team_name):
    colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99','#c2c2f0','#ffb3e6','#c4e17f']
    labels = ['Home Win', 'Draw', 'Away Win', 'Home/Draw', 'Away/Draw']
    sizes = [match_results['home_win'], match_results['draw'], match_results['away_win'], 
             match_results['home_or_draw'], match_results['away_or_draw']]
    explode = (0.1, 0, 0, 0, 0)  

    fig, ax = plt.subplots()
    wedges, texts, autotexts = ax.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
                                      shadow=True, startangle=90, colors=colors)

    ax.set_title(f'Probabilities for {home_team_name} vs {away_team_name}', fontsize=18, color='#333333')
    btts_x_position = -1.0  
    btts_y_position = 0.7   

    plt.text(btts_x_position, btts_y_position,
             f'BTTS Yes: {match_results["btts_yes"]:.2%}\nBTTS No: {match_results["btts_no"]:.2%}',
             fontsize=10, transform=ax.transAxes, color='black')

    over_under_x_position = 1.2  
    over_under_y_position = 0.7  
    over_under_text = '\n'.join([f"{key}: {value:.2%}" for key, value in match_results['over_under_goals_prob'].items()])
    plt.text(over_under_x_position, over_under_y_position, over_under_text,
             fontsize=10, transform=ax.transAxes, color='black')
    
    scores = match_results['top_scores']
    cell_text = [[f"{score[0]}-{score[1]}", f"{prob:.2%}"] for score, prob in scores if score]
    columns = ['Score', 'Probability']
    
    if cell_text:
        table = plt.table(cellText=cell_text, colLabels=columns, loc='upper left', cellLoc='center', colLoc='center',
                          bbox=[-0.4, 0.7, 0.28, 0.28])  
        table.auto_set_font_size(False)
        table.set_fontsize(12)
        table.scale(1.2, 1.2)
        for key, cell in table.get_celld().items():
            cell.set_edgecolor('darkgray')
    
    plt.subplots_adjust(left=0.3, bottom=0.2, right=0.8, top=0.8)
    plt.legend(wedges, labels, title="Match Outcomes", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
    plt.show()




def predict_match(home_team_id, away_team_id, league_id, season):
    top_n = int(input("Enter the number of most probable scores to display: ")) 
    home_goals_for, home_goals_against = get_team_stats(home_team_id, league_id, season)
    away_goals_for, away_goals_against = get_team_stats(away_team_id, league_id, season)
    league_avg_goals = get_league_average_goals(league_id, season)
    
    home_goals_expected = (home_goals_for / league_avg_goals) * (away_goals_against / league_avg_goals) * league_avg_goals
    away_goals_expected = (away_goals_for / league_avg_goals) * (home_goals_against / league_avg_goals) * league_avg_goals
    
    home_goals_prob = poisson.pmf(np.arange(10), home_goals_expected)
    away_goals_prob = poisson.pmf(np.arange(10), away_goals_expected)
    
    match_outcome = np.outer(home_goals_prob, away_goals_prob)
    home_win_prob = np.sum(np.tril(match_outcome, -1))
    draw_prob = np.sum(np.diag(match_outcome))
    away_win_prob = np.sum(np.triu(match_outcome, 1))
    
    home_or_draw_prob = home_win_prob + draw_prob
    away_or_draw_prob = away_win_prob + draw_prob
    
    btts_yes = 1 - (home_goals_prob[0] * away_goals_prob[0])
    btts_no = 1 - btts_yes
    
    top_scores = [(divmod(idx, 10), match_outcome.ravel()[idx]) for idx in np.argsort(match_outcome.ravel())[::-1][:top_n]]
    
    if btts_yes > 0.70:
        top_scores = [score for score in top_scores if score[0][0] > 0 and score[0][1] > 0]
    
    over_under_goals_prob = {}
    for i in range(6):
        over_under_goals_prob[f"Over {i}.5"] = 1 - poisson.cdf(i, home_goals_expected + away_goals_expected)
        over_under_goals_prob[f"Under {i}.5"] = poisson.cdf(i, home_goals_expected + away_goals_expected)
    
    return {
        "home_win": home_win_prob, "draw": draw_prob, "away_win": away_win_prob,
        "home_or_draw": home_or_draw_prob, "away_or_draw": away_or_draw_prob,
        "btts_yes": btts_yes, "btts_no": btts_no, "top_scores": top_scores,
        "over_under_goals_prob": over_under_goals_prob
    }


def main():
    choice = input("Choose 'E' for Europa League or 'A' for all leagues: ").upper()
    if choice == 'E':
        season = int(input("Enter the season year for Europa League predictions: "))
        teams_dict = fetch_teams_for_europa_league(season)
        league_id = EUROPA_LEAGUE_ID
    else:
        list_countries()
        country_name = input("Enter the country name for which you want leagues: ").strip()
        list_leagues_by_country(country_name)
        league_id = int(input("Enter the League ID for which you want teams: "))
        season = int(input("Enter the season (year) for which you want to predict the match: "))
        teams_dict = fetch_teams(league_id, season)

    if teams_dict:
        home_team_id = int(input("Enter the Home Team ID: "))
        away_team_id = int(input("Enter the Away Team ID: "))
        match_results = predict_match(home_team_id, away_team_id, league_id, season)
        home_team_name = teams_dict[home_team_id]
        away_team_name = teams_dict[away_team_id]
        plot_probabilities(match_results, home_team_name, away_team_name)
        print(match_results)
    else:
        print("No teams available for this season or league.")

if __name__ == "__main__":
    main()
