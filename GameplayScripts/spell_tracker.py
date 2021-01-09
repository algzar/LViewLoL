from lview import *

show_local_champ = False
show_allies = False
show_enemies = False

lview_script_info = {
	"script": "Spell Tracker",
	"author": "leryss",
	"description": "Tracks spell cooldowns and levels"
}

def get_color_for_cooldown(cooldown):
	if cooldown > 0.0:
		return Color.DARK_RED
	else:
		return Color(1, 1, 1, 1)


def draw_spell(game, spell, pos, size, show_lvl = True, show_cd = True):
	
	cooldown = spell.get_current_cooldown(game.time)
	color = get_color_for_cooldown(cooldown) if spell.level > 0 else Color.GRAY
	
	game.draw_image(spell.icon, pos, pos.add(Vec2(size, size)), color, 10.0)
	if show_cd and cooldown > 0.0:
		game.draw_text(pos.add(Vec2(4, 5)), str(int(cooldown)), Color.WHITE)
	if show_lvl:
		for i in range(spell.level):
			offset = i*4
			game.draw_rect_filled(Vec4(pos.x + offset, pos.y + 24, pos.x + offset + 3, pos.y + 26), Color.YELLOW)

def draw_overlay_on_champ(game, champ):
	p = Vec3(champ.pos.x, champ.pos.y, champ.pos.z)

	p = game.world_to_screen(p)
	p.x -= 60
	
	if not game.is_point_on_screen(p):
		return
	
	draw_spell(game, champ.Q, p, 26)
	p.x += 28
	draw_spell(game, champ.W, p, 26)
	p.x += 28
	draw_spell(game, champ.E, p, 26)
	p.x += 28
	draw_spell(game, champ.R, p, 26)
	
	p.x += 28
	draw_spell(game, champ.D, p, 13, False, False)
	p.y += 14
	draw_spell(game, champ.F, p, 13, False, False)
	
	#draw_spell_btn(game, champ.W, p.x + 33,  p.y,      30, 15)
	#draw_spell_btn(game, champ.E, p.x + 66,  p.y,      30, 15)
	#draw_spell_btn(game, champ.R, p.x + 99,  p.y,      30, 15)
	#draw_spell_btn(game, champ.D, p.x,       p.y - 18, 63, 15, True, False)
	#draw_spell_btn(game, champ.F, p.x + 66,  p.y - 18, 63, 15, True, False)


def lview_update(game, ui):
	global show_allies, show_enemies, show_local_champ
	
	for champ in game.champs:
		if not champ.is_visible or not champ.is_alive:
			continue
		if champ == game.player and show_local_champ:
			draw_overlay_on_champ(game, champ)
		elif champ != game.player:
			if champ.is_ally_to(game.player) and show_allies:
				draw_overlay_on_champ(game, champ)
			elif champ.is_enemy_to(game.player) and show_enemies:
				draw_overlay_on_champ(game, champ)

def lview_load_cfg(cfg):
	global show_allies, show_enemies, show_local_champ
	
	show_allies = cfg.get_bool("show_allies", False)
	show_enemies = cfg.get_bool("show_enemies", True)
	show_local_champ = cfg.get_bool("show_local_champ", False)
	
def lview_save_cfg(cfg):
	global show_allies, show_enemies, show_local_champ
	
	cfg.set_bool("show_allies", show_allies)
	cfg.set_bool("show_enemies", show_enemies)
	cfg.set_bool("show_local_champ", show_local_champ)
	
def lview_draw_settings(game, ui):
	global show_allies, show_enemies, show_local_champ
	
	show_allies = ui.checkbox("Show overlay on allies", show_allies)
	show_enemies = ui.checkbox("Show overlay on enemies", show_enemies)
	show_local_champ = ui.checkbox("Show overlay on self", show_local_champ)
	
