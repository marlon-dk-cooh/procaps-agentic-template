from tools.demo_tools import (
    ITEMS_PATH,
    REPORT_PATH,
    STRUCTURE_PATH,
    build_demo_report_impl,
    extract_demo_items_impl,
    parse_document_source_impl,
)


def _update(command):
    return getattr(command, "update", command["update"])


def test_demo_tools_create_virtual_artifacts():
    first = parse_document_source_impl("/workspace/example.pdf", {"files": {}})
    files = _update(first)["files"]

    second = extract_demo_items_impl({"files": files})
    files = _update(second)["files"]

    third = build_demo_report_impl({"files": files})
    files = _update(third)["files"]

    assert STRUCTURE_PATH in files
    assert ITEMS_PATH in files
    assert REPORT_PATH in files
    assert files[REPORT_PATH]["data"]["item_count"] == 3
