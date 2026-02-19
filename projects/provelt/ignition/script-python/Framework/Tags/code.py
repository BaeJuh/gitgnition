def browseTags(self, path="", filters=None, expanded=False, foldersOnly=False):
	treeItems = []
	results = system.tag.browse(path, {} if filters == None else filters)
	
	if results != None and results.getResults() != None:
		for result in results.getResults():
			name = result["name"]
			fullPath = str(result["fullPath"])
			hasChildren = result["hasChildren"] or str(result["tagType"]) in ["Folder", "UdtInstance"]
			
			if name != "_types_":
				data = {"path":fullPath, "hasChildren":False}
				treeItem = {"label":name, "expanded":expanded, "data":data}
				treeItem["items"] = []
				
				if hasChildren:
					treeItem["items"].append({"label":"Click to load...", "expanded":expanded, "data":{"path":result["fullPath"], "hasChildren":True}, "items":[], "icon":{"path":"material/hourglass_empty"}})
									
				if not foldersOnly or hasChildren:
					treeItems.append(treeItem)
	
	return treeItems