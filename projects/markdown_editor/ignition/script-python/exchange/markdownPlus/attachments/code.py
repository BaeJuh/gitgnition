import re

# Markdown+
#
# Developed for the Deutsche Precision MES by C. Ryan Deardorff
#
# http://deutscheprecision.com

FILE_TYPES = {
	'image': [
		'png',
		'jpg',
		'jpeg',
		'jfif',
		'gif'
	],
	'video': [
		'mov',
		'mp4',
		'avi',
		'qt',
		'wmv',
		'mkv',
		'webm'
	]
}

CONTENT_TYPES = {
    'aac': 'audio/aac',
    'mid': 'audio/midi',
    'midi': 'audio/midi',
    'mp3': 'audio/mpeg',
    'oga': 'audio/ogg',
    'opus': 'audio/opus',
    'wav': 'audio/wav',
    'weba': 'audio/webm',

    'abw': 'application/x-abiword',
    'arc': 'application/x-freearc',
    'azw': 'application/vnd.amazon.ebook',
    'bin': 'application/octet-stream',
    'bz': 'application/x-bzip',
    'bz2': 'application/x-bzip2',
    'cda': 'application/x-cdf',
    'csh': 'application/x-csh',
    'csv': 'text/csv',
    'doc': 'application/msword',
    'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'epub': 'application/epub+zip',
    'gz': 'application/gzip',
    'jar': 'application/java-archive',
    'json': 'application/json',
    'jsonld': 'application/ld+json',
    'mpkg': 'application/vnd.apple.installer+xml',
    'odp': 'application/vnd.oasis.opendocument.presentation',
    'ods': 'application/vnd.oasis.opendocument.spreadsheet',
    'odt': 'application/vnd.oasis.opendocument.text',
    'pdf': 'application/pdf',
    'php': 'application/x-httpd-php',
    'ppt': 'application/vnd.ms-powerpoint',
    'pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
    'rar': 'application/vnd.rar',
    'rtf': 'application/rtf',
    'sh': 'application/x-sh',
    'tar': 'application/x-tar',
    'vsd': 'application/vnd.visio',
    'xhtml': 'application/xhtml+xml',
    'xls': 'application/vnd.ms-excel',
    'xlsm': 'application/vnd.ms-excel',
    'xltx': 'application/vnd.ms-excel',
    'xltm': 'application/vnd.ms-excel',
    'xlsb': 'application/vnd.ms-excel',
    'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'xml': 'application/xml',
    'xul': 'application/vnd.mozilla.xul+xml',
    'zip': 'application/zip',
    '7z': 'application/x-7z-compressed',

    'apng': 'image/apng',
    'avif': 'image/avif',
    'bmp': 'image/bmp',
    'gif': 'image/gif',
    'ico': 'image/vnd.microsoft.icon',
    'jpeg': 'image/jpeg',
    'jpg': 'image/jpeg',
    'png': 'image/png',
    'svg': 'image/svg+xml',
    'tif': 'image/tiff',
    'tiff': 'image/tiff',
    'webp': 'image/webp',

    'avi': 'video/x-msvideo',
    'mp4': 'video/mp4',
    'mpeg': 'video/mpeg',
    'ogv': 'video/ogg',
    'ts': 'video/mp2t',
    'webm': 'video/webm',
    '3gp': 'video/3gpp',
    '3g2': 'video/3gpp2',

    'css': 'text/css',
    'csv': 'text/csv',
    'htm': 'text/html',
    'html': 'text/html',
    'ics': 'text/calendar',
    'js': 'text/javascript',
    'mjs': 'text/javascript',
    'txt': 'text/plain',

    'otf': 'font/otf',
    'ttf': 'font/ttf',
    'woff': 'font/woff',
    'woff2': 'font/woff2',

    'srt': 'text/vtt',
    'vtt': 'text/vtt'
}

ATTACHMENT_TYPE_ICONS = {
	'txt': 'doc',
	'doc': 'doc',
	'docx': 'doc',
	'xls': 'dataset',
	'xlsx': 'dataset',
	'xlsm': 'dataset',
	'xltx': 'dataset',
	'xltm': 'dataset',
	'xlsb': 'dataset',
	'csv': 'dataset',
	'pdf': 'pdf',
	'mp3': 'audio',
	'wav': 'audio',
	'vox': 'audio',
	'wma': 'audio',
	'mp4': 'video',
	'mov': 'video',
	'avi': 'video',
	'wmv': 'video',
	'mkv': 'video',
	'webm': 'video',
	'avchd': 'video',
	'flv': 'video',
	'png': 'image',
	'jpg': 'image',
	'jpeg': 'image',
	'jfif': 'image',
	'gif': 'image'
}

def getImageFileTypes():
	return FILE_TYPES['image'] + FILE_TYPES['video']
	
def getImageType(fileName):
	if re.match('.+\.\S+$', fileName):
		ext = re.sub('^.+\.(\S+)$', '\\1', fileName).lower()
		if ext in FILE_TYPES['video']:
			return 'video'
	return 'image'

def getFileContentType(fileName):
	if re.match('.+\.\S+$', fileName):
		ext = re.sub('^.+\.(\S+)$', '\\1', fileName).lower()
		if CONTENT_TYPES.has_key(ext):
			return CONTENT_TYPES[ext]
	return 'application/octet-stream'
	
def getFileAttachmentIcon(fileName):
	if re.match('.+\.\S+$', fileName):
		ext = re.sub('^.+\.(\S+)$', '\\1', fileName).lower()
		if ATTACHMENT_TYPE_ICONS.has_key(ext):
			return ATTACHMENT_TYPE_ICONS[ext]
	return 'attachment'

def getFileType(attachmentID, attachmentsTable):
	return system.db.runPrepQuery('SELECT type FROM ' + attachmentsTable + ' WHERE id = ?', [attachmentID])[0][0]