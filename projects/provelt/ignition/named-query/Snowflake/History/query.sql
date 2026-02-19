SELECT 
	MIN(res.METRIC_TIMESTAMP) t_stamp,
	{avgCols} 
FROM 
	(SELECT 
		raw.METRIC_TIMESTAMP,
		NTILE(:fixedRows) OVER (PARTITION BY raw.TEMPLATE_PATH ORDER BY raw.METRIC_TIMESTAMP) ntile_buckets,
		{cols}
	FROM 
		(SELECT 
    		dm.TEMPLATE_PATH,
           dm.METRIC_TIMESTAMP,
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
            dm.TEMPLATE_PATH, dm.METRIC_TIMESTAMP
        ORDER BY 
    		dm.METRIC_TIMESTAMP ASC) raw
	ORDER BY 
		ntile_buckets ASC, raw.METRIC_TIMESTAMP ASC) res
GROUP BY 
    res.ntile_buckets
ORDER BY 
    t_stamp ASC    