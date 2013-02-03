
circle_vertex_shader = '''
#ifdef GL_ES
    precision highp float;
#endif

/* Outputs to the fragment shader */
varying vec4 frag_position;
varying vec4 frag_color;
varying vec2 tex_coord0;

/* vertex attributes */
attribute vec2     vPosition;
attribute vec2     vTexCoords0;

/* uniform variables */
uniform mat4       modelview_mat;
uniform mat4       projection_mat;
uniform vec4       color;
uniform float      opacity;

void main (void) {
  frag_color = color * vec4(1.0, 1.0, 1.0, opacity);
  tex_coord0 = vTexCoords0;
  frag_position = vec4(vPosition.xy, 0.0, 1.0);
  gl_Position = projection_mat * modelview_mat * vec4(vPosition.xy, 0.0, 1.0);
}
'''

fs_header = '''
#ifdef GL_ES
precision highp float;
#endif

/* Outputs from the vertex shader */
varying vec4 frag_color;
varying vec2 tex_coord0;
varying vec4 frag_position;

/* uniform texture samplers */
uniform sampler2D texture0;
'''


circle_fragment_shader = fs_header + '''
uniform vec2 centre;
uniform float radius;
uniform float border;

void main(void)
{
    vec4 colour = texture2D(texture0, tex_coord0);
    vec2 delta = frag_position.xy - centre;
    float dist = pow(delta.x*delta.x + delta.y*delta.y, 0.5);
    if (dist > radius)
    {
        dist -= radius;
        if (dist < border)
            colour[3] *= cos(dist / border * 1.5707963267);
        else
            colour[3] = 0.0;
    }
    gl_FragColor = colour;
}
'''
