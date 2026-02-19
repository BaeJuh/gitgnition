def message(message):
	params = {"message":message}
	system.perspective.openPopup(id="message", view="Snowflake/Message", params=params, title="Message", showCloseIcon=True, draggable=True, resizable=True, modal=True, overlayDismiss=True)
	
def escapeDBValue(value):
	import re
	if value == None:
		return None
		
	return re.sub("[\W_]+", "_", value).strip().lower()