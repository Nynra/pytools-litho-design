from typing import Any, List
import gdsfactory as gf
from functools import partial


def single_variabel_sweep_components(
    component: str | gf.Component,
    static_settings: dict[str, Any],
    variable_name: str,
    variable_values: list[Any],
    variable_nickname: str | None = None,
    label_pos: tuple[float, float] | None = None,
    label_size: float = 20,
    label_layer: str | None = None,
) -> List[gf.Component]:
    if isinstance(component, str):
        component = gf.get_component(component)
    # if isinstance(label_layer, str):
    #     label_layer = gf.get_layer_tuple(label_layer)

    sweep = []
    component = partial(component, **static_settings)
    for value in variable_values:
        c = component(**{variable_name: value})

        # Add a label if label_pos is provided
        if label_pos is not None:
            if variable_nickname is None:
                variable_nickname = variable_name
            # new_c = gf.Component()
            LABEL = gf.components.text(
                text=f"{variable_nickname}: {value}",
                size=label_size,
                position=label_pos,
                layer=label_layer,
            )
            new_c = gf.Component()
            label = new_c << LABEL
            label.move(label_pos)
            old_c = new_c << c
            for port in old_c.ports:
                new_c.add_port(name=port.name, port=port)

            c = new_c
        sweep.append(c)

    return sweep
