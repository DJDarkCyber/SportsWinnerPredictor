from django.shortcuts import render
import pickle
from xgboost import XGBClassifier
from .models import PredictedHistory
from django.core.paginator import Paginator

import pandas as pd

# Create your views here.


def main(request):
    predictionHist = PredictedHistory.objects.all().order_by("-predicted_on")[:20]
    games = []
    teams_1 = []
    teams_2 = []
    results = []
    predictedTimes = []

    for predictions in predictionHist:
        games.append(predictions.game)
        teams_1.append(predictions.team_1)
        teams_2.append(predictions.team_2)
        results.append(predictions.result)
        predictedTimes.append(predictions.predicted_on)

    pred_items = zip(games, teams_1, teams_2, results, predictedTimes)

    print(pred_items)

    htmlVars = {
        "pred_items": pred_items,

    }
    return render(request, "index.html", htmlVars)

def predictOptions(request):
    return render(request, "predictOptions.html")


def predictionHistory(request):
    predictionHist = PredictedHistory.objects.all().order_by("-predicted_on")
    games = []
    teams_1 = []
    teams_2 = []
    results = []
    predictedTimes = []

    for predictions in predictionHist:
        games.append(predictions.game)
        teams_1.append(predictions.team_1)
        teams_2.append(predictions.team_2)
        results.append(predictions.result)
        predictedTimes.append(predictions.predicted_on)
    
    items = zip(games, teams_1, teams_2, results, predictedTimes)

    paginator = Paginator(list(items), 40)
    page = request.GET.get("page")
    items = paginator.get_page(page)

    htmlVars = {
        "items": items
    }


    return render(request, "predictionHistory.html", htmlVars)



def predictFootball(request):

    home_team = open("sportsPredictor/data/football/home_team")
    home_team = home_team.readlines()
    home_team = [item.lstrip() for item in home_team]
    home_team = [item.replace("\n", "") for item in home_team]

    away_team = open("sportsPredictor/data/football/away_team")
    away_team = away_team.readlines()
    away_team = [item.lstrip() for item in away_team]
    away_team = [item.replace("\n", "") for item in away_team]    

    tournaments = open("sportsPredictor/data/football/tournament")
    tournaments = tournaments.read()
    tournaments = tournaments.replace("\n", "").replace("\'", "").split(",")
    tournaments = [item.lstrip() for item in tournaments]

    cities = open("sportsPredictor/data/football/city")
    cities = cities.read()
    cities = cities.replace("\n", "").replace("\'", "").split(",")
    cities = [item.lstrip() for item in cities]

    countries = open("sportsPredictor/data/football/country")
    countries = countries.read()
    countries = countries.replace("\n", "").replace("\'", "").split(",")
    countries = [item.lstrip() for item in countries]

    # won_team = open("sportsPredictor/data/football/winner")
    # won_team = won_team.readlines()
    # won_team = [item.lstrip() for item in won_team]
    # won_team = [item.replace("\n", "") for item in won_team]

    

    htmlVars = {
        "home_teams": home_team,
        "away_teams": away_team,
        "tournaments": tournaments,
        "cities": cities,
        "countries": countries,
        # "won_teams": won_team
    }

    return render(request, "predictFootball.html", htmlVars)

