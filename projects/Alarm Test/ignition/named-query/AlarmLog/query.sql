SELECT 
	DATE_FORMAT(MAX(e.eventtime), '%Y-%m-%d %H:%i:%s') AS "시간",
    -- MAX(e.eventtime) AS "시간",
    CASE 
        WHEN MAX(e.eventtype) = 0 THEN '진행 중(Active)'
        WHEN MAX(e.eventtype) = 1 THEN '미확인(Cleared)'
        WHEN MAX(e.eventtype) = 2 THEN '확인됨(Acked)'
    END AS "최종 상태",
    
    MAX(CASE WHEN d.propname = 'from' THEN d.strvalue END) AS "발신자",
    MAX(CASE WHEN d.propname = 'to' THEN d.strvalue END) AS "수신자",
    MAX(CASE WHEN d.propname = 'msg' THEN d.strvalue END) AS "메시지",
    MAX(CASE WHEN d.propname = 'ackuser' THEN d.strvalue END) AS "확인자",
    
    MAX(CASE WHEN d.propname = 'UUID' THEN d.strvalue END) AS "고유ID"
FROM alarm_events e
LEFT JOIN alarm_event_data d ON e.id = d.id
WHERE e.source LIKE '%Alarm Test%'
GROUP BY (SELECT strvalue FROM alarm_event_data WHERE id = e.id AND propname = 'UUID')
ORDER BY MAX(e.eventtime) DESC;