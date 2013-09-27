# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# <pep8 compliant>

import bpy
from bpy.types import Header, Menu
import os
import getpass
from platform import system as currentOS
path = ""

class INFO_HT_header(Header):
    bl_space_type = 'INFO'

    def draw(self, context):
        global path
        layout = self.layout
        
        window = context.window
        scene = context.scene
        rd = scene.render 
        toolsettings = context.tool_settings 
        row = layout.column(align=True)
        sub = row.row(align=True)
        sub.template_header()
        if context.area.show_menus:
            sub.menu("INFO_MT_file")
            sub.menu("INFO_MT_edit")
            sub.menu("INFO_MT_edit_mesh")
            sub.menu("INFO_MT_add")
            if rd.use_game_engine:
                sub.menu("INFO_MT_game")
            else:
                sub.menu("INFO_MT_render")
            sub.menu("INFO_MT_window")
            sub.menu("INFO_MT_help")
        sub.separator()
        sub.separator()
        sub.separator()              

        if rd.has_multiple_engines:
            sub.prop(rd, "engine", text="")

        sub.separator()

        sub.template_running_jobs()

        sub.template_reports_banner()
        

        sub.operator("wm.splash", text="", icon='BLENDER', emboss=False)
        sub.label(text=scene.statistics(), translate=False)
        row.separator()
        
        row1 = row.row(align=True) 
        row1.scale_y = 1.2  
        row1.scale_x = 1.2
        #row1.alignment = 'CENTER'        
        row1.operator("wm.read_homefile",text="", icon='NEW')
        row1.operator("wm.open_mainfile",text="", icon='FILE_FOLDER')
        row1.operator("wm.save_mainfile", text="", icon='SAVE')
        row1.separator()
        row1.separator()
        row1.operator("ed.undo", text="", icon='UNDO')
        row1.operator("ed.redo",text="", icon='REDO')
        row1.separator()
        row1.separator()
        row1.template_ID(context.window, "screen", new="screen.new", unlink="screen.delete")
        row1.separator()
        row1.separator()
        row1.template_ID(context.screen, "scene", new="scene.new", unlink="scene.delete")
        row1.separator()
        row1.separator()
        row1.operator("render.opengl", text="", icon='RENDER_STILL')
        props = row1.operator("render.opengl", text="", icon='RENDER_ANIMATION')
        props.animation = True    
        row1.separator()
        row1.separator()
        row1.operator("anim.update_data_paths", text="", icon='QUESTION')
        row1.operator("wm.url_open", text="", icon='HELP').url = "http://wiki.blender.org/index.php/Doc:2.6/Manual"                 
        row.separator()
        row2 = row.row(align=True)              
        row2.prop(toolsettings, 'tool_shelf', expand = True)
        opts = toolsettings.tool_shelf
        #row4 = row.row(align=True)
        box = row.box()
        box.scale_x = 0.8
        row3 = box.row(align=True)        
        row3.scale_y = 1.3
        row3.scale_x = 1.5
        if opts == 'MESH':                         
              row3.operator("mesh.primitive_plane_add", text="",icon='MESH_PLANE', emboss=False)              
              row3.operator("mesh.primitive_cube_add",text="", icon='MESH_CUBE', emboss=False)              
              row3.operator("mesh.primitive_circle_add",text="", icon='MESH_CIRCLE', emboss=False)              
              row3.operator("mesh.primitive_uv_sphere_add",text="", icon='MESH_UVSPHERE', emboss=False)              
              row3.operator("mesh.primitive_ico_sphere_add",text="", icon='MESH_ICOSPHERE', emboss=False)              
              row3.operator("mesh.primitive_cylinder_add",text="", icon='MESH_CYLINDER', emboss=False)              
              row3.operator("mesh.primitive_cone_add",text="", icon='MESH_CONE', emboss=False)              
              row3.operator("mesh.primitive_grid_add",text="", icon='MESH_GRID', emboss=False)              
              row3.operator("mesh.primitive_monkey_add",text="", icon='MESH_MONKEY', emboss=False)              
              row3.operator("mesh.primitive_torus_add",text="", icon='MESH_TORUS', emboss=False)   
              
        elif opts == 'CURVE':                                                  
              row3.operator("curve.primitive_bezier_curve_add", icon='CURVE_BEZCURVE', text="", emboss=False)              
              row3.operator("curve.primitive_bezier_circle_add", icon='CURVE_BEZCIRCLE', text="", emboss=False)              
              row3.operator("curve.primitive_nurbs_curve_add", icon='CURVE_NCURVE', text="", emboss=False)              
              row3.operator("curve.primitive_nurbs_circle_add", icon='CURVE_NCIRCLE', text="", emboss=False)              
              row3.operator("curve.primitive_nurbs_path_add", icon='CURVE_PATH', text="", emboss=False)
        elif opts == 'SURFACE':              
              row3.operator("surface.primitive_nurbs_surface_curve_add", icon='SURFACE_NCURVE', text="", emboss=False)              
              row3.operator("surface.primitive_nurbs_surface_circle_add", icon='SURFACE_NCIRCLE', text="", emboss=False)              
              row3.operator("surface.primitive_nurbs_surface_surface_add", icon='SURFACE_NSURFACE', text="", emboss=False)              
              row3.operator("surface.primitive_nurbs_surface_cylinder_add", icon='SURFACE_NCYLINDER', text="", emboss=False)              
              row3.operator("surface.primitive_nurbs_surface_sphere_add", icon='SURFACE_NSPHERE', text="", emboss=False)              
              row3.operator("surface.primitive_nurbs_surface_torus_add", icon='SURFACE_NTORUS', text="", emboss=False)
        elif opts == 'METABALL':            
              row3.operator("object.metaball_add", text="", icon='META_BALL', emboss=False).type = 'BALL'
              row3.separator()
              row3.operator("object.metaball_add", text="", icon='META_CAPSULE', emboss=False).type = 'CAPSULE'
              row3.separator()
              row3.operator("object.metaball_add", text="", icon='META_PLANE', emboss=False).type = 'PLANE'
              row3.separator()
              row3.operator("object.metaball_add", text="", icon='META_ELLIPSOID', emboss=False).type = 'ELLIPSOID'
              row3.separator()
              row3.operator("object.metaball_add", text="", icon='META_CUBE', emboss=False).type = 'CUBE'            
        elif opts == 'TEXT':           
              row3.operator("object.text_add", text="", icon='OUTLINER_OB_FONT', emboss=False)
        elif opts == 'ARMATURE':              
              row3.operator("object.armature_add", text="", icon='BONE_DATA', emboss=False)
        elif opts == 'LATTICE':       
              row3.operator("object.add", text="", icon='OUTLINER_OB_LATTICE', emboss=False).type = 'LATTICE'
        elif opts == 'EMPTY':             
              row3.operator("object.add", text="", icon='EMP_PLAINAXES', emboss=False).type = 'EMPTY'
              row3.separator()
              row3.operator("object.empty_add", text="", icon='EMP_ARROWS', emboss=False).type = 'ARROWS'
              row3.separator()
              row3.operator("object.empty_add", text="", icon='EMP_SINGLEARROW', emboss=False).type = 'SINGLE_ARROW'
              row3.separator()
              row3.operator("object.empty_add", text="", icon='EMP_CIRCLE', emboss=False).type = 'CIRCLE'
              row3.separator()
              row3.operator("object.empty_add", text="", icon='EMP_CUBE', emboss=False).type = 'CUBE'
              row3.separator()
              row3.operator("object.empty_add", text="", icon='EMP_SPHERE', emboss=False).type = 'SPHERE'
              row3.separator()
              row3.operator("object.empty_add", text="", icon='EMP_CONE', emboss=False).type = 'CONE'
              row3.separator()
              row3.operator("object.empty_add", text="", icon='EMP_IMAGE', emboss=False).type = 'IMAGE'              
        elif opts == 'SPEAKER':             
              row3.operator("object.speaker_add", text="", icon='OUTLINER_OB_SPEAKER', emboss=False)
        elif opts == 'CAMERA':           
              row3.operator("object.camera_add", text="", icon='OUTLINER_OB_CAMERA', emboss=False)
        elif opts == 'LAMP':             
              row3.operator("object.lamp_add", text="", icon='LAMP_POINT', emboss=False).type = 'POINT'
              row3.separator()
              row3.operator("object.lamp_add", text="", icon='LAMP_SUN', emboss=False).type = 'SUN'
              row3.separator()
              row3.operator("object.lamp_add", text="", icon='LAMP_SPOT', emboss=False).type = 'SPOT'
              row3.separator()
              row3.operator("object.lamp_add", text="", icon='LAMP_HEMI', emboss=False).type = 'HEMI'
              row3.separator()
              row3.operator("object.lamp_add", text="", icon='LAMP_AREA', emboss=False).type = 'AREA'
        elif opts == 'FORCE':              
              row3.operator("object.effector_add", text="", icon='FORCE_TEXTURE', emboss=False).type = 'TEXTURE'
              row3.separator()
              row3.operator("object.effector_add", text="", icon='FORCE_CURVE', emboss=False).type = 'GUIDE'
              row3.separator()
              row3.operator("object.effector_add", text="", icon='FORCE_BOID', emboss=False).type = 'BOID'
              row3.separator()
              row3.operator("object.effector_add", text="", icon='FORCE_TURBULENCE', emboss=False).type = 'TURBULENCE'
              row3.separator()
              row3.operator("object.effector_add", text="", icon='FORCE_DRAG', emboss=False).type = 'DRAG'
              row3.separator()
              row3.operator("object.effector_add", text="", icon='FORCE_FORCE', emboss=False).type = 'FORCE'
              row3.separator()
              row3.operator("object.effector_add", text="", icon='FORCE_WIND', emboss=False).type = 'WIND'
              row3.separator()
              row3.operator("object.effector_add", text="", icon='FORCE_VORTEX', emboss=False).type = 'VORTEX'
              row3.separator()
              row3.operator("object.effector_add", text="", icon='FORCE_MAGNETIC', emboss=False).type = 'MAGNET'
              row3.separator()
              row3.operator("object.effector_add", text="", icon='FORCE_HARMONIC', emboss=False).type = 'HARMONIC'
              row3.separator()
              row3.operator("object.effector_add", text="", icon='FORCE_CHARGE', emboss=False).type = 'CHARGE'
              row3.separator()
              row3.operator("object.effector_add", text="", icon='FORCE_LENNARDJONES', emboss=False).type = 'LENNARDJONES' 
        elif opts == 'CUSTOM':
               row3.scale_y = 1.3
               row3.scale_x = 1.3 
               row3.alignment = 'LEFT'
               file_name = "custom"
               name = getpass.getuser()
               path2 = "/home/" + name
               if not os.path.exists(path2): os.makedirs(path2)
               path2 = path2 + '/.config/'
               if not os.path.exists(path2): os.makedirs(path2)
               path2 = path2 + 'custom'
               if not os.path.exists(path2): os.makedirs(path2)
               path = path2 
               path = os.path.join(path,file_name)
               f = open('/tmp/path','w')
               f.write(path)  
               if os.path.isfile(path): 
                with open(path,'r') as f:
                 output = f.read()
                 if output=="":
                  row3.label("None")
                 else:
                  custom = output 
                  n = custom.split(',')
                  for a in n:             
                   if a == "mesh.primitive_plane_add":                  
                    row3.operator(a, text="", icon='MESH_PLANE', emboss=False) 
                   elif a == "mesh.primitive_cube_add":              
                    row3.operator(a,text="", icon='MESH_CUBE', emboss=False)   
                   elif a == "mesh.primitive_circle_add":           
                    row3.operator(a,text="", icon='MESH_CIRCLE', emboss=False)  
                   elif a == "mesh.primitive_uv_sphere_add":            
                    row3.operator(a,text="", icon='MESH_UVSPHERE', emboss=False) 
                   elif a == "mesh.primitive_ico_sphere_add":             
                    row3.operator(a,text="", icon='MESH_ICOSPHERE', emboss=False) 
                   elif a == "mesh.primitive_cylinder_add":             
                    row3.operator(a,text="", icon='MESH_CYLINDER', emboss=False)
                   elif a == "mesh.primitive_cone_add":              
                    row3.operator(a,text="", icon='MESH_CONE', emboss=False)
                   elif a == "mesh.primitive_grid_add":              
                    row3.operator(a,text="", icon='MESH_GRID', emboss=False) 
                   elif a == "mesh.primitive_monkey_add":             
                    row3.operator(a,text="", icon='MESH_MONKEY', emboss=False)
                   elif a == "mesh.primitive_torus_add":              
                    row3.operator(a,text="", icon='MESH_TORUS', emboss=False) 
                   elif a == "curve.primitive_bezier_curve_add":
                    row3.operator(a, icon='CURVE_BEZCURVE', text="", emboss=False)  
                   elif a == "curve.primitive_bezier_circle_add":            
                    row3.operator(a, icon='CURVE_BEZCIRCLE', text="", emboss=False)
                   elif a == "curve.primitive_nurbs_curve_add":              
                    row3.operator(a, icon='CURVE_NCURVE', text="", emboss=False)  
                   elif a == "curve.primitive_nurbs_circle_add":            
                    row3.operator(a, icon='CURVE_NCIRCLE', text="", emboss=False) 
                   elif a == "curve.primitive_nurbs_path_add":             
                    row3.operator(a, icon='CURVE_PATH', text="", emboss=False) 
                   elif a == "surface.primitive_nurbs_surface_curve_add":
                    row3.operator(a, icon='SURFACE_NCURVE', text="", emboss=False) 
                   elif a == "surface.primitive_nurbs_surface_circle_add":             
                    row3.operator(a, icon='SURFACE_NCIRCLE', text="", emboss=False) 
                   elif a == "surface.primitive_nurbs_surface_surface_add":             
                    row3.operator(a, icon='SURFACE_NSURFACE', text="", emboss=False)
                   elif a == "surface.primitive_nurbs_surface_cylinder_add":              
                    row3.operator(a, icon='SURFACE_NCYLINDER', text="", emboss=False) 
                   elif a == "surface.primitive_nurbs_surface_sphere_add":             
                    row3.operator(a, icon='SURFACE_NSPHERE', text="", emboss=False) 
                   elif a == "surface.primitive_nurbs_surface_torus_add":             
                    row3.operator(a, icon='SURFACE_NTORUS', text="", emboss=False)
                   elif a == "object.metaball_add": 
                    row3.operator(a, text="", icon='META_BALL', emboss=False)
                   elif a == "object.text_add":
                    row3.operator(a, text="", icon='OUTLINER_OB_FONT', emboss=False) 
                   elif a == "object.armature_add": 
                    row3.operator(a, text="", icon='BONE_DATA', emboss=False)
                   elif a == "object.add": 
                    row3.operator(a, text="", icon='OUTLINER_OB_LATTICE', emboss=False)
                   elif a == "object.empty_add": 
                    row3.operator(a, text="", icon='EMP_ARROWS', emboss=False)
                   elif a == "object.speaker_add": 
                    row3.operator(a, text="", icon='OUTLINER_OB_SPEAKER', emboss=False)
                   elif a == "object.camera_add": 
                    row3.operator(a, text="", icon='OUTLINER_OB_CAMERA', emboss=False)
                   elif a == "object.lamp_add": 
                    row3.operator(a, text="", icon='LAMP_POINT', emboss=False)
                   elif a == "object.effector_add": 
                    row3.operator(a, text="", icon='FORCE_TEXTURE', emboss=False)
                   else:   
                    row3.scale_x = 0.7                               
                    row3.operator(a) 
               else:
                  row3.label("None")
        elif opts == 'CUSTOM_DELETE':
                row3.scale_y = 1.3
                row3.scale_x = 1.0 
                row3.alignment = 'LEFT'
                row3.operator("wm.custom_clear_menu", text="Clear")

        # XXX: BEFORE RELEASE, MOVE FILE MENU OUT OF INFO!!!
        """
        sinfo = context.space_data
        row = layout.row(align=True)
        row.prop(sinfo, "show_report_debug", text="Debug")
        row.prop(sinfo, "show_report_info", text="Info")
        row.prop(sinfo, "show_report_operator", text="Operators")
        row.prop(sinfo, "show_report_warning", text="Warnings")
        row.prop(sinfo, "show_report_error", text="Errors")

        row = layout.row()
        row.enabled = sinfo.show_report_operator
        row.operator("info.report_replay")

        row.menu("INFO_MT_report")
        """



