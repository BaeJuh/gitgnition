import re

# Markdown+
#
# Developed for the Deutsche Precision MES by C. Ryan Deardorff
#
# http://deutscheprecision.com

STYLES = '<style>.mdPlus { display: flex; flex-direction: column; gap: 0em; } .mdPlus p { margin-bottom: 1em; } .nums { margin-left: 2em; } .mention { background-color: #00000011; border-radius: 10px; padding-left: 0.3em; padding-right: 0.3em; padding-top: 0em; padding-bottom: 0.1em; } .mdPlus LI { margin-left: 2.9em; padding-left: 0; } .mdPlus TABLE { position: relative; } .mdPlus BLOCKQUOTE DIV { margin-bottom: 1em; }</style>'

BLOB_URL = '/system/blob/markdown-plus/Exchange/MarkdownPlus/'

IMAGE_MARGIN_VERT = '0px'
IMAGE_MARGIN_HOR = '8px'

VIDEO_ATTS = 'autoplay muted'

ATTACHMENT_ICON_STYLE = 'height: 28px; width: 28px;'
ATTACHMENT_ICONS = {
	'attachment': '<svg viewBox="0 0 24 24" class="" data-icon="material/attachment" style="' + ATTACHMENT_ICON_STYLE + '"><g><g class="icon" id="attachment"><path d="M2 12.5C2 9.46 4.46 7 7.5 7H18c2.21 0 4 1.79 4 4s-1.79 4-4 4H9.5C8.12 15 7 13.88 7 12.5S8.12 10 9.5 10H17v2H9.41c-.55 0-.55 1 0 1H18c1.1 0 2-.9 2-2s-.9-2-2-2H7.5C5.57 9 4 10.57 4 12.5S5.57 16 7.5 16H17v2H7.5C4.46 18 2 15.54 2 12.5z"></path></g></g></svg>',
	'image': '<svg viewBox="0 0 24 24" class="" data-icon="material/image" style="' + ATTACHMENT_ICON_STYLE + '"><g><g class="icon" id="image"><path d="M21 19V5c0-1.1-.9-2-2-2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2zM8.5 13.5l2.5 3.01L14.5 12l4.5 6H5l3.5-4.5z"></path></g></g></svg>',
	'video': '<svg viewBox="0 0 24 24" class="" data-icon="material/ondemand_video" style="' + ATTACHMENT_ICON_STYLE + '"><g><g class="icon" id="ondemand_video"><path d="M21 3H3c-1.11 0-2 .89-2 2v12c0 1.1.89 2 2 2h5v2h8v-2h5c1.1 0 1.99-.9 1.99-2L23 5c0-1.11-.9-2-2-2zm0 14H3V5h18v12zm-5-6l-7 4V7z"></path></g></g></svg>',
	'audio': '<svg viewBox="0 0 24 24" class="" data-icon="material/hearing" style="' + ATTACHMENT_ICON_STYLE + '"><g><g class="icon" id="hearing"><path d="M17 20c-.29 0-.56-.06-.76-.15-.71-.37-1.21-.88-1.71-2.38-.51-1.56-1.47-2.29-2.39-3-.79-.61-1.61-1.24-2.32-2.53C9.29 10.98 9 9.93 9 9c0-2.8 2.2-5 5-5s5 2.2 5 5h2c0-3.93-3.07-7-7-7S7 5.07 7 9c0 1.26.38 2.65 1.07 3.9.91 1.65 1.98 2.48 2.85 3.15.81.62 1.39 1.07 1.71 2.05.6 1.82 1.37 2.84 2.73 3.55.51.23 1.07.35 1.64.35 2.21 0 4-1.79 4-4h-2c0 1.1-.9 2-2 2zM7.64 2.64L6.22 1.22C4.23 3.21 3 5.96 3 9s1.23 5.79 3.22 7.78l1.41-1.41C6.01 13.74 5 11.49 5 9s1.01-4.74 2.64-6.36zM11.5 9c0 1.38 1.12 2.5 2.5 2.5s2.5-1.12 2.5-2.5-1.12-2.5-2.5-2.5-2.5 1.12-2.5 2.5z"></path></g></g></svg>',
	'pdf': '<svg viewBox="0 0 24 24" class="" data-icon="material/picture_as_pdf" style="' + ATTACHMENT_ICON_STYLE + '"><g><g class="icon" id="picture_as_pdf"><path d="M20 2H8c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm-8.5 7.5c0 .83-.67 1.5-1.5 1.5H9v2H7.5V7H10c.83 0 1.5.67 1.5 1.5v1zm5 2c0 .83-.67 1.5-1.5 1.5h-2.5V7H15c.83 0 1.5.67 1.5 1.5v3zm4-3H19v1h1.5V11H19v2h-1.5V7h3v1.5zM9 9.5h1v-1H9v1zM4 6H2v14c0 1.1.9 2 2 2h14v-2H4V6zm10 5.5h1v-3h-1v3z"></path></g></g></svg>',
	'dataset': '<svg viewBox="0 0 24 24" class="" data-icon="material/assessment" style="' + ATTACHMENT_ICON_STYLE + '"><g><g class="icon" id="assessment"><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zM9 17H7v-7h2v7zm4 0h-2V7h2v10zm4 0h-2v-4h2v4z"></path></g></g></svg>',
	'doc': '<svg viewBox="0 0 24 24" class="" data-icon="material/description" style="' + ATTACHMENT_ICON_STYLE + '"><g><g class="icon" id="description"><path d="M14 2H6c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 1.99 2H18c1.1 0 2-.9 2-2V8l-6-6zm2 16H8v-2h8v2zm0-4H8v-2h8v2zm-3-5V3.5L18.5 9H13z"></path></g></g></svg>'
}

