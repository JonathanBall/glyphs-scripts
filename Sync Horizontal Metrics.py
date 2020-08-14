#MenuTitle: Sync Horizontal Metrics
# -*- coding: utf-8 -*-
__doc__="""
Syncs the horizontal metrics (keys, side bearings, and kerning groups) for all glyphs/layers of two open files. Exactly two files must be open and contain an equal number of glyphs/layers.
"""

import vanilla
# import AppKit

class SyncHorizontalMetrics(object):

	def __init__(self):

		self.is_syncable 			= True
		self.font_src				= None
		self.font_tar				= None
		self.font_src_glyphs_count	= 0
		self.font_tar_glyphs_count	= 0
		self.font_src_layers_count	= 0
		self.font_tar_layers_count	= 0
		self.font_src_layer_names	= []
		self.font_tar_layer_names	= []
		self.font_src_kerning		= {}

		# If at least one font file is open
		if len(Glyphs.fonts) > 0:
			# Get front window font object
			self.font_src = Glyphs.fonts[0]
			# Get the number of glyphs & layers in font
			self.font_src_glyphs_count = len(self.font_src.glyphs)
			self.font_src_layers_count = self.getLayerSumAllGlyphs(self.font_src)
			self.font_src_layer_names  = self.getLayerNames(self.font_src)
			# If more than one font file open
			if len(Glyphs.fonts) > 1:
				# Get back window font object
				self.font_tar = Glyphs.fonts[1]
				# Get the number of glyphs & layers in font
				self.font_tar_glyphs_count = len(self.font_tar.glyphs)
				self.font_tar_layers_count = self.getLayerSumAllGlyphs(self.font_tar)
				self.font_tar_layer_names  = self.getLayerNames(self.font_tar)
			else:
				# Not syncable
				self.is_syncable = False
		else:
			# Not syncable
			self.is_syncable = False

		if ( # If glyph & layer counts are not equal
			self.font_tar_glyphs_count != self.font_src_glyphs_count
			or self.font_tar_layers_count != self.font_src_layers_count
		):
			# Not syncable
			self.is_syncable = False

		# Init Remaining Variables
		self.update_log 			= []		# List to log updates made
		self.str_lmk				= "LMK"		# String for left metric key
		self.str_rmk				= "RMK"		# String for right metric key
		self.str_lsb				= "LSB"		# String for left side bearing
		self.str_rsb				= "RSB"		# String for right side bearing
		self.str_lkg				= "LKG"		# String for left kerning group
		self.str_rkg				= "RKG"		# String for right kerning group
		self.str_sync_success		= "Horizontal metrics synced!"
		# self.str_legend		= "LSB = Left Side Bearing | RSB = Right Side Bearing | LMK = Left Metrics Key | RMK = Right Metrics Key"
		self.str_macro_panel		= "View complete results in Macro Panel"
		self.str_synced				= "Horizontal metrics in sync. No changes..."
		self.str_open				= u"⚠️ NO FILE OPEN"
		self.str_error_no_file		= (u"❌ ERROR: Nothing to sync! \n\n"
										"1. Close this window \n"
										"2. Open two compatible files "
										"(with equal glyph & layer counts) \n"
										"3. Run script")
		self.str_error_glyph_count	= (u"❌ ERROR: Glyph counts not equal! \n\n"
										"Files must contain the same number of glyphs. "
										"Please close and try again.")
		self.str_error_layer_count	= (u"❌ ERROR: Layer counts not equal! \n\n"
										"Glyphs must contain the same number of layers. "
										"Please close and try again.")
		self.window_w	= 500
		self.window_h	= 500
		self.padding	= 6
		self.results_b_offset = 220
		margin_hor	= 18
		margin_ver	= 22
		line_pos	= 12
		line_h		= 30
		col_1_left	= margin_hor
		col_2_left	= 60
		text_w		= (self.window_w-col_2_left-margin_hor)
		text_h		= 20
		text_y_adj	= -3;
		text_size	= "regular"
		label_w		= col_2_left
		label_h		= text_h
		label_size	= "small"
		footnote_h		= label_h
		footnote_size	= label_size
		button_h 		= text_h
		button_sync_txt	= "Sync"
		button_sync_w	= 150
		button_sync_x1	= (self.window_w/2)-(button_sync_w/2)
		button_sync_y1	= (-margin_ver-button_h)
		button_swap_txt	= "Swap"
		button_swap_w	= 50
		button_swap_x1	= (-margin_hor-button_swap_w)
		button_swap_y1	= ( margin_ver+(line_pos*2) )
		results_txt_def	= u"🟢  Ready to sync..."
		self.results_w	= self.window_w-(margin_hor*2)
		self.results_h	= self.window_h-self.results_b_offset
		rule_height	= 1
		rule_pointer_w = 18
		rule_pointer_x1 = self.window_w-margin_hor-button_swap_w-self.padding-rule_pointer_w
		rule_pointer_y1 = (button_swap_y1+(button_h/2))
		rule_vert_h		= 34

		# Create UI Element: Window
		self.w = vanilla.FloatingWindow((self.window_w, self.window_h), "Sync Horizontal Metrics", minSize=(self.window_w, self.window_h), maxSize=(self.window_w, self.window_h*5))
		self.w.bind("resize", self.windowResizedCallback)
		self.w.center()
		self.w.open()
		self.w.makeKey()

		# Create UI Element: Font source name
		self.w.label_font_src = vanilla.TextBox((col_1_left, (margin_ver+line_pos), label_w, label_h), "From:", sizeStyle=label_size)
		self.w.filename_font_src = vanilla.TextBox((col_2_left, (margin_ver+line_pos+text_y_adj), text_w, text_h), self.getFilename(self.font_src), sizeStyle=text_size)
		line_pos += line_h
		# Create UI Element: Font target name
		self.w.label_font_tar = vanilla.TextBox((col_1_left, (margin_ver+line_pos), label_w, label_h), "To:", sizeStyle=label_size)
		self.w.filename_font_tar = vanilla.TextBox((col_2_left, (margin_ver+line_pos+text_y_adj), text_w, text_h), self.getFilename(self.font_tar), sizeStyle=text_size)
		line_pos += line_h
		# Create UI Element: Horizontal rule (between file select & results box)
		self.w.rule_divider = vanilla.HorizontalLine((margin_hor, (margin_ver+line_pos), -margin_hor, rule_height))
		line_pos += (line_h+rule_height)
		# Create UI Element: Results text
		self.w.results_box = vanilla.Box((col_1_left, (margin_ver+line_pos), self.results_w, self.results_h))
		self.w.results_box.text = vanilla.TextBox((self.padding, self.padding, (self.results_w-(self.padding*2)), (self.results_h-(self.padding*2))), results_txt_def, selectable=True, sizeStyle=label_size)
		# Create UI Element: Footnote
		self.w.footnote = vanilla.TextBox((0, (button_sync_y1-button_h-label_h), self.window_w, footnote_h), "", alignment="center", sizeStyle=footnote_size)

		# If font files are syncable
		if self.is_syncable:
			# Create UI Elements: Swap & Sync Buttons
			self.w.button_swap = vanilla.Button((button_swap_x1, button_swap_y1, button_swap_w, button_h), button_swap_txt, callback=self.buttonSwapCallback)
			self.w.button_sync = vanilla.Button((button_sync_x1, button_sync_y1, button_sync_w, button_h), button_sync_txt, callback=self.buttonSyncCallback)
			self.w.setDefaultButton( self.w.button_sync )
			# Create UI Element: Swap pointer
			self.w.rule_pointer_v = vanilla.VerticalLine( ( rule_pointer_x1, button_swap_y1+(button_h/2)-(rule_vert_h/2), rule_height, rule_vert_h) )
			self.w.rule_pointer_h1 = vanilla.HorizontalLine((rule_pointer_x1, rule_pointer_y1, rule_pointer_w, rule_height))
			self.w.rule_pointer_h2 = vanilla.HorizontalLine((rule_pointer_x1-(rule_pointer_w/2), button_swap_y1+(button_h/2)-(rule_vert_h/2), (rule_pointer_w/2), rule_height))
			self.w.rule_pointer_h3 = vanilla.HorizontalLine((rule_pointer_x1-(rule_pointer_w/2), button_swap_y1+(button_h/2)-(rule_vert_h/2)+rule_vert_h-rule_height, (rule_pointer_w/2), rule_height))
		else: # Change results text to appropriate error
			if (
				self.font_tar_glyphs_count != self.font_src_glyphs_count
				and self.font_tar_glyphs_count != 0
				and self.font_src_glyphs_count != 0
			):
				self.w.results_box.text.set(self.str_error_glyph_count)
			elif (
				self.font_tar_layers_count != self.font_src_layers_count
				and self.font_tar_layers_count != 0
				and self.font_src_layers_count != 0
			):
				self.w.results_box.text.set(self.str_error_layer_count)
			else:
				self.w.results_box.text.set(self.str_error_no_file)

	def windowResizedCallback(self, sender):
		win_pos = self.w.getPosSize()
		# Get new window height
		win_h = win_pos[3]
		# Set results box & text dimensions
		self.w.results_box.resize(self.results_w, win_h-self.results_b_offset)
		self.w.results_box.text.resize((self.results_w-(self.padding*2)), win_h-self.results_b_offset)

	def getFilename(self, font):
		if font is None:
			# Return open file prompt string
			return self.str_open
		# Get glyphs & layers counts
		layers_total = self.getLayerSumAllGlyphs(font)
		glyphs_total = len(font.glyphs)
		layers_per_glyph = layers_total / glyphs_total
		# Get file extension index. Position of last "/" + 1
		ext_index = font.filepath.rfind('/')+1
		# Get file name substring from filepath
		filename = font.filepath[ext_index:]
		# Strip ".glyphs" extension
		if filename.endswith('.glyphs'):
			filename = filename[:-7]
		# Add glyph & layer counts
		filename += " (" + str(glyphs_total) + " glyphs, "
		filename += str(layers_total) + " [" + str(layers_per_glyph)  + "] layers)"
		# Return filename
		return filename

	def buttonSyncCallback(self, sender):
		# Get horizontal metrics of source font
		src_horz_metrics = self.getHorizontalMetrics(self.font_src)
		# Set horizontal metrics of target font
		self.setHorizontalMetrics(src_horz_metrics, self.font_tar)
		# Log completion to results box
		self.logUpdateResults()
		# Clear update log
		self.update_log = []

	def logUpdateResults(self):
		# Get count of updates made
		update_len = len(self.update_log)
		# If any updates were made
		if update_len > 0:
			# Sort updates
			self.update_log.sort()
			# Initial header string for log
			str_log = u"✅ " + str(update_len) + " " + self.str_sync_success + "\n\n"
			# Create list to contain one list for each layer
			logs_by_layer = []
			# Populate list with a list for each layer update
			for i in self.font_tar_layer_names:
				logs_by_layer.append(list())
			# Iterate though all updates
			for msg in self.update_log:
				# Iterate through all layer names
				for index, layer in enumerate(self.font_tar_layer_names):
					# If message string contains layer name substring
					if self.font_tar_layer_names[index] in msg:
						# Add message to this layer's list
						logs_by_layer[index].append(msg)
			for index, layer in enumerate(logs_by_layer):
				# If layer has changes
				if len(layer) > 0:
					# Get layer name
					layer_name = self.font_tar_layer_names[index]
					# Add layer name once
					str_log += "Layer '" + layer_name + "': \n"
					# Iterate through messages
					for msg in layer:
						# Remove layer name from message, add bullet, add to log
						str_log += "  - " + msg.replace(layer_name + " ", "")
						# Add line break
						str_log += "\n"
					# Add line break
					str_log += "\n"
			# Set results box text with result string
			self.w.results_box.text.set(str_log)
			# Set footntoe text with check macro panel tip string
			self.w.footnote.set(self.str_macro_panel)
			# Log completion to console
			print("")
			print(u"✅ " + str_log)
		else: # Else no updates
			# Set results box text with no updates string
			self.w.results_box.text.set(u"✅ " + self.str_synced)
			# Set footntoe text with empty string
			self.w.footnote.set("")
			# Log completion to console
			print("")
			print(u"✅ " + self.str_synced)

	def buttonSwapCallback(self, sender):
		# Swap font source & target
		if self.font_src == Glyphs.fonts[0]:
			self.font_src = Glyphs.fonts[1]
			self.font_tar = Glyphs.fonts[0]
		else:
			self.font_src = Glyphs.fonts[0]
			self.font_tar = Glyphs.fonts[1]
		# Set filename in text objects
		self.w.filename_font_src.set(self.getFilename(self.font_src))
		self.w.filename_font_tar.set(self.getFilename(self.font_tar))

	# Checks if floating point values are approximately equal
	def isClose(self, a, b, rel_tol=1e-09, abs_tol=0.0):
		return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

	def getLayerNames(self, font_obj):
		layer_names = []
		for glyph in font_obj.glyphs:
			for layer in glyph.layers:
				layer_names.append(layer.name)
		layer_names = list(dict.fromkeys(layer_names))
		# Return layer names list
		return layer_names

	def getLayerSumAllGlyphs(self, font_obj):
		layer_counts = []	# List to store layer counts for each glyph
		total_sum = 0
		# Iterate through all glyphs of font
		for glyph in font_obj.glyphs:
			# Get count of layers for this glyph & add to list
			layer_counts.append( len(glyph.layers) )
		for count in layer_counts:
			total_sum += count
		return total_sum

	# Returns dict of horizontal metrics for every glyph of provided font object
	# Each glyph (glyph name is key) contains dict for each layer (layer name is key) to store values
	def getHorizontalMetrics(self, font_obj):
		# Create dict of metrics to return
		metrics = {}
		# Iterate through all glyphs of font
		for glyph in font_obj.glyphs:
			# Create dict for this glyph with key of same name (e.g. "A")
			metrics[glyph.name] = {}
			# Iterate through layers of the glyph
			for i, layer in enumerate(glyph.layers):
				# Create dict for this layer with key of same name (e.g. "Bold Oblique")
				metrics[glyph.name][str(i)] = {}
				# Add horizontal metrics for this layer (with keys for each) to layer dict
				metrics[glyph.name][str(i)][self.str_lmk] = glyph.leftMetricsKey
				metrics[glyph.name][str(i)][self.str_rmk] = glyph.rightMetricsKey
				metrics[glyph.name][str(i)][self.str_lkg] = glyph.leftKerningGroup
				metrics[glyph.name][str(i)][self.str_rkg] = glyph.rightKerningGroup
				metrics[glyph.name][str(i)][self.str_lsb] = layer.LSB
				metrics[glyph.name][str(i)][self.str_rsb] = layer.RSB
		# Return dict
		return metrics

	def setHorizontalMetrics(self, metrics, font):
		# Iterate through all glyphs of target font
		for glyph in font.glyphs:
			# Iterate through layers of this glyph
			for i, layer in enumerate(glyph.layers):
				# If glyph is not auto-aligned & has paths (i.e. not all auto-aligned components)
				if not layer.isAligned and len(layer.paths) > 0:
					# Get side bearings of source glyph
					src_lsb = metrics[glyph.name][str(i)][self.str_lsb]
					src_rsb = metrics[glyph.name][str(i)][self.str_rsb]
					# Set side bearings of target glyph
					self.syncValue(glyph, layer, src_lsb, layer.LSB, self.str_lsb)
					self.syncValue(glyph, layer, src_rsb, layer.RSB, self.str_rsb)
			# Get metric keys of source glyph
			src_lmk = metrics[glyph.name][str(0)][self.str_lmk]
			src_rmk = metrics[glyph.name][str(0)][self.str_rmk]
			# Get kerning groups of source glyph
			src_lkg = metrics[glyph.name][str(0)][self.str_lkg]
			src_rkg = metrics[glyph.name][str(0)][self.str_rkg]
			# Set metric keys of target glyph
			self.syncValue(glyph, layer, src_lmk, glyph.leftMetricsKey, self.str_lmk)
			self.syncValue(glyph, layer, src_rmk, glyph.rightMetricsKey, self.str_rmk)
			# Set kerning groups of target glyph
			self.syncValue(glyph, glyph.layers[0], src_lkg, glyph.leftKerningGroup, self.str_lkg)
			self.syncValue(glyph, glyph.layers[0], src_rkg, glyph.rightKerningGroup, self.str_rkg)
		# # Set kerning data of target font
		# font.kerning = self.font_src.kerning

	def syncValue(self, glyph, layer, val_src, val_tar, val_str):
		# Whether metics should be updated
		is_update = False
		# If values are numbers (i.e. not metric keys like "H" or "=|H")
		if type(val_src) == float and type(val_tar) == float:
			# If target value (float) is not already equal to source value
			if not self.isClose(val_tar, val_src):
				is_update = True
		else: # Else values are metric keys (i.e. not numbers)
			# If target value (metric key) is not already equal to source value
			if val_tar != val_src:
				is_update = True
		# If metrics should be updated
		if is_update:
			# Set appropriate value of target glyph to that of source glyph
			if val_str == self.str_lmk:
				glyph.leftMetricsKey = val_src
			if val_str == self.str_rmk:
				glyph.rightMetricsKey = val_src
			if val_str == self.str_lkg:
				glyph.leftKerningGroup = val_src
			if val_str == self.str_rkg:
				glyph.rightKerningGroup = val_src
			if val_str == self.str_lsb:
				layer.LSB = val_src
			if val_str == self.str_rsb:
				layer.RSB = val_src
			# Get update message for log
			msg = layer.name + " '" + glyph.name + "' " + val_str
			msg += " changed from [" + str(val_tar) + "] to [" + str(val_src) + "]"
			# Add update message to log
			self.update_log.append(msg)
			return True

# Run
SyncHorizontalMetrics()
