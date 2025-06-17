alter table "public"."official_folders" drop column "locale";

alter table "public"."official_folders" drop column "name";

alter table "public"."official_folders" add column "name_en" text;

alter table "public"."official_folders" add column "name_fr" text;

alter table "public"."organization_folders" drop column "locale";

alter table "public"."organization_folders" drop column "name";

alter table "public"."organization_folders" add column "name_en" text;

alter table "public"."organization_folders" add column "name_fr" text;

alter table "public"."prompt_templates" drop column "content";

alter table "public"."prompt_templates" drop column "locale";

alter table "public"."prompt_templates" add column "content_custom" text;

alter table "public"."prompt_templates" add column "content_en" text;

alter table "public"."prompt_templates" add column "content_fr" text;


