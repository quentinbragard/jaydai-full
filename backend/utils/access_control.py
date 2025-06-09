from supabase import Client


def get_user_metadata(supabase: Client, user_id: str) -> dict:
    """Fetch organization_ids and company_id for a user."""
    response = (
        supabase.table("users_metadata")
        .select("organization_ids, company_id")
        .eq("user_id", user_id)
        .single()
        .execute()
    )
    return response.data or {}


def get_access_conditions(supabase: Client, user_id: str) -> list[str]:
    """Build OR conditions to filter records accessible by the user."""
    metadata = get_user_metadata(supabase, user_id)
    conditions = [f"user_id.eq.{user_id}"]
    conditions.append(
        "user_id.is.null,company_id.is.null,organization_id.is.null"
    )

    company_id = metadata.get("company_id")
    if company_id:
        conditions.append(f"company_id.eq.{company_id}")

    for org_id in metadata.get("organization_ids", []) or []:
        conditions.append(f"organization_id.eq.{org_id}")

    return conditions


def apply_access_conditions(query, supabase: Client, user_id: str):
    """Apply user access filters to a Supabase query."""
    conditions = get_access_conditions(supabase, user_id)
    if conditions:
        query = query.or_(",".join(conditions))
    return query
