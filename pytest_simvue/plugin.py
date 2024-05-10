import pytest
import uuid

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


@pytest.fixture
def simvue(request, pytestconfig):
    _simvue_run = SimvueSingleton()
    
    if not (_name_prefix := pytestconfig.getini("simvue_prefix")):
        _name_prefix = request.config.getoption("name_prefix")

    if not (_tags := pytestconfig.getini("simvue_tags")):
        _tags_str = request.config.getoption("simvue_tags")
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
    yield _simvue_run.get_run()
    if request.session.testsfailed > 0:
        _simvue_run.get_run().set_status("failed")
    _simvue_run.get_run().close()
