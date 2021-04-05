import subprocess


def test_main(capsys):
    proc = subprocess.Popen(
        ["python", "-m", "kedro_diff"], stderr=subprocess.PIPE, stdout=subprocess.PIPE
    )
    proc.wait()
    stdout = "".join([str(line) for line in proc.stdout.readlines()])
    stderr = "".join([str(line) for line in proc.stderr.readlines()])
    assert stderr == ""
    assert_contains = [
        "KedroDiff Examples",
        "KedroDiff.stat()",
        "__default__",
        "+++",
        "---",
        "M",
    ]
    for check_contains in assert_contains:
        assert check_contains in stdout
