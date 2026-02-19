import time
import re
	
# Markdown+
#
# Developed for the Deutsche Precision MES by C. Ryan Deardorff
#
# http://deutscheprecision.com

FORMATTING_STYLES = [
	['Bold', '**', '**'],
	['Italic', '*', '*'],
	['Line-through', '<s>', '</s>'],
	['Overline', '<span style="text-decoration: overline">', '</span>'],
	['Superscript', '<sup>', '</sup>'],
	['Underline', '<u>', '</u>'],
	['Text Shadow', '<span style="text-shadow: 2px 2px 2px rgba(0, 0, 0, 0.5)">', '</span>'],
	['Box Shadow', '<span style="box-shadow: 2px 2px 2px rgba(0, 0, 0, 0.5)">', '</span>']
]

FORMATTING_FONTS = [
	'Arial',
	'Arial Narrow',
	'Courier New',
	'Futura',
	'Garamond',
	'Georgia',
	'Helvetica',
	'Merriweather',
	'Monospace',
	'Roboto',
	'Sans-serif',
	'Times New Roman',
	'Verdana'
]

FORMATTING_SIZES = [
	'25%',
	'50%',
	'75%',
	'100%',
	'125%',
	'150%',
	'175%',
	'200%',
	'250%',
	'300%',
	'350%',
	'400%',
	'450%',
	'500%'
]

FORMATTING_TEXT_ALIGN = [
	'left',
	'right',
	'center'
]

FORMATTING_MARGIN_PADDING = [
	'0.1em',
	'0.2em',
	'0.3em',
	'0.4em',
	'0.5em',
	'0.6em',
	'0.7em',
	'0.8em',
	'0.9em',
	'1em',
	'1.25em',
	'1.5em',
	'1.75em',
	'2em'
]

BORDER_STYLES = [
	'solid',
	'dashed',
	'dotted',
	'double',
	'groove',
	'ridge',
	'inset',
	'outset',
	'hidden',
	'none'
]

BORDER_SIZES = [
	'1px',
	'2px',
	'3px',
	'4px',
	'5px',
	'6px',
	'7px',
	'8px',
	'9px',
	'10px',
	'15px',
	'20px',
	'25px',
	'30px',
	'40px',
	'50px'
]

