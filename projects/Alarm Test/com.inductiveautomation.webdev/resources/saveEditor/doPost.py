def doPost(request, session):
	data = request['postData']
	content = data.get("content", "")
	
	system.perspective.sendMessage(
		messageType="quill-data",
		payload={"content": content},
	)
	
	return {'html': 'ok', 'content': content}