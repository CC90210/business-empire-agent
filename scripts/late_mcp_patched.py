"""
Late MCP Server - Patched Version.

This is a local patched copy that fixes Pydantic model vs dict access
mismatches in the Late SDK's MCP server. The SDK returns Pydantic BaseModel
objects from resource methods, but the original server.py called .get() on
them as if they were dicts.

This file is used by scripts/late-mcp-wrapper.cmd instead of the packaged
server module, ensuring our fixes persist across SDK reinstalls.

Fix summary:
  - _safe_dump(): converts Pydantic models to dicts via .model_dump()
  - _get_accounts_as_dicts(): safely gets accounts with raw HTTP fallback
  - _get_posts_as_dicts(): safely gets posts with raw HTTP fallback
  - All .get() calls go through safe dict access, never raw Pydantic attrs
"""

from __future__ import annotations

import os
import sys
from datetime import datetime, timedelta

# Ensure late-sdk is importable (uvx environment)
from mcp.server.fastmcp import FastMCP

from late import Late, MediaType, PostStatus

# Initialize MCP server
mcp = FastMCP(
    "Late",
    instructions="""
Late API server for scheduling social media posts.

Available tools are prefixed by resource:
- accounts_* : Manage connected social media accounts
- profiles_* : Manage profiles (groups of accounts)
- posts_*    : Create, list, update, delete posts
- media_*    : Upload images and videos
""",
)


def _get_client() -> Late:
    """Get Late client with API key from environment."""
    api_key = os.getenv("LATE_API_KEY", "")
    if not api_key:
        raise ValueError("LATE_API_KEY environment variable is required")
    base_url = os.getenv("LATE_BASE_URL", None)
    return Late(api_key=api_key, base_url=base_url)


def _safe_dump(response) -> dict:
    """Convert a Pydantic model or dict to a plain dict."""
    if hasattr(response, "model_dump"):
        return response.model_dump(by_alias=True)
    if isinstance(response, dict):
        return response
    return {}


def _get_accounts_as_dicts(client: Late) -> list[dict]:
    """Get accounts as plain dicts, with raw HTTP fallback."""
    try:
        response = client.accounts.list()
        data = _safe_dump(response)
        return data.get("accounts", [])
    except Exception:
        try:
            raw = client._get("/v1/accounts")
            if isinstance(raw, dict):
                return raw.get("accounts", [])
            return []
        except Exception:
            return []


def _get_posts_as_dicts(client: Late, **kwargs) -> list[dict]:
    """Get posts as plain dicts, with raw HTTP fallback."""
    try:
        response = client.posts.list(**kwargs)
        data = _safe_dump(response)
        return data.get("posts", [])
    except Exception:
        try:
            params = {}
            if "limit" in kwargs:
                params["limit"] = kwargs["limit"]
            if "status" in kwargs and kwargs["status"]:
                s = kwargs["status"]
                params["status"] = s.value if hasattr(s, "value") else str(s)
            raw = client._get("/v1/posts", params=params)
            if isinstance(raw, dict):
                return raw.get("posts", [])
            return []
        except Exception:
            return []


def _safe_platform_name(target) -> str:
    """Extract platform name from a target dict or Pydantic model."""
    if isinstance(target, dict):
        return target.get("platform") or "?"
    if hasattr(target, "platform"):
        return target.platform or "?"
    return "?"


def _get_id(obj: dict) -> str:
    """Get the ID from an object that might use _id or field_id."""
    return obj.get("_id") or obj.get("field_id") or "unknown"


# ============================================================================
# ACCOUNTS
# ============================================================================


@mcp.tool()
def accounts_list() -> str:
    """
    List all connected social media accounts.

    Returns the platform, username, and account ID for each connected account.
    """
    client = _get_client()
    accounts = _get_accounts_as_dicts(client)

    if not accounts:
        return "No accounts connected. Connect accounts at https://getlate.dev"

    lines = [f"Found {len(accounts)} connected account(s):\n"]
    for acc in accounts:
        aid = _get_id(acc)
        username = acc.get("username") or acc.get("displayName") or acc.get("name") or aid
        platform = acc.get("platform") or "unknown"
        lines.append(f"- {platform}: {username} (ID: {aid})")

    return "\n".join(lines)