class INFO_MT_report(Menu):
    bl_label = "Report"

    def draw(self, context):
        layout = self.layout

        layout.operator("console.select_all_toggle")
        layout.operator("console.select_border")
        layout.operator("console.report_delete")
        layout.operator("console.report_copy")


class INFO_MT_file(Menu):
    bl_label = "File"

    def draw(self, context):
        layout = self.layout

        layout.operator_context = 'INVOKE_AREA'
        layout.operator("wm.read_homefile", text="New", icon='NEW')
        layout.operator("wm.open_mainfile", text="Open...", icon='FILE_FOLDER')
        layout.menu("INFO_MT_file_open_recent", icon='OPEN_RECENT')
        layout.operator("wm.recover_last_session", icon='RECOVER_LAST')
        layout.operator("wm.recover_auto_save", text="Recover Auto Save...", icon='RECOVER_AUTO')

        layout.separator()

        layout.operator_context = 'EXEC_AREA' if context.blend_data.is_saved else 'INVOKE_AREA'
        layout.operator("wm.save_mainfile", text="Save", icon='FILE_TICK')

        layout.operator_context = 'INVOKE_AREA'
        layout.operator("wm.save_as_mainfile", text="Save As...", icon='SAVE_AS')
        
        layout.separator()
        layout.operator(Production_Folder.bl_idname,text="Create Production", icon="FILESEL")
        if pfopath != "":
            layout.operator(Show_Production_Folder.bl_idname,text="Show Production", icon="SHOW_PRODUCTION")
            layout.operator(Set_Production_Folder.bl_idname,text="Set Production", icon="SAVE")
        
        layout.separator()
        layout.operator_context = 'INVOKE_AREA'
        layout.operator("wm.save_as_mainfile", text="Save Copy...", icon='SAVE_COPY').copy = True

        layout.separator()

        layout.operator("screen.userpref_show", text="User Preferences...", icon='PREFERENCES')

        layout.operator_context = 'INVOKE_AREA'
        layout.operator("wm.save_homefile", icon='SAVE_PREFS')
        layout.operator_context = 'EXEC_AREA'
        layout.operator("wm.read_factory_settings", icon='LOAD_FACTORY')

        layout.separator()

        layout.operator_context = 'INVOKE_AREA'
        layout.operator("wm.link_append", text="Link", icon='LINK_BLEND')
        props = layout.operator("wm.link_append", text="Append", icon='APPEND_BLEND')
        props.link = False
        props.instance_groups = False

        layout.separator()

        layout.menu("INFO_MT_file_import", icon='IMPORT')
        layout.menu("INFO_MT_file_export", icon='EXPORT')

        layout.separator()

        layout.menu("INFO_MT_file_external_data", icon='EXTERNAL_DATA')

        layout.separator()

        layout.operator_context = 'EXEC_AREA'
        layout.operator("wm.quit_blender", text="Quit", icon='QUIT')


