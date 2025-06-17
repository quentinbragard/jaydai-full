alter table "public"."users_metadata" add column "linkedin_headline" text;

alter table "public"."users_metadata" add column "linkedin_id" text;

alter table "public"."users_metadata" add column "linkedin_profile_url" text;

CREATE INDEX idx_users_metadata_linkedin_id ON public.users_metadata USING btree (linkedin_id);


