"""
.. _blend-modes:

================================
Blending and compositing artists
================================

When an artist is drawn on top off all previously drawn artists, its full extent
is normally shown, with its colors blended into the existing colors based on its
alpha value.  Matplotlib provides alternative behaviors via the
`.Artist.blend_mode` property instead of the default ("normal") behavior:

* 15 `blend modes`_
* 6 `Porter-Duff compositing operators`_

(See also :ref:`blend-groups` for the additional capability of blending groups
of artists.)

Below is a gallery illustrating the effect of each `.Artist.blend_mode` option
for a variety of artists.  Although the gallery has the artists in each panel
using the same blend mode, they can have different blend modes, as desired.

Be aware that the background of the axes and the background of the figure are
artists as well, so their respective colors may factor into the blending result.

Backends using the Agg renderer (the default) or the Cairo renderer support all
of these blend modes and compositing operators, but other backends may not
support all of them.  See the table at the bottom for details.

.. _blend modes: https://en.wikipedia.org/wiki/Blend_modes
.. _Porter-Duff compositing operators: https://www.w3.org/TR/compositing-1/#advancedcompositing

"""
import matplotlib.pyplot as plt
import numpy as np

from matplotlib.patches import Circle, Rectangle

N = 10
data = np.arange(N**2).reshape((N, N)) % (N-1)

fig, axs = plt.subplots(3, 8, figsize=(10, 6), layout="tight")
axs = axs.flatten()
fig.set_facecolor("none")

blend_modes = ["normal",

               # Blend modes
               "multiply", "screen", "overlay", "darken", "lighten",
               "color dodge", "color burn", "hard light", "soft light",
               "difference", "exclusion",
               "hue", "saturation", "color", "luminosity",

               # Porter-Duff compositing operators
               "knockout", "erase", "clear", "atop", "xor", "plus"]

for ax in axs:
    ax.set_facecolor("none")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1.2)
    ax.set_axis_off()

for i, blend_mode in enumerate(blend_modes):
    axs[i].imshow(data, cmap='Reds', alpha=0.75, extent=(0, 0.8, 0, 0.8))

    # Four different artist types drawn using this blend_mode setting
    axs[i].imshow(data[::-1, :], cmap='Blues', alpha=0.75, extent=(0.2, 1, 0.4, 1.2),
                  blend_mode=blend_mode)
    axs[i].text(0.05, 0.15, "Test", weight="bold", color="c",
                blend_mode=blend_mode)
    axs[i].plot([0, 1], [1.2, 0], color="y",
                blend_mode=blend_mode)
    circ = Circle((.65, 0.5), .3, facecolor='g', alpha=0.5,
                     blend_mode=blend_mode, zorder=2)
    axs[i].add_artist(circ)

    rect = Rectangle((0, 1.2), 1, .3, facecolor='lightgray', clip_on=False)
    axs[i].add_artist(rect)
    axs[i].set_title(blend_mode)

plt.show()

# %%
#
# This table shows which options for `.Artist.blend_mode` are supported by each
# backend type (✅ = supported, ❌ = not supported).
#
# +----------------+-----+-------+-----+-----+-----+----+
# | Option         | Agg | Cairo | SVG | PDF | PGF | PS |
# +================+=====+=======+=====+=====+=====+====+
# | normal [#]_    | ✅  |  ✅   | ✅  | ✅  | ✅  | ✅ |
# +----------------+-----+-------+-----+-----+-----+----+
# | multiply,      | ✅  |  ✅   | ✅  | ✅  | ✅  | ❌ |
# | screen,        |     |       |     |     |     |    |
# | overlay,       |     |       |     |     |     |    |
# | darken,        |     |       |     |     |     |    |
# | lighten,       |     |       |     |     |     |    |
# | color dodge,   |     |       |     |     |     |    |
# | color burn,    |     |       |     |     |     |    |
# | hard light,    |     |       |     |     |     |    |
# | soft light,    |     |       |     |     |     |    |
# | difference,    |     |       |     |     |     |    |
# | exclusion,     |     |       |     |     |     |    |
# | hue,           |     |       |     |     |     |    |
# | saturation,    |     |       |     |     |     |    |
# | color,         |     |       |     |     |     |    |
# | luminosity     |     |       |     |     |     |    |
# +----------------+-----+-------+-----+-----+-----+----+
# | knockout [#]_, | ✅  |  ✅   | ❌  | ❌  | ❌  | ❌ |
# | erase [#]_,    |     |       |     |     |     |    |
# | clear,         |     |       |     |     |     |    |
# | atop,          |     |       |     |     |     |    |
# | xor,           |     |       |     |     |     |    |
# | plus           |     |       |     |     |     |    |
# +----------------+-----+-------+-----+-----+-----+----+
#
# .. [#] also known as "over"
# .. [#] also known as "source"
# .. [#] also known as "destination out"
