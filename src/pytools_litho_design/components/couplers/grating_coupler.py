import numpy as np
import gdsfactory as gf
from gdsfactory.typings import LayerSpec


@gf.cell
def grating_coupler_traditional(
    cross_section="strip",
    full_opening_angle=np.deg2rad(40),
    grating_period=1.13,
    grating_ff=0.7,
    n_gratings=22,
    ap_max_ff=0.96,
    n_ap_gratings=10,
    taper_length=None,
    angle=0,
) -> gf.Component:
    """Generates a traditional grating coupler using gdsfactory.

    This function constructs a radial grating coupler cell with specified parameters like grating period,
    fill factor, and number of gratings. The component integrates both apodized and traditional gratings
    with a circular to elliptical taper at the beginning.

    Parameters
    ----------
    cross_section : str or CrossSection, optional
        Specifies the cross-section specification for the grating coupler, by default "strip".
    full_opening_angle : float, optional
        The full opening angle of the grating in radians, by default np.deg2rad(40).
    grating_period : float, optional
        The period of the gratings, by default 1.13.
    grating_ff : float, optional
        Fill factor for the grating, representing the fraction of each period that contains material, by default 0.7.
    n_gratings : int, optional
        Number of gratings with constant fill factor, by default 22.
    ap_max_ff : float, optional
        Maximum fill factor for the apodized region, by default 0.96.
    n_ap_gratings : int, optional
        Number of apodized gratings, by default 10.
    taper_length : float, optional
        Length of the initial taper radius, by default None.
    angle : float, optional
        Orientation angle of the coupler in radians, by default 0.

    Returns
    -------
    gf.Component
        A gdsfactory component representing the grating coupler.
    """
    if isinstance(cross_section, str):
        cross_section = gf.get_cross_section(cross_section)
    c = gf.Component()
    opening_angle = full_opening_angle / 2

    # Initialize radii with the taper_length, if provided
    initial_radius = taper_length if taper_length else 0

    # Handling of apodized gratings
    apodized_ffs = np.linspace(ap_max_ff, grating_ff, n_ap_gratings)
    apodized_periods = np.linspace(grating_period, grating_period, n_ap_gratings)

    # Collect all radii information
    radii = [initial_radius]
    for ap_period, ap_ff in zip(apodized_periods, apodized_ffs):
        radii.append(ap_period * (1 - ap_ff))  # Gap
        radii.append(ap_period * ap_ff)  # Material

    # Handling of constant fill factor gratings
    for _ in range(n_gratings):
        radii.append(grating_period * (1 - grating_ff))  # Gap
        radii.append(grating_period * grating_ff)  # Material

    # Calculate and draw all grating arcs
    current_radius = radii[0]
    origin = (0, 0)
    for i in range(1, len(radii), 2):
        gap = radii[i]
        material = radii[i + 1]
        inner_radius = current_radius + gap
        outer_radius = inner_radius + material

        phi = np.linspace(-opening_angle, opening_angle, 100)
        inner_arc = np.array(
            [
                np.cos(phi) * inner_radius + origin[0],
                np.sin(phi) * inner_radius + origin[1],
            ]
        )
        outer_arc = np.array(
            [
                np.cos(phi[::-1]) * outer_radius + origin[0],
                np.sin(phi[::-1]) * outer_radius + origin[1],
            ]
        )

        grating_polygon = np.column_stack((inner_arc, outer_arc)).T
        c.add_polygon(grating_polygon, layer=cross_section.layer)

        current_radius = outer_radius  # Update radius for next iteration

    # Add the taper (circular to elliptical transition)
    taper_radius = radii[0]
    taper_phi = np.linspace(-opening_angle, opening_angle, 100)
    taper_xpts = np.cos(taper_phi) * taper_radius + origin[0]
    taper_ypts = np.sin(taper_phi) * taper_radius + origin[1]

    taper_points = np.array(
        [
            [origin[0], origin[1] - cross_section.width / 2],
            *zip(taper_xpts, taper_ypts),
            [origin[0], origin[1] + cross_section.width / 2],
        ]
    )

    c.add_polygon(taper_points, layer=cross_section.layer)

    c.add_port(
        name="o1",
        center=(origin[0], origin[1]),
        orientation=180,
        cross_section=cross_section,
    )
    return c


if __name__ == "__main__":
    grating_coupler = grating_coupler_traditional(
        full_opening_angle=np.deg2rad(40),
        grating_period=1.155,
        grating_ff=0.3,
        ap_max_ff=0.9,
        n_gratings=20,
        n_ap_gratings=15,
        taper_length=16.0,
    )
    grating_coupler.draw_ports()
    grating_coupler.show()
