def test_static_pages_as_cbv():
    try:
        from pages.urls import urlpatterns
    except Exception:
        raise AssertionError(
            "Убедитесь, что в файле `pages/urls.py` задан список urlpatterns."
        )
    for path in urlpatterns:
        if not hasattr(path.callback, "view_class"):
            raise AssertionError(
                "Убедитесь, что в файле `pages/urls.py` маршруты статических"
                " страниц подключены с помощью CBV."
            )
