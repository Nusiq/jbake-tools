# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from .jb_operators import *
from .jb_panel import *
from bpy.props import *
import bpy
bl_info = {
    "name": "JBake Tools",
    "author": "Jayanam",
    "description": "Blender Addon to simplify baking image maps",
    "blender": (2, 80, 0),
    "version": (0, 3, 0, 3),
    "location": "View3D",
    "category": "Object"
}

# Blender imports


# Low poly object to bake onto
bpy.types.Scene.jbake_low_poly = PointerProperty(type=bpy.types.Object)

# High poly object with the details to bake
bpy.types.Scene.jbake_high_poly = PointerProperty(type=bpy.types.Object)

# Bake to copy settings
bpy.types.Scene.jbake_bake_to_copy = BoolProperty(default=False)
bpy.types.Scene.jbake_decimation_mode = EnumProperty(
    items=[
        ("Remesh", "Remesh", "Remesh"),
        ("Decimate", "Decimate", "Decimate")
    ]
)
bpy.types.Scene.jbake_decimation_ratio = FloatProperty(
    name="Decimation Ratio",
    min=0.0, max=1.0, default=0.5
)
#   data.remesh_voxel_size



bpy.types.Scene.img_bake_width = bpy.props.IntProperty(
    name="Image Width",  description="Width of image to bake", default=2048)
bpy.types.Scene.img_bake_height = bpy.props.IntProperty(
    name="Image Height", description="Height of image to bake", default=2048)

classes = (JB_Bake_Op, JB_PT_Panel, JB_PT_Settings_Panel)


def register():
    for c in classes:
        bpy.utils.register_class(c)


def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)
