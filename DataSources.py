from bs4 import BeautifulSoup
import requests
from DataTypes import Column
import urllib.parse


def getUserProfileData(username: str) -> list:
    link = f"https://typegg.io/user/{username}"

    html = requests.get(link).text
    data = BeautifulSoup(html, 'lxml')

    data = data.find(id="leaderboard-table")
    rows = data.find_all("tr")

    columns = []

    for row in rows:
        column = Column(list(map(lambda c: c.text if not c.find("a") else c.find("a")["href"], row.find_all("td"))))

        if column.succeeded:
            columns.append(column)
        else:
            print(f"broken column: {row}")

    return columns


def getQuote(quote_id: str):
    link = f"https://api.typegg.io/api/collections/quotes/records?filter=(id=%27{quote_id}%27)"

    data = requests.get(link).json()

    return data["items"][0]["text"]


def getQuoteKeystrokes(quote_id: str):
    quote_id = quote_id.replace(":", "%3A")
    quote_id = quote_id.replace("<", "%3C")
    quote_id = quote_id.replace("\\", "%5C")
    quote_id = quote_id.replace(">", "%3E")
    quote_id = quote_id.replace("\"", "%5C%22")
    quote_id = quote_id.replace("|", "%7C")

    link = f"https://api.typegg.io/api/collections/top_replays/records?page=1&perPage=10&filter=quote.id%20%3D%20%22{quote_id}%22&expand=user&sort=-wpm"
    print("url: ", link)

    data = requests.get(link).json()

    data = data["items"]

    keystroke_list = []

    for userdata in data:
        username = userdata["expand"]["user"]["username"]
        keystrokes = userdata["keystroke_data"]["keystrokes"]
        keystroke_list.append((username, keystrokes))

    return keystroke_list


def getQuoteUserKeystrokes(quote_id: str, username: str):
    link = f"https://typegg.io/solo/thorsbc_2466/vs/{username}/__data.json"

    data = requests.get(link).json()
    print(data)
    data = data["nodes"]
    data = data[2]["data"]
    # for i, val in enumerate(data):
    #     print(i, val)
    #     print("--------------------")
    # print(data)
    # print(data.keys())



    # data = data["items"]
    #
    # keystroke_list = []
    #
    # keystrokes = userdata["keystroke_data"]["keystrokes"]
    # keystroke_list.append((username, keystrokes))
    #
    # return keystroke_list
