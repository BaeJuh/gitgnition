def createTables(self):
	from com.inductiveautomation.ignition.gateway import IgnitionGateway
	
	try:
		context = IgnitionGateway.get()
		projectName = system.project.getProjectName()
		dbName = context.getProjectManager().getProjectProps(projectName).getDefaultDatasourceName()
		ds = system.dataset.toPyDataSet(system.db.getConnectionInfo(dbName))
		dbType = ds[0]["DBType"]
	except:
		dbType = "MYSQL"
	
	if dbType == None:
		dashboard.showError("Unable to determine your project's default database. Please create tables manually.")
	else:
		try:
			# Schema
			queries = eval("db.%s.getQueries()" % dbType)
			for query in queries:
				system.db.runUpdateQuery(query)
				
			# Data
			queries = db.data.getQueries(dbType)
			for query in queries:
				system.db.runUpdateQuery(query)
				
			# Refresh session objects
			dashboard.refresh(self)
		except:
			dashboard.showError("Database type '%s' is not currently supported" % dbType)
	
def getDashboards(ds, parentId=None, parentPath=None, defaultDashboard=None, firstDashboard=None):
	dashboards = []
	gps = []
	
	for row in ds:
		id = row["id"]
		dashboardParentId = row["parent_id"]
		name = row["name"]
		icon = row["icon"]
		dashboardUrl = row["url"]
		gps_enabled = row["gps_enabled"]
		gps_lat = row["gps_lat"]
		gps_lon = row["gps_lon"]
		gps_radius = row["gps_radius"]
		showDefault = row["show_default"]
		showPublic = row["show_public"]
		username = row["username"]
		grid = row["grid"]
		cellSize = row["cell_size"]
		gridRows = row["grid_rows"]
		gridRowGutterSize = row["row_gutter_size"]
		gridCols = row["grid_cols"]
		gridColGutterSize = row["col_gutter_size"]	  
		dashboardOrder = row["dashboard_order"]
		
		if parentId == None:
			if gps_enabled:
				gps.append({"url":dashboardUrl, "lat":gps_lat, "lon":gps_lon, "radius":gps_radius})
		
		d = {"id":id, "name":name, "url":dashboardUrl, "icon":icon, "parent_id":dashboardParentId, "parent_path":parentPath, "allow_edit": True, "default":showDefault, "public":showPublic, "gps":{"enabled":gps_enabled, "lat":gps_lat, "lon":gps_lon, "radius":gps_radius}, "grid":grid, "cellSize":cellSize, "gridRows":gridRows, "gridRowGutterSize":gridRowGutterSize, "gridCols":gridCols, "gridColGutterSize":gridColGutterSize, "order":dashboardOrder, "action":{"action":"edit"}}		
		sizes = []
		if dashboardParentId == parentId:
			res = system.db.runNamedQuery(path="Dashboard/Widget/Get", parameters={"dashboard":id})
			res = system.dataset.toPyDataSet(res)
			
			widgets = {}
			idx = 0
			for w in res:
				if w["id"] not in widgets:
					widgets[w["id"]] = {"id":w["id"], "widget_id":w["widget_id"], "idx":idx, "name":w["name"], "widget":w["widget"], "path":w["path"], "params":{}, "sizes":{}, "action":{"action":"", "params":[]}}
					idx += 1
				
				size = int(w["size"])
				if size not in widgets[w["id"]]["sizes"]:
					widgets[w["id"]]["sizes"][size] = w["position"]
					
				if size not in sizes:
					sizes.append(size)
				
				param = w["parameter"]
				if param != None and param not in widgets[w["id"]]["params"]:
					paramValue = w["parameter_value"]					
					widgets[w["id"]]["params"][param] = dashboard.getParamValue(w["parameter_type_id"], paramValue)
					widgets[w["id"]]["action"]["params"].append({"id":w["parameter_id"], "parameter":param, "parameter_type_id":w["parameter_type_id"], "label":w["parameter_name"], "value":dashboard.getParamValue(w["parameter_type_id"], paramValue, True), "path":w["parameter_type_path"], "configuration":dashboard.encodeConfiguration(w["parameter_configuration"])})
			
			if parentPath == None:
				pp = name
			else:
				pp = "%s/%s" % (parentPath, name)
				
			d["widgets"] = [w[1] for w in widgets.items()]
			d["children"] = dashboard.getDashboards(ds, id, pp, defaultDashboard, firstDashboard)		
			d["sizes"] = [0] if len(sizes) == 0 else sizes	
			dashboards.append(d)
		
			if firstDashboard == None and len(d["children"]) == 0:
				firstDashboard = d
			
			if defaultDashboard == None and showDefault:
				defaultDashboard = d
			
	if parentId == None:
		return {"default":defaultDashboard, "first":firstDashboard, "dashboards":dashboards, "valid":True, "gps":gps, "numDashboards":len(ds)}
		
	return dashboards

