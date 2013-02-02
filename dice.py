from kivy.uix.widget import Widget
from kivy.properties import NumericProperty
from kivy.graphics import Ellipse, Line, Fbo, Rectangle

from shader import circle_shader


class DiceWidget(Widget):
    number = NumericProperty(0)

    # Dots are drawn on a grid dividing the die face into 16 squares
    # and starting from the bottom left. Define coords for each.
    #  _______
    # |_|_|_|_|
    # |_|_|_|_|
    # |_|_|_|_|
    # |_|_|_|_|
    #

    # Locations of dots for each face
    dotmap = {
        0: (),
        1: ((2, 2),),
        2: ((1, 1), (3, 3)),
        3: ((1, 1), (2, 2), (3, 3)),
        4: ((1, 1), (1, 3), (3, 3), (3, 1)),
        5: ((1, 1), (1, 3), (2, 2), (3, 3), (3, 1)),
        6: ((1, 1), (1, 2), (1, 3), (3, 1), (3, 2), (3, 3))
    }

    def __init__(self, **kwargs):
        super(DiceWidget, self).__init__(**kwargs)

        self.bind(size=self.redraw, pos=self.redraw)

        # Components drawn on the canvas
        self.dot_fbo = None
        self.number = 0

        self.redraw()

    def redraw(self, *_args, **_kwargs):
        self.canvas.clear()

        x, y, w, h = self.bounding_box

        # Size of a dot
        dot_w = w / 5
        dot_h = h / 5

        # Render a single dot
        self.dot_fbo = self.render_dot((dot_w, dot_h))

        # Frame buffer objects can be invalidated when apps are minimized,
        # this event rebuilds it.
        self.dot_fbo.add_reload_observer(self.redraw)

        with self.canvas:
            # Draw the outline
            Line(rectangle=(x, y, w, h))

        # Update dots
        self.on_number()

    def on_number(self, *_args):
        x, y, w, h = self.bounding_box

        # Size of a dot
        dot_w = w / 5
        dot_h = h / 5

        # Size of a grid unit
        unit = w / 4

        self.canvas.remove_group('dot')
        with self.canvas:
            # Draw dots
            for grid_x, grid_y in self.dotmap[self.number]:
                Rectangle(
                    pos=(x + (grid_x * unit) - dot_w / 2,
                         y + (grid_y * unit) - dot_h / 2),
                    size=(dot_w, dot_h),
                    texture=self.dot_fbo.texture,
                    group='dot')

    def render_dot(self, size):
        # Render an antialiased dot using the circle shader.
        with self.canvas:
            dot_fbo = Fbo(size=size)

        # Install the shader, and check it compiled.
        original_fs = dot_fbo.shader.fs
        dot_fbo.shader.fs = circle_shader
        if not dot_fbo.shader.success:
            # Shader didn't compile, just render an ellipse.
            dot_fbo.shader.fs = original_fs
            with dot_fbo:
                Ellipse(pos=(2, 2), size=(size[0]-4, size[1]-4))
        else:
            # Render a rectangle with the circle shader.
            border = 3.0
            dot_fbo['centre'] = (size[0] * 0.5, size[1] * 0.5)
            dot_fbo['radius'] = max(size[0] * 0.5 - border, 0.0)
            dot_fbo['border'] = border
            with dot_fbo:
                Rectangle(size=size)

        return dot_fbo

    @property
    def bounding_box(self):
        'Returns a square box (x, y, width, height) centred on this widget.'
        dim = min(self.width, self.height)
        half = dim / 2
        return (self.center_x - half, self.center_y - half, dim, dim)
