from pydantic import BaseModel, Field, computed_field


class ModerationResult(BaseModel):

    rationale: str = Field(description="Explanation of what was harmful and why")
    contains_pii: bool = Field(
        default=False,
        description="Whether the content contains any personally-identifiable information (PII)",
    )
    is_unfriendly: bool = Field(default=False, description="Whether unfriendly tone or content was detected")
    is_unprofessional: bool = Field(default=False, description="Whether unprofessional tone or content was detected")

    @computed_field
    @property
    def is_flagged(self) -> bool:
        """True if any of the core moderation flags tripped."""
        return any([self.contains_pii, self.is_unfriendly, self.is_unprofessional])


class TextModerationResult(ModerationResult):
    pass


class ImageModerationResult(ModerationResult):

    is_disturbing: bool = Field(default=False, description="Whether the image is disturbing")
    is_low_quality: bool = Field(default=False, description="Whether the image is low quality")

    @computed_field
    @property
    def is_flagged(self) -> bool:
        """True if any base flag or any image-specific flag tripped."""
        return super().is_flagged or self.is_disturbing or self.is_low_quality


class VideoModerationResult(ModerationResult):

    is_disturbing: bool = Field(default=False, description="Whether the video is disturbing")
    is_low_quality: bool = Field(default=False, description="Whether the video is low quality")

    @computed_field
    @property
    def is_flagged(self) -> bool:
        """True if any base flag or any video-specific flag tripped."""
        return super().is_flagged or self.is_disturbing or self.is_low_quality


class AudioModerationResult(ModerationResult):

    transcription: str = Field(description="Transcription of the audio content")