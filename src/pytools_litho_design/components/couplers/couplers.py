import gdsfactory as gf
from functools import partial
import numpy as np


# coupler = partial(gf.components.coupler)
from gdsfactory.components import coupler, grating_coupler_elliptical_arbitrary


@gf.cell
def grating_coupler_traditional(
    cross_section="asic",
    full_opening_angle=np.deg2rad(36),
    grating_period=tuple(1.2 + np.arange(-0.2, 0.3, 0.2)),
    grating_ff=tuple(0.6 + np.arange(-0.05, 0.06, 0.05)),
    n_gratings=20,
    ap_max_ff=tuple(0.96 + np.arange(-0.02, 0.03, 0.02)),
    n_ap_gratings=20,
    taper_length=48,
) -> gf.Component:
    if isinstance(cross_section, str):
        cross_section = gf.get_cross_section(cross_section)

    c = gf.Component()
    opening_angle = full_opening_angle / 2
    initial_radius = taper_length if taper_length else 0

    # Ensure inputs are arrays
    grating_period = np.atleast_1d(grating_period)
    grating_ff = np.atleast_1d(grating_ff)
    ap_max_ff = np.atleast_1d(ap_max_ff)

    # Handling of apodized gratings
    apodized_ffs = np.linspace(ap_max_ff[0], grating_ff[0], n_ap_gratings)
    apodized_periods = np.linspace(grating_period[0], grating_period[0], n_ap_gratings)

    radii = [initial_radius]
    for ap_period, ap_ff in zip(apodized_periods, apodized_ffs):
        radii.append(ap_period * (1 - ap_ff))  # Gap
        radii.append(ap_period * ap_ff)  # Material

    # Handling of constant fill factor gratings
    for i in range(n_gratings):
        period = grating_period[i % len(grating_period)]
        ff = grating_ff[i % len(grating_ff)]
        radii.append(period * (1 - ff))  # Gap
        radii.append(period * ff)  # Material

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

        current_radius = outer_radius

    # Add the taper
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
    # nc =

    c.add_port(
        name="o1",
        center=(origin[0], origin[1]),
        orientation=180,
        cross_section=cross_section,
    )

    # # Check if the cross_section has cladding
    # if len(cross_section.sections) > 1:
    #     # Add the cladding sections
    #     for section in cross_section.sections[1:]:

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