def footballPredictionResult(request):
    if request.method == "POST":
        home_team = request.POST.get("HOMETEAM")
        away_team = request.POST.get("AWAYTEAM")
        tournament = request.POST.get("TOURNAMENT")
        city = request.POST.get("CITY")
        country = request.POST.get("COUNTRY")

        xclf = XGBClassifier()
        xclf.load_model("sportsPredictor/data/football/footballPredictorXGBModel.json")

        home_teams = open("sportsPredictor/data/football/home_team")
        home_teams = home_teams.readlines()
        home_teams = [item.lstrip() for item in home_teams]
        home_teams = [item.replace("\n", "") for item in home_teams]

        away_teams = open("sportsPredictor/data/football/away_team")
        away_teams = away_teams.readlines()
        away_teams = [item.lstrip() for item in away_teams]
        away_teams = [item.replace("\n", "") for item in away_teams]    

        tournaments = open("sportsPredictor/data/football/tournament")
        tournaments = tournaments.read()
        tournaments = tournaments.replace("\n", "").replace("\'", "").split(",")
        tournaments = [item.lstrip() for item in tournaments]

        cities = open("sportsPredictor/data/football/city")
        cities = cities.read()
        cities = cities.replace("\n", "").replace("\'", "").split(",")
        cities = [item.lstrip() for item in cities]

        countries = open("sportsPredictor/data/football/country")
        countries = countries.read()
        countries = countries.replace("\n", "").replace("\'", "").split(",")
        countries = [item.lstrip() for item in countries]

        won_teams = open("sportsPredictor/data/football/winner")
        won_teams = won_teams.readlines()
        won_teams = [item.lstrip() for item in won_teams]
        won_teams = [item.replace("\n", "") for item in won_teams]

        predictedWinner = xclf.predict([[home_teams.index(home_team), away_teams.index(away_team), tournaments.index(tournament), cities.index(city), countries.index(country)]])
        print([home_teams.index(home_team), away_teams.index(away_team), tournaments.index(tournament), cities.index(city), countries.index(country)])
        print(won_teams[predictedWinner[0]])

        won_team = won_teams[predictedWinner[0]]
        if won_team != home_team and won_team != away_team:
            won_team = "Error"
        
        if home_team == away_team:
            won_team = "Error"

        htmlVars = {
            "home_team": home_team,
            "away_team": away_team,
            "won_team": won_team
        }

        del xclf


        if won_team != "Error":
            prediction = PredictedHistory(game="Foot Ball", team_1=home_team, team_2=away_team, result=won_team)
            prediction.save()

        return render(request, "footballPredictionResult.html", htmlVars)


def predictBaseketball(request):

    home_teams = open("sportsPredictor/data/baseketball/HomeTeam")
    home_teams = home_teams.readlines()
    home_teams = [item.replace("\n", "") for item in home_teams]

    away_teams = open("sportsPredictor/data/baseketball/AwayTeam")
    away_teams = away_teams.readlines()
    away_teams = [item.replace("\n", "") for item in away_teams]    

    game_types = open("sportsPredictor/data/baseketball/GameType")
    game_types = game_types.readlines()
    game_types = [item.replace("\n", "") for item in game_types]  

    locations = open("sportsPredictor/data/baseketball/Location")
    locations = locations.readlines()
    locations = [item.replace("\n", "") for item in locations]      

    htmlVars = {
        "home_teams": home_teams,
        "away_teams": away_teams,
        "game_types": game_types,
        "locations": locations,
    }

    return render(request, "predictBaseketball.html", htmlVars)


def baseketballPredictionResult(request):
    if request.method == "POST":
        home_team = request.POST.get("HOMETEAM")
        away_team = request.POST.get("AWAYTEAM")
        game_type = request.POST.get("GAMETYPE")
        location = request.POST.get("LOCATION")

        xclf = XGBClassifier()
        xclf.load_model("sportsPredictor/data/baseketball/BaseketBallXGB.json")

        home_teams = open("sportsPredictor/data/baseketball/HomeTeam")
        home_teams = home_teams.readlines()
        home_teams = [item.replace("\n", "") for item in home_teams]

        away_teams = open("sportsPredictor/data/baseketball/AwayTeam")
        away_teams = away_teams.readlines()
        away_teams = [item.replace("\n", "") for item in away_teams]    

        game_types = open("sportsPredictor/data/baseketball/GameType")
        game_types = game_types.readlines()
        game_types = [item.replace("\n", "") for item in game_types]  

        locations = open("sportsPredictor/data/baseketball/Location")
        locations = locations.readlines()
        locations = [item.replace("\n", "") for item in locations]      

        won_teams = open("sportsPredictor/data/baseketball/WinningTeam")
        won_teams = won_teams.readlines()
        won_teams = [item.replace("\n", "") for item in won_teams]  

        predictedWinner = xclf.predict([[home_teams.index(home_team), away_teams.index(away_team), game_types.index(game_type), locations.index(location)]])
        print([home_teams.index(home_team), away_teams.index(away_team), game_types.index(game_type), locations.index(location)])
        print(won_teams[predictedWinner[0]])

        won_team = won_teams[predictedWinner[0]]
        if won_team != home_team and won_team != away_team:
            won_team = "Error"
        
        if home_team == away_team:
            won_team = "Error"

        htmlVars = {
            "home_team": home_team,
            "away_team": away_team,
            "won_team": won_team
        }

        del xclf


        if won_team != "Error":
            prediction = PredictedHistory(game="Baseket Ball", team_1=home_team, team_2=away_team, result=won_team)
            prediction.save()

        return render(request, "baseketballPredictionResult.html", htmlVars)


