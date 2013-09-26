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
 * Contributor(s): Michael Neilly
 *
 * ***** END GPL LICENSE BLOCK *****
 */
 
/** \file blender/editors/space_layer/space_layer.c
 *  \ingroup splayer
 */
 
#include <string.h>
 
#include "DNA_text_types.h"
#include "DNA_object_types.h"
#include "DNA_scene_types.h"
#include "DNA_view3d_types.h" 
#include "MEM_guardedalloc.h"
 
#include "BLI_blenlib.h"
 
#include "BKE_context.h"
#include "BKE_screen.h"
 
#include "ED_space_api.h"
#include "ED_screen.h"
 
#include "BIF_gl.h"
 
#include "WM_api.h"
#include "WM_types.h"
 
#include "UI_interface.h"
#include "UI_resources.h"
#include "UI_view2d.h"

 
static SpaceLink *layer_new(const bContext *C)
{
	Scene *scene = CTX_data_scene(C);
	ARegion *ar;
	SpaceLayer *slayer;
 
	slayer = MEM_callocN(sizeof(SpaceLayer), "initlayer");
	slayer->spacetype = SPACE_LAYER;
	slayer->lay = slayer->layact = 1;
    if (scene) {
		slayer->lay = slayer->layact = scene->lay;
		slayer->camera = scene->camera;
	}
	slayer->scenelock = TRUE;
	/* header */
	ar = MEM_callocN(sizeof(ARegion), "header for layer");
 
	BLI_addtail(&slayer->regionbase, ar);
	ar->regiontype = RGN_TYPE_HEADER;
	ar->alignment = RGN_ALIGN_TOP;
	
 
	/* main area */
	ar = MEM_callocN(sizeof(ARegion), "main area for layer");
 
	BLI_addtail(&slayer->regionbase, ar);
	ar->regiontype = RGN_TYPE_WINDOW;
 
	return (SpaceLink *)slayer;
}
 static void layer_free(SpaceLink *UNUSED(sl))
{	
	//SpaceLayer *slayer = (SpaceLayer *) sl;

}
static void layer_init(struct wmWindowManager *UNUSED(wm), ScrArea *sa)
{
	SpaceLayer *slayer = sa->spacedata.first;

	// auto-align based on size 
	if (slayer->align == BUT_AUTO || !slayer->align) {
		
		slayer->align = BUT_VERTICAL;
	}
}
static SpaceLink *layer_duplicate(SpaceLink *sl)
{
	SpaceLayer *slayern = MEM_dupallocN(sl);
	
	/* clear or remove stuff from old */
	slayern->path = NULL;
	slayern->texuser = NULL;
	
	return (SpaceLink *)slayern;
}

/* add handlers, stuff you only do once or on area/region changes */
static void layer_main_area_init(wmWindowManager *wm, ARegion *ar)
{
	wmKeyMap *keymap;

	ED_region_panels_init(wm, ar);

	keymap = WM_keymap_find(wm->defaultconf, "Layer Editor", SPACE_LAYER, 0);
	WM_event_add_keymap_handler(&ar->handlers, keymap);
    keymap = WM_dropboxmap_find("View3D", SPACE_VIEW3D, RGN_TYPE_WINDOW);
	
	WM_event_add_dropbox_handler(&ar->handlers, keymap);
}
 
static void layer_main_area_draw(const bContext *C, ARegion *ar)
{
	/* draw entirely, view changes should be handled here */
	SpaceLayer *slayer = CTX_wm_space_layer(C);
	int vertical = (slayer->align == BUT_VERTICAL);
   // layer_context_compute(C, slayer);
	if (slayer->mainb == BCONTEXT_SCENE)
		ED_region_panels(C, ar, vertical, "scene", slayer->mainb);
	else if (slayer->mainb == BCONTEXT_RENDER)
		ED_region_panels(C, ar, vertical, "render", slayer->mainb);
	else if (slayer->mainb == BCONTEXT_OBJECT)
		ED_region_panels(C, ar, vertical, "object", slayer->mainb);
	
	slayer->re_align = 0;
	slayer->mainbo = slayer->mainb;

}
static void layer_operatortypes(void)
{
	
}
static void layer_area_listener(ScrArea *sa, wmNotifier *wmn)
{
	SpaceLayer *slayer = sa->spacedata.first;
	switch (wmn->category) {
		case NC_WM:
			if (wmn->data == ND_HISTORY)
				ED_region_tag_redraw(sa);
			break;
		
		case NC_SPACE:
			if (wmn->data == ND_SPACE_VIEW3D)
				ED_region_tag_redraw(sa);
			break;
	}
}
static void view3d_recalc_used_layers(ARegion *ar, wmNotifier *wmn, Scene *scene)
{
	wmWindow *win = wmn->wm->winactive;
	ScrArea *sa;
	unsigned int lay_used = 0;
	Base *base;

	if (!win) return;

	base = scene->base.first;
	while (base) {
		lay_used |= base->lay & ((1 << 20) - 1); /* ignore localview */

		if (lay_used == (1 << 20) - 1)
			break;

		base = base->next;
	}

	for (sa = win->screen->areabase.first; sa; sa = sa->next) {
		if (sa->spacetype == SPACE_LAYER) {
			if (BLI_findindex(&sa->regionbase, ar) != -1) {
				SpaceLayer *slayer = sa->spacedata.first;
				slayer->lay_used = lay_used;
				break;
			}
		}
	}
}
 static void layer_keymap(struct wmKeyConfig *keyconf)
{
	wmKeyMap *keymap = WM_keymap_find(keyconf, "Layer Editor", SPACE_LAYER, 0);
	
}
static void layer_header_area_init(wmWindowManager *UNUSED(wm), ARegion *ar)
{
	ED_region_header_init(ar);
}
 