@mcp.tool()
def accounts_get(platform: str) -> str:
    """
    Get account details for a specific platform.

    Args:
        platform: Platform name (twitter, instagram, linkedin, tiktok, bluesky, facebook, youtube, pinterest, threads)
    """
    client = _get_client()
    accounts = _get_accounts_as_dicts(client)

    matching = [a for a in accounts if (a.get("platform") or "").lower() == platform.lower()]
    if not matching:
        available = list({a.get("platform", "?") for a in accounts})
        return f"No {platform} account found. Available: {', '.join(available)}"

    acc = matching[0]
    return f"Platform: {acc.get('platform')}\nUsername: {acc.get('username', 'N/A')}\nID: {_get_id(acc)}"


# ============================================================================
# PROFILES
# ============================================================================


@mcp.tool()
def profiles_list() -> str:
    """
    List all profiles.

    Profiles group multiple social accounts together for easier management.
    """
    client = _get_client()
    data = _safe_dump(client.profiles.list())
    profiles = data.get("profiles", [])

    if not profiles:
        return "No profiles found."

    lines = [f"Found {len(profiles)} profile(s):\n"]
    for p in profiles:
        default = " (default)" if p.get("isDefault") else ""
        color = f" [{p.get('color', '')}]" if p.get("color") else ""
        lines.append(f"- {p.get('name', 'Unnamed')}{default}{color} (ID: {_get_id(p)})")
        if p.get("description"):
            lines.append(f"  Description: {p['description']}")

    return "\n".join(lines)


@mcp.tool()
def profiles_get(profile_id: str) -> str:
    """
    Get details of a specific profile.

    Args:
        profile_id: The profile ID
    """
    client = _get_client()
    data = _safe_dump(client.profiles.get(profile_id))
    profile = data.get("profile", data)

    lines = [
        f"Name: {profile.get('name', 'N/A')}",
        f"ID: {_get_id(profile)}",
        f"Default: {'Yes' if profile.get('isDefault') else 'No'}",
    ]
    if profile.get("description"):
        lines.append(f"Description: {profile['description']}")
    if profile.get("color"):
        lines.append(f"Color: {profile['color']}")
    return "\n".join(lines)


@mcp.tool()
def profiles_create(name: str, description: str = "", color: str = "") -> str:
    """
    Create a new profile.

    Args:
        name: Profile name (required)
        description: Optional description
        color: Optional hex color (e.g., '#4CAF50')
    """
    client = _get_client()
    params = {"name": name}
    if description:
        params["description"] = description
    if color:
        params["color"] = color

    data = _safe_dump(client.profiles.create(**params))
    profile = data.get("profile", {})
    return f"✅ Profile created!\nName: {profile.get('name')}\nID: {_get_id(profile)}"


@mcp.tool()
def profiles_update(
    profile_id: str,
    name: str = "",
    description: str = "",
    color: str = "",
    is_default: bool = False,
) -> str:
    """
    Update an existing profile.

    Args:
        profile_id: The profile ID to update
        name: New name (leave empty to keep current)
        description: New description (leave empty to keep current)
        color: New hex color (leave empty to keep current)
        is_default: Set as default profile
    """
    client = _get_client()
    params = {}
    if name:
        params["name"] = name
    if description:
        params["description"] = description
    if color:
        params["color"] = color
    if is_default:
        params["is_default"] = True
    if not params:
        return "⚠️ No changes specified."

    data = _safe_dump(client.profiles.update(profile_id, **params))
    profile = data.get("profile", {})
    return f"✅ Profile updated!\nName: {profile.get('name')}\nID: {_get_id(profile)}"


@mcp.tool()
def profiles_delete(profile_id: str) -> str:
    """
    Delete a profile.

    Note: Profile must have no connected accounts.

    Args:
        profile_id: The profile ID to delete
    """
    client = _get_client()
    client.profiles.delete(profile_id)
    return f"✅ Profile {profile_id} deleted"


# ============================================================================
# POSTS
# ============================================================================


