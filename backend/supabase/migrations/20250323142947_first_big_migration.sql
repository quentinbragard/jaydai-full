alter table "public"."prompt_templates" drop constraint "official_prompt_templates_folder_id_fkey";

alter table "public"."official_folders" drop column "path";

alter table "public"."official_folders" add column "name" text;

alter table "public"."organization_folders" add column "locale" text;

alter table "public"."organization_folders" add column "name" text;

alter table "public"."prompt_templates" add column "last_used_at" timestamp with time zone;

alter table "public"."prompt_templates" add column "path" text;

alter table "public"."prompt_templates" add column "type" text;

alter table "public"."prompt_templates" add column "usage_count" bigint;

alter table "public"."user_folders" add column "description" text;

alter table "public"."user_folders" add column "locale" text;

alter table "public"."user_folders" add column "name" text;

alter table "public"."users_metadata" drop column "additional_emails";

alter table "public"."users_metadata" drop column "additional_organizations";

alter table "public"."users_metadata" add column "additional_email" text;

alter table "public"."users_metadata" add column "additional_organization" text;

alter table "public"."users_metadata" add column "organization_id" uuid;

alter table "public"."users_metadata" add constraint "users_metadata_organization_id_fkey" FOREIGN KEY (organization_id) REFERENCES organizations(id) not valid;

alter table "public"."users_metadata" validate constraint "users_metadata_organization_id_fkey";

create policy "Enable insert for users based on user_id"
on "public"."chats"
as permissive
for insert
to authenticated
with check ((( SELECT auth.uid() AS uid) = user_id));


create policy "Enable read for users based on user_id"
on "public"."chats"
as permissive
for select
to authenticated
using ((( SELECT auth.uid() AS uid) = user_id));


create policy "Enable insert for users based on user_id"
on "public"."messages"
as permissive
for insert
to authenticated
with check ((( SELECT auth.uid() AS uid) = user_id));


create policy "Enable read for users based on user_id"
on "public"."messages"
as permissive
for select
to authenticated
using ((( SELECT auth.uid() AS uid) = user_id));


create policy "Enable insert for service role only"
on "public"."notifications"
as permissive
for insert
to service_role
with check (true);


create policy "Enable read for users based on user_id"
on "public"."notifications"
as permissive
for select
to authenticated
using ((( SELECT auth.uid() AS uid) = user_id));


create policy "Enable read access for authenticated users"
on "public"."official_folders"
as permissive
for select
to authenticated
using (true);


create policy "Enable insert for authenticated users only"
on "public"."prompt_templates"
as permissive
for insert
to authenticated
with check (true);


create policy "Enable read for authenticated users only"
on "public"."prompt_templates"
as permissive
for select
to authenticated
using (true);


create policy "Enable insert for users based on user_id"
on "public"."user_folders"
as permissive
for insert
to authenticated
with check ((( SELECT auth.uid() AS uid) = user_id));


create policy "Enable read for users based on user_id"
on "public"."user_folders"
as permissive
for select
to authenticated
using ((( SELECT auth.uid() AS uid) = user_id));


create policy "Enable insert for service role only"
on "public"."users_metadata"
as permissive
for insert
to public
with check (true);


create policy "Enable read for users based on user_id"
on "public"."users_metadata"
as permissive
for select
to authenticated
using ((( SELECT auth.uid() AS uid) = user_id));