class INFO_MT_file_import(Menu):
    bl_idname = "INFO_MT_file_import"
    bl_label = "Import"

    def draw(self, context):
        if bpy.app.build_options.collada:
            self.layout.operator("wm.collada_import", text="Collada (Default) (.dae)")


class INFO_MT_file_export(Menu):
    bl_idname = "INFO_MT_file_export"
    bl_label = "Export"

    def draw(self, context):
        if bpy.app.build_options.collada:
            self.layout.operator("wm.collada_export", text="Collada (Default) (.dae)")


class INFO_MT_file_external_data(Menu):
    bl_label = "External Data"

    def draw(self, context):
        layout = self.layout

        layout.operator("file.pack_all", text="Pack into .blend file")
        layout.operator("file.unpack_all", text="Unpack into Files")

        layout.separator()

        layout.operator("file.make_paths_relative")
        layout.operator("file.make_paths_absolute")
        layout.operator("file.report_missing_files")
        layout.operator("file.find_missing_files")


class INFO_MT_edit(Menu):
    bl_label = "Edit"

    def draw(self, context):
        layout = self.layout        
        
        layout.operator("ed.undo", text="Undo", icon='UNDO')
        layout.operator("ed.redo", text="Redo", icon='REDO')        
        layout.operator("screen.repeat_last", text="Repeat Action", icon='FILE_REFRESH')
        layout.operator("screen.repeat_history", text="History", icon='FILE')
        layout.operator("duplicate.selected", text="Duplicate|Shift D", icon='DUPLICATE')
        layout.operator("instance.selected", text="Instance|Alt D", icon='DUPLICATE')    
        props = layout.operator("object.freeze_transform_apply", text="Freeze Transform", icon='MANIPUL')
        props.location, props.rotation, props.scale = True, True, True     
        

