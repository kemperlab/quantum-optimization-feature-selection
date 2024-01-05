from ast import literal_eval
from jax import numpy as np, Array
from pathlib import Path
from orjson import loads
from types import SimpleNamespace
from typing import Any, Literal


class ExperimentRun:
    iterations: list[SimpleNamespace]
    run_number: int
    log_file: str

    def __init__(self, run_path: Path) -> None:
        with run_path.open('rb') as f:
            data: dict[str, Any] = loads(f.read())

        for key, var in data.items():
            if key == 'iterations':
                setattr(self, key, [SimpleNamespace(**i) for i in var])
            else:
                setattr(self, key, var)

        for iteration in self.iterations:
            if isinstance(iteration.params, str):
                iteration.params = literal_eval(iteration.params)

    def get_x_axis(self, axis_type: Literal['iterations', 'shots']) -> Array:
        match axis_type:
            case 'iterations':
                return np.arange(len(self.iterations))

            case 'shots':
                return np.cumsum(
                    np.array([
                        i.samples * i.shots_per_hamiltonians
                        for i in self.iterations
                    ]))

            case _:
                raise ValueError(f'Invalid axis type, got {axis_type}')

    def get_costs(self) -> Array:
        return np.array([i.cost for i in self.iterations])

    def get_params(self) -> Array:
        return np.array([i.params for i in self.iterations])
