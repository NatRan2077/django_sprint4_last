import pytest
from django.db.models import Model
from mixer.backend.django import Mixer

from fixtures.types import CommentModelAdapterT


@pytest.fixture
def comment(
    mixer: Mixer,
    user: object,
        comment_model: type,
        comment_model_adapter: CommentModelAdapterT,
) -> CommentModelAdapterT:
    comment = mixer.blend(f"blog.{comment_model.__name__}")
    adapted = comment_model_adapter(comment)
    return adapted


@pytest.fixture
def comment_to_a_post(
    mixer: Mixer,
    post_with_published_location: Model,
        comment_model,
        comment_model_adapter: CommentModelAdapterT,
):
    comment_model_name = comment_model.__name__
    post_field_name = comment_model_adapter(comment_model).post.field.name
    mixer_kwargs = {post_field_name: post_with_published_location}
    return mixer.blend(f"blog.{comment_model_name}", **mixer_kwargs)
