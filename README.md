# Pytest Simvue

Send pytest test results to a [Simvue](https://simvue.io) server.

## Installation

```sh
pip install git+https://github.com/simvue-io/pytest-simvue.git
```

## Usage

Simply include the `simvue` fixture when creating tests:

```python
def test_this_works(simvue):
    assert 2 == 3
```

## Configuration

Configure Simvue run options via the `pytest.ini` configuration file:

```ini
[pytest]
simvue_folder = /other_folder
simvue_tags =
    special
    test
    tags
simvue_prefix = my_tests
```

## Command Line Flags

You can configure options also via the command line:

```sh
pytest --simvue-folder "/other-folder" --simvue-tags "special,test,tags" --simvue-prefix "my_tests"
```