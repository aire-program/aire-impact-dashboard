def test_app_imports_without_running():
    import importlib

    app_module = importlib.import_module("app")
    assert hasattr(app_module, "main")
