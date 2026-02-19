import re

# Markdown+
#
# Developed for the Deutsche Precision MES by C. Ryan Deardorff
#
# http://deutscheprecision.com

def getUserIDs(userMention):
	ids = []
	users = system.user.getUsers('default')
	for user in users:
		userID = user.get('username')
		if userID == userMention:
			ids.append(userID)
		else:
			fullName = getUserFullName(userID)
			if fullName == userMention.replace('_', ' '):
				ids.append(userID)
	return ids

def getMentionedUserIDs(note):
	try:
		ids = []
		s = note
		while re.match('^[\s\S]*\@[\w\d\_\.]+[\w\d][\s\S]*$', s):
			name = re.sub('^[\s\S]*\@([\w\d\_\.]+[\w\d])[\s\S]*$', '\\1', s)
			for userID in getUserIDs(name):
				ids.append(userID)
			s = re.sub('^([\s\S]*)\@[\w\d\_\.]+[\w\d]([\s\S]*)$', '\\1\\2', s)
		return ids
	except Exception as e:
		return str(e)

def getMentionOptions(domID, userSearch, mentionType):
	mention = []
	try:
		mentioned = []
		if userSearch is None or userSearch == '':
			return mention
		userSearch = userSearch.lower()
		users = system.user.getUsers('default')
		index = 0
		for user in users:
			userID = user.get('username')
			firstName = user.get('firstname') or ''
			lastName = user.get('lastname') or ''
			if (userID.lower().startswith(userSearch) or firstName.lower().startswith(userSearch) or lastName.lower().startswith(userSearch)):
				if mentionType == 'Full Name':
					if firstName != '' or lastName != '':
						userName = getUserFullName(userID)
					else:
						userName = None
				else:
					userName = userID
				if userName is not None and not userName in mentioned:
					mention.append({ 
						'domID': domID,
						'user': userName,
						'index': index
					})
					mentioned.append(userName)
					index += 1
	except Exception as e:
		mention.append({ 
			'domID': domID,
			'user': str(e),
			'index': index
		})
	return mention
	
def getUserFullName(userID, abbreviateLastName=False, abbreviateFirstName=False):
	return UserInfo(userID).getFullName(abbreviateLastName, abbreviateFirstName)
	
class UserInfo:

	def __init__(self, userID):
		self._userID = str(userID).strip()
		self._userData = system.user.getUser('default', self._userID)
		self._isValidUser = True
		if self._userData is None:
			self._isValidUser = False 
			
	def isValidUser(self):
		return self._isValidUser
			
	def get(self, id):
		return self._userData.get(id)
		
	def getUserName(self):
		return self._userData.get('username')
			
	def getFirstName(self):
		try:
			return self._userData.get('firstname').strip()
		except:
			return ''
				
	def getLastName(self):
		try:
			return self._userData.get('lastname').strip()
		except:
			return ''
				
	def getFullName(self, abbreviateLastName=False, abbreviateFirstName=False):
		if self._userID == '':
			return ''
		if self._isValidUser:
			if abbreviateLastName:
				fullName = re.sub('^(\S+) .+$', '\\1', self._userData.get('firstname')) + ' ' + self._userData.get('lastname')[0:1] + '.'
			elif abbreviateFirstName:
				fullName = self._userData.get('firstname')[0:1] + '. ' + re.sub('^(\S+)\s?\S*$', '\\1', self._userData.get('lastname'))
			else:
				fullName = self.getFirstName() + ' ' + self.getLastName()
			return fullName
		if self._userID == 'None' or self._userID == 'N/A':
			return 'N/A'
		if re.match('^\d+', self._userID):
			return 'Unknown User ' + self._userID
		return self._userID
		
	def getEmailAddress(self):
		for con in self._userData.getContactInfo():
			if con.contactType == 'email':
				return con.value
		return ''