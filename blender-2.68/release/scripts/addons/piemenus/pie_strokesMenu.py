# -*- coding: utf-8 -*-
 
# Copyright (c) 2010, Dan Eicher.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions and the following disclaimer in the documentation
#     and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 
# <pep8 compliant>

import bpy
from pie_menu import MenuItem, PieMenu
import pie_menu_utils as pmu
import modal_behavior

import math
import blf
import bgl

default_keybind = 'A'
 
bl_info = {
    "name": "Pie: Strokes Menu",
    "author": "Dan Eicher, Sean Olson, Patrick Moore",
    "version": (0, 1, 0),
    "blender": (2, 6, 4),
    "location": "View3D",
    "description": "Stokes modes pie menu",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "3D View"
}
 
class VIEW3D_MT_Strokes_Menu(bpy.types.Operator):
    '''Strokes Menu'''
    bl_idname = "view3d.strokes_menu"
    bl_label = "Pie Strokes Menu"
 
    @classmethod
    def poll(cls, context):
        return context.area.type == 'VIEW_3D'
        

 
    def modal(self, context, event):
        context.area.tag_redraw()
        
        ret_val = modal_behavior.slider_modal(self, context, event) #could it be this simple?
        
        return ret_val
 
    def invoke(self, context, event):
        self.current = None
        current_keybind = bpy.context.window_manager.keyconfigs.user.keymaps['Sculpt'].keymap_items['view3d.strokes_menu'].type
        # generate menu content
        self.menu = menu_init(PieMenu(x=event.mouse_region_x,
                                      y=event.mouse_region_y,
                                      keybind = current_keybind,
                                      layout_radius=80,
                                      text_size=11,
                                      text_dpi=72,
                                      center_radius_squared=225,
                                      max_radius_squared=62500#22500
                                      ))
 
        context.window_manager.modal_handler_add(self)
        pmu.callback_register(self,context)
        return {'RUNNING_MODAL'}
 
def menu_init(menu):
   
    menu.menu_items.append(Space("Space", 0, 35))
    menu.menu_items.append(Airbrush("Airbrush", 85, 0))
    menu.menu_items.append(Dragdot("Drag Dot", 65, -30))

    if bpy.context.tool_settings.sculpt.brush.use_smooth_stroke:
       menu.menu_items.append(SmoothStrokeOff("Smooth Off", 0, -55))
    else:
       menu.menu_items.append(SmoothStrokeOn("Smooth On", 0, -55))

    menu.menu_items.append(Anchored("Anchored", -65, -30))  
    menu.menu_items.append(Dots("Dots", -85, 0))
 
    menu.calc_text() #need to figure out the box size from text..only once...not every draw.
    menu.calc_boxes()
        
    menu.layout_predefined(auto_slice = True)  #this includes updating the local box coords to screen coords
    
    return menu
 
 
class Space(MenuItem):
    def op(self, parent, context):
        bpy.context.tool_settings.sculpt.brush.stroke_method='SPACE'
 
 
class Airbrush(MenuItem):
    def op(self, parent, context):
        bpy.context.tool_settings.sculpt.brush.stroke_method='AIRBRUSH'

 
class Dragdot(MenuItem):
    def op(self, parent, context):
         bpy.context.tool_settings.sculpt.brush.stroke_method='DRAG_DOT'

 
class Anchored(MenuItem):
    def op(self, parent, context):
       bpy.context.tool_settings.sculpt.brush.stroke_method='ANCHORED'

 
class Dots(MenuItem):
    def op(self, parent, context):
        bpy.context.tool_settings.sculpt.brush.stroke_method='DOTS'

class SmoothStrokeOn(MenuItem):
    def op(self, parent, context):
        bpy.context.tool_settings.sculpt.brush.use_smooth_stroke=True

class SmoothStrokeOff(MenuItem):
    def op(self, parent, context):
        bpy.context.tool_settings.sculpt.brush.use_smooth_stroke=False


def setBind():
    #enable the addon keybinding
    km = bpy.context.window_manager.keyconfigs.active.keymaps['Sculpt']
    for kmi in km.keymap_items:
        if kmi.idname == 'view3d.strokes_menu':
            if kmi.type == default_keybind and kmi.ctrl==False and kmi.alt==False and kmi.shift==False and kmi.oskey==False and kmi.any==False and kmi.key_modifier=='NONE':
                kmi.active=True
                break

    #disable the default keybinding
    km = bpy.context.window_manager.keyconfigs.active.keymaps['Sculpt']
    for kmi in km.keymap_items:
        if kmi.idname == 'wm.context_menu_enum':
            if kmi.type == default_keybind and kmi.ctrl==False and kmi.alt==False and kmi.shift==False and kmi.oskey==False and kmi.any==False and kmi.key_modifier=='NONE':
                kmi.active=False
                break

def removeBind():
    #disable the addon keybinding
    km = bpy.context.window_manager.keyconfigs.active.keymaps['Sculpt']
    for kmi in km.keymap_items:
        if kmi.idname == 'view3d.strokes_menu':
            if kmi.type == default_keybind and kmi.ctrl==False and kmi.alt==False and kmi.shift==False and kmi.oskey==False and kmi.any==False and kmi.key_modifier=='NONE':
                kmi.active=False
                break

    #enable the default keybinding
    km = bpy.context.window_manager.keyconfigs.active.keymaps['Sculpt']
    for kmi in km.keymap_items:
        if kmi.idname == 'wm.context_menu_enum':
            if kmi.type == default_keybind and kmi.ctrl==False and kmi.alt==False and kmi.shift==False and kmi.oskey==False and kmi.any==False and kmi.key_modifier=='NONE':
                kmi.active=True
                break
       
def register():
    bpy.utils.register_class(VIEW3D_MT_Strokes_Menu)

    #add the keybinding   
    km = bpy.context.window_manager.keyconfigs.active.keymaps['Sculpt']
    km.keymap_items.new('view3d.strokes_menu', default_keybind, 'PRESS')

    #disable the default keybinding
    km = bpy.context.window_manager.keyconfigs.active.keymaps['Sculpt']
    for kmi in km.keymap_items:
        if kmi.idname == 'wm.context_menu_enum':
            if kmi.type == default_keybind and kmi.ctrl==False and kmi.alt==False and kmi.shift==False and kmi.oskey==False and kmi.any==False and kmi.key_modifier=='NONE':
                kmi.active=False
                break
 
 
def unregister():
    bpy.utils.unregister_class(VIEW3D_MT_Strokes_Menu)

    #replace default
    km = bpy.context.window_manager.keyconfigs.active.keymaps['Sculpt']
    for kmi in km.keymap_items:
        if kmi.idname == 'wm.context_menu_enum':
            if kmi.type == default_keybind and kmi.ctrl==False and kmi.alt==False and kmi.shift==False and kmi.oskey==False and kmi.any==False and kmi.key_modifier=='NONE':
                kmi.active=True
                break
   
    #remove pie key
    for kmi in km.keymap_items:
        if kmi.idname == 'view3d.strokes_menu':
            km.keymap_items.remove(kmi)
            break
 
if __name__ == "__main__":
    register()
