import json
import numpy as np
import pyautogui

class Vec2:
    def __init__(self):
        pass

class Vec3:
    def __init__(self, x, y, z):
        pass

class Mat4:
    def __init__(self):
        pass

    def translation_matrix(vec3):
        mat4 = np.identity(4)
        mat4[0][3] = vec3[0]
        mat4[1][3] = vec3[1]
        mat4[2][3] = vec3[2]

        return mat4
    
    def scale_matrix(vec3):
        mat4 = np.identity(4)
        mat4[0][0] = vec3[0]
        mat4[1][1] = vec3[1]
        mat4[2][2] = vec3[2]

        return mat4
    
    def rotation_matrix(vec3):
        return np.identity(4)

class Node:
    def __init__(self, config):
        self._anchor = config["AnchorPoint"]
        self._position = config["Position"]
        self._left_margin = config["LeftMargin"]
        self._right_margin = config["RightMargin"]
        self._top_margin = config["TopMargin"]
        self._bottom_margin = config["BottomMargin"]
        self._size = config["Size"]
        self._scale = config["Scale"]
        self._name = config["Name"]
        self._children = []
        self._parent = None

        self._position = np.array([self._position["X"], self._position["Y"], 0])
        self._rotation = np.array([0, 0, 0])
        self._scale = np.array([self._scale["ScaleX"], self._scale["ScaleY"], 0])

        if "Children" in config:
            for child_config in config["Children"]:
                child = Node(child_config)
                self._children.append(child)
                child._parent = self
    
    def __str__(self) -> str:
        return "".join(
            "name: " + str(self._name) +
            ", anchor: " + str(self._anchor) +
            ", position: " + str(self._position) +
            ", rotation: " + str(self._rotation) +
            ", size: " + str(self._size) +
            ", scale: " + str(self._scale)
        )

    def convert_to_world_space(self, vec3):
        mat4 = self.get_node_to_world_transform()
        vec4 = np.array([-vec3[0], -vec3[1], -vec3[2], 1.0])

        vec4 = mat4.dot(vec4)

        return np.array([vec4[0], vec4[1], vec4[2]])

    def get_node_to_world_transform(self):
        mat4 = Mat4.translation_matrix(self._position) # transform matrix (not including rotation & scale)

        return mat4

def load_ui():
    f = open("scene_login.json")
    data = json.load(f)
    f.close()

    layer = data["Content"]["Content"]["ObjectData"]
    layer_size = layer["Size"]

    img_bg = Node(layer["Children"][0])
    print(img_bg)

    for child in img_bg._children:
        if child._name == "btnLogin":
            child_node_position = child._position
            child_world_position = img_bg.convert_to_world_space(child_node_position)

            print(child_node_position, child_world_position)



            return child_world_position

            # img_bg_left_margin = img_bg._left_margin
            # img_bg_top_margin = img_bg._top_margin

            # btn_left_margin = child._left_margin
            # btn_top_margin = child._top_margin

            # left_margin = img_bg_left_margin - btn_left_margin
            # top_margin = img_bg_top_margin + btn_top_margin + 50

            # return np.array([left_margin, top_margin])

if __name__ == '__main__':
    position = load_ui()

    pyautogui.moveTo(position[0], position[1])
    # pyautogui.click()

    # vec3 = np.array([10, 0, 0])

    # translation_matrix = Mat4.translation_matrix(vec3)
    # scale_matrix = Mat4.scale_matrix(vec3)
    # rotation_matrix = Mat4.rotation_matrix(vec3)

    # print(translation_matrix, '\n\n', scale_matrix, '\n\n', rotation_matrix)