@mcp.tool()
def posts_list(status: str = "", limit: int = 10) -> str:
    """
    List posts with optional filtering.

    Args:
        status: Filter by status (scheduled, published, failed, draft). Empty for all.
        limit: Maximum number of posts to return (default 10)
    """
    client = _get_client()
    kwargs = {"limit": limit}
    if status:
        kwargs["status"] = status
    posts = _get_posts_as_dicts(client, **kwargs)

    if not posts:
        return f"No posts found{f' with status {status}' if status else ''}."

    lines = [f"Found {len(posts)} post(s):\n"]
    for post in posts:
        content = post.get("content") or ""
        preview = content[:60] + "..." if len(content) > 60 else content
        plats = ", ".join(_safe_platform_name(t) for t in (post.get("platforms") or []))
        st = post.get("status") or "unknown"
        if hasattr(st, "value"):
            st = st.value
        lines.append(f"- [{st}] {preview}")
        lines.append(f"  Platforms: {plats} | ID: {_get_id(post)}")

    return "\n".join(lines)


@mcp.tool()
def posts_get(post_id: str) -> str:
    """
    Get details of a specific post by ID.

    Args:
        post_id: The post ID to retrieve
    """
    client = _get_client()
    try:
        data = _safe_dump(client.posts.get(post_id))
        post = data.get("post", data)
    except Exception:
        try:
            raw = client._get(f"/v1/posts/{post_id}")
            post = raw.get("post", raw) if isinstance(raw, dict) else raw
        except Exception as e:
            return f"❌ Could not fetch post {post_id}: {e}"

    content = post.get("content") or ""
    preview = content[:100] + "..." if len(content) > 100 else content
    plats = ", ".join(_safe_platform_name(t) for t in (post.get("platforms") or []))
    st = post.get("status") or "unknown"
    if hasattr(st, "value"):
        st = st.value

    lines = [
        f"Post ID: {_get_id(post)}",
        f"Status: {st}",
        f"Platforms: {plats}",
        f"Content: {preview}",
    ]
    if post.get("scheduledFor"):
        lines.append(f"Scheduled for: {post['scheduledFor']}")
    if post.get("publishedAt"):
        lines.append(f"Published at: {post['publishedAt']}")
    if post.get("error"):
        lines.append(f"Error: {post['error']}")
    return "\n".join(lines)


@mcp.tool()
def posts_create(
    content: str,
    platform: str,
    is_draft: bool = False,
    publish_now: bool = False,
    schedule_minutes: int = 0,
    media_urls: str = "",
    title: str = "",
) -> str:
    """
    Create a new social media post, optionally with media.

    Scheduling behavior:
    - is_draft=True: Save as draft (no scheduling, can edit later)
    - publish_now=True: Publish immediately
    - Neither: Schedule for schedule_minutes from now (default: 60 min)

    Args:
        content: The post content/text
        platform: Target platform (twitter, instagram, linkedin, tiktok, bluesky, facebook, youtube, pinterest, threads)
        is_draft: Save as draft without scheduling (default: False)
        publish_now: Publish immediately instead of scheduling (default: False)
        schedule_minutes: Minutes from now to schedule (ignored if publish_now=True or is_draft=True). Default 60 min.
        media_urls: Comma-separated URLs of media files to attach. Optional.
        title: Optional title (required for YouTube, recommended for Pinterest)
    """
    client = _get_client()

    accounts = _get_accounts_as_dicts(client)
    matching = [a for a in accounts if (a.get("platform") or "").lower() == platform.lower()]
    if not matching:
        available = list({a.get("platform", "?") for a in accounts})
        return f"No {platform} account connected. Available platforms: {', '.join(available)}"

    account = matching[0]
    account_id = _get_id(account)

    params = {
        "content": content,
        "platforms": [{"platform": account.get("platform"), "accountId": account_id}],
    }
    if title:
        params["title"] = title

    if media_urls:
        urls = [u.strip() for u in media_urls.split(",") if u.strip()]
        media_items = []
        for url in urls:
            mt = MediaType.IMAGE
            if any(ext in url.lower() for ext in [".mp4", ".mov", ".avi", ".webm", ".m4v"]):
                mt = MediaType.VIDEO
            elif ".gif" in url.lower():
                mt = MediaType.GIF
            media_items.append({"type": mt, "url": url})
        params["media_items"] = media_items

    if is_draft:
        params["is_draft"] = True
    elif publish_now:
        params["publish_now"] = True
    else:
        minutes = schedule_minutes if schedule_minutes > 0 else 60
        params["scheduled_for"] = datetime.now() + timedelta(minutes=minutes)

    # Use raw HTTP to avoid Pydantic PostCreateResponse validation bug
    # (accountId comes back as a dict from the API, but Pydantic expects a string)
    try:
        # Build raw payload for HTTP POST
        raw_payload = {
            "content": content,
            "platforms": [{"platform": account.get("platform"), "accountId": account_id}],
        }
        if title:
            raw_payload["title"] = title
        if is_draft:
            raw_payload["isDraft"] = True
        elif publish_now:
            raw_payload["publishNow"] = True
        elif "scheduled_for" in params:
            raw_payload["scheduledFor"] = params["scheduled_for"].isoformat()
        if media_urls:
            urls_list = [u.strip() for u in media_urls.split(",") if u.strip()]
            raw_media = []
            for url in urls_list:
                mtype = "image"
                if any(ext in url.lower() for ext in [".mp4", ".mov", ".avi", ".webm", ".m4v"]):
                    mtype = "video"
                elif ".gif" in url.lower():
                    mtype = "gif"
                raw_media.append({"type": mtype, "url": url})
            raw_payload["mediaItems"] = raw_media

        raw_response = client._post("/v1/posts", json=raw_payload)
        if isinstance(raw_response, dict):
            post = raw_response.get("post", raw_response)
        else:
            post = _safe_dump(raw_response).get("post", {})
    except Exception as e:
        # Fallback: try SDK method anyway
        try:
            response = client.posts.create(**params)
            data = _safe_dump(response)
            post = data.get("post", {})
        except Exception as e2:
            return f"❌ Failed to create post: {e2}"

    username = account.get("username") or account.get("displayName") or account.get("name") or account_id
    media_info = f" with {len(params.get('media_items', []))} media file(s)" if params.get("media_items") else ""
    pid = post.get("_id") or post.get("field_id") or "N/A"

    if is_draft:
        return f"📝 Draft saved for {platform} (@{username}){media_info}\nPost ID: {pid}\nStatus: draft"
    elif publish_now:
        return f"✅ Published to {platform} (@{username}){media_info}\nPost ID: {pid}"
    else:
        scheduled = params["scheduled_for"].strftime("%Y-%m-%d %H:%M")
        return f"✅ Scheduled for {platform} (@{username}){media_info}\nPost ID: {pid}\nScheduled: {scheduled}"


