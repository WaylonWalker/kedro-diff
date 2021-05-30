should_prints = [
    "name_changed",
    "input_changed",
    "output_changed",
    "new_node",
    "deleted_node",
    "inputs",
    "outputs",
]


def test_node_diff_main(capsys, caplog):
    from kedro_diff.node_diff import __main__  # noqa F401

    assert caplog.text == ""
    captured = capsys.readouterr()
    for should_print in should_prints:
        assert should_print in captured.out
