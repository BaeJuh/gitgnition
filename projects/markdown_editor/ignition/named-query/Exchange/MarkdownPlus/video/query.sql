SELECT
	data AS "Content",
	"video/mp4" AS "ContentType"
FROM
	mes.markdown_attachments
WHERE
	id = :id