def getParamValue(typeId, paramValue, edit=False):
	try:
		if typeId == 3:
			paramValue = int(paramValue)
		elif typeId == 4:
			paramValue = float(paramValue)
		elif typeId == 7:
			paramValue = True if paramValue in ["true", "True"] else False
		elif typeId == 15:
			if not edit:
				paramValue = dashboard.encodeConfiguration(paramValue) 
	except:
		pass
	return paramValue
	
def getWidgets(ds, size=0, configurable=False):
	widgets = []	
	for row in ds:
		if row["action"]["action"] != "delete":
			position = row["sizes"][size].split(",")
			widget = {
			  "name": row["name"],
			  "viewPath": "Page/Configuration/Widget Edit Wrapper" if configurable else row["path"],
			  "viewParams": {"id":row["id"], "configuring":False, "name":row["name"], "widgetId":row["widget_id"], "widgetName":row["widget"], "viewPath":row["path"], "viewParams":row["params"], "editParams":row["action"]["params"]} if configurable else row["params"],
			  "isConfigurable": configurable,
			  "header": {
				"enabled": True,
				"title": row["name"],
				"style": {
				  "classes": ""
				}
			  },
			  "body": {
				"style": {
				  "classes": "",
				  "padding": "5px"
				}
			  },
			  "minSize": {
				"columnSpan": 1,
				"rowSpan": 1
			  },
			  "position": {
				"rowStart": int(position[0]),
				"rowEnd": int(position[1]),
				"columnStart": int(position[2]),
				"columnEnd": int(position[3])
			  },
			  "style": {
				"classes": ""
			  }
			}
			widgets.append(widget)
	return widgets
	
def getInstalledWidgets(ds):
	widgets = {}
	for row in ds:
		if row["id"] not in widgets:
			widgets[row["id"]] = {
								  "name": row["widget"],
								  "viewPath": "Page/Configuration/Widget Edit Wrapper",
								  "viewParams": {"id":None, "configuring":False, "name":row["widget"], "widgetId":row["id"], "widgetName":row["widget"], "viewPath":row["path"], "viewParams":{}, "editParams":[]},
								  "isConfigurable": True,
								  "header": {
									"enabled": True,
									"title": row["widget"],
									"style": {
									  "classes": ""
									}
								  },
								  "body": {
									"style": {
									  "classes": ""
									}
								  },
								  "defaultSize": {
									"columnSpan": 1,
									"rowSpan": 1
								  },
								  "minSize": {
									"columnSpan": 1,
									"rowSpan": 1
								  },
								  "category":"Widgets",
								  "style": {
									"classes": ""
								  }
								}
		if row["parameter"] != None:
			widgets[row["id"]]["viewParams"]["viewParams"][row["parameter"]] = dashboard.getParamValue(row["parameter_type_id"], row["parameter_value"])
			widgets[row["id"]]["viewParams"]["editParams"].append({"id":row["parameter_id"], "parameter":row["parameter"], "parameter_type_id":row["parameter_type_id"], "label":row["parameter_name"], "value":dashboard.getParamValue(row["parameter_type_id"], row["parameter_value"], True), "path":row["parameter_type_path"], "configuration":dashboard.encodeConfiguration(row["parameter_configuration"])})
	return [w[1] for w in widgets.items()]

