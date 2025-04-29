# MenuTitle: Wordsmith
# -*- coding: utf-8 -*-

__doc__ = """
Script to generate random strings from a provided set of glyphs.
"""

import random
import vanilla


class Wordsmith(object):

    def __init__(self):
        self.windowWidth = 500
        self.windowHeight = 500
        self.padding = 6
        self.results_b_offset = 220
        marginHorizontal = 18
        marginVertical = 22
        line_pos = 12
        line_h = 30
        col_1_left = marginHorizontal
        col_2_left = 60
        text_h = 20
        label_w = col_2_left
        label_h = text_h
        labelSizeStyle = "small"
        footnote_h = label_h
        button_w = 150
        button_h = text_h
        button_txt = "Sync"
        button_x1 = (self.windowWidth/2)-(button_w/2)
        button_y1 = (-marginVertical-button_h)
        results_txt_def = u"🟢  Ready to sync..."
        self.results_w = self.windowWidth-(marginHorizontal*2)
        self.results_h = self.windowHeight-self.results_b_offset
        rule_height = 1

        # Create UI Element: Window
        windowSize = (self.windowWidth, self.windowHeight)
        self.w = vanilla.FloatingWindow(
            windowSize, 
            "Sync Horizontal Metrics", 
            minSize=windowSize, 
            maxSize=windowSize
        )
        self.w.bind("resize", self.onWindowResized)
        self.w.center()
        self.w.open()
        self.w.makeKey()

        # Create UI Element: Label
        self.w.label = vanilla.TextBox(
            (col_1_left, (marginVertical+line_pos), label_w, label_h), 
            "Label", 
            sizeStyle=labelSizeStyle
        )

        line_pos += line_h

        # Create UI Element: Horizontal Rule
        self.w.rule_divider = vanilla.HorizontalLine(
            (
                marginHorizontal, 
                (marginVertical+line_pos), 
                -marginHorizontal, 
                rule_height
            )
        )

        line_pos += (line_h+rule_height)

        # Create UI Element: Box
        self.w.results_box = vanilla.Box(
            (col_1_left, (marginVertical+line_pos), self.results_w, self.results_h)
        )
        self.w.results_box.text = vanilla.TextBox(
            (
                self.padding, 
                self.padding, 
                (self.results_w-(self.padding*2)), 
                (self.results_h-(self.padding*2))
            ), 
            results_txt_def, 
            selectable=True, 
            sizeStyle=labelSizeStyle
        )

        # Create UI Element: Center TextBox
        self.w.footnote = vanilla.TextBox(
            (0, (button_y1-button_h-label_h), self.windowWidth, footnote_h), 
            "Footnote", 
            alignment="center", 
            sizeStyle=labelSizeStyle
        )

        # Create UI Element: Button
        self.w.button = vanilla.Button(
            (button_x1, button_y1, button_w, button_h), 
            button_txt, 
            callback=self.onButtonPressed
        )
        self.w.setDefaultButton(self.w.button)

    def onWindowResized(self, sender):
        win_pos = self.w.getPosSize()
        # Get new window height
        win_h = win_pos[3]
        # Set results box & text dimensions
        self.w.results_box.resize(self.results_w, win_h-self.results_b_offset)
        self.w.results_box.text.resize(
            (self.results_w-(self.padding*2)), 
            win_h-self.results_b_offset
        )

    def onButtonPressed(self, sender):
        print("Button Callback")

    def getLayerNames(self, font_obj):
        layer_names = []
        for glyph in font_obj.glyphs:
            for layer in glyph.layers:
                layer_names.append(layer.name)
        layer_names = list(dict.fromkeys(layer_names))
        # Return layer names list
        return layer_names


class Size(object):

    def __init__(self, width, height):
        self.width = width
        self.height = height


class Position(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y


class ButtonData(object):

    def __init__(self, title, position, size):
        self.title = title
        self.position = position
        self.size = size


# Run
Wordsmith()
