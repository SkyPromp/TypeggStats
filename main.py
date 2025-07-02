#! /bin/python3

import matplotlib as mpl
import pickle
from DataSources import getQuote, getQuoteKeystrokes, getUserProfileData
from Stats import getQuotesIntersection, histWPMDistribution, histAccDistribution, histPpDistribution, flaneurQuotes, plotSpeedGraph


mpl.use("Qt5Agg")

while True:
    statstype = input("""What statistics would you like to see?
    press 1 for: WPM distribution
    press 2 for: PP distribution
    press 3 for: Acc distribution
    press 4 for: What quotes you need to flaneur someone
    press 5 for: Keystroke data
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

            keystrokes_list = getQuoteKeystrokes(quote_id)
            plotSpeedGraph(*keystrokes_list)
        case "q":
            break
        case _:
            print("This command has not been found, if you would like to quit, press q")

