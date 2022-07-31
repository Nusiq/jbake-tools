import bpy
from bpy.types import Operator

from . utils.select_utils import *


class JB_Bake_Op(Operator):
    bl_idname = "object.jbake_bake_op"
    bl_label = "Bake maps"
    bl_description = "Bake image maps for low and high poly objects"
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        low_poly = context.scene.jbake_low_poly
        high_poly = context.scene.jbake_high_poly
        bake_to_copy = context.scene.jbake_bake_to_copy
        return (low_poly or bake_to_copy) and high_poly

    def add_link(self, node_tree, node, node2, output_name, input_name, non_color_data=False):
        '''
        Links two nodes in the node tree.
        '''
        node_tree.links.new(
            node.outputs[output_name], node2.inputs[input_name])

        if(hasattr(node, "color_space")):
            if(non_color_data):
                node.color_space = "NONE"
            else:
                node.color_space = "COLOR"

    def create_normal_img_node(self, node_tree):
        '''
        Image texture node for the normal map.
        '''
        img_node = node_tree.nodes.new('ShaderNodeTexImage')
        img_name = bpy.context.scene.jbake_low_poly.name + "_" + "normal"
        img_width = bpy.context.scene.img_bake_width
        img_height = bpy.context.scene.img_bake_height

        image = bpy.data.images.new(
            img_name, width=img_width, height=img_height)
        image.colorspace_settings.name = "Non-Color"

        img_node.image = image
        return img_node

    def create_normal_map_node(self, node_tree):
        '''
        Creates a nomral map image node.
        '''
        return node_tree.nodes.new('ShaderNodeNormalMap')

    def get_node(self, node_type, node_tree):
        '''
        Finds node in node tree by its type, or returns None if not found.
        '''
        for node in node_tree.nodes:
            if node.type == node_type:
                return node

        return None

    def bake_normal_map(self):
        '''
        Runs the bake normal map operator.
        '''
        bpy.ops.object.bake(type="NORMAL", use_selected_to_active=True)

    def execute(self, context):
        if context.scene.jbake_bake_to_copy:
            self.make_low_poly_copy(context)
        low_poly = context.scene.jbake_low_poly
        high_poly = context.scene.jbake_high_poly

        if len(low_poly.data.materials) == 0:
            err_material = "Assign a material to {0} before baking"
            self.report({'ERROR'}, err_material.format(low_poly.name))
            return {'CANCELLED'}

        node_tree = low_poly.data.materials[0].node_tree

        # Bake the image maps from high poly to low poly

        # 1. Check if the low poly object has a principled shader
        pri_shader_node = self.get_node("BSDF_PRINCIPLED", node_tree)
        if(pri_shader_node is None):
            return {'CANCELLED'}

        # Use Cycles as renderer
        render_engine_old = bpy.context.scene.render.engine
        bpy.context.scene.render.engine = 'CYCLES'

        low_poly.hide_set(False)
        low_poly.select_set(True)
        bpy.ops.object.mode_set(mode='OBJECT')

        self.create_normal_map(node_tree, pri_shader_node)

        hp_hide = high_poly.hide_get()
        high_poly.hide_set(False)
        high_poly.select_set(True)
        low_poly.select_set(True)

        make_active(low_poly)

        self.bake_normal_map()

        high_poly.hide_set(hp_hide)

        deselect_all()

        # reset render engine
        bpy.context.scene.render.engine = render_engine_old

        return {'FINISHED'}

    def create_normal_map(self, node_tree, pri_shader_node):
        '''
        Creates a normal map and image, if it's not attached to the material
        of the model already.
        '''
        # 2. Check if there is a normal map attached already.
        #    If not, create a normal map and attach it
        normal_map_node = None
        if not pri_shader_node.inputs["Normal"].is_linked:
            normal_map_node = self.create_normal_map_node(node_tree)
            self.add_link(node_tree, normal_map_node,
                          pri_shader_node, "Normal", "Normal")
        else:
            normal_map_node = pri_shader_node.inputs["Normal"].links[0].from_node

        # 3. Now check if the normal map has an image texture assigned
        #    If not, create an image texture node and attach it
        normal_img_node = None
        if not normal_map_node.inputs["Color"].is_linked:
            normal_img_node = self.create_normal_img_node(node_tree)
            self.add_link(node_tree, normal_img_node,
                          normal_map_node, "Color", "Color", True)
        else:
            normal_img_node = normal_map_node.inputs["Color"].links[0].from_node

    def make_low_poly_copy(self, context):
        # Make the copy of the high poly object
        high_poly = context.scene.jbake_high_poly
        high_poly.hide_set(False)
        high_poly.select_set(True)
        make_active(high_poly)
        duplicate_object()
        context.scene.jbake_low_poly = get_active()
        # Add a material to the copy
        add_material()

        # Decimate/remesh the copied object
        if context.scene.jbake_decimation_mode == 'Remesh':
            to_sculpt()
            remesh()
            to_object()
        else:
            to_edit()
            select_mesh()
            decimate(context.scene.jbake_decimation_ratio)
            to_object()
        # Map UV of the copy
        to_edit()
        select_mesh()
        map_uv()
        to_object()
