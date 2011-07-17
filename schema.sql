DROP TABLE IF EXISTS "urls";
CREATE TABLE "urls" (
	 "id" INTEGER NOT NULL,
	 "key" text,
	 "url" text NOT NULL,
	PRIMARY KEY("id")
);