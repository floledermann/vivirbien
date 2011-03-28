CREATE TABLE "openresources_area" (LIKE resources_area INCLUDING DEFAULTS INCLUDING CONSTRAINTS INCLUDING INDEXES);
CREATE TABLE "openresources_context" (LIKE "resources_context" INCLUDING DEFAULTS INCLUDING CONSTRAINTS INCLUDING INDEXES);
CREATE TABLE "openresources_icon" (LIKE "resources_icon" INCLUDING DEFAULTS INCLUDING CONSTRAINTS INCLUDING INDEXES);
CREATE TABLE "openresources_resource" (LIKE "resources_resource" INCLUDING DEFAULTS INCLUDING CONSTRAINTS INCLUDING INDEXES);
CREATE TABLE "openresources_resourcetemplate" (LIKE "resources_resourcetemplate" INCLUDING DEFAULTS INCLUDING CONSTRAINTS INCLUDING INDEXES);
CREATE TABLE "openresources_tag" (LIKE "resources_tag" INCLUDING DEFAULTS INCLUDING CONSTRAINTS INCLUDING INDEXES);
CREATE TABLE "openresources_tagmapping" (LIKE "resources_tagmapping" INCLUDING DEFAULTS INCLUDING CONSTRAINTS INCLUDING INDEXES);
CREATE TABLE "openresources_tagquery" (LIKE "resources_tagquery" INCLUDING DEFAULTS INCLUDING CONSTRAINTS INCLUDING INDEXES);
CREATE TABLE "openresources_tagtemplate" (LIKE "resources_tagtemplate" INCLUDING DEFAULTS INCLUDING CONSTRAINTS INCLUDING INDEXES);
CREATE TABLE "openresources_tagtemplategroup" (LIKE "resources_tagtemplategroup" INCLUDING DEFAULTS INCLUDING CONSTRAINTS INCLUDING INDEXES);
CREATE TABLE "openresources_userprofile" (LIKE "resources_userprofile" INCLUDING DEFAULTS INCLUDING CONSTRAINTS INCLUDING INDEXES);
CREATE TABLE "openresources_view" (LIKE "resources_view" INCLUDING DEFAULTS INCLUDING CONSTRAINTS INCLUDING INDEXES);
CREATE TABLE "openresources_view_sub_views" (LIKE "resources_view_sub_views" INCLUDING DEFAULTS INCLUDING CONSTRAINTS INCLUDING INDEXES);

INSERT INTO "openresources_area" SELECT * FROM "resources_area";
INSERT INTO "openresources_context" SELECT * FROM "resources_context";
INSERT INTO "openresources_icon" SELECT * FROM "resources_icon";
INSERT INTO "openresources_resource" SELECT * FROM "resources_resource";
INSERT INTO "openresources_resourcetemplate" SELECT * FROM "resources_resourcetemplate";
INSERT INTO "openresources_tag" SELECT * FROM "resources_tag";
INSERT INTO "openresources_tagmapping" SELECT * FROM "resources_tagmapping";
INSERT INTO "openresources_tagquery" SELECT * FROM "resources_tagquery";
INSERT INTO "openresources_tagtemplate" SELECT * FROM "resources_tagtemplate";
INSERT INTO "openresources_tagtemplategroup" SELECT * FROM "resources_tagtemplategroup";
INSERT INTO "openresources_userprofile" SELECT * FROM "resources_userprofile";
INSERT INTO "openresources_view" SELECT * FROM "resources_view";
INSERT INTO "openresources_view_sub_views" SELECT * FROM "resources_view_sub_views";


CREATE SEQUENCE "openresources_resource_id_seq";
SELECT setval('openresources_resource_id_seq', nextval('resources_resource_id_seq'));
ALTER TABLE "openresources_resource" ALTER "id" SET DEFAULT nextval('openresources_resource_id_seq'::regclass);

CREATE SEQUENCE "openresources_tag_id_seq";
SELECT setval('openresources_tag_id_seq', nextval('resources_tag_id_seq'));
ALTER TABLE "openresources_tag" ALTER "id" SET DEFAULT nextval('openresources_tag_id_seq'::regclass);

CREATE SEQUENCE "openresources_area_id_seq";
SELECT setval('openresources_area_id_seq', nextval('resources_area_id_seq'));
ALTER TABLE "openresources_area" ALTER "id" SET DEFAULT nextval('openresources_area_id_seq'::regclass);

CREATE SEQUENCE "openresources_context_id_seq";
SELECT setval('openresources_context_id_seq', nextval('resources_context_id_seq'));
ALTER TABLE "openresources_context" ALTER "id" SET DEFAULT nextval('openresources_context_id_seq'::regclass);

CREATE SEQUENCE "openresources_icon_id_seq";
SELECT setval('openresources_icon_id_seq', nextval('resources_icon_id_seq'));
ALTER TABLE "openresources_icon" ALTER "id" SET DEFAULT nextval('openresources_icon_id_seq'::regclass);

CREATE SEQUENCE "openresources_resourcetemplate_id_seq";
SELECT setval('openresources_resourcetemplate_id_seq', nextval('resources_resourcetemplate_id_seq'));
ALTER TABLE "openresources_resourcetemplate" ALTER "id" SET DEFAULT nextval('openresources_resourcetemplate_id_seq'::regclass);

CREATE SEQUENCE "openresources_tagmapping_id_seq";
SELECT setval('openresources_tagmapping_id_seq', nextval('resources_tagmapping_id_seq'));
ALTER TABLE "openresources_tagmapping" ALTER "id" SET DEFAULT nextval('openresources_tagmapping_id_seq'::regclass);

CREATE SEQUENCE "openresources_tagquery_id_seq";
SELECT setval('openresources_tagquery_id_seq', nextval('resources_tagquery_id_seq'));
ALTER TABLE "openresources_tagquery" ALTER "id" SET DEFAULT nextval('openresources_tagquery_id_seq'::regclass);

CREATE SEQUENCE "openresources_tagtemplate_id_seq";
SELECT setval('openresources_tagtemplate_id_seq', nextval('resources_tagtemplate_id_seq'));
ALTER TABLE "openresources_tagtemplate" ALTER "id" SET DEFAULT nextval('openresources_tagtemplate_id_seq'::regclass);

CREATE SEQUENCE "openresources_tagtemplategroup_id_seq";
SELECT setval('openresources_tagtemplategroup_id_seq', nextval('resources_tagtemplategroup_id_seq'));
ALTER TABLE "openresources_tagtemplategroup" ALTER "id" SET DEFAULT nextval('openresources_tagtemplategroup_id_seq'::regclass);

CREATE SEQUENCE "openresources_userprofile_id_seq";
SELECT setval('openresources_userprofile_id_seq', nextval('resources_userprofile_id_seq'));
ALTER TABLE "openresources_userprofile" ALTER "id" SET DEFAULT nextval('openresources_userprofile_id_seq'::regclass);

CREATE SEQUENCE "openresources_view_id_seq";
SELECT setval('openresources_view_id_seq', nextval('resources_view_id_seq'));
ALTER TABLE "openresources_view" ALTER "id" SET DEFAULT nextval('openresources_view_id_seq'::regclass);

CREATE SEQUENCE "openresources_view_sub_views_id_seq";
SELECT setval('openresources_view_sub_views_id_seq', nextval('resources_view_sub_views_id_seq'));
ALTER TABLE "openresources_view_sub_views" ALTER "id" SET DEFAULT nextval('openresources_view_sub_views_id_seq'::regclass);


