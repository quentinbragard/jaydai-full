alter table "public"."blog_posts" drop column "content";

alter table "public"."blog_posts" add column "call_to_action_metadata" jsonb;

alter table "public"."blog_posts" add column "content_metadata" jsonb[];

alter table "public"."blog_posts" add column "page_metadata" jsonb;