def encodeConfiguration(config):
	return {} if config == None else system.util.jsonDecode(config)
	
def getBreakpointConfiguration(sizes):
	ret = {}
	if len(sizes) == 1:
		ret = {
			"viewPath":"Page/Dashboard Component",
			"viewParams":{
				"size":sizes[0]
			}
		}
	elif len(sizes) == 2:
		ret = {
			"viewPath":"Page/Dashboard Component Breakpoint",
			"viewParams":{
				"large":sizes[0], 
				"small":sizes[1]
			}
		}
	elif len(sizes) == 3:
		ret = {
			"viewPath":"Page/Dashboard Configurable Breakpoint",
			"viewParams":{
				"configuration":{
					"large":{
						"viewPath":"Page/Dashboard Component Breakpoint",
						"viewParams":{"large":sizes[0], "small":sizes[1]}
					},
					"small":{
						"viewPath":"Page/Dashboard Component",
						"viewParams":{"size":sizes[2]}
					}
				}
			}
		}
	elif len(sizes) == 4:
		ret = {
			"viewPath":"Page/Dashboard Configurable Breakpoint",
			"viewParams":{
				"configuration":{
					"large":{
						"viewPath":"Page/Dashboard Component Breakpoint",
						"viewParams":{"large":sizes[0], "small":sizes[1]}
					},
					"small":{
						"viewPath":"Page/Dashboard Component Breakpoint",
						"viewParams":{"large":sizes[2], "small":sizes[3]}
					}
				}
			}
		}
	
	return ret
	
def getCurrentDashboard(dashboards, url, sub=False):
	d = None
	
	if not sub:
		dbObj = dashboards.dashboards
	else:
		dbObj = dashboards
		
	for row in dbObj:
		if row["url"] == url:
			d = dashboard.getDashboardObject(row)
		else:
			d = dashboard.getCurrentDashboard(row["children"], url, True)
			
		if d != None:
			break
	
	if d == None and not sub:
		if dashboards.default != None:
			d = dashboard.getDashboardObject(dashboards.default)
		elif dashboards.first != None:
			d = dashboard.getDashboardObject(dashboards.first)
		else:
			d = dashboard.getDashboardObject(False)
			
	return d
	
