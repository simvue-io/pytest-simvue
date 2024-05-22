import simvue
import typing

class SimvueSingleton:
    _simvue_run = simvue.Run()
    test_results: dict[str, typing.Optional[bool]] = {}
    alert_ids: dict[str, typing.Optional[str]] = {}
    initialised = False
    def __new__(cls: "type[SimvueSingleton]", *args: tuple, **kwargs: dict) -> "SimvueSingleton":
        if not hasattr(cls, "_instance"):
            cls._instance = super(SimvueSingleton, cls).__new__(cls)
        return cls._instance

    def get_run(self) -> simvue.Run:
        return self._simvue_run
    
    def set_test_result(self, test_name: str, status: bool) -> None:
        self.test_results[test_name] = status
