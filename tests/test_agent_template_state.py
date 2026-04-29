from state.state import file_reducer


def test_file_reducer_merges_virtual_files():
    merged = file_reducer(
        {"/demo/a.json": {"data": 1}},
        {"/demo/b.json": {"data": 2}},
    )

    assert merged == {
        "/demo/a.json": {"data": 1},
        "/demo/b.json": {"data": 2},
    }
