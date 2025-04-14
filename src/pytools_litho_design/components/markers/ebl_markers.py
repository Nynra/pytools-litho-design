import gdsfactory as gf
from typing import Union, List


@gf.cell
def ebl_marker_jb(
    width_box: float = 20,
    gap: float = 250,
    cross_section: Union[gf.CrossSection, str] = "strip",
    text: Union[str, None] = None,
    text_coordinates: List[int] = [0, 0],
    text_size: int = 10,
) -> gf.Component:
    """Creates a marker used in EBL lithography.

    Created by J. van der Boom, updated to match the new gdsfactory version by
    B. Klein Ikkink. The marker consists of four boxes arranged in a square
    pattern with a specified gap between them. The boxes are centered around
    the origin (0, 0) and can be customized with a text label.

    Geometry
    ---------

    .. code-block:: python

        [ ]       [ ]
       |
    gap|
       | --- cross section width
        [ ]       [ ]

    Parameters
    ----------
    width_box : float
        Width of the complete marker box (bbox containing the marker features).
    gap : float
        Gap between the marker boxes.
    cross_section : str or CrossSection
        Cross-section to use for writing the marker boxes, defaults to waveguides
        using the "strip" cross-section.
    text : str or None
        Text to add to the marker, defaults to None.
    text_coordinates : List[int]
        Coordinates for the text, defaults to [0, 0], only used if text is not None.
    text_size : int
        Size of the text, defaults to 10, only used if text is not None.

    Returns
    -------
    Component
        A component containing the EBL marker with the specified parameters.
    """
    if isinstance(cross_section, str):
        cross_section = gf.get_cross_section(cross_section)

    # Create a new Device
    MARKER = gf.Component()

    # Calculate the positions of the boxes
    positions = [
        (-width_box / 2 - gap / 2, width_box / 2 + gap / 2),  # Top-left
        (width_box / 2 + gap / 2, width_box / 2 + gap / 2),  # Top-right
        (-width_box / 2 - gap / 2, -width_box / 2 - gap / 2),  # Bottom-left
        (width_box / 2 + gap / 2, -width_box / 2 - gap / 2),  # Bottom-right
    ]

    # Create four boxes and add them to the device at the calculated positions
    for pos in positions:
        box = gf.components.rectangle(
            size=(width_box, width_box), layer=cross_section.layer
        )
        box_ref = MARKER << box
        box_ref.center = pos

    # Center the entire device around (0, 0)
    MARKER.center = (0, 0)
    if text is not None:
        T = gf.components.text(text, size=text_size, layer=cross_section.layer)
        text = MARKER << T
        text.center = text_coordinates

    MARKER.flatten()
    return MARKER


def ebl_marker(
    width_box: float = 20,
    gap: float = 250,
    cross_section: Union[gf.CrossSection, str] = "strip",
    text: Union[str, None] = None,
    text_coordinates: List[int] = [0, 0],
    text_size: int = 10,
) -> gf.Component:
    """Creates a marker used in EBL lithography.

    Uses the :func:`ebl_marker_jb` function to create the corner markers and
    adds a cross in the middle.
    """
    if isinstance(cross_section, str):
        cross_section = gf.get_cross_section(cross_section)

    # Create a new Device
    CORNER_MARKERS = ebl_marker_jb(
        width_box=width_box,
        gap=gap,
        cross_section=cross_section,
        text=text,
        text_coordinates=text_coordinates,
        text_size=text_size,
    )
    CROSS = gf.components.cross(
        length=gap / 2,
        width=2 * width_box,
        layer=cross_section.layer,
        port_type="optical",
    )
    MARKER = gf.Component()
    MARKER << CORNER_MARKERS
    cross = MARKER << CROSS
    cross.center = (0, 0)
    MARKER.flatten()
    return MARKER


# @gf.cell
# def ebl_marker_ns(
#     center_x=-110, center_y=-100, gap=200, width=20, cross_section="strip"
# ):
#     """Creates a marker used in EBL lithography.

#     Created by NS, updated to match the new gdsfactory version by
#     B. Klein Ikkink.
#     """
#     # Block_1 = Waveguide.make_at_port(port=Port((center_x, center_y), angle=0, width=Width))
#     # Block_1.add_straight_segment(length=Width)
#     # Block_2 = Waveguide.make_at_port(port=Port((center_x+Gap, center_y), angle=0, width=Width))
#     # Block_2.add_straight_segment(length=Width)
#     # Block_3 = Waveguide.make_at_port(port=Port((center_x, center_y+Gap), angle=0, width=Width))
#     # Block_3.add_straight_segment(length=Width)
#     # Block_4 = Waveguide.make_at_port(port=Port((center_x+Gap, center_y+Gap), angle=0, width=Width))
#     # Block_4.add_straight_segment(length=Width)
#     # cell.add_to_layer(Marker_layer,Block_1,Block_2,Block_3,Block_4)
#     if isinstance(cross_section, str):
#         cross_section = gf.get_cross_section(cross_section)

#     MARKER = gf.Component()
#     BLOCK = gf.components.straight(cross_section=cross_section, length=width)

#     b1 = MARKER << BLOCK
#     b1.center = (center_x, center_y)
#     b2 = MARKER << BLOCK
#     b2.center = (center_x + gap, center_y)
#     b3 = MARKER << BLOCK
#     b3.center = (center_x, center_y + gap)
#     b4 = MARKER << BLOCK
#     b4.center = (center_x + gap, center_y + gap)

#     MARKER.flatten()
#     return MARKER


if __name__ == "__main__":
    # Test the corner_ebl_marker function
    # c = corner_ebl_marker_jb()
    # c = ebl_marker_ns()
    c = ebl_marker()
    c.show()
