-- After Hours / Tokyo Night — current Lua configuration API.
hl.monitor({ output = "", mode = "preferred", position = "auto", scale = "auto" })
hl.env("XCURSOR_THEME", "default")
hl.env("XCURSOR_SIZE", "20")
hl.config({
    general = { gaps_in = 6, gaps_out = 12, border_size = 2, layout = "dwindle",
        col = { active_border = { colors = {"rgba(7aa2f7ff)", "rgba(bb9af7ff)"}, angle = 45 },
                inactive_border = "rgba(414868ff)" } },
    decoration = { rounding = 12, blur = { enabled = true, size = 5, passes = 2 },
        shadow = { enabled = true, range = 16, color = "rgba(15161e99)" } },
    input = { kb_layout = "us", touchpad = { tap_to_click = true, natural_scroll = true } },
    misc = { disable_hyprland_logo = true, force_default_wallpaper = -1 },
})
hl.on("hyprland.start", function() hl.exec_cmd("~/.local/bin/after-hours-shell") end)
hl.bind("SUPER + Return", hl.dsp.exec_cmd("foot"))
hl.bind("SUPER + D", hl.dsp.exec_cmd("~/.local/bin/after-hours-shell launcher"))
hl.bind("SUPER + Q", hl.dsp.window.close())
hl.bind("SUPER + V", hl.dsp.window.float({ action = "toggle" }))
hl.bind("SUPER + SHIFT + E", hl.dsp.exit())
for _, direction in ipairs({"left", "right", "up", "down"}) do
    hl.bind("SUPER + " .. direction, hl.dsp.focus({ direction = direction }))
end
for i = 1, 9 do
    hl.bind("SUPER + " .. i, hl.dsp.focus({ workspace = i }))
    hl.bind("SUPER + SHIFT + " .. i, hl.dsp.window.move({ workspace = i }))
end
hl.bind("SUPER + mouse:272", hl.dsp.window.drag(), { mouse = true })
hl.bind("SUPER + mouse:273", hl.dsp.window.resize(), { mouse = true })