static void layer_header_area_draw(const bContext *C, ARegion *ar)
{
	ED_region_header(C, ar);
}
/* reused! */
/*
 static void layer_area_listener(ScrArea *sa, wmNotifier *wmn)
{
	SpaceLayer *slayer = sa->spacedata.first;
	switch (wmn->category) {
		case NC_WM:
			if (wmn->data == ND_HISTORY)
				ED_region_tag_redraw(sa);
			break;
		
		case NC_SPACE:
			if (wmn->data == ND_SPACE_VIEW3D)
				ED_region_tag_redraw(sa);
			break;
	}
}*/
static void layer_main_area_listener(ARegion *ar, wmNotifier *wmn)
{
	
	/* context changes */
	switch (wmn->category) {
		
		case NC_SCENE:
			switch (wmn->data) {
				case ND_LAYER_CONTENT:
					if (wmn->reference)
						view3d_recalc_used_layers(ar, wmn, wmn->reference);
					ED_region_tag_redraw(ar);
					break;
				case ND_FRAME:
				case ND_TRANSFORM:
				case ND_OB_ACTIVE:
				case ND_OB_SELECT:
				case ND_OB_VISIBLE:
				case ND_LAYER:
				case ND_RENDER_OPTIONS:
				case ND_MODE:
					ED_region_tag_redraw(ar);
					break;
				case ND_WORLD:
					/* handled by space_view3d_listener() for v3d access */
					break;
			}
			if (wmn->action == NA_EDITED)
				ED_region_tag_redraw(ar);
			break;
		case NC_OBJECT:
			switch (wmn->data) {
				case ND_BONE_ACTIVE:
				case ND_BONE_SELECT:
				case ND_TRANSFORM:
				case ND_POSE:
				case ND_DRAW:
				case ND_MODIFIER:
				case ND_CONSTRAINT:
				case ND_KEYS:
				case ND_PARTICLE:
					ED_region_tag_redraw(ar);
					break;
			}
			switch (wmn->action) {
				case NA_ADDED:
					ED_region_tag_redraw(ar);
					break;
			}
			break;
		
		case NC_SPACE:
			if (wmn->data == ND_SPACE_VIEW3D) {
				if (wmn->subtype == NS_VIEW3D_GPU) {
					RegionView3D *rv3d = ar->regiondata;
					rv3d->rflag |= RV3D_GPULIGHT_UPDATE;
				}
				ED_region_tag_redraw(ar);
			}
			break;
		case NC_ID:
			if (wmn->action == NA_RENAME)
				ED_region_tag_redraw(ar);
			break;
		case NC_SCREEN:
			switch (wmn->data) {
				case ND_ANIMPLAY:
				case ND_SKETCH:
					ED_region_tag_redraw(ar);
					break;
				case ND_SCREENBROWSE:
				case ND_SCREENDELETE:
				case ND_SCREENSET:
					/* screen was changed, need to update used layers due to NC_SCENE|ND_LAYER_CONTENT */
					/* updates used layers only for View3D in active screen */
					if (wmn->reference) {
						bScreen *sc = wmn->reference;
						view3d_recalc_used_layers(ar, wmn, sc->scene);
					}
					ED_region_tag_redraw(ar);
					break;
			}

			break;
		
	}
}
/********************* registration ********************/
 
/* only called once, from space/spacetypes.c */
void ED_spacetype_layer(void)
{
	SpaceType *st = MEM_callocN(sizeof(SpaceType), "spacetype layer");
	ARegionType *art;
 
	st->spaceid = SPACE_LAYER;
	strncpy(st->name, "Layer", BKE_ST_MAXNAME);
 
	st->new = layer_new;
	st->free = layer_free;
	st->init = layer_init;
	st->duplicate = layer_duplicate;
	st->operatortypes = layer_operatortypes;
	st->keymap = layer_keymap;
    st->listener = layer_area_listener;
    //st->context = layer_context;
	/* regions: main window */
	art = MEM_callocN(sizeof(ARegionType), "spacetype layer region");
	art->regionid = RGN_TYPE_WINDOW;
 
	art->init = layer_main_area_init;
	art->draw = layer_main_area_draw;
    art->keymapflag = ED_KEYMAP_UI | ED_KEYMAP_FRAMES;
	BLI_addhead(&st->regiontypes, art);
	//layer_context_register(art);
 
	/* regions: header */
	art = MEM_callocN(sizeof(ARegionType), "spacetype layer region");
	art->regionid = RGN_TYPE_HEADER;
	art->prefsizey = HEADERY;
	art->keymapflag = ED_KEYMAP_UI | ED_KEYMAP_VIEW2D | ED_KEYMAP_HEADER | ED_KEYMAP_FRAMES ;
	art->init = layer_header_area_init;
	art->draw = layer_header_area_draw;
 
	BLI_addhead(&st->regiontypes, art);
 
	BKE_spacetype_register(st);
}
