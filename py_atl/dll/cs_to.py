"""
functions to convert objects from c# to python
"""

from System import Array, Single

from mathutils import Euler, Matrix


def bpy_matrix(mat4: Array[Single]) -> Matrix:
    if len(mat4) != 16:
        raise ValueError(f"Expected 16 elements, got {len(mat4)}")

    matrix: Matrix = Matrix((
        (mat4[0],  mat4[1],  mat4[2],  mat4[3]),
        (mat4[4],  mat4[5],  mat4[6],  mat4[7]),
        (mat4[8],  mat4[9],  mat4[10], mat4[11]),
        (mat4[12], mat4[13], mat4[14], mat4[15])
    ))

    return matrix


def bpy_euler(vec3: Array[Single]) -> Euler:
    if len(vec3) != 3:
        raise ValueError(f"Expected 3 elements, got {len(vec3)}")

    euler: Euler = Euler((vec3[0],  vec3[1],  vec3[2]))

    return euler
