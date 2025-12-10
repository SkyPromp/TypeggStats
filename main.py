#! /bin/python3

from DataApi import getLeaderboard, getQuotes, getRaces, getTop250RacesByPP
from StatsApi import findSatisfyingScores, getRacePpPb, histAccDistributionApi, histRecoveryTimeDistributionApi, histWPMDistributionApi, plotDifficultyByLength, plotPpByDifficulty, plotPpByLength, plotPpPerWpm, plotRacetime, plotTop250Pp, plotTotalPp, plotWpmByDifficulty, plotWpmByLength, quoteLikesPerUser, quotesPerUser
import matplotlib as mpl
import pickle
from DataSources import getQuote, getQuoteKeystrokes, getQuoteUserKeystrokes, getUserProfileData
from Stats import getQuotesIntersection, histWPMDistribution, histAccDistribution, histPpDistribution, flaneurQuotes, plotSpeedGraph
import numpy as np
import requests as r
import matplotlib.pyplot as plt

mpl.use("Qt5Agg")

ranked_quotes, unranked_quotes = getQuotes()

while True:
    statstype = input("""What statistics would you like to see?
    press 1 for: WPM distribution
    press 2 for: PP distribution
    press 3 for: Acc distribution
    press 4 for: What quotes you need to flaneur someone
    press 5 for: Quote leaderboard speed graph
    press 6 for: Quote comparison between specific users
    press 7 for: solo WPM distribution
    press 8 for: multi WPM distribution
    press 9 for: All WPM distribution
    press 10 for: All error recovery time distribution
    press 11 for: Total quote submissions per user
    press 12 for: Total quote likes per user
    press 13 for: Find all satisfying races
    press 14 for: Compare top 250 Non unique pp races
    press 15 for: Total racetime graph
    press 16 for: Total pp graph
    press 17 for: Get race quoteId's from old to new
    press 18 for: Get typing speed per quote length
    press 19 for: Get pp per quote length
    press 20 for: Get quote difficulty by quote length
    press 21 for: Get typing speed per quote difficulty
    press 22 for: Get pp per quote difficulty
    press 23 for: Get pp per typing speed
    press 24 for: Get acc distribution
    press 25 for: Compare top 250 unique pp races
    press 26 for: Checking the gauntlet
    """)

    match statstype:
        case "1":
            user = getUserProfileData(input("For what username would you like to get the graph? "))

            histWPMDistribution(user)
        case "2":
            user = getUserProfileData(input("For what username would you like to get the graph? "))

            histPpDistribution(user)
        case "3":
            user = getUserProfileData(input("For what username would you like to get the graph? "))

            histAccDistribution(user)
        case "4":
            user1 = getUserProfileData(input("What username are you? "))
            user2 = getUserProfileData(input("What username would you like to beat? "))

            flaneurQuotes(user1, user2)
        case "5":
            quote_id = input("What quote id would you like to check? ")

            # keystrokes_list = getQuoteKeystrokes(quote_id)
            keystrokes_list = list(map(lambda race: race["keystrokes"], getLeaderboard(quote_id)))
            
            plotSpeedGraph(*keystrokes_list)
        case "6":
            # quote_id = input("What quote id would you like to check? ")
            #
            # users = []
            # user = input("What username would you like to add to the list? type q to stop adding new ones ")
            #
            # while user != "q":
            #     users.append(user)
            #     user = input("What username would you like to add to the list? type q to stop adding new ones ")
            #
            getQuoteUserKeystrokes("thorsbc_2466", "flaneur")
            # keystrokes_list = [getQuoteUserKeystrokes(quote_id, username) for username in users]
        case "7":
            solo, multi = getRaces(input("For what username would you like to get the graph? "))

            histWPMDistributionApi(solo)
        case "8":
            solo, multi = getRaces(input("For what username would you like to get the graph? "))

            histWPMDistributionApi(multi)
        case "9":
            solo, multi = getRaces(input("For what username would you like to get the graph? "))

            histWPMDistributionApi(solo, alpha=0.5, label="solo")
            histWPMDistributionApi(multi, alpha=0.5, label="multi")

            plt.legend()
            plt.show()
        case "10":
            solo, multi = getRaces(input("For what username would you like to get the graph? "))

            try:
                histRecoveryTimeDistributionApi(solo, alpha=0.5, label="solo", exclude_zero=True)
            except Exception:
                pass
            try:
                histRecoveryTimeDistributionApi(multi, alpha=0.5, label="multi", exclude_zero=True)
            except Exception:
                pass

            plt.legend()
            plt.show()

        case "11":
            # print(ranked, unranked)
            print(len(ranked_quotes), len(ranked_quotes))

            try:
                quotesPerUser(ranked_quotes, alpha=0.5, label="ranked")
            except Exception:
                pass
            try:
                pass
                # quotesPerUser(unranked, alpha=0.5, label="unranked")
            except Exception:
                pass

            plt.legend()
            plt.show()
        case "12":
            # print(ranked, unranked)
            print(len(ranked_quotes), len(unranked_quotes))

            try:
                quoteLikesPerUser(ranked_quotes, alpha=0.5, label="ranked")
            except Exception:
                pass
            try:
                pass
                # quoteLikesPerUser(unranked, alpha=0.5, label="unranked")
            except Exception:
                pass

            plt.legend()
            plt.show()

        case "13":
            solo, multi = getRaces(input("For what username would you like to get the stats? "))
            findSatisfyingScores(np.concatenate([solo, multi]))

        case "14":
            username = input("For what username would you like to get the graph? ")

            while username != "q":
                races = getTop250RacesByPP(username)
                print(len(set(map(lambda race: race["quoteId"], races))))

                if races is not None:
                    print(len(races))
                    plotTop250Pp(races, label=username)

                username = input("For what username would you like to get the graph or q to show data: ")

            plt.legend()
            plt.show()
        
        case "15":
            username = input("For what username would you like to get the graph? ")

            while username != "q":
                solo, multi = getRaces(username)

                if solo is not None and multi is not None:
                    print("succeeded")
                    plotRacetime(np.concatenate([solo, multi]), label=username)
                else:
                    print("failed")

                username = input("For what username would you like to get the graph or q to show data: ")

            plt.legend()
            plt.show()

        case "16":
            username = input("For what username would you like to get the graph? ")

            while username != "q":
                solo, multi = getRaces(username)

                if solo is not None and multi is not None:
                    print("succeeded")
                    plotTotalPp(np.concatenate([solo, multi]), label=username)
                else:
                    print("failed")

                username = input("For what username would you like to get the graph or q to show data: ")

            plt.legend()
            plt.show()
        case "17":
            username = input("For what username would you like to get the stats? ")
            solo, multi = getRaces(username)
            print(list(map(lambda race: race["quoteId"], sorted(np.concatenate([solo, multi]), key=lambda race: race["timestamp"]))))

        case "18":
            username = input("For what username would you like to get the stats? ")
            solo, multi = getRaces(username)
            races = np.concatenate([solo, multi])
            races = getRacePpPb(races)

            plotWpmByLength(races, ranked_quotes, label=username)

            plt.legend()
            plt.show()

        case "19":
            username = input("For what username would you like to get the stats? ")
            solo, multi = getRaces(username)
            races = np.concatenate([solo, multi])

            plotPpByLength(races, ranked_quotes, label=username)

            plt.legend()
            plt.show()

        case "20":
            plotDifficultyByLength(ranked_quotes)

            plt.show()

        case "21":
            username = input("For what username would you like to get the stats? ")
            solo, multi = getRaces(username)
            races = np.concatenate([solo, multi])

            plotWpmByDifficulty(races, ranked_quotes, label=username)

            plt.legend()
            plt.show()

        case "22":
            username = input("For what username would you like to get the stats? ")
            solo, multi = getRaces(username)
            races = np.concatenate([solo, multi])

            plotPpByDifficulty(races, ranked_quotes, label=username)

            plt.legend()
            plt.show()
        case "23":
            username = input("For what username would you like to get the stats? ")

            while username != "q":
                solo, multi = getRaces(username)
                races = np.concatenate([solo, multi])
                races = getRacePpPb(races)
                plotPpPerWpm(races, label=username)
                username = input("For what username would you like to get the stats? ")

            plt.legend()
            plt.show()
        case "24":
            username = input("For what username would you like to get the stats? ")
            solo, multi = getRaces(username)
            races = np.concatenate([solo, multi])

            histAccDistributionApi(races, label=username)

            plt.legend()
            plt.show()

        case "25":
            username = input("For what username would you like to get the graph? ")

            while username != "q":
                solo, multi = getRaces(username)
                if solo is None:
                    solo = []
                if multi is None:
                    multi = []

                races = np.concatenate([solo, multi])
                races = list(sorted(races, key=lambda race: race["pp"], reverse=True))

                print(len(set(map(lambda race: race["quoteId"], races))))

                if races is not None:
                    print(type(races))
                    races = getRacePpPb(races)
                    print(type(races))

                    races = races[:250]
                    plotTop250Pp(races, label=username)

                username = input("For what username would you like to get the graph or q to show data: ")

            plt.legend()
            plt.show()

        case "26":
            username = input("For what username would you like to get the graph? ")
            solo, multi = getRaces(username)
            races = np.concatenate([solo, multi])
            races = {race["quoteId"]: race for race in races}
            quotes = np.concatenate([ranked_quotes, unranked_quotes])

            i = 1
            total = 0

            with open("Gauntlet.txt", "r") as f:
                for uri in f:
                    uri = uri.strip()
                    total += 1
                    quoteId = uri.split("/")[-1]

                    if quoteId in races.keys():
                        i += 1
                    else:
                        quote = None

                        for quote_el in quotes:
                            if quote_el["quoteId"] == quoteId:
                                quote = quote_el

                        if quote != None:
                            print(f'len:{len(quote["text"])}, diff:{quote["difficulty"]}, quote: {uri}')
                        else:
                            print(f"quote not found: {uri}")

            print(f"{i}/{total}={100*i/total:.2f}% done")

                    # status = r.get(f"http://api.typegg.io/v1/users/{username}/quotes/{quoteId}").status_code

                    # if status != 200:
                    #     print(uri)

        case "q":
            break
        case _:
            print("This command has not been found, if you would like to quit, press q ")

