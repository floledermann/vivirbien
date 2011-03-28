CREATE TABLE "openresources_area" ("id" integer PRIMARY KEY, "name_en" varchar(100), "name_de" varchar(100), "bounds" varchar(255));
INSERT INTO "openresources_area" SELECT * FROM "resources_area";

CREATE TABLE "openresources_context" ("id" integer NOT NULL PRIMARY KEY, "area_id" integer NULL);
INSERT INTO "openresources_context" SELECT * FROM "resources_context";

CREATE TABLE "openresources_icon" ("creator_id" integer NULL, "image" varchar(100), "id" integer PRIMARY KEY, "name" varchar(100));
INSERT INTO "openresources_icon" SELECT * FROM "resources_icon";

CREATE TABLE "openresources_resource" ("name" varchar(200), "end_date" datetime, "template_id" integer NULL, "featured" bool, "creation_date" datetime, "creator_id" integer, "protected" bool, "start_date" datetime, "shortname" varchar(200) UNIQUE, "id" integer PRIMARY KEY);
INSERT INTO "openresources_resource" SELECT * FROM "resources_resource";

CREATE TABLE "openresources_resourcetemplate" ("featured" bool, "description_en" text, "id" integer PRIMARY KEY, "name_de" varchar(255), "shortname" varchar(100) UNIQUE, "creator_id" integer NULL, "description_de" text, "creation_date" datetime, "name_en" varchar(255));
INSERT INTO "openresources_resourcetemplate" SELECT * FROM "resources_resourcetemplate";

CREATE TABLE "openresources_tag" ("value_date" datetime, "resource_id" integer, "value" text, "creation_date" datetime, "creator_id" integer, "key" varchar(100), "value_relation_id" integer NULL, "id" integer PRIMARY KEY);
INSERT INTO "openresources_tag" SELECT * FROM "resources_tag";

CREATE TABLE "openresources_tagmapping" ("subicon" bool, "icon_id" integer NULL, "view_id" integer, "value" varchar(100), "id" integer PRIMARY KEY, "order" integer, "creator_id" integer, "key" varchar(100), "creation_date" datetime, "show_in_list" bool);
INSERT INTO "openresources_tagmapping" SELECT * FROM "resources_tagmapping";

CREATE TABLE "openresources_tagquery" ("comparison" integer, "view_id" integer, "value" varchar(100), "id" integer PRIMARY KEY, "creator_id" integer, "boolean" integer, "key" varchar(100), "exclude" bool, "creation_date" datetime NULL, "order" integer);
INSERT INTO "openresources_tagquery" SELECT * FROM "resources_tagquery";

CREATE TABLE "openresources_tagtemplate" ("group_id" integer, "multiple" bool, "name_de" varchar(255), "value" text, "template_id" integer, "creator_id" integer NULL, "key" varchar(100), "id" integer PRIMARY KEY, "name_en" varchar(255), "creation_date" datetime, "order" integer);
INSERT INTO "openresources_tagtemplate" SELECT * FROM "resources_tagtemplate";

CREATE TABLE "openresources_tagtemplategroup" ("template_id" integer, "name_de" varchar(255), "id" integer PRIMARY KEY, "creator_id" integer NULL, "name_en" varchar(255), "creation_date" datetime, "order" integer);
INSERT INTO "openresources_tagtemplategroup" SELECT * FROM "resources_tagtemplategroup";

CREATE TABLE "openresources_userprofile" ("id" integer NOT NULL PRIMARY KEY, "user_id" integer NOT NULL UNIQUE, "context_id" integer NULL);
INSERT INTO "openresources_userprofile" SELECT * FROM "resources_userprofile";

CREATE TABLE "openresources_view" ("include_upcoming" bool, "order_by" varchar(200), "name_de" varchar(200), "creation_date" datetime, "creator_id" integer, "protected" bool, "include_current" bool, "include_past" bool, "id" integer PRIMARY KEY, "shortname" varchar(100) UNIQUE, "featured" bool, "show_map" bool NOT NULL DEFAULT True, "name_en" varchar(200));
INSERT INTO "openresources_view" SELECT * FROM "resources_view";

CREATE TABLE "openresources_view_sub_views" ("id" integer NOT NULL PRIMARY KEY, "from_view_id" integer NOT NULL, "to_view_id" integer NOT NULL);
INSERT INTO "openresources_view_sub_views" SELECT * FROM "resources_view_sub_views";


