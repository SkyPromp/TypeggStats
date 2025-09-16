import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd


def getRacePpPb(data):
    pbs = {}

    for race in data:
        quoteId = race["quoteId"]
        
        if quoteId in pbs:
            if pbs[quoteId]["pp"] < race["pp"]:
                pbs[quoteId] = race
        else:
            pbs[quoteId] = race

    return list(pbs.values())


def histPpDistributionApi(data):
    data = np.array(list(map(lambda col: col["pp"], data)))
    # print(data)
    # bins = np.round((data / 10)) * 10
    bins = np.arange(min(data), max(data), 10)

    plt.hist(data, bins=bins)

    plt.title("PP distribution in top 250 races")
    plt.xlabel("PP (binsize = 10)")
    plt.ylabel("Amount of races")
    plt.show()


def histWPMDistributionApi(data, alpha = 1, label = None):
    data = [row for row in data if row["wpm"] < 600]
    data = np.array(list(map(lambda col: col["wpm"], data)))
    binsize = 5
    bins = np.arange(min(data), max(data), binsize)

    if label is not None:
        plt.hist(data, bins=bins, alpha=alpha, label=label)
    else:
        plt.hist(data, bins=bins, alpha=alpha)

    plt.title("WPM distribution")
    plt.xlabel(f"Typing speed (in WPM, binsize = {binsize})")
    plt.ylabel("Amount of races")


def histRecoveryTimeDistributionApi(data, alpha = 1, label = None, exclude_zero = False):
    if exclude_zero:
        data = [row for row in data if row["errorRecoveryTime"] != 0]
        [print(row) for row in data if row["errorRecoveryTime"] > 6000]

    data = np.array(list(map(lambda col: col["errorRecoveryTime"], data)))
    binsize = 10
    bins = np.arange(min(data), max(data), binsize)

    if label is not None:
        plt.hist(data, bins=bins, alpha=alpha, label=label)
    else:
        plt.hist(data, bins=bins, alpha=alpha)

    plt.title("Error recovery time")
    plt.xlabel(f"Error recovery time (in ms, binsize = {binsize})")
    plt.ylabel("Amount of races")


def histReactionTimeDistributionApi(data, alpha = 1, label = None, exclude_zero = False):
    if exclude_zero:
        data = [row for row in data if row["errorReactionTime"] != 0]
        [print(row) for row in data if row["errorReactionTime"] > 6000]

    data = np.array(list(map(lambda col: col["errorRecoveryTime"], data)))
    binsize = 10
    bins = np.arange(min(data), max(data), binsize)

    if label is not None:
        plt.hist(data, bins=bins, alpha=alpha, label=label)
    else:
        plt.hist(data, bins=bins, alpha=alpha)

    plt.title("Error recovery time")
    plt.xlabel(f"Error recovery time (in ms, binsize = {binsize})")
    plt.ylabel("Amount of races")


def histAccDistributionApi(data, label=None):
    min_display_acc = 0.85
    data = np.array(list(map(lambda col: col["accuracy"], data)))
    print(data)

    bins = np.floor(np.arange(np.floor(max(min(data), min_display_acc) * 100) / 100, 1.011, 0.01) * 100)
    data *= 100

    plt.hist(data, bins=bins, label=label)

    plt.title("Accuracy distribution")
    plt.xlabel("Accuracy (in %)")
    plt.ylabel("Amount of races")


def plotTop250Pp(data, label=None):
    data = list(map(lambda el: el["pp"], data))

    if label is not None:
        plt.plot(data, label=label)
    else:
        plt.plot(data)
    
    plt.title("Top 250 pp scores")
    plt.xlabel("Quote Ranking")
    plt.ylabel("Pp")


def plotRacetime(data, label=None):
    data = list(sorted(list(map(lambda race: (race["duration"], race["timestamp"]), data)),key=lambda race: race[1]))

    duration = [item[0] / 1000 /3600 for item in data]
    duration = np.cumsum(duration)
    starttime = [item[1] for item in data]

    starttime = pd.to_datetime(starttime, utc=True)

    plt.plot(starttime, duration, label=label)

    ax = plt.gca()
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m %Y'))

    plt.xticks(rotation=90)
    plt.title("Total typing time")
    plt.xlabel("date")
    plt.ylabel("Time typing (in hours)")


def plotTotalPp(data, label=None):
    data = list(sorted(list(map(lambda race: (race["pp"], race["quoteId"], race["timestamp"]), data)),key=lambda race: race[2]))

    quote_id = [item[1] for item in data]

    starttime = [item[2] for item in data]
    starttime = pd.to_datetime(starttime, utc=True)

    pp_data = [item[0] for item in data]
    x = []
    y = []
    pp_dict = {}

    def calculateTotalPp(values: dict):
        values = np.array(sorted(values.values(), reverse=True))
        multiply = np.array([0.97 ** i for i in range(0, len(values))])
        total_pp = (values * multiply)
        total_pp[total_pp < 1] = 0

        return sum(total_pp)

    for p, id, timestamp in zip(pp_data, quote_id, starttime):
        if id in pp_dict:
            if p > pp_dict[id]:
                pp_dict[id] = p

                x.append(timestamp)
                y.append(calculateTotalPp(pp_dict))
        else:
            pp_dict[id] = p
            new_pp = calculateTotalPp(pp_dict)

            if len(y) == 0 or new_pp >= y[-1]:
                x.append(timestamp)
                y.append(new_pp)

    plt.plot(x, y, label=label)

    ax = plt.gca()
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m %Y'))

    plt.xticks(rotation=90)
    plt.title("Total pp progression")
    plt.xlabel("date")
    plt.ylabel("Pp")