def getMenu(value, sub=False):
	menuItems = []
	publicMenuItems = []
	
	dashboards = value["dashboards"]
	path = value["path"]
	
	if not sub:
		menuItems.append({
    "target": "/",
    "items": [],
    "navIcon": {},
    "label": {
      "text": "Home",
      "icon": {
        "path": "material/home"
      }
    },
    "showHeader": False,
    "style": {
      "classes": "",
      "fontWeight": "bold" if path == "/" else "normal"
    }
  })
	
	for row in dashboards:
		menuItem = {"target":"/dashboard/%s" % row["url"], "label":{"text":row["name"], "icon":{"path":"" if row["icon"] == None else "material/%s" % row["icon"]}}, "showHeader":False}
		children = dashboard.getMenu({"dashboards":row["children"], "path":path}, True)
		menuItem["items"] = children
		if len(children) == 0:
			menuItem["navIcon"] = {}
		else:
			menuItem["navIcon"] = {"path":"material/chevron_right"}
		if not sub and row["public"]:
			publicMenuItems.append(menuItem)
		else:
			menuItems.append(menuItem)
	
	if not sub and len(publicMenuItems):
		menuItem = {"target":"/", "label":{"text":"Dashboards", "icon":{"path":"material/public"}}, "showHeader":False}
		menuItem["items"] = publicMenuItems
		menuItem["navIcon"] = {"path":"material/chevron_right"}
		menuItems.append(menuItem)
	
	if not sub:
		menuItems.extend([
  {
    "target": "/tags",
    "items": [],
    "navIcon": {},
    "label": {
      "text": "Tags",
      "icon": {
        "path": "ignition/add_child"
      }
    },
    "showHeader": False,
    "style": {
      "classes": "",
      "fontWeight": "bold" if path == "/tags" else "normal"
    }
  },
  {
  "target": "",
  "items": [
    {
      "target": "/snowflake/dashboard",
      "items": [],
      "navIcon": {
        "path": ""
      },
      "label": {
        "text": "Dashboard",
        "icon": {
          "path": "material/ac_unit"
        }
      },
      "visible": True,
      "enabled": True,
      "showHeader": True,
      "resetOnClick": False,
      "backActionText": "",
      "style": {
        "classes": "",
        "fontWeight": "bold" if path == "/snowflake/dashboard" else "normal"
      }
    },
    {
      "target": "/snowflake/history",
      "items": [],
      "navIcon": {
        "path": ""
      },
      "label": {
        "text": "History",
        "icon": {
          "path": "material/trending_up"
        }
      },
      "visible": True,
      "enabled": True,
      "showHeader": True,
      "resetOnClick": False,
      "backActionText": "",
      "style": {
        "classes": "",
        "fontWeight": "bold" if path == "/snowflake/history" else "normal"
      }
    }
  ],
  "navIcon": {
    "path": "material/chevron_right"
  },
  "label": {
    "text": "Snowflake",
    "icon": {
      "path": "material/ac_unit"
    }
  },
  "showHeader": False,
  "style": {
    "classes": "",
    "fontWeight": "bold" if path == "/snowflake/dashboard" or path == "/snowflake/history" else "normal"
  }
},
  {
    "target": "/diagnostics",
    "items": [],
    "navIcon": {},
    "label": {
      "text": "Diagnostics",
      "icon": {
        "path": "material/search"
      }
    },
    "showHeader": False,
    "style": {
      "classes": "",
      "fontWeight": "bold" if path == "/diagnostics" else "normal"
    }
  }
])
	
	return menuItems
	
def getTree(dashboards, id=None, sub=False):
	treeItems = []
	publicTreeItems = []
	
	lastPublic = None
	for i in range(len(dashboards)):
		row = dashboards[i]
		dashboardId = row["id"]
		if id == None or id == -1 or int(dashboardId) != int(id):
			if row["public"]:
				canMoveUp = lastPublic != None
				canMoveDown = False
				for j in range(i+1, len(dashboards)):
					if dashboards[j]["public"]:
						canMoveDown = True
						break
				lastPublic = i
			else:
				canMoveUp = i > 0
				canMoveDown = False
				if (i+1) < len(dashboards):
					for j in range(i+1, len(dashboards)):
						if not dashboards[j]["public"]:
							canMoveDown = True
							break
				
			treeItem = {"label":row["name"], "expanded":True, "data":{"id":row["id"], "order":row["order"], "canMoveUp":canMoveUp, "canMoveDown":canMoveDown, "path":row["name"] if row["parent_path"] == None else "%s/%s" % (row["parent_path"], row["name"])}}
			children = dashboard.getTree(row["children"], id, True)
			treeItem["items"] = children
			
			if not sub and row["public"]:
				publicTreeItems.append(treeItem)
			else:
				treeItems.append(treeItem)
	
	if not sub:
		if len(publicTreeItems):
			treeItem = {"label":"Public", "expanded":True, "data":{"id":None, "order":1, "canMoveUp":False, "canMoveDown":False, "path":""}, "items":publicTreeItems}
			treeItems.append(treeItem)
			
		treeItem = {"label":"Root", "expanded":True, "data":{"id":None, "order":1, "canMoveUp":False, "canMoveDown":False, "path":""}, "items":treeItems}
		treeItems = [treeItem]
	
	return treeItems

