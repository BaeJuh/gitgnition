import java.lang.Exception
import re

# Markdown+
#
# Developed for the Deutsche Precision MES by C. Ryan Deardorff
#
# http://deutscheprecision.com

COLOR_NAMES = [
	'Aquamarine',
	'Black',
	'Blue',
	'BlueViolet',
	'Brown',
	'Chocolate',
	'Crimson',
	'Cyan',
	'FireBrick',
	'ForestGreen',
	'Gold',
	'Green',
	'GreenYellow',
	'HotPink',
	'Indigo',
	'Magenta',
	'Maroon',
	'MidnightBlue',
	'Orange',
	'Pink',
	'PowderBlue',
	'Purple',
	'Red',
	'Salmon',
	'SeaGreen',
	'SkyBlue',
	'SteelBlue',
	'Teal',
	'Turquoise',
	'White',
	'Yellow',
	'YellowGreen',
	'Other...'
]

DK = 88			# 58
MD = 220		# DC
LT = 250		# FA

rainbow = [
	[DK, DK, DK],
	[LT, DK, DK],
	[LT, MD, DK],
	[MD, MD, DK],
	[DK, MD, DK],
	[DK, MD, MD],
	[DK, DK, LT],
	[MD, DK, LT],
	[LT, DK, MD]
]
  
def rgb(r, g, b):
	return 'rgb(' + str(int(r)) + ',' + str(int(g)) + ',' + str(int(b)) + ')'