class INFO_MT_edit_mesh(Menu):
    bl_label = "Edit Mesh"
    bl_context = "mesh_edit"

    def draw(self, context):
        layout = self.layout           
        
        layout.operator("extrudenormal.selected", text="Extrude|E")
        layout.menu("INFO_MT_edit_mesh_extrude_indiv")        
        layout.operator("mesh.bridge_edge_loops", text="Bridge|Ctrl E")
        layout.operator("mesh.edge_face_add",text="Make Edge/Face|F")        
        layout.operator("anim.keyframe_insert_menu", text="Insert Face|I")
        layout.operator("mesh.subdivide", text="Subdivide|W")
        layout.operator("mesh.unsubdivide", text="Un Subdivide|Ctrl E")
        layout.operator("transform.edge_slide", text="Edge Slide|Ctrl E")
        layout.operator("duplicate.selected", text="Duplicate Face|Shift D")
        layout.operator("mesh.merge", text="Merge|Ctrl M")
        layout.menu("INFO_MT_edit_mesh_delete", text="Delete|X")  
        layout.operator("mesh.bevel", text="Chamfer|Shift Ctrl B").vertex_only = True              
        layout.operator("mesh.bevel", text="Bevel|Ctrl B")  
        layout.operator("transform.edge_crease", text="Crease Tool|Shift E")                
        layout.operator("object.join", text="Join(Combine)|Ctrl J")
        layout.operator_menu_enum("mesh.separate", "type", text="Separate|P")
        layout.operator("mesh.fill", text="Fill Hole|F")
        layout.operator("mesh.remove_doubles", text="Clean Up|X")
        layout.operator("mesh.quads_convert_to_tris", text="Triangle|Ctrl T")
        layout.operator("mesh.tris_convert_to_quads", text="Quadrangulate|Alt J")
        layout.menu("INFO_MT_edit_mesh_mirror", text="Mirror|Ctrl M") 
                     


