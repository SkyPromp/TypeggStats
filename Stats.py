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


def _plotSpeedGraph(username: str, keystrokes):
    output = []
    delays = []

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

            if index == 0:
                output.append([])
                delays.append([])

            output[-1].append((index, key))
            delays[-1].append(keystroke["time"])
        elif "dEnd" in action and "dStart" in action:  # delete characters
            start = action["dStart"]
            end = action["dEnd"]

            output[-1] = output[-1][:start] + output[-1][end:]
            delays[-1] = delays[-1][:start] + delays[-1][end:]
        elif "rEnd" in action and "rStart" in action and "key" in action:  # replace characters
            start = action["rStart"]
            end = action["rEnd"]

            output[-1] = output[-1][:start] + [(start, action["key"])] + output[-1][end:]
            delays[-1] = delays[-1][:start] + [keystroke["time"]] + delays[-1][end:]
        else:
            print("UNKNOWN ACTION: ", action, end="")

    delays = [delay for _delays in delays for delay in _delays]
    x = np.array(range(1, len(delays) + 1))
    delays /= x
    delays = 12000 / delays

    plt.plot(x, delays, label=username)

    output = "".join([char[1] for word in output for char in word])

    return delays, output


def plotSpeedGraph(*keystrokes):
    ymin = 999999999
    ymax = 0
    xmax = 0
    quote = ""

    for username, keystroke in keystrokes:
        delays, quote = _plotSpeedGraph(username, keystroke)

        # ypadding = 0.05
        ypadding = 0.1
        _ymin = min(delays) * (1 - ypadding)
        _ymax = max(delays[int(len(delays) * ypadding):]) * (1 + ypadding)

        if _ymin < ymin:
            ymin = _ymin

        if _ymax > ymax:
            ymax = _ymax

        if len(delays) > xmax:
            xmax = len(delays)

    title = f"Typing speed: {quote}"
    max_title_length = 80
    plt.title(title if len(title) <= max_title_length else title[:max_title_length] + "...")
    plt.xlabel("Characters")
    plt.ylabel("Typing Speed (in WPM)")
    plt.yticks()
    plt.ylim(ymin, ymax)
    plt.xlim(0, xmax)
    plt.legend()
    plt.show()

