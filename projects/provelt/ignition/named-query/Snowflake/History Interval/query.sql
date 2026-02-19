SELECT 
	MIN(dm.MEASURE_TIMESTAMP) t_stamp,
	{avgRawCols}
FROM 
	TEMPLATES.{dataModel}_ASOF_VW dm
WHERE 
	dm.GROUP_ID = :groupId AND 
	dm.EDGE_NODE_ID = :edgeNodeId AND 
	dm.DEVICE_ID = :deviceId AND 
	dm.TEMPLATE_PATH = :instanceName AND 
	dm.METRIC_TIMESTAMP BETWEEN :startDate AND :endDate
GROUP BY 
    DATE_TRUNC(:interval, dm.METRIC_TIMESTAMP)
ORDER BY 
	DATE_TRUNC(:interval, dm.METRIC_TIMESTAMP) ASC