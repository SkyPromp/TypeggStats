import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib import cm
from typing import Dict, List


class K:
    def __init__(self, matches, width=1, text=None, fontsize=12):
        self.width = width
        self.matches = matches
        self.fontsize = fontsize

        if text is None:
            self.text = matches
        else:
            self.text = text


fig, ax = plt.subplots()


def getKeymap(keymap: str) -> List[List[K]]:
    keymaps = {"qwerty": [[K("~`"), K("1!"), K("2@"), K("3#"), K("4$"), K("5%"), K("6^"), K("7&"), K("8*"), K("9("), K("0)"), K("-_"), K("=+"), K("", text="Backspace", width=2, fontsize=10)],
              [K("", width=1.5, text="Tab"), K("qQ"), K("wW"), K("eE"), K("rR"), K("tT"), K("yY"), K("uU"), K("iI"), K("oO"), K("pP"), K("[{"), K("]}"), K("\\|", width=1.5)],
              [K("", width=1.75, text="Caps Lock", fontsize=10), K("aA"), K("sS"), K("dD"), K("fF"), K("gG"), K("hH"), K("jJ"), K("kK"), K("lL"), K(";:"), K("'\""), K("\n", width=2.25 ,text="Enter")],
              [K("", width=2, text="Shift"), K("zZ"), K("xX"), K("cC"), K("vV"), K("bB"), K("nN"), K("mM"), K(",<"), K(".>"), K("/?"), K("", width=3, text="Shift")],
              [K("", width=1.25, text="Ctrl"), K("", width=1.25, text="Super"), K("", width=1.25, text="Alt"), K(" ", width=6.25, text="Space"), K("", width=1.25, text="Alt"), K("", width=1.25, text="Super"), K("", width=1.25, text="?"), K("", width=1.25, text="Ctrl")]]
     }

    if keymap in keymaps:
        return keymaps[keymap]

    return keymaps["qwerty"]


def getMaxPresses(keypresses: Dict[str, int], keymap: List[List[K]]) -> int:
    max_presses = 0

    max_presses = 10  # TODO remove

    if max_presses == 0:
        max_presses = 1

    return max_presses


def drawHeatmap(keypresses: Dict[str, int], keymap: List[List[K]]):
    cmap = cm.get_cmap("managua")

    max_presses = getMaxPresses(keypresses=keypresses, keymap=keymap)

    for row_i, row in enumerate(keymap):
        total_width = 0

        for key in row:
            total_presses = 0

            for character in key.matches:
                if character in keypresses:
                    total_presses += keypresses[character]

            total_presses = total_presses / max_presses

            square = patches.Rectangle((total_width, -row_i), key.width, 1, edgecolor="black", facecolor=cmap(total_presses))
            ax.add_patch(square)
            ax.text(total_width + key.width / 2, 0.5 - row_i, key.text, ha="center", va="center", fontsize=key.fontsize)
            total_width += key.width

    plt.xlim(-0.5, 16)
    plt.ylim(-5, 2)
    plt.gca().set_aspect("equal", adjustable="box")
    plt.show()


def textToKeypresses(text: str) -> Dict[str, int]:
    frequencies = {}

    for char in text:
        if char in frequencies:
            frequencies[char] += 1

        else:
            frequencies[char] = 1

    return frequencies


keypresses = textToKeypresses("Hello, how is it going with you Eiko?")

drawHeatmap(keypresses=keypresses, keymap=getKeymap("qwerty"))
