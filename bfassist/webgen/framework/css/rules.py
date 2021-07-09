#############################################################################
#
#
#   webGenCSS module to BFA v.5 standalone
#
#
#############################################################################
""" Module to improve python to CSS coding with the bfa webGen modules. Contains most important CSS rules.

    Dependencies:

        bfassist <- (webgen.framework.css.)rules
            |
            \-> colours -> rgbcolours
             -> webgen -> framework -> css

        note::  Author(s): Mitch last-check: 07.07.2021 """

from bfassist.colours.rgbcolours import RGBA_Colour, RGB_Colour, Colour
from bfassist.webgen.framework.css import CSS_Rule


# noinspection PyUnusedLocal
def __preload__(forClient: bool = True):
    pass


# noinspection PyUnusedLocal
def __postload__(forClient: bool = True):
    pass


def set_background_colour(colour: Colour):
    """ Creates the css rule for styling the background colour.

        :param colour:  The colour the background should be styled with.

        :return:        CSS rule for styling the background colour accordingly.

            note::  Author(s): Mitch """

    if isinstance(colour, Colour):
        return CSS_Rule('background-color', colour.toCSS())
    else:
        return CSS_Rule('background-color', colour)


def set_padding(top: str, right: str = None, bot: str = None, left: str = None):
    """ Creates the css rule for padding.

        :param top:     Padding at the top side.
        :param right:   Padding at the right side.
        :param bot:     Padding at the bottom side.
        :param left:    Padding at the left side.

        :return:        CSS rule for applying padding as specified.

            note::  Author(s): Mitch """
    values = [top]
    if right is not None:
        values.append(right)
    if bot is not None:
        values.append(bot)
    if left is not None:
        values.append(left)

    return CSS_Rule('padding', ' '.join(values))


def set_font_family(primary: str, fallbacks: list):
    """ Creates the CSS rule for setting a font including fallbacks.

        :param primary:     The primary font to use.
        :param fallbacks:   A list of fallback fonts, higher priorities at front.

        :return:            CSS rule for applying the font family choices.

            note::  Author(s): Mitch """

    return CSS_Rule('font-family', primary + ', ' + ', '.join(fallbacks))


def set_text_align(alignment: str):
    """ Creates the CSS rule for text-alignment.

        :param alignment:   Specification of the alignment.

        :return:            CSS rule for applying the alignment.

            note::  Author(s): Mitch """

    return CSS_Rule('text-align', alignment)


def set_colour(colour: RGBA_Colour):
    """ Creates the CSS rule for setting a colour.

        :param colour:   Colour to be set.

        :return:         CSS rule for applying the colour.

            note::  Author(s): Mitch """

    if isinstance(colour, Colour):
        return CSS_Rule('color', colour.toCSS())
    else:
        return CSS_Rule('color', colour)


def set_position(position: str):
    """ Creates the CSS rule for setting a position.

        :param position:    Position to be set.

        :return:            CSS rule for applying the position.

            note::  Author(s): Mitch """

    return CSS_Rule('position', position)


def set_top(top: str):
    """ Creates the CSS rule for setting the top property.

        :param top:     Top property to be set.

        :return:        CSS rule for applying the top property.

            note::  Author(s): Mitch """

    return CSS_Rule('top', top)


def set_left(left: str):
    """ Creates the CSS rule for setting the top property.

        :param left:     Top property to be set.

        :return:        CSS rule for applying the top property.

            note::  Author(s): Mitch """

    return CSS_Rule('left', left)


def set_transform(x: str, y: str, Type: str = None):
    """ Creates the CSS rule for translating x and y.

        :param x:       X translation value.
        :param y:       Y translation value.
        :param Type:    Transformation type.

        :return:        CSS rule for applying the transformation.

            note::  Author(s): Mitch """

    if Type is None:
        return CSS_Rule('transform', 'translateX(' + x + ") translateY(" + y + ")")
    else:
        return CSS_Rule('-' + Type + '-transform', 'translateX(' + x + ") translateY(" + y + ")")