@mcp.tool()
def posts_publish_now(content: str, platform: str, media_urls: str = "") -> str:
    """
    Publish a post immediately to a platform.

    Args:
        content: The post content/text
        platform: Target platform (twitter, instagram, linkedin, tiktok, bluesky, etc.)
        media_urls: Comma-separated URLs of media files to attach. Optional.
    """
    return posts_create(content=content, platform=platform, publish_now=True, media_urls=media_urls)


@mcp.tool()
def posts_cross_post(
    content: str,
    platforms: str,
    is_draft: bool = False,
    publish_now: bool = False,
    media_urls: str = "",
) -> str:
    """
    Post the same content to multiple platforms at once.

    Scheduling behavior:
    - is_draft=True: Save as draft (no scheduling, can edit later)
    - publish_now=True: Publish immediately
    - Neither: Schedule for 1 hour from now

    Args:
        content: The post content/text
        platforms: Comma-separated list of platforms (e.g., "twitter,linkedin,bluesky")
        is_draft: Save as draft without scheduling (default: False)
        publish_now: Publish immediately instead of scheduling (default: False)
        media_urls: Comma-separated URLs of media files to attach. Optional.
    """
    client = _get_client()
    target_platforms = [p.strip().lower() for p in platforms.split(",")]
    accounts = _get_accounts_as_dicts(client)

    platform_targets = []
    not_found = []

    for plat in target_platforms:
        match = [a for a in accounts if (a.get("platform") or "").lower() == plat]
        if match:
            acc = match[0]
            platform_targets.append({"platform": acc.get("platform"), "accountId": _get_id(acc)})
        else:
            not_found.append(plat)

    if not platform_targets:
        available = list({a.get("platform", "?") for a in accounts})
        return f"No matching accounts found. Available: {', '.join(available)}"

    params = {"content": content, "platforms": platform_targets}

    if media_urls:
        urls = [u.strip() for u in media_urls.split(",") if u.strip()]
        media_items = []
        for url in urls:
            mt = MediaType.IMAGE
            if any(ext in url.lower() for ext in [".mp4", ".mov", ".avi", ".webm", ".m4v"]):
                mt = MediaType.VIDEO
            elif ".gif" in url.lower():
                mt = MediaType.GIF
            media_items.append({"type": mt, "url": url})
        params["media_items"] = media_items

    if is_draft:
        params["is_draft"] = True
    elif publish_now:
        params["publish_now"] = True
    else:
        params["scheduled_for"] = datetime.now() + timedelta(hours=1)

    # Use raw HTTP to avoid Pydantic PostCreateResponse validation bug
    try:
        raw_payload = {
            "content": content,
            "platforms": platform_targets,
        }
        if is_draft:
            raw_payload["isDraft"] = True
        elif publish_now:
            raw_payload["publishNow"] = True
        elif "scheduled_for" in params:
            raw_payload["scheduledFor"] = params["scheduled_for"].isoformat()
        if media_urls:
            urls_list = [u.strip() for u in media_urls.split(",") if u.strip()]
            raw_media = []
            for url in urls_list:
                mtype = "image"
                if any(ext in url.lower() for ext in [".mp4", ".mov", ".avi", ".webm", ".m4v"]):
                    mtype = "video"
                elif ".gif" in url.lower():
                    mtype = "gif"
                raw_media.append({"type": mtype, "url": url})
            raw_payload["mediaItems"] = raw_media

        raw_response = client._post("/v1/posts", json=raw_payload)
        if isinstance(raw_response, dict):
            post = raw_response.get("post", raw_response)
        else:
            post = _safe_dump(raw_response).get("post", {})
    except Exception as e:
        try:
            response = client.posts.create(**params)
            data = _safe_dump(response)
            post = data.get("post", {})
        except Exception as e2:
            return f"❌ Failed to create cross-post: {e2}"

    posted_to = [t["platform"] for t in platform_targets]
    media_info = f" with {len(params.get('media_items', []))} media file(s)" if params.get("media_items") else ""
    pid = post.get("_id") or post.get("field_id") or "N/A"

    if is_draft:
        result = f"📝 Draft saved for: {', '.join(posted_to)}{media_info}\nPost ID: {pid}\nStatus: draft"
    else:
        result = f"✅ {'Published' if publish_now else 'Scheduled'} to: {', '.join(posted_to)}{media_info}\nPost ID: {pid}"

    if not_found:
        result += f"\n⚠️ Accounts not found for: {', '.join(not_found)}"
    return result