def getFormattingMenuItems(includeHeader=False, domID=''):
	items = []
	if includeHeader:
		items.append(getHeaderItem('Format:'))
	for f in FORMATTING_STYLES:
		items.append(getMessageItem('    ' + f[0], 'insert-format', {
			'pre': f[1],
			'post': f[2],
			'domID': domID
	    }))
	fonts = []
	for f in FORMATTING_FONTS:
		fonts.append(getMessageItem('    ' + f, 'insert-format', {
			'pre': '<span style="font-family: ' + f + '">',
			'post': '</span>',
			'domID': domID
	    }))
	items.append(getHeaderItem('    Font', fonts))   
	sizes = []
	for f in FORMATTING_SIZES:
		sizes.append(getMessageItem('    ' + f, 'insert-format', {
			'pre': '<span style="font-size: ' + f + '">',
			'post': '</span>',
			'domID': domID
	    }))
	items.append(getHeaderItem('    Size', sizes))   
	aligns = []
	for f in FORMATTING_TEXT_ALIGN:
		aligns.append(getMessageItem('    ' + f.title(), 'insert-format', {
			'pre': '<div style="text-align: ' + f + '">',
			'post': '</div>',
			'domID': domID
	    }))
	items.append(getHeaderItem('    Align', aligns)) 
	margins = []
	for m in FORMATTING_MARGIN_PADDING:
		margins.append(getMessageItem('    ' + m, 'insert-format', {
			'pre': '<span style="margin: ' + m + '">',
			'post': '</span>',
			'domID': domID
	    }))
	items.append(getHeaderItem('    Margin', margins))
	paddings = []
	for p in FORMATTING_MARGIN_PADDING:
		paddings.append(getMessageItem('    ' + p, 'insert-format', {
			'pre': '<span style="padding: ' + p + '">',
			'post': '</span>',
			'domID': domID
	    }))
	items.append(getHeaderItem('    Padding', paddings))
	borders = []
	borderStyles = []
	for style in BORDER_STYLES:
		borderStyles.append(getMessageItem('    ' + style.title(), 'insert-format', {
			'pre': '<span style="border-style: ' + style + '">',
			'post': '</span>',
			'domID': domID
	    }))
	borders.append(getHeaderItem('    Style', borderStyles))
	borderWidths = []
	for width in BORDER_SIZES:
		borderWidths.append(getMessageItem('    ' + width, 'insert-format', {
			'pre': '<span style="border-width: ' + width + '">',
			'post': '</span>',
			'domID': domID
	    }))
	borders.append(getHeaderItem('    Width', borderWidths))
	borderRadiuses = []
	for radius in BORDER_SIZES:
		borderRadiuses.append(getMessageItem('    ' + radius, 'insert-format', {
			'pre': '<span style="border-radius: ' + radius + '">',
			'post': '</span>',
			'domID': domID
	    }))
	borders.append(getHeaderItem('    Radius', borderRadiuses))
	borderColors = []
	for c in exchange.markdownPlus.colors.COLOR_NAMES:
		borderColors.append(getMessageItem('    ' + c, 'insert-format', {
			'pre': '<span style="border-color: ' + c + '">',
			'post': '</span>',
			'domID': domID
	    }))
	borders.append(getHeaderItem('    Color', borderColors))
	items.append(getHeaderItem('    Border', borders))
	colors = []
	for c in exchange.markdownPlus.colors.COLOR_NAMES:
		colors.append(getMessageItem('    ' + c, 'insert-format', {
			'pre': '<span style="color: ' + c + '">',
			'post': '</span>',
			'domID': domID
	    }))
	items.append(getHeaderItem('    Color', colors))    
	backgrounds = []
	for c in exchange.markdownPlus.colors.COLOR_NAMES:
		label = c
		if c == 'Other...':
			c = 'Background Other...'
			label = 'Other...'
		backgrounds.append(getMessageItem('    ' + label, 'insert-format', {
			'pre': '<span style="background-color: ' + c + '">',
			'post': '</span>',
			'domID': domID
	    }))
	items.append(getHeaderItem('    Background', backgrounds))    
	return items

def getSeparator():
	return {
		"type": "separator"
	}

def getHeaderItem(label, children=[], style={"classes": ""}):
	return {
		"text": label,
		"icon": {
			"path": "",
			"color": "",
			"style": {}
		},
		"style": style,
		"type": "submenu" if len(children) > 0 else "link",
		"children": children,
		"link": {
			"url": "",
			"target": "self"
		},
		"method": {
			"name": "",
			"params": {}
		},
		"message": {}
	}
			
def getMessageItem(label, messageType, messagePayload, messageScope='page', style={"classes": ""}):
	return {
		"text": label,
		"icon": {
			"path": "",
			"color": "",
			"style": {}
		},
		"style": style,
		"type": "message",
		"children": [],
		"link": {
			"url": "",
			"target": "self"
		},
		"method": {
			"name": "",
			"params": {}
		},
		"message": {
			"type": messageType,
			"payload": messagePayload,
			"scope": messageScope
		}
	}
			
def getFormattingContextMenu(domID, selectionStart, selectionEnd, htmlEnabled):
	
	def getSubMenu(symbols):
		submenu = []
		for s in symbols:
			submenu.append(getMessageItem(u'' + s[0], 'insert-symbol', { 
				'char': u'' + s[0],
				'domID': domID
			}, style={'font-size': '120%'}))
		return submenu
	
	if selectionStart == selectionEnd:
		items = [getHeaderItem('Insert:')]
		stypes = exchange.markdownPlus.symbols.SYMBOLS.keys()
		stypes.sort()
		if htmlEnabled:
			items.append(getHeaderItem(u'    Formatting', getFormattingMenuItems(False, domID)))
			items.append(getSeparator())
		for key in stypes:
			if key == '':
				for s in exchange.markdownPlus.symbols.SYMBOLS[key]:
					items.append(getMessageItem(u'    ' + s[2] + ' ' + s[0], 'insert-symbol', { 
						'char': u'' + s[0],
						'domID': domID
					}))
		items.append(getSeparator())
		for key in stypes:
			if key != '':
				items.append(getHeaderItem('    ' + key, getSubMenu(exchange.markdownPlus.symbols.SYMBOLS[key])))
		return items
	if not htmlEnabled:
		return None
	return getFormattingMenuItems(True, domID)

