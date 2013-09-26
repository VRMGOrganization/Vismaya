/*
 * ***** BEGIN GPL LICENSE BLOCK *****
 *
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License
 * as published by the Free Software Foundation; either version 2
 * of the License, or (at your option) any later version. 
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software Foundation,
 * Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
 *
 * The Original Code is Copyright (C) 2008 Blender Foundation.
 * All rights reserved.
 *
 * 
 * Contributor(s): Blender Foundation
 *
 * ***** END GPL LICENSE BLOCK *****
 */

/** \file blender/editors/space_view3d/view3d_view.c
 *  \ingroup spview3d
 */


#include "DNA_camera_types.h"
#include "DNA_scene_types.h"
#include "DNA_object_types.h"
#include "DNA_lamp_types.h"

#include "MEM_guardedalloc.h"

#include "BLI_math.h"
#include "BLI_rect.h"
#include "BLI_listbase.h"
#include "BLI_utildefines.h"

#include "BKE_anim.h"
#include "BKE_action.h"
#include "BKE_camera.h"
#include "BKE_context.h"
#include "BKE_depsgraph.h"
#include "BKE_object.h"
#include "BKE_global.h"
#include "BKE_main.h"
#include "BKE_report.h"
#include "BKE_scene.h"
#include "BKE_screen.h"

#include "BIF_gl.h"
#include "BIF_glutil.h"

#include "WM_api.h"
#include "WM_types.h"

#include "ED_screen.h"
#include "ED_armature.h"

#ifdef WITH_GAMEENGINE
#include "BL_System.h"
#endif

#include "RNA_access.h"
#include "RNA_define.h"

#include "layer_intern.h"  /* own include */

/* use this call when executing an operator,
 * event system doesn't set for each event the
 * opengl drawing context */

int ED_spacelayer_scene_layer_set(int lay, const int *values, int *active)
{
	int i, tot = 0;
	
	/* ensure we always have some layer selected */
	for (i = 0; i < 20; i++)
		if (values[i])
			tot++;
	
	if (tot == 0)
		return lay;
	
	for (i = 0; i < 20; i++) {
		
		if (active) {
			/* if this value has just been switched on, make that layer active */
			if (values[i] && (lay & (1 << i)) == 0) {
				*active = (1 << i);
			}
		}
			
		if (values[i]) lay |= (1 << i);
		else lay &= ~(1 << i);
	}
	
	/* ensure always an active layer */
	if (active && (lay & *active) == 0) {
		for (i = 0; i < 20; i++) {
			if (lay & (1 << i)) {
				*active = 1 << i;
				break;
			}
		}
	}
	
	return lay;
}


