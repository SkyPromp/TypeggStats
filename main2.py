#! /bin/python3

from DataApi import getQuotes, getRaces, getTop250RacesByPP
from StatsApi import findSatisfyingScores, histRecoveryTimeDistributionApi, histWPMDistributionApi, plotDifficultyByLength, plotPpByDifficulty, plotPpByLength, plotPpPerWpm, plotRacetime, plotTop250Pp, plotTotalPp, plotWpmByDifficulty, plotWpmByLength, quoteLikesPerUser, quotesPerUser
import matplotlib as mpl
import pickle
import numpy as np

import matplotlib.pyplot as plt

mpl.use("Qt5Agg")

ranked_quotes, unranked_quotes = getQuotes()

while True:
    command, *settings = input("""What statistics would you like to see?
    atg: for all time overviews (time, pp) . many
    dis: for all distributions (wpm, recovery, reaction) (solo, multi, both) . one
    quo: for quote statistics (submission, likes) . none
    sat: for satisfying races
    cov: for a pp coverage graph
    old: get races from old to new . one
    dbl: get difficulty by quote length
    rbs: get races by stats (wpm, pp) (length, difficulty) - many
    dia: get pp by typing speed
    """)

    # command [options] user1 user2 user3

    match command:
        case "atg":
            if "." in settings:
                i = settings.index(".")

                for name_i in range(i + 1, len(settings))

        case "dis":
        case "quo":
        case "sat":
        case "cov":
        case "old":
        case "dbl":
        case "rbs":
        case "dia":


    match statstype:
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

            plotWpmByLength(np.concatenate([solo, multi]), ranked_quotes, label=username)

            plt.legend()
            plt.show()

        case "19":
            username = input("For what username would you like to get the stats? ")
            solo, multi = getRaces(username)

            plotPpByLength(np.concatenate([solo, multi]), ranked_quotes, label=username)

            plt.legend()
            plt.show()

        case "20":
            plotDifficultyByLength(ranked_quotes)

            plt.show()

        case "21":
            username = input("For what username would you like to get the stats? ")
            solo, multi = getRaces(username)

            plotWpmByDifficulty(np.concatenate([solo, multi]), ranked_quotes, label=username)

            plt.legend()
            plt.show()

        case "22":
            username = input("For what username would you like to get the stats? ")
            solo, multi = getRaces(username)

            plotPpByDifficulty(np.concatenate([solo, multi]), ranked_quotes, label=username)

            plt.legend()
            plt.show()
        case "23":
            username = input("For what username would you like to get the stats? ")
            solo, multi = getRaces(username)

            plotPpPerWpm(np.concatenate([solo, multi]), label=username)

            plt.legend()
            plt.show()
        case "q":
            break
        case _:
            print("This command has not been found, if you would like to quit, press q ")


