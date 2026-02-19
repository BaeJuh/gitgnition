SELECT
	data AS "Content",
	:type AS "ContentType",
	CONCAT("attachment; filename=", :name) AS "ContentDisposition"
FROM
	mes.markdown_attachments
WHERE
	id = :id