class INFO_MT_mesh_add(Menu):
    bl_idname = "INFO_MT_mesh_add"
    bl_label = "Mesh"

    def draw(self, context):
        layout = self.layout

        layout.operator_context = 'INVOKE_REGION_WIN'
        layout.operator("mesh.primitive_plane_add", icon='MESH_PLANE', text="Plane")
        layout.operator("mesh.primitive_cube_add", icon='MESH_CUBE', text="Cube")
        layout.operator("mesh.primitive_circle_add", icon='MESH_CIRCLE', text="Circle")
        layout.operator("mesh.primitive_uv_sphere_add", icon='MESH_UVSPHERE', text="UV Sphere")
        layout.operator("mesh.primitive_ico_sphere_add", icon='MESH_ICOSPHERE', text="Icosphere")
        layout.operator("mesh.primitive_cylinder_add", icon='MESH_CYLINDER', text="Cylinder")
        layout.operator("mesh.primitive_cone_add", icon='MESH_CONE', text="Cone")
        layout.separator()
        layout.operator("mesh.primitive_grid_add", icon='MESH_GRID', text="Grid")
        layout.operator("mesh.primitive_monkey_add", icon='MESH_MONKEY', text="Monkey")
        layout.operator("mesh.primitive_torus_add", icon='MESH_TORUS', text="Torus")


