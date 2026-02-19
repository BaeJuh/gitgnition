SELECT
	data AS "Content",
	"image/png" AS "ContentType"
FROM
	mes.markdown_attachments
WHERE
	id = :id