import pytest
import uuid
import typing

from .session import SimvueSingleton


def pytest_addoption(parser):
    group = parser.getgroup("simvue")
    parser.addini(
        "simvue_prefix",
        "Set the name prefix for Pytest runs stored on Simvue.",
        default="pytest_run",
        type="string",
    )
    parser.addini(
        "simvue_tags",
        "Tags to add to Pytest runs in Simvue.",
        default=[],
        type="linelist",
    )
    parser.addini(
        "simvue_folder",
        "Folder to store test runs in Simvue.",
        default="/pytest_simvue",
        type="string",
    )
    group.addoption(
        "--simvue-prefix",
        action="store",
        dest="name_prefix",
        default="pytest_run",
        help="Set the name prefix for Pytest runs stored on Simvue.",
    )
    group.addoption(
        "--simvue-tags",
        action="store",
        dest="simvue_tags",
        default="",
        help="Comma separated tags to add to Pytest runs in Simvue.",
    )
    group.addoption(
        "--simvue-folder",
        action="store",
        dest="simvue_folder",
        default="/pytest_simvue",
        help="Folder to store test runs in Simvue.",
    )


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    simvue_instance = SimvueSingleton()
    if not simvue_instance.initialised:
        return

    outcome = yield
    
    if (result := outcome.get_result()) and result.when == "call":
        simvue_instance.set_test_result(item, result.passed)

def pytest_collection_modifyitems(session, config, items):
    _simvue_run = SimvueSingleton()
    for test in items:
        _simvue_run.test_results[test.nodeid] = None

def pytest_terminal_summary(terminalreporter, exitstatus, config):
    _simvue_run = SimvueSingleton()
    for test, status in _simvue_run.test_results.items():
        if not status:
            continue
        _simvue_run.get_run().log_alert(f"{test}", "ok" if status else "critical")
    _simvue_run.get_run().set_status("failed" if not exitstatus else "completed")
    _simvue_run.get_run().close()

@pytest.fixture
def simvue(request: pytest.FixtureRequest, pytestconfig):
    _simvue_run = SimvueSingleton()
    
    if not (_name_prefix := pytestconfig.getini("simvue_prefix")):
        _name_prefix = request.config.getoption("name_prefix")

    if not (_tags := pytestconfig.getini("simvue_tags")):
        _tags_str: str = request.config.getoption("simvue_tags")
        _tags = _tags_str.split(",") if _tags_str else []

    _tags = [i.strip() for i in _tags]

    if not (_folder := pytestconfig.getini("simvue_folder")):
        _folder = request.config.getoption("simvue_folder")

    if not _simvue_run.initialised:
        _simvue_run.get_run().init(
            f"{_name_prefix}_{str(uuid.uuid4()).split('-')[0]}",
            tags=["pytest_simvue"] + _tags,
            folder=_folder,
        )
        for key in _simvue_run.test_results:
            _simvue_run.get_run().create_alert(
                name=f"{key}",
                source="user",
                description=f"Alert for failure of test '{key}'"
            )
        _simvue_run.initialised = True
        if request.function:
            _simvue_run.get_run().update_tags([request.function.__name__])
            _simvue_run.get_run().update_metadata({
                "function": request.function.__name__,
                "module": request.module.__name__,
                "root": request.config.rootpath.__str__(),
            })

    yield _simvue_run.get_run()


