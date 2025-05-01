import moderngl
from array import array
import sys
from conf import *

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.OPENGL | pygame.DOUBLEBUF)

vert_shader = '''
#version 330 core

in vec2 vert;
in vec2 texcoord;
out vec2 uvs;

void main() {
    uvs = texcoord;
    gl_Position = vec4(vert, 0.0, 1.0);
}
'''

frag_shader = '''
#version 330 core

uniform sampler2D sceneTexture;

uniform float weight[5] = float[](0.227027, 0.1945946, 0.1216216, 0.054054, 0.016216);

in vec2 uvs;
out vec4 fragColor;


void main() {

	vec2 texOffset = 1.0 / textureSize(sceneTexture, 0);

	vec3 originalColor = texture(sceneTexture, uvs).rgb;
	vec3 newColor = originalColor * (weight[0]*weight[0]);
	int N = 5;
	for(int i=1;i<N;++i)for(int j=1;j<N;++j)
	{
		vec2 ri = vec2(texOffset.x , 0.0);
		vec2 rj = vec2(0.0, texOffset.y);
		newColor += texture(sceneTexture, uvs + i*ri + j*rj).rgb * weight[i] * weight[j];
		newColor += texture(sceneTexture, uvs - i*ri + j*rj).rgb * weight[i] * weight[j];
		newColor += texture(sceneTexture, uvs + i*ri - j*rj).rgb * weight[i] * weight[j];
		newColor += texture(sceneTexture, uvs - i*ri - j*rj).rgb * weight[i] * weight[j];
	}
	fragColor = vec4(4*(newColor.x+newColor.y+newColor.z)*newColor.xyz+originalColor, 1.0);

	// vec2 r = uvs.xy;
    // fragColor = vec4(texture(sceneTexture, r.xy).rgb, 1.0);
}
'''

ctx = moderngl.create_context()
quad_buffer = ctx.buffer(data=array('f', [
    # position (x, y), uv coords (x, y)
    -1.0, 1.0, 0.0, 0.0,  # topleft
    1.0, 1.0, 1.0, 0.0,   # topright
    -1.0, -1.0, 0.0, 1.0, # bottomleft
    1.0, -1.0, 1.0, 1.0,  # bottomright
]))
program = ctx.program(vertex_shader=vert_shader, fragment_shader=frag_shader)
render_object = ctx.vertex_array(program, [(quad_buffer, '2f 2f', 'vert', 'texcoord')])

def surf_to_texture(surf):
    tex = ctx.texture(surf.get_size(), 4)
    tex.filter = (moderngl.NEAREST, moderngl.NEAREST)
    tex.swizzle = 'BGRA'
    tex.write(surf.get_view('1'))
    return tex