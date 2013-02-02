
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


circle_shader = header + '''
uniform vec2 centre;
uniform float radius;
uniform float border;

void main(void)
{
    vec4 colour = texture2D(texture0, tex_coord0);
    vec2 delta = gl_FragCoord.xy - centre;
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