class INFO_MT_curve_add(Menu):
    bl_idname = "INFO_MT_curve_add"
    bl_label = "Curve"

    def draw(self, context):
        layout = self.layout

        layout.operator_context = 'EXEC_REGION_WIN'
        layout.operator("curve.primitive_bezier_curve_add", icon='CURVE_BEZCURVE', text="Bezier")
        layout.operator("curve.primitive_bezier_circle_add", icon='CURVE_BEZCIRCLE', text="Circle")
        layout.operator("curve.primitive_nurbs_curve_add", icon='CURVE_NCURVE', text="Nurbs Curve")
        layout.operator("curve.primitive_nurbs_circle_add", icon='CURVE_NCIRCLE', text="Nurbs Circle")
        layout.operator("curve.primitive_nurbs_path_add", icon='CURVE_PATH', text="Path")


class INFO_MT_surface_add(Menu):
    bl_idname = "INFO_MT_surface_add"
    bl_label = "Surface"

    def draw(self, context):
        layout = self.layout

        layout.operator_context = 'EXEC_REGION_WIN'
        layout.operator("surface.primitive_nurbs_surface_curve_add", icon='SURFACE_NCURVE', text="NURBS Curve")
        layout.operator("surface.primitive_nurbs_surface_circle_add", icon='SURFACE_NCIRCLE', text="NURBS Circle")
        layout.operator("surface.primitive_nurbs_surface_surface_add", icon='SURFACE_NSURFACE', text="NURBS Surface")
        layout.operator("surface.primitive_nurbs_surface_cylinder_add", icon='SURFACE_NCYLINDER', text="NURBS Cylinder")
        layout.operator("surface.primitive_nurbs_surface_sphere_add", icon='SURFACE_NSPHERE', text="NURBS Sphere")
        layout.operator("surface.primitive_nurbs_surface_torus_add", icon='SURFACE_NTORUS', text="NURBS Torus")