def set_margin_bottom(margin: str):
    """ Creates the CSS rule for setting a bottom margin.

        :param margin:  The margin to set.

        :return:        CSS rule for applying the margin.

            note::  Author(s): Mitch """

    return CSS_Rule('margin-bottom', margin)


def set_margin_right(margin: str):
    """ Creates the CSS rule for setting a right margin.

        :param margin:  The margin to set.

        :return:        CSS rule for applying the margin.

            note::  Author(s): Mitch """

    return CSS_Rule('margin-right', margin)


def set_margin_top(margin: str):
    """ Creates the CSS rule for setting a top margin.

        :param margin:  The margin to set.

        :return:        CSS rule for applying the margin.

            note::  Author(s): Mitch """

    return CSS_Rule('margin-top', margin)


def set_width(width: str):
    """ Creates the CSS rule for setting the width.

        :param width:   The width to set.

        :return:        CSS rule for applying the width.

            note::  Author(s): Mitch """

    return CSS_Rule('width', width)


def set_font_weight(weight: str):
    """ Creates the CSS rule for setting the font weight.

        :param weight:  The weight to set.

        :return:        CSS rule for applying the weight.

            note::  Author(s): Mitch """

    return CSS_Rule('font-weight', weight)


def set_font_size(size: str):
    """ Creates the CSS rule for setting the font size.

        :param size:  The size to set.

        :return:        CSS rule for applying the size.

            note::  Author(s): Mitch """

    return CSS_Rule('font-size', size)


def set_border_radius(radius: str):
    """ Creates the CSS rule for setting the border radius.

        :param radius:  The radius to set.

        :return:        CSS rule for applying the border radius.

            note::  Author(s): Mitch """

    return CSS_Rule('border-radius', radius)


def set_cursor(cursor: str):
    """ Creates the CSS rule for setting the cursor.

        :param cursor:  The cursor to set.

        :return:        CSS rule for applying the cursor.

            note::  Author(s): Mitch """

    return CSS_Rule('cursor', cursor)


def set_border(size: str, style: str, colour: RGB_Colour):
    """ Creates the CSS rule for setting a border.

        :param size:    Border size.
        :param style:   Border style.
        :param colour:  Border colour.

        :return:        CSS rule for applying the border.

            note::  Author(s): Mitch """

    if isinstance(colour, RGB_Colour):
        return CSS_Rule('border', ' '.join([size, style, colour.toCSS()]))
    else:
        return CSS_Rule('border', ' '.join([size, style, colour]))


def set_height(height: str):
    """ Creates the CSS rule for setting the height.

        :param height:  The height to be set.

        :return:        CSS rule for applying the height.

            note::  Author(s): Mitch """

    return CSS_Rule('height', height)


def set_margin(margin: str):
    """ Creates the CSS rule for setting the margin.

        :param margin:  The margin to be set.

        :return:        CSS rule for applying the margin.

            note::  Author(s): Mitch """

    return CSS_Rule('margin', margin)


def set_display(display: str):
    """ Creates the CSS rule for setting the display style.

        :param display: The display style to be set.

        :return:        CSS rule for applying the display style.

            note::  Author(s): Mitch """

    return CSS_Rule('display', display)


def set_text_decoration(decoration: str):
    """ Creates the CSS rule for setting text decoration.

        :param decoration:  Text decoration to be set.

        :return:            CSS rule for applying the text decoration.

            note::  Author(s): Mitch """

    return CSS_Rule('text-decoration', decoration)


def set_vertical_align(valign: str):
    """ Creates the CSS rule for setting vertical alignment.

        :param valign:  Vertical alignment setting.

        :return:        CSS rule for applying vertical alignment.

            note::  Author(s): Mitch """

    return CSS_Rule('vertical-align', valign)