def massage(src, openLinksInNewTab=True):
	
	src = re.sub('<[Ss][Cc][Rr][Ii][Pp][Tt][^>]*>', '', src) 		# remove attempted scripting injection
	src = re.sub('(<\S[^>]*)\s[Oo][Nn][^>]+>', '\\1>', src) 		# remove attempted scripting via onclick, onmouseover, etc.
	src = re.sub('<[Ii][Ff][Rr][Aa][Mm][Ee][^>]*>', '', src)		# remove attempted injection via IFRAME

	try:
		ct = 0
		while re.match('^[\s\S]*<\[image\?id=\d+ [^i][\s\S]*$', src) and ct < 10000:
			imgID = re.sub('^[\s\S]*<\[image\?id=(\d+) [^i][\s\S]*$', '\\1', src)
			onload = exchange.markdownPlus.javaScript.getImageOnLoad(imgID)
			src = re.sub('^([\s\S]*<\[image\?id=\d+)( [^i][\s\S]*)$', '\\1' + onload + '\\2', src)
			ct += 1
		ct = 0
		while re.match('^[\s\S]*<\[video\?id=\d+ [^i][\s\S]*$', src) and ct < 10000:
			imgID = re.sub('^[\s\S]*<\[video\?id=(\d+) [^i][\s\S]*$', '\\1', src)
			onload = exchange.markdownPlus.javaScript.getImageOnLoad(imgID, 'onloadstart')
			src = re.sub('^([\s\S]*<\[video\?id=\d+)( [^i][\s\S]*)$', '\\1' + onload + '\\2', src)
			ct += 1

		src = re.sub('<\[(image\S+)\s+([^\]]+)\s+align=([^\]]+)\s+caption *=([^\]]+)\s*\]>', '<div style="text-align: \\3"><img style="margin-bottom: ' + IMAGE_MARGIN_VERT + '; cursor: pointer;" src="' + BLOB_URL + '\\1" \\2 />\n\\4</div>', src)
		src = re.sub('<\[(image\S+)\s+([^\]]+)\s+align=([^\]]+)\s+caption\s+top=([^\]]+)\s*\]>', '<div style="text-align: \\3">\\4\n<img style="margin-top: ' + IMAGE_MARGIN_VERT + '; cursor: pointer;" src="' + BLOB_URL + '\\1" \\2 /></div>', src)
		src = re.sub('<\[(image\S+)\s+([^\]]+)\s+align=([^\]]+)\s+caption\s+left=([^\]]+)\s*\]>', '<div style="text-align: \\3"><img style="float: right; margin: 0 0 ' + IMAGE_MARGIN_HOR + ' ' + IMAGE_MARGIN_HOR + '; cursor: pointer;" src="' + BLOB_URL + '\\1" \\2 />\\4</div>', src)
		src = re.sub('<\[(image\S+)\s+([^\]]+)\s+align=([^\]]+)\s+caption\s+right=([^\]]+)\s*\]>', '<div style="text-align: \\3"><img style="float: left; margin: 0 ' + IMAGE_MARGIN_HOR + ' ' + IMAGE_MARGIN_HOR + ' 0; cursor: pointer;" src="' + BLOB_URL + '\\1" \\2 />\\4</div>', src)
		src = re.sub('<\[(image\S+)\s+([^\]]+)\s+align=([^\]]+)\s*\]>', '<div style="text-align: \\3"><img style="cursor: pointer;" src="' + BLOB_URL + '\\1" \\2/></div>', src)
		
		src = re.sub('<\[(image\S+)\s+align=([^\]]+)\s+caption *=([^\]]+)\s*\]>', '<div style="text-align: \\2"><img style="margin-bottom: ' + IMAGE_MARGIN_VERT + '; cursor: pointer;" src="' + BLOB_URL + '\\1" />\n\\3</div>', src)
		src = re.sub('<\[(image\S+)\s+align=([^\]]+)\s+caption\s+top=([^\]]+)\s*\]>', '<div style="text-align: \\2">\\3\n<img style="margin-top: ' + IMAGE_MARGIN_VERT + '; cursor: pointer;" src="' + BLOB_URL + '\\1" /></div>', src)
		src = re.sub('<\[(image\S+)\s+align=([^\]]+)\s+caption\s+left=([^\]]+)\s*\]>', '<div style="text-align: \\2"><img style="float: right; margin: 0 0 ' + IMAGE_MARGIN_HOR + ' ' + IMAGE_MARGIN_HOR + '; cursor: pointer;" src="' + BLOB_URL + '\\1" />\\3</div>', src)
		src = re.sub('<\[(image\S+)\s+align=([^\]]+)\s+caption\s+right=([^\]]+)\s*\]>', '<div style="text-align: \\2"><img style="float: left; margin: 0 ' + IMAGE_MARGIN_HOR + ' ' + IMAGE_MARGIN_HOR + ' 0; cursor: pointer;" src="' + BLOB_URL + '\\1" />\\3</div>', src)
		src = re.sub('<\[(image\S+)\s+align=([^\]]+)\s*\]>', '<div style="text-align: \\3"><img style="cursor: pointer;" src="' + BLOB_URL + '\\1" \\2/></div>', src)
		
		src = re.sub('<\[(video\S+)\s+([^\]]+)\s+align=([^\]]+)\s+caption *=([^\]]+)\s*\]>', '<div style="text-align: \\3"><video style="margin-bottom: ' + IMAGE_MARGIN_VERT + '; cursor: pointer;" \\2 ' + VIDEO_ATTS + '><source src="' + BLOB_URL + '\\1" /></video>\n\\4</div>', src)
		src = re.sub('<\[(video\S+)\s+([^\]]+)\s+align=([^\]]+)\s+caption\s+top=([^\]]+)\s*\]>', '<div style="text-align: \\3">\\4\n<video style="margin-top: ' + IMAGE_MARGIN_VERT + '; cursor: pointer;" \\2 ' + VIDEO_ATTS + '><source src="' + BLOB_URL + '\\1" /></video></div>', src)
		src = re.sub('<\[(video\S+)\s+([^\]]+)\s+align=([^\]]+)\s+caption\s+left=([^\]]+)\s*\]>', '<div style="text-align: \\3"><video style="float: right; margin: 0 0 ' + IMAGE_MARGIN_HOR + ' ' + IMAGE_MARGIN_HOR + '; cursor: pointer;" \\2 ' + VIDEO_ATTS + '><source src="' + BLOB_URL + '\\1" /></video>\\4</div>', src)
		src = re.sub('<\[(video\S+)\s+([^\]]+)\s+align=([^\]]+)\s+caption\s+right=([^\]]+)\s*\]>', '<div style="text-align: \\3"><video style="float: left; margin: 0 ' + IMAGE_MARGIN_HOR + ' ' + IMAGE_MARGIN_HOR + ' 0; cursor: pointer;" \\2 ' + VIDEO_ATTS + '><source src="' + BLOB_URL + '\\1" /></video>\\4</div>', src)
		src = re.sub('<\[(video\S+)\s+([^\]]+)\s+align=([^\]]+)\s*\]>', '<div style="text-align: \\3"><video style="cursor: pointer;" \\2 ' + VIDEO_ATTS + '><source src="' + BLOB_URL + '\\1"/></video></div>', src)
		
		src = re.sub('<\[(video\S+)\s+align=([^\]]+)\s+caption *=([^\]]+)\s*\]>', '<div style="text-align: \\2"><video style="margin-bottom: ' + IMAGE_MARGIN_VERT + '; cursor: pointer;" ' + VIDEO_ATTS + '><source src="' + BLOB_URL + '\\1" /></video>\n\\3</div>', src)
		src = re.sub('<\[(video\S+)\s+align=([^\]]+)\s+caption\s+top=([^\]]+)\s*\]>', '<div style="text-align: \\2">\\3\n<video style="margin-top: ' + IMAGE_MARGIN_VERT + '; cursor: pointer;" ' + VIDEO_ATTS + '><source src="' + BLOB_URL + '\\1" /></video></div>', src)
		src = re.sub('<\[(video\S+)\s+align=([^\]]+)\s+caption\s+left=([^\]]+)\s*\]>', '<div style="text-align: \\2"><video style="float: right; margin: 0 0 ' + IMAGE_MARGIN_HOR + ' ' + IMAGE_MARGIN_HOR + '; cursor: pointer;" ' + VIDEO_ATTS + '><source src="' + BLOB_URL + '\\1" /></video>\\3</div>', src)
		src = re.sub('<\[(video\S+)\s+align=([^\]]+)\s+caption\s+right=([^\]]+)\s*\]>', '<div style="text-align: \\2"><video style="float: left; margin: 0 ' + IMAGE_MARGIN_HOR + ' ' + IMAGE_MARGIN_HOR + ' 0; cursor: pointer;" ' + VIDEO_ATTS + '><source src="' + BLOB_URL + '\\1" /></video>\\3</div>', src)
		src = re.sub('<\[(video\S+)\s+align=([^\]]+)\s*\]>', '<div style="text-align: \\3"><video style="cursor: pointer;" ' + VIDEO_ATTS + '><source src="' + BLOB_URL + '\\1" \\2/></video></div>', src)

		hrefAtts = ' target="_blank"' if openLinksInNewTab else ''
		src = re.sub('<\[(file[^]]+&name=)([^]]+)(\.[^]\.]+) +type=([^]]+)\s*\]>', '<div style="display: flex; align-items: center; gap: 2px"><a href="' + BLOB_URL + '\\1\\2\\3"' + hrefAtts + ' style="color: inherit"><[icon-\\4]></a><a href="' + BLOB_URL + '\\1\\2\\3"' + hrefAtts + '>\\2</a></div>', src)
		for key in ATTACHMENT_ICONS:
			src = re.sub('<\[icon\-' + key + '\]>', ATTACHMENT_ICONS[key], src)
		
		src = src.replace('~CB~', ']')
		src = src.replace('<img', '<img title="Click for full size"')
		src = src.replace('<video', '<video poster="/system/images/loading.gif" title="Click to play full size with sound"')

		ct = 0
		while re.match('[\s\S]*\:[^\s\:]+\:[\s\S]*', src) and ct < 10000:
			emoji = re.sub('[\s\S]*\:([^\s\:]+)\:[\s\S]*', '\\1', src)
			src = re.sub('([\s\S]*)\:' + emoji + '\:([\s\S]*)', '\\1' + exchange.markdownPlus.emojis.getCode(emoji) + '\\2', src)
			ct += 1
	except Exception as e:
		src = 'ERROR: ' + str(e) + '\n\n' + src
	
	src = re.sub('^\s*\|', '\n|', src) 
	
	src = '`\n' + exchange.markdownPlus.symbols.htmlEncode(str(src))
	
	src = re.sub('\n\>(.+)', '\n<blockquote>\\1</blockquote>', src)
	
	src = re.sub('^(`\n\s*)(\@[\w\_\.]+[\w\d])([\s\S]*)$', '\\1<p><span class="mention">\\2</span>\\3', src)
	
	src = exchange.markdownPlus.strings.replaceAll(src,
		'^[\s\S]*\n[\s\S]*[ \n]\@[\w\d\_\.]+[\w\d][\s\S]*', 
		'^([\s\S]*\n)([\s\S]*[ \n])(\@[\w\_\.]+[\w\d])([\s\S]*)$',
		'\\1<p>\\2<span style="background-color: #00000011; border-radius: 10px; padding-left: 0.3em; padding-right: 0.3em; padding-top: 0em; padding-bottom: 0em;">\\3</span>\\4')
	src = exchange.markdownPlus.strings.replaceAll(src,
		'^ [\s\S]*',
		'^ ([\s\S]*)', 
		'&nbsp;\\1')
	src = exchange.markdownPlus.strings.replaceAll(src,
		'[\s\S]*\n [\s\S]*',
		'\n( *) ',
		'\n\\1&nbsp;')

	src = re.sub('^(\d\.[^\n]+)\n', '<div class="nums">\\1</div>', src)
	src = re.sub('\n(\d\.[^\n]+)', '<div class="nums">\\1</div>', src)
		
	src = src.strip()
	src = re.sub('\[([^]]+)\]([^\(])', '[\\1]\\2', src)	
		
	src = re.sub('^\-([^\n]+)\n', '<li><span>\\1</span></li>', src)
	src = re.sub('\n\-([^\n]+)', '<li><span>\\1</span></li>', src)
	
	src = re.sub('\*\*([^\*]+)\*\*', '<b>\\1</b>', src)
	src = re.sub('\*([^\*]+)\*', '<i>\\1</i>', src)

	src = re.sub('(\n\> .+)', '\\1\n\n<br>', src) 
	src = re.sub('(\n\- .+)', '\\1<br>', src) 
	src = re.sub('(\n\- .+\n)([^\-])', '\\1\n<br>\\2', src)  
	
	src = src.replace('ö', '&ouml;')
	src = src.replace('’', "'")
	src = src.replace('|\n\n', '|\n<br>\n\n')
	src = src.replace('\n', '<br>')
	src = src[1:]
	src = '<p>' + src.replace('<br>|', '\n|').replace('|<br>', '|\n').replace('<br>\n|', '\n\n|').replace('<br><br>', '<p>').replace('<p>', '</p><p>')
	src = src.replace('<p><br>', '<p>')
	
	src = re.sub('([^\|])\n\|', '\\1<br>\n\n\n|', src) 
	
	src = src.replace('<br><li>', '</p><div style="margin-bottom: 0.7em;"><li>')
	src = src.replace('</li><br>', '</li></div>')
	src = src.replace('</li></p>', '</li></div>')
	src = src.replace('</p>', '</p><br>')
	src = src.replace('<p></p>', '' )
	src = src.replace('<br></div>', '</div>')
	if src.startswith('<br><br>'):
		src = src[8:]
	if src.startswith('<br><p>'):
		src = src[4:]
	if src.endswith('<p>'):
		src = src[:-3]
	src = re.sub('<p>(#[^<]+)</p>', '\n\n\\1\n<p>', src) 
	src = src.replace('<p><br>', '<p>')
	src = src.replace('<p><p>', '<p>')
	src = src.replace('<p><div', '<div')
	src = src.replace('<br><br>', '</p><p>')
	src = src.replace('</p><br><p>', '</p><p>')
	src = src.replace('</div><br><div', '</div><div')
	src = re.sub('(<div[^>]*>)<br>', '\\1', src)

	if src.strip() != '':
		return STYLES + '<div class="mdPlus">' + src + '\n\n</p></div>'
	return src
