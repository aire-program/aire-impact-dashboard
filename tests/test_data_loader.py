import pytest
from app.data_loader import load_all_data

def test_data_loader_returns_dict():
    data = load_all_data()
    assert isinstance(data, dict)
    assert "departments" in data
    assert "workshops" in data

def test_data_loader_non_empty():
    data = load_all_data()
    for key, df in data.items():
        assert not df.empty, f"{key} DataFrame is empty"
