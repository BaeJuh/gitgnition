SELECT 
	nmr.GROUP_ID groupId,
	nmr.EDGE_NODE_ID edgeNodeId,
	nmr.DEVICE_ID deviceId,
	nmr.TEMPLATE_REFERENCE dataModel,
	nmr.TEMPLATE_VERSION dataModelVersion,
	nmr.TEMPLATE_PATH dataModelInstance,
	nmr.LAST_UPDATE timestamp
FROM 
	{stageDB}.SPARKPLUG_TEMPLATE_INSTANCE_REGISTRY nmr 
WHERE 
	(:groupId IS NULL OR :groupId = '' OR nmr.GROUP_ID = :groupId) AND 
	(:edgeNodeId IS NULL OR :edgeNodeId = '' OR nmr.EDGE_NODE_ID = :edgeNodeId) AND 
	(:deviceId IS NULL OR :deviceId = '' OR nmr.DEVICE_ID = :deviceId) AND 
	(:dataModel IS NULL OR :dataModel = '' OR nmr.TEMPLATE_REFERENCE = :dataModel) AND 
	(:dataModelVersion IS NULL OR :dataModelVersion = '' OR nmr.TEMPLATE_VERSION = :dataModelVersion) AND 
	(:search IS NULL OR :search = '' OR nmr.TEMPLATE_PATH ILIKE CONCAT('%', :search, '%'))
ORDER BY 
	nmr.GROUP_ID,
	nmr.EDGE_NODE_ID,
	nmr.TEMPLATE_REFERENCE,
	nmr.TEMPLATE_VERSION,
	nmr.TEMPLATE_PATH