def getDashboardObject(dbObj):
	if isinstance(dbObj, bool):
		if dbObj:
			return {"id":None, "name":"", "url":"", "icon":"dashboard", "parent_id":None, "parent_path":"", "allow_edit":True, "default":False, "public":False, "gps":{"enabled":False, "lat":None, "lon":None, "radius":None}, "order":None, "widgets":[], "grid":"stretch", "cellSize":100, "gridRows":10, "gridCols":10, "gridRowGutterSize":6, "gridColGutterSize":6, "sizes":[0], "action":{"action":"add"}}
		else:
			return {"id":None, "name":None, "url":None, "icon":None, "parent_id":None, "parent_path":None, "allow_edit":False, "default":False, "public":False, "gps":{"enabled":False, "lat":None, "lon":None, "radius":None}, "order":None, "widgets":[], "grid":"stretch", "cellSize":100, "gridRows":10, "gridCols":10, "gridRowGutterSize":6, "gridColGutterSize":6, "sizes":[0], "action":{"action":""}}
	elif dbObj != None:
		return dashboard.copyDictionary(dbObj)

def copyArray(items):
	ret = []
	for value in items:
		if str(type(value)) == "<type 'com.inductiveautomation.perspective.gateway.script.PropertyTreeScriptWrapper$MapWrapper'>" or type(value) == dict:
			ret.append(dashboard.copyDictionary(value))
		else:
			ret.append(value)
	return ret
		
def copyDictionary(items):
	ret = {}
	for key in items:
		value = items[key]
		
		if str(type(value)) == "<type 'com.inductiveautomation.perspective.gateway.script.PropertyTreeScriptWrapper$MapWrapper'>" or type(value) == dict:
			ret[key] = dashboard.copyDictionary(value)
		else:
			ret[key] = value
	return ret
	
def editDashboard(self, add=True):
	if not self.session.props.auth.authenticated:
		dashboard.showMessage("Please login to create or edit dashboards. Click on the user icon (Guest) on the left.")
		return
		
	if add:
		self.session.custom.dashboard.objects.edit = dashboard.getDashboardObject(True)
		maxId = system.db.runNamedQuery(path="Dashboard/Get URL", parameters={}) + 1
		self.session.custom.dashboard.objects.edit.name = "Dashboard %d" % (maxId)
		self.session.custom.dashboard.objects.edit.url = "dash%d" % (maxId)
	else:
		if self.session.custom.dashboard.objects.current.id == None:
			return
			
		self.session.custom.dashboard.objects.edit = dashboard.getDashboardObject(self.session.custom.dashboard.objects.current)
	
	system.perspective.navigate(view="Page/Configuration/AddEdit Dashboard")
	
def getConfiguration(config, key, default=""):
	try:
		return config.get(key, default)
	except:
		return default

def addUpdateWidget(self):
	from java.util import UUID
	size = int(self.parent.getChild("Breakpoints").getChild("Breakpoints").props.controlValue)
	sizes = self.session.custom.dashboard.objects.edit.sizes
	sessionWidgets = self.session.custom.dashboard.objects.edit.widgets
	
	foundIds = []
	for row in self.props.widgets:
		positionStr = "%s,%s,%s,%s" % (row.position.rowStart, row.position.rowEnd, row.position.columnStart, row.position.columnEnd)
		
		foundId = False
		for i in range(len(sessionWidgets)):
			if sessionWidgets[i]["id"] == row.viewParams.id:
				sessionWidgets[i]["sizes"][size] = positionStr
				foundIds.append(sessionWidgets[i]["id"])
				foundId = True
				break
			
		if not foundId:
			id = UUID.randomUUID()
			sessionWidgets.append({"id":id, "widget_id":row.viewParams.widgetId, "name":row.viewParams.name, "widget":row.viewParams.widgetName, "path":row.viewParams.viewPath, "params":dashboard.copyDictionary(row.viewParams.viewParams), "sizes":{newSize:positionStr for newSize in sizes}, "action":{"action":"add", "params":dashboard.copyArray(row.viewParams.editParams)}})
			foundIds.append(id)

	for i in range(len(sessionWidgets)):
		id = sessionWidgets[i]["id"]
		if id not in foundIds:
			sessionWidgets[i]["action"]["action"] = "delete"
		
