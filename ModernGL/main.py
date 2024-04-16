from moderngl_window.context.base import KeyModifiers
from pyrr import Matrix44
import moderngl
from _example import Example
from math import sin


class LoadingOBJ(Example):
    title = "Loading OBJ"
    gl_version = (3, 3)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.obj = self.load_scene('Sting-Sword-lowpoly.obj')
        self.texture = self.load_texture_2d('Sting_Base_Color.png')

        self.prog = self.ctx.program(
            vertex_shader='''
                #version 330

                uniform mat4 Mvp;

                in vec3 in_position;
                in vec3 in_normal;
                in vec2 in_texcoord_0;

                out vec3 v_vert;
                out vec3 v_norm;
                out vec2 v_text;

                void main() {
                    v_vert = in_position;
                    v_norm = in_normal;
                    v_text = in_texcoord_0;
                    gl_Position = Mvp * vec4(in_position, 1.0);
                }
            ''',
            fragment_shader='''
                #version 330

                uniform sampler2D Texture;
                uniform vec4 Color;
                uniform vec3 Light;

                in vec3 v_vert;
                in vec3 v_norm;
                in vec2 v_text;

                out vec4 f_color;

                void main() {
                    float lum = dot(normalize(v_norm), normalize(v_vert - Light));
                    lum = acos(lum) / 3.14159265;
                    lum = clamp(lum, 0.0, 1.0);
                    lum = lum * lum;
                    lum = smoothstep(0.0, 1.0, lum);
                    lum *= smoothstep(0.0, 80.0, v_vert.z) * 0.3 + 0.7;
                    lum = lum * 0.8 + 0.2;

                    vec3 color = texture(Texture, v_text).rgb;
                    color = color * (1.0 - Color.a) + Color.rgb * Color.a;
                    f_color = vec4(color * lum, 1.0);
                }
            ''',
        )

        self.light = self.prog['Light']
        self.color = self.prog['Color']
        self.mvp = self.prog['Mvp']

        # Create a vao from the first root node (attribs are auto mapped)
        self.vao = self.obj.root_nodes[0].mesh.vao.instance(self.prog)

        # Some coords for movement
        self._x, self._y, self._z = 0.01, 0.01, 0.01        

        # Obj Speed
        self._speed = 5       
        

    def render(self, time, frame_time):
        self.ctx.clear(1.0, 1.0, 1.0)
        self.ctx.enable(moderngl.DEPTH_TEST)

        proj = Matrix44.perspective_projection(90, self.aspect_ratio, 0.1, 1000.0)
        lookat = Matrix44.look_at(
            (self._x, self._y, self._z),
            (0.0, 0.0, 65),
            (1.0, 0.0, 0.0),
        )

        self.light.value = (self._x, self._y, self._z)
        self.color.value = (1.0, 1.0, 1.0, 0.25)
        # self.mvp.write((proj * lookat).astype('f4'))

        
        self.vao.render()
        rot = Matrix44.from_eulers((time / 2, time / 3, time / 4), dtype='f4')
        self.texture.use(location=1)
        self.obj.draw(proj, Matrix44.from_translation((self._x, self._y, self._z), dtype='f4') * rot)
        
        self.wnd.title = f'Frame time: {frame_time}'
        
                 
    def key_event(self, key, action, modifiers):
        if action == self.wnd.keys.ACTION_PRESS:
            if key == self.wnd.keys.W:
                self._z += self._speed
            elif key == self.wnd.keys.S:
                self._z -= self._speed
            elif key == self.wnd.keys.A:
                self._y += self._speed
            elif key == self.wnd.keys.D:
                self._y -= self._speed
            elif key == self.wnd.keys.Q:
                self._x += self._speed
            elif key == self.wnd.keys.E:
                self._x -= self._speed


if __name__ == '__main__':
    LoadingOBJ.run()
