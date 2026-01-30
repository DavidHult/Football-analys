import kagglehub
import pandas as pd

# Download latest version
path = kagglehub.dataset_download("martj42/international-football-results-from-1872-to-2017")

print("Path to dataset files:", path)

df_goalscorers = pd.read_csv("filer/goalscorers.csv")
df_results = pd.read_csv("filer/results.csv")
df_shootouts = pd.read_csv("filer/shootouts.csv")
df_former_names = pd.read_csv("filer/former_names.csv")


df_forsta_1000 = df_results.head(1000).copy()
df_forsta_1000["total_score"] = df_forsta_1000["away_score"] + df_forsta_1000["home_score"]


# Total goals of the first 1000 matches played. 
total_goals_first_1000 = df_results.head(1000)[["away_score", "home_score"]].sum().sum()
print(total_goals_first_1000)


# AVG goals of the first 1000 matches played. 
average_goals_first_1000 = total_goals_first_1000 / 1000
print(average_goals_first_1000)


# Latest 1000 matches 
df_results.tail(1000)


total_goals_latest_1000 = df_results.tail(1000)[["away_score", "home_score"]].sum().sum()
print(total_goals_latest_1000)


# Average goals latest 1000 macthes
average_goals_latest_1000 = total_goals_latest_1000 / 1000
print(average_goals_latest_1000)


# Average minute someone scores
min_avg_goal = df_goalscorers["minute"].mean()
print(min_avg_goal)


# Who has scored the most goals
df_goalscorers["scorer"].value_counts().head(10)


# Who has scorde most golas excluding penalties
scorer_no_pen = df_goalscorers[df_goalscorers["penalty"] == False]
scorer_no_pen["scorer"].value_counts().head(10)


# How many games played and how many of them are wins
home = df_results[["home_team", "home_score", "away_score"]].copy()
home.columns = ["team", "goals_for", "goals_against"]

away = df_results[["home_team", "home_score", "away_score"]].copy()
away.columns = ["team", "goals_for", "goals_against"]

matches = pd.concat([home, away], ignore_index=True)

matches["win"]= matches["goals_for"] > matches["goals_against"]

summary = (matches.groupby("team").agg(matches_played =("team", "count"), wins=("win", "sum")).reset_index())
# Ends here


# Adding win percentage to the table
summary["win_percentage"] = (summary["wins"] / summary["matches_played"] * 100)

summary["win_percentage"] = summary["win_percentage"].round(2)

summary.sort_values("win_percentage", ascending=False).head(10)


# Cleaning the data and only allowing teams that have played more than 50 games
summary_clean = summary[summary["matches_played"] > 50]

summary_clean = (summary.query("matches_played > 50").sort_values("win_percentage", ascending=False))

summary_clean.head(20)

summary_clean.tail(20)


# Penalty shootouts statistics
wins = df_shootouts["winner"].value_counts()
wins.head(10)

matches_played = (
    pd.concat([
        df_shootouts["home_team"],
        df_shootouts["away_team"]
    ])
    .value_counts()
)

wins = df_shootouts["winner"].value_counts()

summary_pen = pd.DataFrame({
    "matches_played": matches_played,
    "wins": wins
}).fillna(0)

summary_pen["wins"] = summary_pen["wins"].astype(int)
summary_pen["win_percentage"] = (
    summary_pen["wins"] / summary_pen["matches_played"] * 100
).round(2)

summary_pen = summary_pen.sort_values("win_percentage", ascending=False)

summary_pen.head(10)

summary_pen_clean = summary_pen.query("matches_played >= 10")

summary_pen_clean.head(10)