SELECT 
	dw.id,
	dw.name,
	w.id widget_id,
	w.name widget,
	w.path,
	w.icon,
	p.id parameter_id,
	p.parameter_name,
	p.parameter,
	COALESCE(dp.parameter_value, p.default_value) parameter_value,
	t.id parameter_type_id,
	t.path parameter_type_path,
	p.configuration parameter_configuration,
	s.size,
	ds.position
FROM 
	dashboard_widgets dw 
		JOIN widgets w ON w.id = dw.widget_id 
		JOIN dashboard_sizes s ON s.dashboard_id = dw.dashboard_id
		JOIN dashboard_widget_sizes ds ON ds.dashboard_size_id = s.id AND ds.dashboard_widget_id = dw.id 
		LEFT JOIN widget_parameters p ON p.widget_id = dw.widget_id
		LEFT JOIN widget_parameter_types t ON t.id = p.parameter_type_id
		LEFT JOIN dashboard_widget_parameters dp ON dp.dashboard_widget_id = dw.id AND dp.parameter_id = p.id  
WHERE 
	dw.dashboard_id = :dashboard
ORDER BY 
	s.size DESC, dw.id ASC, p.parameter ASC, p.id ASC