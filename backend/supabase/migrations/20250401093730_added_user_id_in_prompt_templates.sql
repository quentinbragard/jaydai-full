alter table "public"."official_folders" add column "locale" text;

alter table "public"."prompt_templates" add column "user_id" uuid;

alter table "public"."prompt_templates" add constraint "prompt_templates_user_id_fkey" FOREIGN KEY (user_id) REFERENCES auth.users(id) not valid;

alter table "public"."prompt_templates" validate constraint "prompt_templates_user_id_fkey";