def set_flex(size: str, flex: str):
    """ Creates the CSS rule for setting a flex setting.

        :param size:    Size of flex.
        :param flex:    Flex setting.

        :return:        CSS rule for setting a flex setting.

            note::  Author(s): Mitch """

    return CSS_Rule('flex', size + ' ' + flex)


def set_border_bottom(size: str, style: str, colour: RGB_Colour):
    """ Creates the CSS rule for setting the bottom border.

        :param size:    Size of the border.
        :param style:   Style of the border.
        :param colour:  Colour of the border.

        :return:        CSS rule for applying the bottom border.

            note::  Author(s): Mitch """

    if isinstance(colour, RGB_Colour):
        return CSS_Rule('border-bottom', ' '.join([size, style, colour.toCSS()]))
    else:
        return CSS_Rule('border-bottom', ' '.join([size, style, colour]))


def set_border_left(size: str, style: str, colour: RGB_Colour):
    """ Creates the CSS rule for setting the left border.

        :param size:    Size of the border.
        :param style:   Style of the border.
        :param colour:  Colour of the border.

        :return:        CSS rule for applying the left border.

            note::  Author(s): Mitch """

    if isinstance(colour, RGB_Colour):
        return CSS_Rule('border-left', ' '.join([size, style, colour.toCSS()]))
    else:
        return CSS_Rule('border-left', ' '.join([size, style, colour]))


def set_border_right(size: str, style: str, colour: RGB_Colour):
    """ Creates the CSS rule for setting the right border.

        :param size:    Size of the border.
        :param style:   Style of the border.
        :param colour:  Colour of the border.

        :return:        CSS rule for applying the right border.

            note::  Author(s): Mitch """

    if isinstance(colour, RGB_Colour):
        return CSS_Rule('border-right', ' '.join([size, style, colour.toCSS()]))
    else:
        return CSS_Rule('border-right', ' '.join([size, style, colour]))


def set_overflowX(setting: str):
    """ Creates the CSS rule for setting the overflow behaviour on the x axis.

        :param setting: Setting.

        :return:        CSS rule for applying the overflow setting.

            note::  Author(s): Mitch """

    return CSS_Rule('overflow-x', setting)


def set_overflow(setting: str):
    """ Creates the CSS rule for setting the overflow behaviour.

        :param setting: Setting.

        :return:        CSS rule for applying the overflow setting.

            note::  Author(s): Mitch """

    return CSS_Rule('overflow', setting)


def set_overflowY(setting: str):
    """ Creates the CSS rule for setting the overflow behaviour on the y axis.

        :param setting: Setting.

        :return:        CSS rule for applying the overflow setting.

            note::  Author(s): Mitch """

    return CSS_Rule('overflow-y', setting)


def set_max_height(max_height: str):
    """ Creates the CSS rule for setting the max height.

        :param max_height:  Max height to be set.

        :return:            CSS rule for applying the maximum height.

            note::  Author(s): Mitch """

    return CSS_Rule('max-height', max_height)


def set_content(content: str):
    """ Creates the CSS rule for setting content.

        :param content: The content to be set.

        :return:        CSS rule for applying the content.

            note::  Author(s): Mitch """

    return CSS_Rule('content', content)


def set_white_space(setting: str):
    """ Creates the CSS rule for setting white-space behaviour.

        :param setting: The white-space behaviour to set.

        :return:        CSS rule for applying the behaviour.

            note::  Author(s): Mitch """

    return CSS_Rule('white-space', setting)


def set_visibility(visibility: str):
    """ Creates the CSS rule for setting visibility.

        :param visibility:  Visibility.

        :return:            CSS rule for applying the visibility.

            note::  Author(s): Mitch """

    return CSS_Rule('visibility', visibility)


def set_border_collapse(setting: str):
    """ Creates the CSS rule for setting border collapse.

        :param setting:  Collapsing setting.

        :return:         CSS rule for applying the collapse.

            note::  Author(s): Mitch """

    return CSS_Rule('border-collapse', setting)
