import requests


def getRaces(user: str):
    perPage = 1000

    url_base = f"https://api.typegg.io/v1/users/{user}/races?perPage={perPage}"
    url = url_base
    data = requests.get(url).json()

    try:
        pages = data["totalPages"]
    except Exception:
        pages = 0
        print(url)
        print(data)
        print(dict(data))

    solo = []
    multi = []

    for page in range(1, pages + 1):
        url = f"{url_base}&page={page}"
        data = requests.get(url).json()
        try:
            for race in data["races"]:
                gamemode = race["gamemode"]

                if gamemode == "solo":
                    solo.append(race)
                elif gamemode == "multiplayer":
                    multi.append(race)
                else:
                    print(race)
                    print("---------")
        except KeyError:
            return None, None

    return solo, multi


def getTop250RacesByPP(user: str, perPage = 250):
    url_base = f"https://api.typegg.io/v1/users/{user}/races?sort=pp&perPage={perPage}"
    url = url_base
    data = requests.get(url).json()

    return data["races"]


def getQuotes():
    perPage = 1000

    url_base = f"https://api.typegg.io/v1/quotes?perPage={perPage}&status=any"
    url = url_base

    data = requests.get(url).json()
    # try:
    pages = data["totalPages"]

    ranked = []
    unranked = []

    for page in range(1, pages + 1):
        url = f"{url_base}&page={page}"
        data = requests.get(url).json()

        for quote in data["quotes"]:
            is_ranked = quote["ranked"]

            if is_ranked:
                ranked.append(quote)
            else:
                unranked.append(quote)

    return ranked, unranked

    # except Exception:
    #     print(url)
    #     # print(data)
    #     # print(dict(data))
    #
    # raise Exception
