import os
import subprocess
import json
from libqtile import hook, layout, bar
from libqtile.config import EzKey as Key, EzClick as Click, EzDrag as Drag, Group, Match, Screen
from libqtile.lazy import lazy

from qtile_extras import widget
from qtile_extras.widget.decorations import BorderDecoration, RectDecoration, PowerLineDecoration

#from modules._volume import Volume

from dataclasses import dataclass

with open("/home/es/.cache/wal/colors.json") as f:
    wal_colors = json.load(f)
@dataclass(frozen=True)
class Colors:
    transparent = wal_colors['colors']['color0']
    background  = wal_colors['colors']['color0']
    foreground  = wal_colors['special']['foreground']
    
    black       = wal_colors['colors']['color0']
    red         = wal_colors['colors']['color1']
    green       = wal_colors['colors']['color2']
    yellow      = wal_colors['colors']['color3']
    blue        = wal_colors['colors']['color4']
    magenta     = wal_colors['colors']['color5']
    cyan        = wal_colors['colors']['color6']
    white       = wal_colors['colors']['color7']
    gray        = wal_colors['colors']['color8']
    graylight   = wal_colors['colors']['color9']

palette = Colors() 

# Start flavours
#@dataclass(frozen=True)
#class Colors:
#    transparent = '#00000000'
#    background  = '#1e1e2e'
#    foreground  = '#cdd6f4'
#
#    black       = '#1e1e2e'
#    red         = '#f38ba8'
#    green       = '#a6e3a1'
#    yellow      = '#f9e2af'
#    blue        = '#89b4fa'
#    magenta     = '#f5c2e7'
#    cyan        = '#94e2d5'
#    white       = '#cdd6f4'
#    gray        = '#585b70'
#    graylight   = '#6c7086'
#
#palette = Colors()
# End flavours
#
#class Colors:
#    transparent=  '#00000000'
#    background=   '#1b1b1b'
#    foreground=   '#d4be98'
#
#    black     = '#282828'
#    red       = '#ea6962'
#    green     = '#a9b665'
#    yellow    = '#d8a657'
#    blue      = '#7daea3'
#    magenta   = '#d3869b'
#    cyan      = '#89b482'
#    white     = '#ddc7a1'
#    gray      = '#32302f'
#    graylight = '#45403d'
#    
#palette = Colors()
# End flavours

@dataclass(frozen=True)
class Preferences:
    terminal            =   "kitty"
    browser             =   "zen-browser"
    private             =   "zen-browser --private-window"
    file_manager        =   "nemo"
    screenshot_tool     =   'flameshot gui'
    code_editor         =   "pragtical"
    launcher            =   "rofi -show drun"
    power_menu          =   os.path.expanduser('~/.local/bin/powermenu.sh')
    font                =   'CaskaydiaCove NF Bold'
    corner              =   10

prefs = Preferences()

def rectdeco(hexcolor,corner=None): #kesekki iwa
	return RectDecoration(
		filled=True, colour=hexcolor,padding=5,
		radius=corner if corner is not None else 0)	

widget_list=[  
    widget.TextBox(
        text="  󰣇   ",
        foreground=palette.blue, 
        font=prefs.font, fontsize=13,
        mouse_callbacks={"Button1": lambda: qtile.cmd_spawn(prefs.launcher)},
        margin=6, borderwidth=1, decorations=[rectdeco(palette.graylight,prefs.corner)]
    ),
    widget.GroupBox(  
        this_current_screen_border=palette.blue, 
        active=palette.white, 
        inactive=palette.white,
        highlight_method='text',
        hide_unused='true',
        borderwidth=1, margin_x=4, padding=0,
        font=prefs.font, fontsize=19,
        decorations=[rectdeco(palette.transparent,prefs.corner)],
    ),
    widget.Spacer(
        background=palette.transparent
    ),
    widget.Volume(
       foreground=palette.black,
       padding=12,marfin=7,
       font=prefs.font, fontsize=13,
       decorations=[rectdeco(palette.yellow,prefs.corner)], 

    ), 
	widget.Clock(  
        foreground=palette.black, 
        format="   󱨴 %a, %d %b   ",        
        font=prefs.font, fontsize=14,
        decorations=[rectdeco(palette.green,prefs.corner)],
    ),
    widget.Clock(  
        foreground=palette.black, 
        format="   󱦟 %I:%M   ",        
        font=prefs.font, fontsize=14,
        decorations=[rectdeco(palette.blue,prefs.corner)],
    ),
    widget.WidgetBox(
        fmt= '   {} ⠀  ', 
        foreground=palette.black, 
        text_closed='', text_open='', 
        close_button_location='right',
        widgets=[widget.Systray()], 
        font=prefs.font, fontsize=14,
        decorations=[rectdeco(palette.red,prefs.corner)],
    ), 
]

def group(group_labels):
    group = []
    group_names = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
    for i in range(len(group_names)):
        group.append(Group(name=group_names[i], label=group_labels[i]))
    return group

groups = group(["󰎤", "󰎧", "󰎪", "󰎭", "󰎱", "󰎳", "󰎸", "󰎻", "󰎼"])

def init_layout_theme():
    return {
        "border_width"      :   0,
        "margin"            :   15,
        "border_focus"      :   [palette.background],
        "border_normal"     :   [palette.background],
        "grow_amount"       :   5,
        "num_columns"       :   3, 
    }

