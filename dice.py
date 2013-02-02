from kivy.uix.widget import Widget
from kivy.properties import NumericProperty
from kivy.graphics import Ellipse, Line, Fbo, Rectangle


header = '''
#ifdef GL_ES
precision highp float;
#endif

/* Outputs from the vertex shader */
varying vec4 frag_color;
varying vec2 tex_coord0;

/* uniform texture samplers */
uniform sampler2D texture0;
'''


blur_shader = header + '''
uniform vec2 resolution;
uniform float time;

void main(void)
{
    vec2 coord = tex_coord0.st;
    float blur_offset = 0.04;

    vec4 colour = vec4(0.0, 0.0, 0.0, 0.0);
    colour += texture2D(texture0, coord + vec2(-blur_offset, -blur_offset));
    colour += texture2D(texture0, coord + vec2(-blur_offset, 0.0));
    colour += texture2D(texture0, coord + vec2(-blur_offset, blur_offset));
    colour += texture2D(texture0, coord + vec2(0.0, -blur_offset));
    colour += texture2D(texture0, coord + vec2(0.0, 0.0));
    colour += texture2D(texture0, coord + vec2(0.0, blur_offset));
    colour += texture2D(texture0, coord + vec2(blur_offset, -blur_offset));
    colour += texture2D(texture0, coord + vec2(blur_offset, 0.0));
    colour += texture2D(texture0, coord + vec2(blur_offset, blur_offset));
    colour /= 9.0;

    gl_FragColor = colour;
}
'''


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
        # Render an antialiased dot using two frame buffer objects.
        # An ellipse is rendered into the first using geometry.
        # The first is then rendered into the second as a texture, using
        # a blurring shader.
        with self.canvas:
            geometry_fbo = Fbo(size=(512, 512))
            blurred_fbo = Fbo(size=size)

        with geometry_fbo:
            Ellipse(pos=(2, 2), size=(507, 507))
        
        # Install the shader, but fallback to the default shader if it
        # does not compile.
        original_fs = blurred_fbo.shader.fs
        blurred_fbo.shader.fs = blur_shader
        if not blurred_fbo.shader.success:
            blurred_fbo.shader.fs = original_fs

        with blurred_fbo:
            Rectangle(size=size, texture=geometry_fbo.texture)
        
        return blurred_fbo

    @property
    def bounding_box(self):
        'Returns a square box (x, y, width, height) centred on this widget.'
        dim = min(self.width, self.height)
        half = dim / 2
        return (self.center_x - half, self.center_y - half, dim, dim)
