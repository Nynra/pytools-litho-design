from .demo import get_demo_pdk
import gdsfactory as gf


def get_pdk(name: str = "Demo", set_active: bool = True) -> gf.Pdk:
    """Returns the PDK with the given name.

    Parameters
    ----------
    name : str
        The name of the PDK to return. Currently only "IMPHYS" is supported.
    set_active : bool
        If True, sets the PDK as the active PDK in gdsfactory.

    Returns
    -------
    gf.Pdk
        The PDK with the given name.
    """
    match name.lower():
        case "demo":
            pdk = get_demo_pdk()
        case "generic":
            pdk = gf.generic_tech.get_generic_pdk()
        case _:
            raise ValueError(f"PDK {name} not supported.")

    if set_active:
        pdk.activate()

    return pdk