def editWidget(self):
	id = self.view.params.id
	name = self.view.params.name
	editParams = self.view.params.editParams
	
	widgets = self.session.custom.dashboard.objects.edit.widgets
	widget = None
	for i in range(len(widgets)):
		if widgets[i]["id"] == id:
			widget = widgets[i]
			break
	
	params = widget["params"]
	actionParams = widget["action"]["params"]
	
	for i in range(len(editParams)):
		paramValue = editParams[i]["value"]
		actionParams[i]["value"] = paramValue
		
		paramValue = dashboard.encodeConfiguration(paramValue) if editParams[i]["parameter_type_id"] == 15 else paramValue
		params[editParams[i]["parameter"]] = paramValue
		
	widget["name"] = name
	system.perspective.closePopup(id="widget-parameters")
	
def syncDashboardDB(self):
	if not self.session.props.auth.authenticated:
		dashboard.showMessage("Please login to create or edit dashboards")
		return
		
	d = self.session.custom.dashboard.objects.edit
	username = self.session.custom.dashboard.options.username
	parentId = d.parent_id
	
	if d.name == None or d.name == "":
		dashboard.showError("Please enter in a name")
		return
		 
	if d.url == None or d.url == "":
		dashboard.showError("Please enter in a URL")
		return 
		
	if d.icon == None or d.icon == "":
		dashboard.showError("Please enter in an icon")
		return 
		
	if not d.gps.enabled:
		d.gps.lat = None
		d.gps.lon = None
		d.gps.radius = None
	else:
		if d.gps.lat == None or d.gps.lon == None or d.gps.radius == None:
			dashboard.showError("Please enter in GPS lat/lon/radius")
			return
			
	if d.cellSize == None or d.gridRows == None or d.gridCols == None or d.gridRowGutterSize == None or d.gridColGutterSize == None:
		dashboard.showError("Please enter in grid data (cell size, rows, cols, gutter size)")
		return
		
	urlId = system.db.runNamedQuery(path="Dashboard/Check URL", parameters={"url":d.url})
	if urlId != None and (d.id == None or d.id != urlId):
		dashboard.showError("URL '%s' already exists. Please try another." % d.url)
		return 
	
	if d.public:
		d.default = False
	
	if d.action.action == "add":
		dashboardOrder = system.db.runNamedQuery(path="Dashboard/Max Order", parameters={"parent_id":-1 if parentId is None else parentId, "show_public":d.public})
		id = system.db.runNamedQuery(path="Dashboard/Add", parameters={"dashboard_order":dashboardOrder, "enabled":True, "gps_enabled":d.gps.enabled, "gps_lat":d.gps.lat, "gps_lon":d.gps.lon, "gps_radius":d.gps.radius, "grid":d.grid, "cell_size":d.cellSize, "grid_rows":d.gridRows, "grid_cols":d.gridCols, "grid_row_gutter_size":d.gridRowGutterSize, "grid_col_gutter_size":d.gridColGutterSize, "icon":d.icon, "name":d.name, "parent_id":parentId, "show_default":d.default, "show_public":d.public, "url":d.url, "username":username}, getKey=True)
	else:
		id = d.id
		system.db.runNamedQuery(path="Dashboard/Edit", parameters={"id":id, "dashboard_order":d.order, "enabled":True, "gps_enabled":d.gps.enabled, "gps_lat":d.gps.lat, "gps_lon":d.gps.lon, "gps_radius":d.gps.radius, "grid":d.grid, "cell_size":d.cellSize, "grid_rows":d.gridRows, "grid_cols":d.gridCols, "grid_row_gutter_size":d.gridRowGutterSize, "grid_col_gutter_size":d.gridColGutterSize, "icon":d.icon, "name":d.name, "parent_id":parentId, "show_default":d.default, "show_public":d.public, "url":d.url, "username":username})
				
	if d.default:
		system.db.runNamedQuery(path="Dashboard/Update Default", parameters={"id":id, "username":username})
	
	sizes = {}
	system.db.runNamedQuery(path="Dashboard/Widget/Size/Delete All", parameters={"dashboard_id":id})
	system.db.runNamedQuery(path="Dashboard/Sizes/Delete All", parameters={"dashboard_id":id})
	for size in d.sizes:
		sizes[size] = system.db.runNamedQuery(path="Dashboard/Sizes/Add", parameters={"dashboard_id":id, "size":size}, getKey=True)
			
	for widget in d.widgets:
		widgetId = None
		
		if widget.action.action == "delete":
			try:
				system.db.runNamedQuery(path="Dashboard/Widget/Delete", parameters={"id":widget.id})
			except:
				pass
		elif widget.action.action == "add":
			widgetId = system.db.runNamedQuery(path="Dashboard/Widget/Add", parameters={"dashboard_id":id, "widget_id":widget.widget_id, "name":widget.name}, getKey=True)
		else:
			widgetId = widget.id
			system.db.runNamedQuery(path="Dashboard/Widget/Edit", parameters={"id":widgetId, "dashboard_id":id, "widget_id":widget.widget_id, "name":widget.name})
			
		if widgetId != None:
			for size in sizes:
				sizeId = sizes[size]
				system.db.runNamedQuery(path="Dashboard/Widget/Size/Add", parameters={"widget_id":widgetId, "size_id":sizeId, "position":widget.sizes[size]})
			
			for param in widget.action.params:
				system.db.runNamedQuery(path="Dashboard/Widget/Parameter/Add" if widget.action.action == "add" else "Dashboard/Widget/Parameter/Edit", parameters={"widget_id":widgetId, "parameter_id":param.id, "parameter_value":param.value})
	
	dashboard.refresh(self)
	
	if d.action.action == "add":
		system.perspective.navigate(page="/dashboard/%s" % d.url)
	else:
		dashboard.back(self)

