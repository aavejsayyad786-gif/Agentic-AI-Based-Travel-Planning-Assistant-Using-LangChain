from src.data_tools import load_all_data

def test_datasets_load_and_have_records():
    data = load_all_data()
    assert data["flights"]
    assert data["hotels"]
    assert data["places"]
    assert {"origin", "destination", "price_inr", "duration_hours"} <= set(data["flights"][0])
