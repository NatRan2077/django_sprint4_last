from inspect import isclass

import pytest
from django.contrib.auth import get_user_model
from django.db import models

from adapters.student_adapter import StudentModelAdapter
from blog.models import Post
from conftest import COMMENT_TEXT_DISPLAY_LEN_FOR_TESTS
from fixtures.types import CommentModelAdapterT


@pytest.fixture
def comment_model_adapter(comment_model: type) -> CommentModelAdapterT:
    class _CommentModelAdapter(StudentModelAdapter):

        @property
        def _access_by_name_fields(self):
            return ["id", "refresh_from_db"]

        @property
        def adapter_fields(self) -> type:
            user = get_user_model()

            class _AdapterFields:
                post = models.ForeignKey(Post, on_delete=models.CASCADE)
                author = models.ForeignKey(user, on_delete=models.CASCADE)
                text = models.TextField()
                created_at = models.DateTimeField()

                field_description = {
                    "post": (
                        "связывает модель `blog.models.Comment` "
                        "с моделью `blog.models.Post`"
                    ),
                    "author": (
                        "задаёт автора комментария, "
                        "связывая модель `blog.models.Comment` "
                        "с моделью `blog.models.Post`"
                    ),
                    "text": "задаёт текст комментария",
                    "created_at": "задаёт дату комментария",
                }

            return _AdapterFields

        @property
        def item_model(self) -> type:
            return comment_model

        @property
        def displayed_field_name_or_value(self):
            if isclass(self._item_or_cls):
                return "text"
            else:
                return self.text.split("\n")[0][
                    :COMMENT_TEXT_DISPLAY_LEN_FOR_TESTS
                ]

    # checking expected fields exist
    _comment_model_cls_adapter = _CommentModelAdapter(comment_model)
    fields = {"text", "post", "author", "created_at"}
    for field in fields:
        getattr(_comment_model_cls_adapter, field)

    return _CommentModelAdapter