def moveDashboard(self, firstId, firstOrder, secondId, secondOrder):
	if not self.session.props.auth.authenticated:
		dashboard.showMessage("Please login to reorder dashboards")
		return
		
	system.db.runNamedQuery(path="Dashboard/Update Order", parameters={"id":firstId, "dashboard_order":secondOrder})
	system.db.runNamedQuery(path="Dashboard/Update Order", parameters={"id":secondId, "dashboard_order":firstOrder})
	dashboard.refresh(self)

def deleteDashboard(self):
	if not self.session.props.auth.authenticated:
		dashboard.showMessage("Please login to remove dashboards")
		return
		
	id = self.session.custom.dashboard.objects.edit.id
	system.db.runNamedQuery(path="Dashboard/Widget/Size/Delete All", parameters={"dashboard_id":id})
	system.db.runNamedQuery(path="Dashboard/Delete", parameters={"id":id})
	dashboard.refresh(self)
	system.perspective.navigate(page="/")
	
def back(self):
	system.perspective.navigate(page=self.page.props.path)
	
def refresh(self, fromSession=False):
	if fromSession:
		obj = self
	else:
		obj = self.session
		
	obj.refreshBinding("custom.dbValid")
	obj.refreshBinding("custom.dashboard.dashboards")
	system.perspective.sendMessage("dashboardRefresh")
	
def showError(message):
	dashboard.popupMessage("error", message, "Error_Text")
	
def showMessage(message):
	dashboard.popupMessage("info", message, "Text")
	
def popupMessage(icon, message, displayClass):
	params = {"icon":icon, "display":message, "class":displayClass}
	system.perspective.openPopup(id="message", view="Page/Popup/Message", params=params, showCloseIcon=True, draggable=False, resizable=True, modal=True, overlayDismiss=False)
	
def showConfirmation(message, function, params={}):
	params = {"icon":"help", "display":message, "class":"Text", "function":{"script":function, "params":params}}
	system.perspective.openPopup(id="confirmation", view="Page/Popup/Confirmation", params=params, showCloseIcon=True, draggable=False, resizable=True, modal=True, overlayDismiss=False)
	
def convertJSON(value, defaultValue):
	try:
		return system.util.jsonDecode(value)
	except:
		return defaultValue