def insertFormat(self, payload):
	try:
		if payload['domID'] == self.view.custom.domID:
			if 'Other...' in payload['pre']:
				system.perspective.openPopup('ColorPicker', 'Exchange/ColorPicker/ColorPickerPopup', params = {
						'id': self.view.custom.domID,
						'isBackground': 'Background' in payload['pre']
					},
					title = '',
					draggable = False,
					showCloseIcon = False,
					modal = True,
					overlayDismiss = True)	
			else:
				self.view.custom.setCursorAt = -2
				self.props.rejectUpdatesWhileFocused = False
				self.view.custom.undoText = self.view.params.text
				self.custom.cursorWasAt = self.view.custom.selectionEnd
				index1 = self.view.custom.selectionStart
				index2 = self.view.custom.selectionEnd
				text = self.view.params.text
				beginning = text[0:index1]
				ending = text[index2:]
				pre = payload['pre']
				post = payload['post']
				isDivOrSpan = pre.startswith('<div') or pre.startswith('<span')
				# Expand selection to include surrounding DIV/SPAN:
				if isDivOrSpan and ('<' in beginning and (beginning.endswith('>') or beginning.endswith('>\n'))) and ('>' in ending and (ending.startswith('<') or ending.startswith('\n<'))):
					while not beginning.endswith('<'):
						index1 -= 1
						beginning = text[0:index1]
					index1 -= 1
					while not ending.startswith('>'):
						index2 += 1
						ending = text[index2:]
					index2 += 1
				selection = text[index1:index2]
				# "Strip" whitespace from selection range:
				while selection.startswith(' ') and len(selection) > 2:
					selection = selection[1:]
					index1 += 1
				while selection.endswith(' ') and len(selection) > 1:
					selection = selection[:-1]
					index2 -= 1
				# Change SPAN to DIV when selection indicates a paragraph vs. word/phrase:
				if (index1 == 0 or text[index1 - 1:index1] == '\n') and (index2 == len(text) or text[index2:index2 + 1] == '\n'):
					pre = pre.replace('span', 'div')
					post = post.replace('span', 'div')
				replaceExistingStyle = False
				styleType = ''
				if 'style="' in pre:
					styleType = re.sub('^.+style="([^:]+).+$', '\\1', pre)
					if re.match('^<\w+ style="' + styleType, selection) or re.match('^<\w+ style="[^"]*; ' + styleType, selection):
						replaceExistingStyle = True
				if replaceExistingStyle:
					# Replace within existing DIV/SPAN:
					newValue = re.sub('^.+style="[^:]+: *([^;"]+).+$', '\\1', pre)
					if re.match('^\n?<\w+ style="' + styleType, selection):
						selection = re.sub('^(\n?<\w+ style="' + styleType + ':) *[^;"]+([\s\S]+)$', '\\1 ' + newValue + '\\2', selection)
					else:
						selection = re.sub('^(\n?<\w+ style="[^"]*; ' + styleType + ':) *[^;"]+([\s\S]+)$', '\\1 ' + newValue + '\\2', selection)
					self.props.text = text[0:index1] + selection + text[index2:]
					time.sleep(0.2)
					self.view.custom.setCursorAt = index1 + len(selection)
				else:
					# Add to existing DIV/SPAN:
					if (pre.startswith('<div style="') or pre.startswith('<span style="')) and ((selection.startswith('<div style="') and selection.endswith('</div>')) or (selection.startswith('<span style="') and selection.endswith('</span>'))):
						selection = re.sub('^(<\w+ style="[^"]+)', '\\1; ' + re.sub('^<\w+ style="([^"]+)".+$', '\\1', pre), selection)
						self.props.text = text[0:index1] + selection + text[index2:]
						time.sleep(0.2)
						self.view.custom.setCursorAt = index1 + len(selection)
					else:
						if pre.startswith('<div'):
							pre += '\n'
							post = '\n' + post
						self.props.text = text[0:index1] + pre + selection + post + text[index2:]
						time.sleep(0.2)
						self.view.custom.setCursorAt = index1 + len(pre) + len(selection)
				time.sleep(0.5)
				self.focus()
				self.restoreUpdatesSettings()
	except Exception as e:
		system.perspective.print(str(e))