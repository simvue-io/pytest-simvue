import simvue

class SimvueSingleton:
    _simvue_run = simvue.Run()
    initialised = False
    def __new__(cls: "type[SimvueSingleton]", *args: tuple, **kwargs: dict) -> "SimvueSingleton":
        if not hasattr(cls, "_instance"):
            cls._instance = super(SimvueSingleton, cls).__new__(cls)
        return cls._instance

    def get_run(self) -> simvue.Run:
        return self._simvue_run
