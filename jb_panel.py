import bpy
from bpy.types import Panel


class JB_PT_Panel(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Bake objects"
    bl_category = "JBake"

    def draw(self, context):

        layout = self.layout

        row = layout.row()
        row.prop(context.scene, "jbake_bake_to_copy", text="Bake to copy")

        if not context.scene.jbake_bake_to_copy:
            row = layout.row()
            split = row.split(factor=0.4, align=True)
            col = split.column()
            col.label(text='Low Poly')

            col = split.column()
            col.prop(context.scene, "jbake_low_poly", text="")

        row = layout.row()
        split = row.split(factor=0.4, align=True)
        col = split.column()
        col.label(text='High Poly')

        col = split.column()
        col.prop(context.scene, "jbake_high_poly", text="")

        row = layout.row()
        row.operator('object.jbake_bake_op', text='Bake maps', icon='MOD_BOOLEAN')


class JB_PT_Settings_Panel(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Bake settings"
    bl_category = "JBake"

    def draw(self, context):

        layout = self.layout
        scene = context.scene

        row = layout.row()
        row.prop(context.scene.render.bake, "cage_extrusion", text="Extrusion")

        row = layout.row()
        row.prop(context.scene.render.bake,
                 "max_ray_distance", text="Max Ray Distance")

        row = layout.row()
        col = row.column()
        col.prop(context.scene, "img_bake_width", text="Width")

        col = row.column()
        col.prop(context.scene, "img_bake_height", text="Height")

        row = layout.row()
        row.prop(context.scene.render.bake, "use_cage", text="Use Cage")

        if context.scene.render.bake.use_cage:
            row = layout.row()
            split = row.split(factor=0.4, align=True)
            col = split.column()
            col.label(text='Cage Object')

            col = split.column()
            col.prop(context.scene.render.bake, "cage_object", text="")

        if context.scene.jbake_bake_to_copy:
            row = layout.row()
            row.prop(context.scene, "jbake_decimation_mode", text="Decimation Mode")
            if context.scene.jbake_decimation_mode == 'Remesh':
                row = layout.row()
                row.prop(
                    context.scene.jbake_high_poly.data, "remesh_voxel_size",
                    text="Voxel Size")
            else:
                row = layout.row()
                row.prop(
                    context.scene, "jbake_decimation_ratio",
                    text="Decimation Ratio")