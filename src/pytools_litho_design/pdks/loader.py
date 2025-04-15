from .demo import get_demo_pdk
import gdsfactory as gf


def get_pdk(name: str = "IMPHYS", set_active: bool = True) -> gf.Pdk:
    """Returns the PDK with the given name.

    Parameters
    ----------
    name : str
        The name of the PDK to return. Currently only "IMPHYS" is supported.

    Returns
    -------
    gf.Pdk
        The PDK with the given name.
    """
    match name.lower():
        case "demo":
            pdk = get_demo_pdk(set_active=set_active)
        case _:
            raise ValueError(f"PDK {name} not supported.")

    return pdk
