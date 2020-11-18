from typing import List  # noqa: F401
import subprocess
import os

from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

mod = "mod4"
terminal = "alacritty"

keys = [
    # Switch between windows
    Key([mod], "h", lazy.layout.left()),
    Key([mod], "l", lazy.layout.right()),
    Key([mod], "j", lazy.layout.down()),
    Key([mod], "k", lazy.layout.up()),

    # Swap windows
    Key([mod, "shift"], "h", lazy.layout.swap_left()),
    Key([mod, "shift"], "l", lazy.layout.swap_right()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up()),
    Key([mod], "i", lazy.layout.grow()),
    Key([mod], "m", lazy.layout.shrink()),
    Key([mod], "n", lazy.layout.normalize()),
    Key([mod], "o", lazy.layout.maximize()),

    # Switch window focus to other pane(s) of stack
    Key([mod], "space", lazy.layout.next(),
        desc="Switch window focus to other pane(s) of stack"),

    # Swap panes of split stack
    Key([mod, "shift"], "space", lazy.layout.rotate(),
        desc="Swap panes of split stack"),

    Key([mod], "p", lazy.spawn(
        "rofi -show run -font 'hack 10' -lines 3 -eh 2 -bw 0 -width 100 -padding 400 -fullscreen"), desc="Spawn rofi"),

    # Key([mod], "-", lazy.spawn("pamixer --allow-boost -d 5"),
    #     desc="Decrease the volume"),
    # Key([mod], "=", lazy.spawn("pamixer --allow-boost -i 5"),
    #     desc="Increase the volume"),
    Key([mod, "control"], "d", lazy.spawn(
        "alacritty -e ranger"), desc="Spawn file browser"),
    Key([mod, "shift"], "a", lazy.spawn(
        "alacritty -e calcurse"), desc="Spawn calendar"),
    Key([mod, "control"], "j", lazy.spawn(
        "alacritty -e joplin"), desc="Spawn Note taking"),
    Key([mod, "control"], "t", lazy.spawn(
        "alacritty -e tg"), desc="Spawn Telegram client"),
    Key([mod, "control"], "l", lazy.spawn(
        "/home/cherry/bin/switch_keyboard_layout"), desc="Switch keyboard language"),
    Key([mod, "shift"], "p", lazy.spawn("/home/cherry/bin/switch_project"),
        desc="Spawn alacritty with tmux in different projects"),
    Key([mod, "control"], "p", lazy.spawn(
        "flameshot gui"), desc="Take screenshot"),
    Key([mod], "w", lazy.spawn("firefox"), desc="Spawn web browser"),
    Key([mod], "s", lazy.spawn("alacritty -e /home/cherry/bin/slack"),
        desc="Spawn slack client"),
    Key([mod, "control"], "s", lazy.spawn("/home/cherry/bin/open-web-apps"),
        desc="Spawn util web applications in surf"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack"),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "BackSpace", lazy.window.kill(), desc="Kill focused window"),

    Key([mod, "control"], "r", lazy.restart(), desc="Restart qtile"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown qtile"),
    Key([mod], "r", lazy.spawncmd(),
        desc="Spawn a command using a prompt widget")
]

# Custom functions


def format_appointment():
    result = os.popen("calcurse --next").read()

    result2 = result.replace('next appointment:', '')

    result3 = result2.split('\n')

    wipe_list = list(filter(None, result3))

    if len(wipe_list) == 1:
        data = wipe_list[0].strip()
        info = data[:40] + (data[40:] and '..')
        return info

# Autostart applications


@hook.subscribe.startup_once
def autostart():
    processes = [
        ['/usr/bin/setxkbmap', 'us'],
        ['/usr/bin/xrandr', '--output',  'HDMI-1', '--mode', '1920.1080'],
        ['/usr/bin/picom', '-f'],
        ['/usr/bin/dunst'],
        ['/usr/bin/feh', '--bg-scale',
            '/home/cherry/Pictures/wallpapers/wallpaper03.jpg']
    ]

    for p in processes:
        subprocess.Popen(p)


# Changing the names of the workspaces.

group_names = [("", {'layout': 'monadtall'}),
               ("", {'layout': 'monadtall'}),
               ("", {'layout': 'monadtall'}),
               ("", {'layout': 'monadtall'}),
               ("", {'layout': 'monadtall'}),
               ("", {'layout': 'monadtall'}),
               ("", {'layout': 'monadtall'}),
               ("", {'layout': 'monadtall'}),
               ("", {'layout': 'monadtall'})]

groups = [Group(name, **kwargs) for name, kwargs in group_names]

for i, (name, kwargs) in enumerate(group_names, 1):
    # Switch to another group
    keys.append(Key([mod], str(i), lazy.group[name].toscreen()))
    # Send current window to another group
    keys.append(Key([mod, "shift"], str(i), lazy.window.togroup(name)))

layout_theme = {"border_width": 2,
                "margin": 10,
                "border_focus": "e1acff",
                "border_normal": "1D2330"
                }

layouts = [
    layout.MonadTall(**layout_theme),
    layout.Max(**layout_theme),
    # layout.Stack(num_stacks=2)
    # Try more layouts by unleashing below layouts.
    # layout.Bsp(),
    # layout.Columns(),
    # layout.Matrix(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font='Mononoki',
    fontsize=14,
    padding=3,
)

extension_defaults = widget_defaults.copy()

calcurse_appt = format_appointment()

screens = [
    Screen(
        bottom=bar.Bar(
            [
                widget.CurrentLayout(),
                widget.GroupBox(inactive="#808080"),
                widget.Prompt(),
                widget.WindowName(background="#924441"),
                widget.Chord(
                    chords_colors={
                        'launch': ("#ff0000", "#ffffff"),
                    },
                    name_transform=lambda name: name.upper()
                ),
                widget.TextBox(" "),
                widget.TextBox(""),
                widget.PulseVolume(),
                widget.TextBox(" "),
                widget.Sep(),
                widget.TextBox(" "),
                widget.TextBox("⌨"),
                widget.KeyboardLayout(),
                widget.TextBox(" "),
                widget.Sep(),
                widget.TextBox(" "),
                widget.TextBox(""),
                widget.TextBox(calcurse_appt),
                widget.TextBox(" "),
                widget.Sep(),
                widget.TextBox(" "),
                widget.TextBox(""),
                widget.Clock(format='%a %d-%m-%Y %I:%M %p'),
                widget.TextBox(" "),
                widget.Sep(),
                widget.TextBox(" "),
                widget.Systray(),
                # widget.QuickExit()
            ],
            30,
            background="#292d3e"
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None  # WARNING: this is deprecated and will be removed soon
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    {'wmclass': 'confirm'},
    {'wmclass': 'dialog'},
    {'wmclass': 'download'},
    {'wmclass': 'error'},
    {'wmclass': 'file_progress'},
    {'wmclass': 'notification'},
    {'wmclass': 'splash'},
    {'wmclass': 'toolbar'},
    {'wmclass': 'confirmreset'},  # gitk
    {'wmclass': 'makebranch'},  # gitk
    {'wmclass': 'maketag'},  # gitk
    {'wname': 'branchdialog'},  # gitk
    {'wname': 'pinentry'},  # GPG key password entry
    {'wmclass': 'ssh-askpass'},  # ssh-askpass
])
auto_fullscreen = True
focus_on_window_activation = "smart"

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
