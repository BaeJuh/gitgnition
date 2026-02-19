def browseTags(path="", filters=None):
	treeItems = []
	results = system.tag.browse(path, {} if filters == None else filters)
	
	for result in results.getResults():
		name = result["name"]
		if name != "_types_":
			treeItem = {"label":name, "expanded":False, "data":{"path":result["fullPath"], "hasChildren":result["hasChildren"]}}
			#if result['hasChildren']:
			#	children = tags.browseTags(result["fullPath"], filters)
			#else:
			#	children = []
			treeItem["items"] = []
			treeItems.append(treeItem)
	
	return treeItems
	
def browseHistoryTags(path="", filters=None):
	treeItems = []
	results = system.tag.browseHistoricalTags(path, {} if filters == None else filters)
	
	for result in results.getResults():
		name = result.getPath().toString().replace(path, "").replace(":/", "").replace("/", "")
		treeItem = {"label":name, "expanded":False, "data":{"path":result.getPath().toString(), "hasChildren":result.hasChildren()}}
#		if result.hasChildren():
#			children = tags.browseHistoryTags(result.getPath().toString(), filters)
#		else:
#			children = []
		treeItem["items"] = []
		treeItems.append(treeItem)
	
	return treeItems