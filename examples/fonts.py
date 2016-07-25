import ugfx
import pyb

ugfx.clear()

ugfx.set_default_font(ugfx.FONT_SMALL)
ugfx.text(20,30,"Tiny AbCdEfGhiJkLmNoPqRsTuVwXyZ 1\"3$5^7*9) ",0)
ugfx.set_default_font(ugfx.FONT_TITLE)
ugfx.text(20,50,"Title AbCdEfGhiJkLmNoPqRsTuVwXyZ 1\"3$5^7*9) ",0)
ugfx.set_default_font(ugfx.FONT_NAME)
ugfx.text(20,80,"Name AbCdEfGhiJkLmNoPqRsTuVwXyZ 1\"3$5^7*9) ",0)
ugfx.set_default_font(ugfx.FONT_MEDIUM)
ugfx.text(20,120,"Medium AbCdEfGhiJkLmNoPqRsTuVwXyZ 1\"3$5^7*9) ",0)
ugfx.set_default_font(ugfx.FONT_MEDIUM_BOLD)
ugfx.text(20,150,"Medium-Bold AbCdEfGhiJkLmNoPqRsTuVwXyZ 1\"3$5^7*9) ",0)

while True:
	pyb.wfi()