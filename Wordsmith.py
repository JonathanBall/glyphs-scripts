# MenuTitle: Wordsmith
# -*- coding: utf-8 -*-

__doc__ = """
Script to generate random strings from a provided set of glyphs.
"""

# import random
import vanilla
# import nltk
from enum import Enum
import requests

# class Dictionary(object):

#     def __init__(self):
#         nltk.download('words')

#         self.englishWords = set(nltk.corpus.words.words())

#     def isEnglish(self, word):
#         return word.lower() in self.englishWords


class Wordsmith(object):

    def __init__(self):
        self.padding = 20
        self.spacing = 10
        self.buttonSize = Size(100, 20)

        buttons = [
            vanilla.Button("auto", "Cancel", self.onCancel),
            vanilla.Button("auto", "Submit", self.onSubmit)
        ]
        self.setPosSizes(
            buttons, (self.padding, self.padding), self.buttonSize, self.spacing
        )

        count = len(buttons)
        
        width = self.padding * 2
        width += self.buttonSize.width * count
        width += (self.spacing * (count-1))

        height = self.padding * 2
        height += self.buttonSize.height

        self.window = vanilla.FloatingWindow((width, height), "Wordsmith")
        self.window.bind("resize", self.onWindowResized)
        self.window.center()
        self.window.open()
        self.window.makeKey()
        
        for button in buttons:
            setattr(self.window, button.getTitle(), button)
        
        if len(buttons) > 0:
            defaultButton = buttons[0].getTitle()
            self.window.setDefaultButton(getattr(self.window, defaultButton))

    def setPosSizes(self, elements, position, size, spacing):
        offsetX = position[0]

        for element in elements:
            element.setPosSize((offsetX, position[1], size.width, size.height))
            offsetX += size.width + spacing

    def onWindowResized(self, sender):
        print("onWindowResized")

    def onCancel(self, sender):
        self.window.close()

    def onSubmit(self, sender):
        print("onSubmit")

    def getLayerNames(self, font):
        layerNames = []
        for glyph in font.glyphs:
            for layer in glyph.layers:
                layerNames.append(layer.name)
        return list(dict.fromkeys(layerNames))


class UINode(object):

    def __init__(
        self, 
        parent,
        vanilla,
        position,
        size,
        padding,
        axis,
        spacing=0
    ):
        self.parent = parent
        self.vanilla = vanilla
        self.position = position
        self.size = size
        self.padding = padding
        self.axis = axis
        self.spacing = spacing
        self.children = None

    def open(self):
        pass

    def close(self):
        self.size.width += self.padding.left + self.padding.right
        self.size.height += self.padding.top + self.padding.bottom
        
        parent = self.parent
        spacing = (len(parent.children)-1) * parent.spacing
        
        if self.axis == Axis.HORIZONTAL:
            self.size.width += spacing
            parent.size.width += self.size.width
            parent.size.height = max(self.size.height, parent.size.height)
        elif self.axis == Axis.VERTICAL:
            self.size.height += spacing
            parent.size.width = max(self.size.width, parent.size.width)
            parent.size.height += self.size.height


class Padding(object):

    def __init__(self, left, right, top, bottom):
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom


class Axis(Enum):
    HORIZONTAL = 0
    VERTICAL = 1


class Position(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y


class Size(object):

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.size = (width, height)

x = requests.get('https://w3schools.com')
print(x.status_code)

# dictionary = Dictionary()
# word = "butt"
# isEnglish = dictionary.isEnglish(word)
# result = f"'{word}' is a word: {isEnglish}"
# print(result)

# Run
Wordsmith()
