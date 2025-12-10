import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib import cm
from typing import Dict, List
import matplotlib.colors as mcolors
from collections import Counter


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
    keymaps = {
        "qwerty": [[K("~`"), K("1!"), K("2@"), K("3#"), K("4$"), K("5%"), K("6^"), K("7&"), K("8*"), K("9("), K("0)"), K("-_"), K("=+"), K("", text="Backspace", width=2, fontsize=10)],
              [K("", width=1.5, text="Tab"), K("qQ"), K("wW"), K("eE"), K("rR"), K("tT"), K("yY"), K("uU"), K("iI"), K("oO"), K("pP"), K("[{"), K("]}"), K("\\|", width=1.5)],
              [K("", width=1.75, text="Caps Lock", fontsize=10), K("aA"), K("sS"), K("dD"), K("fF"), K("gG"), K("hH"), K("jJ"), K("kK"), K("lL"), K(";:"), K("'\""), K("\n", width=2.25 ,text="Enter")],
              [K("", width=2, text="Shift"), K("zZ"), K("xX"), K("cC"), K("vV"), K("bB"), K("nN"), K("mM"), K(",<"), K(".>"), K("/?"), K("", width=3, text="Shift")],
              [K("", width=1.25, text="Ctrl"), K("", width=1.25, text="Super"), K("", width=1.25, text="Alt"), K(" ", width=6.25, text="Space"), K("", width=1.25, text="Alt"), K("", width=1.25, text="Super"), K("", width=1.25, text="Menu"), K("", width=1.25, text="Ctrl")]],

        "dvorak": [[K("~`"), K("1!"), K("2@"), K("3#"), K("4$"), K("5%"), K("6^"), K("7&"), K("8*"), K("9("), K("0)"), K("[{"), K("]}"), K("", text="Backspace", width=2, fontsize=10)],
              [K("", width=1.5, text="Tab"), K("'\""), K(",<"), K(".>"), K("pP"), K("yY"), K("fF"), K("gG"), K("cC"), K("rR"), K("lL"), K("?/"), K("=+"), K("\\|", width=1.5)],
              [K("", width=1.75, text="Caps Lock", fontsize=10), K("aA"), K("oO"), K("eE"), K("uU"), K("iI"), K("dD"), K("hH"), K("tT"), K("nN"), K("sS"), K("-_"), K("\n", width=2.25 ,text="Enter")],
              [K("", width=2, text="Shift"), K(";:"), K("qQ"), K("jJ"), K("kK"), K("xX"), K("bB"), K("mM"), K("wW"), K("vV"), K("zZ"), K("", width=3, text="Shift")],
              [K("", width=1.25, text="Ctrl"), K("", width=1.25, text="Super"), K("", width=1.25, text="Alt"), K(" ", width=6.25, text="Space"), K("", width=1.25, text="Alt"), K("", width=1.25, text="Super"), K("", width=1.25, text="Menu"), K("", width=1.25, text="Ctrl")]]
     }

    if keymap in keymaps:
        return keymaps[keymap]

    return keymaps["qwerty"]


def drawHeatmap(keypresses: Dict[str, int], keymap: List[List[K]]):
    cmap = cm.get_cmap("managua")

    max_presses = 0
    rectangles = []
    shift_presses = 0
    alt_presses = 0

    for row_i, row in enumerate(keymap):
        total_width = 0

        for key in row:
            total_presses = 0

            for i, character in enumerate(key.matches):
                if character not in keypresses:
                    continue

                presses = keypresses[character]
                total_presses += presses

                if i == 1:
                    shift_presses += presses

                if i == 2:
                    alt_presses += presses

            if total_presses > max_presses:
                max_presses = total_presses

            square = patches.Rectangle((total_width, -row_i), key.width, 1, edgecolor="black")
            ax.text(total_width + key.width / 2, 0.5 - row_i, key.text, ha="center", va="center", fontsize=key.fontsize)

            if key.text == "Shift":
                total_presses = -1

            if key.text == "Alt":
                total_presses = -2

            rectangles.append((square, total_presses))
            total_width += key.width

    for rectangle, presses in rectangles:
        if presses == -1:
            presses = shift_presses
        elif presses == -2:
            presses = alt_presses

        rectangle.set_facecolor(cmap(presses/max_presses))
        ax.add_patch(rectangle)

    plt.xlim(-0.1, 15.1)
    plt.ylim(-4.1, 1.1)
    plt.axis('off')
    plt.gca().set_aspect("equal", adjustable="box")

    # Cmap legend
    sm = cm.ScalarMappable(cmap=cmap, norm=mcolors.Normalize(vmin=0, vmax=max_presses))
    sm.set_array([])
    cbar_ax = fig.add_axes([0.91, 0.3715, 0.02, 0.245])
    cbar = plt.colorbar(sm, cax=cbar_ax)
    cbar.set_label('Key Presses')

    plt.show()


def textToKeypresses(text: str, amount=1) -> Dict[str, int]:
    frequencies = {}

    for char in text:
        if char in frequencies:
            frequencies[char] += amount

        else:
            frequencies[char] = amount

    return frequencies


def textToKeypresses2(text: str, amount=1) -> Dict[str, int]:
    if amount == 1:
        return dict(Counter(text))

    return {key: value * amount for key, value in dict(Counter(text)).items()}


keypresses = textToKeypresses2("You may not yet be at a point where you have fully recovered your power or all of your memories... But courage need not be remembered... For it is never forgotten. That energy covering Ganon's body is called Malice. None of your attacks will get through as he now is... I will hold the Malice back as much as I can, but my power is waning. Attack any glowing points that you see! May you be victorious!")

drawHeatmap(keypresses=keypresses, keymap=getKeymap("dvorak"))