class INFO_MT_edit_curve_add(Menu):
    bl_idname = "INFO_MT_edit_curve_add"
    bl_label = "Add"

    def draw(self, context):
        is_surf = context.active_object.type == 'SURFACE'

        layout = self.layout
        layout.operator_context = 'EXEC_REGION_WIN'

        if is_surf:
            INFO_MT_surface_add.draw(self, context)
        else:
            INFO_MT_curve_add.draw(self, context)


class INFO_MT_armature_add(Menu):
    bl_idname = "INFO_MT_armature_add"
    bl_label = "Armature"

    def draw(self, context):
        layout = self.layout

        layout.operator_context = 'EXEC_REGION_WIN'
        layout.operator("object.armature_add", text="Single Bone", icon='BONE_DATA')


class INFO_MT_add(Menu):
    bl_label = "Add"

    def draw(self, context):
        layout = self.layout

        # note, don't use 'EXEC_SCREEN' or operators wont get the 'v3d' context.

        # Note: was EXEC_AREA, but this context does not have the 'rv3d', which prevents
        #       "align_view" to work on first call (see [#32719]).
        layout.operator_context = 'EXEC_REGION_WIN'

        #layout.operator_menu_enum("object.mesh_add", "type", text="Mesh", icon='OUTLINER_OB_MESH')
        layout.menu("INFO_MT_mesh_add", icon='OUTLINER_OB_MESH')

        #layout.operator_menu_enum("object.curve_add", "type", text="Curve", icon='OUTLINER_OB_CURVE')
        layout.menu("INFO_MT_curve_add", icon='OUTLINER_OB_CURVE')
        #layout.operator_menu_enum("object.surface_add", "type", text="Surface", icon='OUTLINER_OB_SURFACE')
        layout.menu("INFO_MT_surface_add", icon='OUTLINER_OB_SURFACE')
        layout.operator_menu_enum("object.metaball_add", "type", text="Metaball", icon='OUTLINER_OB_META')
        layout.operator("object.text_add", text="Text", icon='OUTLINER_OB_FONT')
        layout.separator()

        layout.menu("INFO_MT_armature_add", icon='OUTLINER_OB_ARMATURE')
        layout.operator("object.add", text="Lattice", icon='OUTLINER_OB_LATTICE').type = 'LATTICE'
        layout.operator_menu_enum("object.empty_add", "type", text="Empty", icon='OUTLINER_OB_EMPTY')
        layout.separator()

        layout.operator("object.speaker_add", text="Speaker", icon='OUTLINER_OB_SPEAKER')
        layout.separator()

        layout.operator("object.camera_add", text="Camera", icon='OUTLINER_OB_CAMERA')
        layout.operator_menu_enum("object.lamp_add", "type", text="Lamp", icon='OUTLINER_OB_LAMP')
        layout.separator()

        layout.operator_menu_enum("object.effector_add", "type", text="Force Field", icon='OUTLINER_OB_EMPTY')
        layout.separator()

        if len(bpy.data.groups) > 10:
            layout.operator_context = 'INVOKE_REGION_WIN'
            layout.operator("object.group_instance_add", text="Group Instance...", icon='OUTLINER_OB_EMPTY')
        else:
            layout.operator_menu_enum("object.group_instance_add", "group", text="Group Instance", icon='OUTLINER_OB_EMPTY')


