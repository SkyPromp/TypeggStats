import matplotlib.pyplot as plt
import numpy as np
from DataTypes import Column


def histPpDistribution(data: Column):
    data = np.array(list(map(lambda col: col.pp, data)))
    # print(data)
    # bins = np.round((data / 10)) * 10
    bins = np.arange(min(data), max(data), 10)

    plt.hist(data, bins=bins)

    plt.title("PP distribution in top 250 races")
    plt.xlabel("PP (binsize = 10)")
    plt.ylabel("Amount of races")
    plt.show()


def histWPMDistribution(data: Column):
    data = np.array(list(map(lambda col: col.wpm, data)))
    binsize = 5
    # print(data)
    # bins = np.round((data / 10)) * 10
    bins = np.arange(min(data), max(data), binsize)

    plt.hist(data, bins=bins)

    plt.title("WPM distribution in top 250 races")
    plt.xlabel(f"Typing speed (in WPM, binsize = {binsize})")
    plt.ylabel("Amount of races")
    plt.show()


def histAccDistribution(data: Column):
    min_display_acc = 85
    data = np.array(list(map(lambda col: col.acc, data)))

    bins = np.floor(np.arange(np.floor(max(min(data), min_display_acc)) / 100, 1.011, 0.01) * 100)

    plt.hist(data, bins=bins)

    plt.title("Accuracy distribution in top 250 races")
    plt.xlabel("Accuracy (in %)")
    plt.ylabel("Amount of races")
    plt.show()


def flaneurQuotes(data1, data2):
    data1_int = sorted(getQuotesIntersection(data1, data2), key=lambda col: col.quote_id)
    data2_int = sorted(getQuotesIntersection(data2, data1), key=lambda col: col.quote_id)

    print("quote_id, wpm A, wpm B, pp A, pp B")

    data_combined = sorted(zip(data1_int, data2_int), key=lambda data_unit: abs(data_unit[0].pp - data_unit[1].pp), reverse=True)

    for data1_quote, data2_quote in data_combined:
        if data1_quote.wpm <= data2_quote.wpm:
            print(f"https://typegg.io/solo/{data1_quote.quote_id}, A: {data1_quote.wpm}wpm, B: {data2_quote.wpm}wpm, A: {data1_quote.pp}pp, {data2_quote.pp}pp")


def getQuotesIntersection(data1: Column, data2: Column):
    data2_quotes = list(map(lambda col: col.quote_id, data2))
    shared = [column for column in data1 if column.quote_id in data2_quotes]

    return shared


def _plotSpeedGraph(username: str, keystrokes):  # TODO BUGFIX dEnd and rEnd works for every word, not the full quote in reverse
    output = ""
    delays = np.array([], dtype="float")

    for keystroke in keystrokes:
        if "action" in keystroke:
            action = keystroke["action"]
        else:
            print("no action detected")
            print(keystroke)
            continue

        if "i" in action:
            index = action["i"]
            key = action["key"]
            # print(index, end="")
            # print(key, end="")
            output += key
            delays = np.append(delays, keystroke["time"])
        elif "dEnd" in action and "dStart" in action:  # delete characters
            print(output)
            print("#", action)
            print()
            print()
            start = len(output) - action["dStart"]
            end = len(output) - action["dEnd"]
            start, end = end, start

            output = output[:start] + output[end:]
            delays = np.append(delays[:start], delays[end:])
        elif "rEnd" in action and "rStart" in action and "key" in action:  # replace characters
            start = len(output) - action["rStart"]
            end = len(output) - action["rEnd"]
            start, end = end, start

            output = output[:start] + action["key"] + output[end:]
            delays = np.concatenate((delays[:start], np.array([keystroke["time"]]), delays[end:]))
        else:
            print("UNKNOWN ACTION: ", action, end="")

    x = np.array(range(1, len(delays) + 1))
    delays /= x
    delays = 12000 / delays

    plt.plot(x, delays, label=username)
    print(output, end="\n\n")

    plt.title("Typing speed")
    plt.xlabel("Characters")
    plt.ylabel("Typing Speed (in WPM)")
    plt.yticks()

    return delays


def plotSpeedGraph(*keystrokes):
    ymin = 999999999
    ymax = 0
    xmax = 0

    keystrokes = [keystrokes[-1]]

    for username, keystroke in keystrokes:
        delays = _plotSpeedGraph(username, keystroke)

        ypadding = 0.05
        _ymin = min(delays) * (1 - ypadding)
        _ymax = max(delays[int(len(delays) * 0.05):]) * (1 + ypadding)

        if _ymin < ymin:
            ymin = _ymin

        if _ymax > ymax:
            ymax = _ymax

        if len(delays) > xmax:
            xmax = len(delays)

    plt.ylim(ymin, ymax)
    plt.xlim(0, xmax)
    plt.legend()
    plt.show()

