import pandas as pd

from src import data_loader


def test_individual_loaders_return_dataframe():
    loaders = [
        data_loader.load_workshops,
        data_loader.load_participants,
        data_loader.load_confidence_surveys_pre,
        data_loader.load_confidence_surveys_post,
        data_loader.load_reflections,
        data_loader.load_departments,
    ]
    for loader in loaders:
        df = loader()
        assert isinstance(df, pd.DataFrame)
        assert not df.empty


def test_expected_columns_present():
    assert set(data_loader.load_workshops().columns) == {
        "workshop_id",
        "date",
        "title",
        "format",
        "audience",
        "department_id",
        "registrations",
        "attendances",
        "completion_rate",
    }
    assert set(data_loader.load_participants().columns) == {
        "participant_id",
        "role",
        "department_id",
        "workshops_attended",
        "last_attended_date",
        "adoption_level",
        "ai_confidence_self_rating",
    }


def test_load_all_data_returns_expected_keys():
    data = data_loader.load_all_data()
    expected = {
        "workshops",
        "participants",
        "confidence_pre",
        "confidence_post",
        "reflections",
        "departments",
    }
    assert set(data.keys()) == expected