def predictHockey(request):

    home_teams = open("sportsPredictor/data/hockey/Home_Team")
    home_teams = home_teams.readlines()
    home_teams = [item.replace("\n", "") for item in home_teams]

    away_teams = open("sportsPredictor/data/hockey/Away_Team")
    away_teams = away_teams.readlines()
    away_teams = [item.replace("\n", "") for item in away_teams]    

    game_events = open("sportsPredictor/data/hockey/Event")
    game_events = game_events.readlines()
    game_events = [item.replace("\n", "") for item in game_events]  

    home_coaches = open("sportsPredictor/data/hockey/Home_Coach")
    home_coaches = home_coaches.readlines()
    home_coaches = [item.replace("\n", "") for item in home_coaches]

    away_coaches = open("sportsPredictor/data/hockey/Away_Coach")
    away_coaches = away_coaches.readlines()
    away_coaches = [item.replace("\n", "") for item in away_coaches]

    htmlVars = {
        "home_teams": home_teams,
        "away_teams": away_teams,
        "game_events": game_events,
        "home_coaches": home_coaches,
        "away_coaches": away_coaches
    }

    return render(request, "predictHockey.html", htmlVars)


def hockeyPredictionResult(request):
    if request.method == "POST":
        home_team = request.POST.get("HOMETEAM")
        away_team = request.POST.get("AWAYTEAM")
        game_event = request.POST.get("GAMEEVENT")
        home_coach = request.POST.get("HOMECOACH")
        away_coach = request.POST.get("AWAYCOACH")
        away_players = request.POST.get("AWAYPLAYERS")
        home_players = request.POST.get("HOMEPLAYERS")

        xclf = XGBClassifier()
        xclf.load_model("sportsPredictor/data/hockey/nhlXGBModel2.json")

        home_teams = open("sportsPredictor/data/hockey/Home_Team")
        home_teams = home_teams.readlines()
        home_teams = [item.replace("\n", "") for item in home_teams]

        away_teams = open("sportsPredictor/data/hockey/Away_Team")
        away_teams = away_teams.readlines()
        away_teams = [item.replace("\n", "") for item in away_teams]    

        game_events = open("sportsPredictor/data/hockey/Event")
        game_events = game_events.readlines()
        game_events = [item.replace("\n", "") for item in game_events]  

        home_coaches = open("sportsPredictor/data/hockey/Home_Coach")
        home_coaches = home_coaches.readlines()
        home_coaches = [item.replace("\n", "") for item in home_coaches]

        away_coaches = open("sportsPredictor/data/hockey/Away_Coach")
        away_coaches = away_coaches.readlines()
        away_coaches = [item.replace("\n", "") for item in away_coaches]  

        won_teams = open("sportsPredictor/data/hockey/Winning_Team")
        won_teams = won_teams.readlines()
        won_teams = [item.replace("\n", "") for item in won_teams]  



        predictedWinner = xclf.predict([[game_events.index(game_event), away_teams.index(away_team), home_teams.index(home_team), int(away_players), int(home_players), home_coaches.index(home_coach), away_coaches.index(away_coach)]])
        print([game_events.index(game_event), away_teams.index(away_team), home_teams.index(home_team), int(away_players), int(home_players), home_coaches.index(home_coach), away_coaches.index(away_coach)])
        print(won_teams[predictedWinner[0]])

        won_team = won_teams[predictedWinner[0]]

        if won_team == "Tie":
            pass
        elif won_team != home_team and won_team != away_team:
            won_team = "Error"
        
        elif home_team == away_team:
            won_team = "Error"

        htmlVars = {
            "home_team": home_team,
            "away_team": away_team,
            "won_team": won_team
        }

        del xclf


        if won_team != "Error":
            prediction = PredictedHistory(game="Hockey", team_1=home_team, team_2=away_team, result=won_team)
            prediction.save()

        return render(request, "hockeyPredictionResult.html", htmlVars)
