
# Markdown+
#
# Developed for the Deutsche Precision MES by C. Ryan Deardorff
#
# http://deutscheprecision.com

def getCaretPositionJS(domID):
	return """<img style='display: none' src='/favicon.ico' onload="
		const view = [...window.__client.page.views._data.values()].find(view =>
			view.value.mountPath == this.parentNode.parentNode.parentNode.getAttributeNode('data-component-path').value.split('.')[0]).value;
		const notesTextArea = document.getElementById('""" + domID + """');
		var keepAlive""" + domID + """ = 0;
		var lastRunJS""" + domID + """ = -1;
		function getSelected() {
			const selectionStart = notesTextArea.selectionStart;
			view.custom.write('selectionStart', selectionStart);
			const selectionEnd = notesTextArea.selectionEnd;
			view.custom.write('selectionEnd', selectionEnd);
		}
		function reportSelection() {
			setCursorAt = view.custom.read('setCursorAt');
			if (setCursorAt > -1) {
				notesTextArea.blur();
				notesTextArea.setSelectionRange(setCursorAt, setCursorAt);
				getSelected();
				notesTextArea.focus();
				view.custom.write('setCursorAt', -1);
			}
			var runJS = view.custom.read('runJS');
			if (lastRunJS""" + domID + """ != runJS) {
				if (keepAlive""" + domID + """ % 100 == 0) {
					lastRunJS""" + domID + """ = runJS;
					view.custom.write('runJS', runJS + 1);
				}
				keepAlive""" + domID + """ += 1;
				setTimeout(reportSelection, 100);
			}
		}
		notesTextArea.onclick = getSelected;
		notesTextArea.onkeyup = getSelected;
		notesTextArea.oncontextmenu = getSelected;
		notesTextArea.onmouseout = getSelected;
		view.custom.write('runJS', 0);
		reportSelection();
	"/>"""

def getImageOnLoad(imgID, att='onload'):
	onLoad = """ id='img""" + imgID + """' """ + att + """="
		var v = null; 
		var n = this.parentNode.parentNode.parentNode.parentNode; 
		var tryCt = 1;
		while (tryCt > 0 && tryCt < 500) try { 
			v = [...window.__client.page.views._data.values()~CB~.find(view => view.value.mountPath == n.getAttributeNode('data-component-path').value.split('.')[0~CB~).value; 
			tryCt = 0; 
		} 
		catch(err) { 
			n = n.parentNode; 
			tryCt++; 
		} 
		const view = v; 
		const imgOpen = document.getElementById('img""" + imgID + """'); 
		function openFullImage() { 
			view.custom.write('imgClick', '""" + imgID + """'); 
		} 
		imgOpen.onclick = openFullImage;
		var ids = view.custom.read('imgIDs');
		ids = ids.filter(id => id !== '""" + imgID + """');
		ids.push('""" + imgID + """');
		view.custom.write('imgIDs', ids);"
	"""
	return onLoad.replace('\n', '') 