@mcp.tool()
def posts_update(
    post_id: str,
    content: str = "",
    scheduled_for: str = "",
    title: str = "",
) -> str:
    """
    Update an existing post.

    Only draft, scheduled, and failed posts can be updated.

    Args:
        post_id: The post ID to update
        content: New content (leave empty to keep current)
        scheduled_for: New schedule time as ISO string (leave empty to keep current)
        title: New title (leave empty to keep current)
    """
    client = _get_client()
    params = {}
    if content:
        params["content"] = content
    if scheduled_for:
        params["scheduled_for"] = scheduled_for
    if title:
        params["title"] = title
    if not params:
        return "⚠️ No changes specified."

    try:
        data = _safe_dump(client.posts.update(post_id, **params))
        post = data.get("post", {})
    except Exception as e:
        return f"❌ Failed to update post: {e}"

    st = post.get("status") or "unknown"
    if hasattr(st, "value"):
        st = st.value
    return f"✅ Post updated!\nID: {_get_id(post)}\nStatus: {st}"


@mcp.tool()
def posts_delete(post_id: str) -> str:
    """
    Delete a post by ID.

    Published posts cannot be deleted.

    Args:
        post_id: The post ID to delete
    """
    client = _get_client()
    client.posts.delete(post_id)
    return f"✅ Post {post_id} deleted"


@mcp.tool()
def posts_retry(post_id: str) -> str:
    """
    Retry a failed post.

    Args:
        post_id: The ID of the failed post to retry
    """
    client = _get_client()
    try:
        data = _safe_dump(client.posts.get(post_id))
        post = data.get("post", data)
        st = post.get("status")
        if hasattr(st, "value"):
            st = st.value
        if st != "failed":
            return f"⚠️ Post {post_id} is not in failed status (current: {st})"
    except Exception as e:
        return f"❌ Could not find post {post_id}: {e}"

    try:
        client.posts.retry(post_id)
        return f"✅ Post {post_id} has been queued for retry"
    except Exception as e:
        return f"❌ Failed to retry post: {e}"


