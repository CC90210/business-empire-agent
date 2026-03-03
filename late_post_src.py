    def create(
        self,
        *,
        content: str,
        platforms: list[dict[str, Any]],
        title: str | None = None,
        media_items: list[dict[str, Any]] | None = None,
        scheduled_for: datetime | str | None = None,
        publish_now: bool = False,
        is_draft: bool = False,
        timezone: str = "UTC",
        tags: list[str] | None = None,
        hashtags: list[str] | None = None,
        mentions: list[str] | None = None,
        crossposting_enabled: bool = True,
        metadata: dict[str, Any] | None = None,
        tiktok_settings: dict[str, Any] | None = None,
        queued_from_profile: str | None = None,
    ) -> PostCreateResponse:
        """
        Create a new post.

        Args:
            content: Post content/text
            platforms: List of platform targets, each with 'platform' and 'accountId'.
                       Can include 'customContent', 'customMedia', 'scheduledFor',
                       and 'platformSpecificData' for per-platform overrides.
            title: Optional title (used by YouTube, Pinterest)
            media_items: Optional list of media items with 'type' and 'url'
            scheduled_for: When to publish (datetime or ISO string)
            publish_now: If True, publish immediately (default: False)
            is_draft: If True, save as draft (default: False)
            timezone: Timezone for scheduled_for (default: UTC)
            tags: Optional tags (for YouTube: max 100 chars each, 500 total)
            hashtags: Optional hashtags
            mentions: Optional mentions
            crossposting_enabled: Enable crossposting (default: True)
            metadata: Optional custom metadata
            tiktok_settings: TikTok-specific settings (required for TikTok posts)
            queued_from_profile: Profile ID if creating via queue

        Returns:
            PostCreateResponse with 'message' and 'post' attributes
        """
        payload = self._build_payload(
            content=content,
            platforms=platforms,
            title=title,
            media_items=media_items,
            scheduled_for=scheduled_for,
            publish_now=publish_now if publish_now else None,
            is_draft=is_draft if is_draft else None,
            timezone=timezone,
            tags=tags,
            hashtags=hashtags,
            mentions=mentions,
            crossposting_enabled=crossposting_enabled
            if not crossposting_enabled
            else None,
            metadata=metadata,
            tiktok_settings=tiktok_settings,
            queued_from_profile=queued_from_profile,
        )
        data = self._client._post(self._BASE_PATH, data=payload)
        return PostCreateResponse.model_validate(data)
