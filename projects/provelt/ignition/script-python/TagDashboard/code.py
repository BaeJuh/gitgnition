def selectFolder(self, tagPath):
	self.session.custom.tagPath = tagPath
	system.perspective.sendMessage(messageType="expand-folder", payload={"tagPath":tagPath})

def refreshTags():
	system.perspective.sendMessage(messageType="tag-refresh")
		
def message(message):
	params = {"message":message}
	system.perspective.openPopup(id="message", view="Tag Dashboard/Message", params=params, title="Message", showCloseIcon=True, draggable=True, resizable=True, modal=True, overlayDismiss=True)

def editTag(tagPath):
	params = {"tagPath":tagPath}
	system.perspective.openPopup(id="tag-edit", view="Tag Dashboard/Table/Tag Edit", params=params, title="Tag Edit", showCloseIcon=True, draggable=True, resizable=True, modal=True, overlayDismiss=True)
	
def getTags(self, tagPath, filters=None):
	ret = []
	
	results = system.tag.browse(tagPath, {} if filters == None else filters)
		
	if results != None and results.getResults() != None:
		i = 0
		for result in results.getResults():
			name = result["name"]
			if name != "_types_":
				hasChildren = result["hasChildren"] or str(result["tagType"]) in ["Folder", "UdtInstance"]
				ret.append({"name":name, "tagPath":result["fullPath"], "folder":hasChildren, "alternate":i%2!=0})
			i += 1
	
	ret.sort(key=lambda x:x["folder"], reverse=True)	
	return ret