def init_float_theme():
    return {
        'float_rules'       :   [
                                    *layout.Floating.default_float_rules,
                                    Match(wm_class="Pavucontrol"),  
                                    Match(wm_class="Nitrogen"),
                                    Match(wm_class="Lxappearance"),
                                ], 
        **init_layout_theme()
    }

layouts = [
    layout.Columns(**init_layout_theme()),
    layout.Floating(**init_layout_theme()),
]

floating_layout = layout.Floating(**init_float_theme())

keys = [
    # Switch between windows
    Key('M-<Left>',                 lazy.layout.left(),                             desc='Move focus to left'),
    Key('M-<Right>',                lazy.layout.right(),                            desc='Move focus to right'),
    Key('M-<Up>',                   lazy.layout.up(),                               desc='Move focus to up'),
    Key('M-<Down>',                 lazy.layout.down(),                             desc='Move focus to down'),
    Key('M-<Space>',                lazy.layout.next(),                             desc='Move window focus to other window'),

    #Move windows between left/right columns or move up/down in current stack.
    Key('M-S-<Left>',               lazy.layout.shuffle_left(),                     desc='Move window to left'),
    Key('M-S-<Right>',              lazy.layout.shuffle_right(),                    desc='Move window to right'),
    Key('M-S-<Up>',                 lazy.layout.shuffle_up(),                       desc='Move window to up'),
    Key('M-S-<Down>',               lazy.layout.shuffle_down(),                     desc='Move window to down'),
    
    # Grow windows.
    Key('M-C-<Left>',               lazy.layout.grow_left(),                        desc='Grow window to left'),
    Key('M-C-<Right>',              lazy.layout.grow_right(),                       desc='Grow window to right'),
    Key('M-C-<Up>',                 lazy.layout.grow_up(),                          desc='Grow window to up'),
    Key('M-C-<Down>',               lazy.layout.grow_down(),                        desc='Grow window to down'),
    Key('M-n',                      lazy.layout.normalize(),                        desc='Reset all window sizes'),

    # Toggle between different layouts 
    Key('M-<Tab>',                  lazy.next_layout(),                             desc='Toggle between layouts'),

    # More Window Stuff
    Key('M-f',                      lazy.window.toggle_floating(),                  desc='Toggle floating window'),

    # Base Qtile
    Key('M-S-r',                    lazy.restart(),                                 desc='Restart Qtile'),
    Key('M-S-q',                    lazy.shutdown(),                                desc='Shutdown Qtile'),
    Key('M-x',                      lazy.window.kill(),                             desc='Kill focused window'),
    Key('M-b',                      lazy.hide_show_bar                              (position="top")), 
    #Rofi
    Key('M-p',                      lazy.spawn(prefs.launcher),                     desc='Launch Menu'),
    Key('M-q',                      lazy.spawn(prefs.power_menu),                   desc='Launch Power Menu'),
    Key('M-<Return>',               lazy.spawn(prefs.terminal),                     desc='Launch Terminal'),

    # Launch Applications
    Key('M-C-b',                    lazy.spawn(prefs.browser),                      desc='Launch Browser'),
    Key('M-C-p',                    lazy.spawn(prefs.private),                      desc='Launch Incognito Browser'),
    Key('M-C-e',                    lazy.spawn(prefs.code_editor),                  desc='Launch Editor'),
    Key('M-C-f',                    lazy.spawn(prefs.file_manager),                 desc='Launch File Manager'),
    Key('M-C-v',                    lazy.spawn('pavucontrol'),                      desc='Launch Volume Control'),
        
    # Take Screenshot
    Key('<Print>',                  lazy.spawn(prefs.screenshot_tool),              desc='Take a Screenshot'),
    
    # Media hotkeys
    Key('<XF86AudioRaiseVolume>',   lazy.spawn('pactl set-sink-volume 0 +5%'),      desc='Raise Volume'),
    Key('<XF86AudioLowerVolume>',   lazy.spawn('pactl set-sink-volume 0 -5%'),      desc='Lower Volume'),
    Key('<XF86AudioMute>',          lazy.spawn('pactl set-sink-mute 0 toggle'),     desc='Mute Volume'),
    Key('<XF86AudioPlay>',          lazy.spawn('playerctl play-pause'),             desc='Play / Pause Media'),
    Key('<XF86AudioNext>',          lazy.spawn('playerctl next'),                   desc='Play Next'),
    Key('<XF86AudioPrev>',          lazy.spawn('playerctl previous'),               desc='Play Previous'),

    # Brigtness
    Key('<XF86MonBrightnessUp>',    lazy.spawn('brightnessctl s 10+'),              desc='Increase Brightness'),
    Key('<XF86MonBrightnessDown>',  lazy.spawn('brightnessctl s 10-'),              desc='Decrease Brightness'), 
]

for i in groups:
    keys.extend(
        [
            Key('M-'+i.name,        lazy.group[i.name].toscreen(),                  desc='Switch to group {}'.format(i.name)),
            Key('M-S-'+i.name,      lazy.window.togroup(i.name, switch_group=False),desc='Move focused window to group {}'.format(i.name)),
        ]
    )

mouse = [
    Drag("M-1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag("M-3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click("M-2", lazy.window.bring_to_front())
]

screens = [
    Screen(       
        top=bar.Bar(
            widget_list,
            size=30, 
            opacity=1,
            border_width=[0,0,0,0], #N E S W
            background=palette.transparent, 
        ),
    ),
]

dgroups_key_binder = None
dgroups_app_rules = [] 
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = False
auto_minimize = True 
wmname = "Qtile"

@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/start.sh')
    subprocess.call([home])