class INFO_MT_game(Menu):
    bl_label = "Game"

    def draw(self, context):
        layout = self.layout

        gs = context.scene.game_settings

        layout.operator("view3d.game_start")

        layout.separator()

        layout.prop(gs, "show_debug_properties")
        layout.prop(gs, "show_framerate_profile")
        layout.prop(gs, "show_physics_visualization")
        layout.prop(gs, "use_deprecation_warnings")
        layout.prop(gs, "use_animation_record")
        layout.separator()
        layout.prop(gs, "use_auto_start")


class INFO_MT_render(Menu):
    bl_label = "Render"

    def draw(self, context):
        layout = self.layout

        layout.operator("render.render", text="Render Image", icon='RENDER_STILL')
        layout.operator("render.render", text="Render Animation", icon='RENDER_ANIMATION').animation = True

        layout.separator()

        layout.operator("render.opengl", text="OpenGL Render Image")
        layout.operator("render.opengl", text="OpenGL Render Animation").animation = True

        layout.separator()

        layout.operator("render.view_show")
        layout.operator("render.play_rendered_anim")


class INFO_MT_window(Menu):
    bl_label = "Window"

    def draw(self, context):
        import sys

        layout = self.layout

        layout.operator("wm.window_duplicate")
        layout.operator("wm.window_fullscreen_toggle", icon='FULLSCREEN_ENTER')

        layout.separator()

        layout.operator("screen.screenshot").full = True
        layout.operator("screen.screencast").full = True

        if sys.platform[:3] == "win":
            layout.separator()
            layout.operator("wm.console_toggle", icon='CONSOLE')


class INFO_MT_help(Menu):
    bl_label = "Help"

    def draw(self, context):
        layout = self.layout

        layout.operator("wm.url_open", text="Manual", icon='HELP').url = "http://wiki.blender.org/index.php/Doc:2.6/Manual"
        layout.operator("wm.url_open", text="Release Log", icon='URL').url = "http://www.blender.org/development/release-logs/blender-268"
        layout.separator()

        layout.operator("wm.url_open", text="Blender Website", icon='URL').url = "http://www.blender.org"
        layout.operator("wm.url_open", text="Blender e-Shop", icon='URL').url = "http://www.blender.org/e-shop"
        layout.operator("wm.url_open", text="Developer Community", icon='URL').url = "http://www.blender.org/community/get-involved"
        layout.operator("wm.url_open", text="User Community", icon='URL').url = "http://www.blender.org/community/user-community"
        layout.separator()
        layout.operator("wm.url_open", text="Report a Bug", icon='URL').url = "http://projects.blender.org/tracker/?atid=498&group_id=9&func=browse"
        layout.separator()

        layout.operator("wm.url_open", text="Python API Reference", icon='URL').url = bpy.types.WM_OT_doc_view._prefix
        layout.operator("wm.operator_cheat_sheet", icon='TEXT')
        layout.operator("wm.sysinfo", icon='TEXT')
        layout.separator()
        layout.operator("anim.update_data_paths", text="FCurve/Driver Version fix", icon='HELP')
        layout.operator("logic.texface_convert", text="TexFace to Material Convert", icon='GAME')
        layout.separator()

        layout.operator("wm.splash", icon='BLENDER')

if __name__ == "__main__":  # only for live edit.
    bpy.utils.register_module(__name__)