def findSatisfyingScores(data):
    for race in data:
        duration_formatted = str(round(race["duration"]))
        duration_formatted = duration_formatted[:-3] + "." + duration_formatted[-3:]

        if ".000" in duration_formatted:
            print(race)
            print()

    print()
    print()
    print()


def quotesPerUser(data, alpha = 1, label = None):
    frequency = dict()

    for quote in data:
        user = quote["submittedByUsername"]

        if user in frequency:
            frequency[user] += 1
        else:
            frequency[user] = 1

    data = sorted(list(frequency.items()), key=lambda value: value[1], reverse=True)

    names = [item[0] for item in data]
    values = [item[1] for item in data]

    if label is not None:
        plt.bar(names, values, alpha=alpha, label=label)
    else:
        plt.bar(names, values, alpha=alpha)

    plt.xticks(rotation=90)
    plt.title("Quotes submitted per user")
    plt.ylabel("Quotes amount")


def quoteLikesPerUser(data, alpha = 1, label = None):
    # frequency = dict()
    # total_likes = dict()
    source = dict()

    for quote in data:
        user = quote["submittedByUsername"]
        likes = quote["likes"]

        if user in source:
            source[user][0] += 1
            source[user][1] += likes

            # total_likes[user] += likes
            # frequency[user] += 1
        else:
            source[user] = [1, likes]

            # total_likes[user] = likes
            # frequency[user] = 1

    # data = [{el[]} for el in zip(frequency, total_likes)]
    print(source.items())
    data = sorted(list(map(lambda el: (el[0], el[1][1]/el[1][0]), source.items())), key=lambda el: el[1], reverse=True)
    print(data)

    # data = sorted(list(frequency.items()), key=lambda value: value[1], reverse=True)

    names = [item[0] for item in data]
    values = [item[1] for item in data]

    if label is not None:
        plt.bar(names, values, alpha=alpha, label=label)
    else:
        plt.bar(names, values, alpha=alpha)

    # if label is not None:
    #     plt.bar(frequency.keys(), frequency.values(), alpha=alpha,label=label)
    # else:
    #     plt.bar(frequency.keys(), frequency.values(), alpha=alpha)

    plt.xticks(rotation=90)
    plt.title("Average likes per quote")
    plt.ylabel("Average likes per quote")


def plotWpmByLength(races, quotes_data, label=None):
    quotes = {quote["quoteId"]: quote["text"] for quote in quotes_data}
    data = [(race["wpm"], len(quotes[race["quoteId"]])) for race in races if race["quoteId"] in quotes]
    wpm = [el[0] for el in data]
    length = [el[1] for el in data]

    plt.scatter(length, wpm, label=label)

    plt.title("Typing speed per quote length")
    plt.xlabel("quote length")
    plt.ylabel("Typing speed (in WPM)")


def plotPpByLength(races, quotes_data, label=None):
    quotes = {quote["quoteId"]: quote["text"] for quote in quotes_data}
    data = [(race["pp"], len(quotes[race["quoteId"]])) for race in races if race["quoteId"] in quotes]
    wpm = [el[0] for el in data]
    length = [el[1] for el in data]

    plt.scatter(length, wpm, label=label)

    plt.title("PP per quote length")
    plt.xlabel("quote length")
    plt.ylabel("PP")


def plotWpmByDifficulty(races, quotes_data, label=None):
    quotes = {quote["quoteId"]: quote["difficulty"] for quote in quotes_data}
    data = [(race["wpm"], quotes[race["quoteId"]]) for race in races if race["quoteId"] in quotes]
    wpm = [el[0] for el in data]
    length = [el[1] for el in data]

    plt.scatter(length, wpm, label=label)

    plt.title("Typing speed per quote difficulty")
    plt.xlabel("Quote difficulty")
    plt.ylabel("Typing speed (in WPM)")


def plotPpByDifficulty(races, quotes_data, label=None):
    quotes = {quote["quoteId"]: quote["difficulty"] for quote in quotes_data}
    data = [(race["pp"], quotes[race["quoteId"]]) for race in races if race["quoteId"] in quotes]
    wpm = [el[0] for el in data]
    length = [el[1] for el in data]

    plt.scatter(length, wpm, label=label)

    plt.title("PP per quote difficulty")
    plt.xlabel("Quote difficulty")
    plt.ylabel("PP")


def plotPpPerWpm(races, label=None):
    for race in races:
        if race["pp"] < 30 and race["pp"] > 1:
            print(race)
    races = [race for race in races if race["pp"] > 0]

    wpm = list(map(lambda el: el["wpm"], races))
    pp = list(map(lambda el: el["pp"], races))

    plt.scatter(wpm, pp, label=label)

    plt.title("PP per typing speed")
    plt.xlabel("Typing speed (in WPM)")
    plt.ylabel("PP")


def plotDifficultyByLength(quotes_data):
    quotes = [(len(quote["text"]), quote["difficulty"]) for quote in quotes_data]

    length = [el[0] for el in quotes]
    difficulty = [el[1] for el in quotes]

    plt.scatter(length, difficulty, s=4)

    plt.title("Quote difficulty by quote length")
    plt.xlabel("Quote length")
    plt.ylabel("Difficulty")


# def averageQuoteDifficultyProgression(races, quotes_data):
#     quotes = {quote["quoteId"]: quote["difficulty"] for quote in quotes_data}
#     data = [(race["wpm"], len(quotes[race["difficulty"]])) for race in races]
#     
#     pass



