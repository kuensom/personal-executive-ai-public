from app.config import settings


def test_settings_exist():
    assert settings is not None


def test_environment_configured():
    assert settings.environment


def test_openai_model_configured():
    assert settings.openai_model


def test_google_paths_configured():
    assert settings.google_credentials_file
    assert settings.google_token_file


def test_log_directory_configured():
    assert settings.log_dir


def test_environment_helpers():
    if settings.environment.lower() == "cloud":
        assert settings.is_cloud is True
        assert settings.is_local is False
    else:
        assert settings.is_local is True
        assert settings.is_cloud is False