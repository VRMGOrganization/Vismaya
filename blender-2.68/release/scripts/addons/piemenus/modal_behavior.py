'''
Created on Jan 21, 2013

@author: Patrick
'''
import bpy
import math
import time

import pie_menu_utils as pmu

#slider, noclick border modal
def slider_modal(self, context, event):
    
    now = time.time()
    if now - self.menu.init_time < context.scene.piemenus.pieBorderDelay:
        #calculate apparent position of mouse
        app_x = event.mouse_region_x + (self.menu.menu_x - self.menu.init_x)
        app_y = event.mouse_region_y + (self.menu.menu_y - self.menu.init_y)
    else:
        app_x = event.mouse_region_x
        app_y = event.mouse_region_y
        
    if event.type == 'MOUSEMOVE':
        # mouse-over highlight
        self.current = self.menu.calc_by_item(app_x, app_y)
        if not self.current:
            self.current = self.menu.calc_by_angle(app_x, app_y)
                    
        # pointer of center circle points at the mouse
        self.menu.pointerangle=-math.atan2(app_x-self.menu.menu_x, app_y-self.menu.menu_y)   #changed this to radians and y = 0 axis theta  0     
        
        if self.current in self.menu.sliders and self.menu.mouse_drag:
            self.current.push_to_prop()
            self.current.update_local_to_screen()
    
        
    elif event.type == 'LEFTMOUSE':
    
        #first identify what item we have the mouse over
        self.current = self.menu.calc_by_item(app_x, app_y)
        if not self.current:
            self.current = self.menu.calc_by_angle(app_x, app_y)
 
        #two things could be happening here
        #clicking a slider or clicking a menu item
        if event.value == 'PRESS':
            self.menu.mouse_drag = True  
            if self.current in self.menu.sliders:
                self.current.push_to_prop()
                self.current.update_local_to_screen()
                
                return {'RUNNING_MODAL'}
            
            else:    
                do_exec = self.current and self.current.poll(context)
                if do_exec:
                    self.current.op(self, context)
            
                if self.current is None or (do_exec and self.current.close_menu):
                    pmu.callback_cleanup(self, context)
                    return {'FINISHED'}
                else:
                    return {'RUNNING_MODAL'}
        
        if event.value == 'RELEASE':
            self.menu.mouse_drag = False
            if self.current in self.menu.sliders:
                self.current.push_to_prop()
                self.current.update_local_to_screen()
            
            return {'RUNNING_MODAL'}
        
        
    elif event.type == self.menu.keybind and event.value == "RELEASE":
        
        do_exec = False
        if self.current not in self.menu.sliders:
            do_exec = self.current and self.current.poll(context)
        if do_exec and self.current.close_menu:
            self.current.op(self, context)
            pmu.callback_cleanup(self,context)
            
            return {'FINISHED'}
    
        elif self.current is None: #the mouse is still in the circle
            return {'RUNNING_MODAL'}
    
        else:
            return {'RUNNING_MODAL'}
        
        
    if self.current == -1 or event.type in ('RIGHTMOUSE', 'ESC'):
        pmu.callback_cleanup(self,context)
        return {'CANCELLED'}
    
    return {'RUNNING_MODAL'}