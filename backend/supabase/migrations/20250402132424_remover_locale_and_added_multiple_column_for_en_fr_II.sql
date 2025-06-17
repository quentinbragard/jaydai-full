alter table "public"."prompt_templates" drop column "title";

alter table "public"."prompt_templates" add column "title_custom" text;

alter table "public"."prompt_templates" add column "title_en" text;

alter table "public"."prompt_templates" add column "title_fr" text;


