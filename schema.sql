CREATE SEQUENCE "urls_id_seq"
CREATE TABLE "urls" (
	"id" int4 NOT NULL DEFAULT nextval('urls_id_seq'::regclass),
	"key" varchar(12),
	"url" varchar(255)
)
ALTER TABLE "urls" ADD CONSTRAINT "urls_pkey" PRIMARY KEY ("id") NOT DEFERRABLE INITIALLY IMMEDIATE;
