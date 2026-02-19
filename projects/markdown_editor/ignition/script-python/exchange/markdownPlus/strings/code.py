import re

# Markdown+
#
# Developed for the Deutsche Precision MES by C. Ryan Deardorff
#
# http://deutscheprecision.com

def replaceAll(src, match, matchCapture, replace, maxReplaces=1000000):
	tryCt = 0
	while re.match(match, src):
		src = re.sub(matchCapture, replace, src)
		tryCt += 1
		if tryCt > maxReplaces:
			raise Exception('exchange.markdownPlus.strings.replaceAll() - Too many replaces (' + str(maxReplaces) + ') for "' + match + '"')
	return src