@mcp.tool()
def posts_list_failed(limit: int = 10) -> str:
    """
    List all failed posts that can be retried.

    Args:
        limit: Maximum number of posts to return (default 10)
    """
    client = _get_client()
    posts = _get_posts_as_dicts(client, status=PostStatus.FAILED, limit=limit)

    if not posts:
        return "No failed posts found."

    lines = [f"Found {len(posts)} failed post(s):\n"]
    for post in posts:
        content = post.get("content") or ""
        preview = content[:50] + "..." if len(content) > 50 else content
        plats = ", ".join(_safe_platform_name(t) for t in (post.get("platforms") or []))
        lines.append(f"- {preview}")
        lines.append(f"  Platforms: {plats} | ID: {_get_id(post)}")
        lines.append(f"  Error: {post.get('error', 'Unknown error')}")
        lines.append("")
    return "\n".join(lines)


@mcp.tool()
def posts_retry_all_failed() -> str:
    """
    Retry all failed posts.
    """
    client = _get_client()
    posts = _get_posts_as_dicts(client, status=PostStatus.FAILED, limit=50)

    if not posts:
        return "No failed posts to retry."

    results = []
    success_count = 0
    fail_count = 0

    for post in posts:
        pid = _get_id(post)
        try:
            client.posts.retry(pid)
            success_count += 1
        except Exception as e:
            fail_count += 1
            results.append(f"❌ {pid}: {e}")

    summary = f"✅ Retried {success_count} post(s)"
    if fail_count > 0:
        summary += f"\n❌ Failed to retry {fail_count} post(s)"
        summary += "\n" + "\n".join(results)
    return summary


# ============================================================================
# MEDIA UPLOAD
# ============================================================================


@mcp.tool()
def media_generate_upload_link() -> str:
    """
    Generate a unique upload URL for the user to upload files via browser.

    Use this when the user wants to include images or videos in their post.
    The flow is:
    1. Call this tool to get an upload URL
    2. Ask the user to open the URL in their browser
    3. User uploads files through the web interface
    4. Call media_check_upload_status to get the uploaded file URLs
    5. Use those URLs when creating the post with posts_create

    Returns:
        Upload URL and token for the user to open in browser
    """
    client = _get_client()
    try:
        response = client.media.generate_upload_token()
        data = _safe_dump(response)
        return f"""📤 Upload link generated!

**Open this link in your browser to upload files:**
{data.get("uploadUrl", "")}

Token: {data.get("token", "")}
Expires: {data.get("expiresAt", "")}

Once you've uploaded your files, let me know and I'll check the status to get the URLs."""
    except Exception as e:
        return f"❌ Failed to generate upload link: {e}"


@mcp.tool()
def media_check_upload_status(token: str) -> str:
    """
    Check the status of an upload token and get uploaded file URLs.

    Use this after the user has uploaded files through the browser upload page.

    Args:
        token: The upload token from media_generate_upload_link

    Returns:
        Status and uploaded file URLs if completed
    """
    client = _get_client()
    try:
        response = client.media.check_upload_token(token)
        data = _safe_dump(response)

        status = data.get("status", "unknown")
        if hasattr(status, "value"):
            status = status.value
        files = data.get("files", [])

        if status == "pending":
            return f"⏳ Upload pending\n\nThe user hasn't uploaded files yet.\nToken: {token}"
        elif status == "expired":
            return "⏰ Upload link expired. Use media_generate_upload_link to create a new one."
        elif status == "completed":
            if not files:
                return "✅ Upload completed but no files were found."
            lines = [f"✅ Upload completed! {len(files)} file(s) uploaded:\n"]
            media_urls = []
            for f in files:
                url = str(f.get("url", ""))
                media_urls.append(url)
                lines.append(f"- {f.get('filename', 'unknown')}")
                lines.append(f"  Type: {f.get('type', 'N/A')}")
                lines.append(f"  URL: {url}")
                size = f.get("size", 0) or 0
                lines.append(f"  Size: {size / 1024:.1f} KB")
                lines.append("")
            lines.append("📝 Use these URLs with posts_create media_urls parameter.")
            lines.append(f"\nMedia URLs: {','.join(media_urls)}")
            return "\n".join(lines)
        else:
            return f"Unknown status: {status}"
    except Exception as e:
        return f"❌ Failed to check upload status: {e}"


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    mcp.run()
