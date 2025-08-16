import os
from storage.excel_store import ExcelStore

def test_excel_store(tmp_path):
    test_file = tmp_path / "test.xlsx"
    store = ExcelStore(file_path=str(test_file))

    product = {"url": "http://test.com", "name": "Test Item", "price": 100, "target": 80}
    store.save(product)

    data = store.load()
    assert len(data) == 1
    assert data[0]["name"] == "Test Item"
    assert data[0]["price"] == 100
