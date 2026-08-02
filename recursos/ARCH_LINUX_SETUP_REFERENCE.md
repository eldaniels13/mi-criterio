# Arch Linux UI Setup Reference — eldaniels

**Purpose:** Complete reference for DeepSeek, ChatGPT, and Claude to understand current Arch Linux configuration and make informed suggestions for UI modifications, system tweaks, battery display, workspace indicators, statusline customization, and other desktop environment improvements.

**Last updated:** 2026-06-18  
**Valid for conversations about:** Arch Linux, COSMIC DE, i3wm, Hyprland, system configuration, UI/UX tweaks, statusline customization, hardware-software integration

---

## Current Setup

### Desktop Environment (Active)
- **Current WM/DE:** COSMIC DE (Rust-based, System76 project)
- **Next targets:** i3wm, then Hyprland
- **OS:** Arch Linux (7.0.11-arch1-1)
- **Shell:** zsh

### Hardware
| Component | Specs |
|-----------|-------|
| Laptop | Dell Latitude 5400 |
| CPU | i7-8665U (4 cores, 8 threads, low power) |
| RAM | ~32 GB |
| Storage | Kingston NV3 500GB M.2 NVMe (USB-C external) |
| Monitors | 2× Yodoit 15.6" FHD IPS (USB-C / HDMI) |
| Connectivity | Thunderbolt 3, 3× USB 3.1 Gen 1, USB-C |
| Hub | UGREEN Revodok Pro 210 (10-in-1, Dual HDMI, PD 3.0 100W) |
| IPv6 | Disabled |

### Audio/Input
| Device | Purpose |
|--------|---------|
| ATH-M50X | Primary headphones (monitoring, professional audio) |
| Bose Companion 3 Series II | Secondary speaker (ambient) — USB-A via UGREEN hub |
| Rapoo MT760L | Wireless mouse |

### Audio Troubleshooting: Bose Companion USB — Silence After Pause (FIXED 2026-06-20)

**Symptom:** After a period of silence (video paused, no audio playing), sound never resumes from the Bose. Spotify and Firefox produce no output. Only fix was unplugging and replugging the USB cable from the UGREEN hub.

**Root cause:** Two independent failures stacking:
1. **WirePlumber idle-suspend** closes the ALSA PCM stream when the Bose node goes idle. The Bose USB firmware can't re-initialize the stream when WirePlumber reopens it — the device accepts the connection but outputs silence.
2. **Kernel USB autosuspend** on the hub chain can reset `power/control` to `auto` on replug/reboot, letting the kernel power-cycle the device without the firmware recovering.

The unplug/replug worked because it forces full USB re-enumeration — a hardware reset — which is the only thing the firmware responds to.

**Fix — Layer 1: WirePlumber (never idle-suspend the Bose)**

File (lives OUTSIDE this repo): `~/.config/wireplumber/wireplumber.conf.d/51-bose-no-suspend.conf`

A `monitor.alsa.rules` drop-in that matches the Bose sink node and sets
`session.suspend-timeout-seconds = 0` + `api.alsa.use-acp = true`, so the ALSA
PCM is held open instead of being idle-suspended.

> Config file body is NOT stored in this repo by design (content-free repo rule).
> The actual file lives in the external backup restore bundle — see
> `P8_Backup_Wiki/Archivos_Criticos_Inventory.md` § Configs de sistema Arch Linux.

Apply: `systemctl --user restart wireplumber`

Verify: `sleep 8; pactl list short sinks | grep -i bose` → should show `IDLE`, not `SUSPENDED`.

**Fix — Layer 2: udev (persistent kernel-level power control)**

File (lives OUTSIDE this repo): `/etc/udev/rules.d/99-bose-usb-no-autosuspend.rules`

A single `ACTION=="add"` rule scoped to the Bose by vendor:product `05a7:1020`
that sets `power/control=on` and `power/autosuspend_delay_ms=-1`, persistent
across reboot and replug.

> Rule file body is NOT stored in this repo (content-free repo rule).
> Actual file lives in the external backup restore bundle.

Bose-only rule by design. **Do NOT add hub rules** — a USB hub cannot
autosuspend while a downstream child is active, so forcing the Bose to `on`
already keeps the parent UGREEN/Genesys hubs (`05e3:0610` → `05e3:0608`) awake.
The `05e3:0608` hub is shared with the display's DisplayPort Alt-Mode Billboard
device (`1d5c:7102`, `Driver=[none]`) — but video is out-of-band over HDMI/DP, so
USB power-control never affects the monitors. Keeping the rule scoped to the Bose
avoids touching anything display-related.

Important: `ACTION=="add"` fires on real plug/boot events. To apply it *now*
without rebooting, trigger an **add** action (NOT the default `change`):

```bash
sudo udevadm control --reload-rules
sudo udevadm trigger --action=add --subsystem-match=usb
```

Verify (Bose = `on`; the two hubs correctly stay `auto`):
```bash
for id in 05a7:1020 05e3:0610 05e3:0608; do
  v=${id%:*}; p=${id#*:}
  for d in /sys/bus/usb/devices/*/; do
    [ "$(cat $d/idVendor 2>/dev/null)" = "$v" ] && [ "$(cat $d/idProduct 2>/dev/null)" = "$p" ] && \
      echo "$id -> control=$(cat $d/power/control)"
  done
done
```

USB topology (for reference — `lsusb -t`):
```
1-1   05e3:0610 hub (UGREEN dock)
└─ 1-1.4   05e3:0608 hub
   ├─ 1-1.4.2  05a7:1020  Bose USB Audio      ← forced control=on
   └─ 1-1.4.4  1d5c:7102  Billboard (DP Alt-Mode, no driver) ← display signaling
```

**Safety:** These rules only keep the device in the same powered state as when audio is actively playing. No overvolting, no firmware writes, no thermal changes. Fully reversible by deleting the two config files.

**Migration note:** When moving to i3wm or Hyprland, WirePlumber carries over automatically (it's DE-independent). Only the udev rule needs to survive — it's in `/etc/udev/rules.d/` so it persists through any DE change.

---

## Known UI Customization Interests

### Statusline / Panel Modifications
User has asked about:
- **Battery percentage display** in statusline / panel
- **Workspace number indicator** (current workspace label/number)
- **Custom panels / bars**
- **System tray icons**
- **Time/date display customization**

### Configuration Touchpoints
- **COSMIC statusline:** location, customization, theme
- **Panel positioning:** top vs bottom, width
- **Font sizing:** readability across 2× 15.6" monitors
- **Color scheme:** preferences TBD (ask user)
- **Transparency/opacity:** preference for clarity vs aesthetics

### Previously Asked Topics (Patterns)
1. How to show battery % in the UI
2. How to display current workspace number
3. Monitor arrangement and scaling
4. Workspace management across dual displays
5. Power management on i7-8665U (battery optimization)

---

## COSMIC DE (Current)

### Known Capabilities
- Native Rust implementation, modern codebase
- Systemwide settings accessible via Settings app
- Statusline / topbar customization limited but present
- Workspaces supported (virtual desktops)
- Multi-monitor support (primary/secondary layout)

### Default Editor (Configured)
```bash
# Active in ~/.zshrc and current sessions:
export EDITOR="cosmic-text-editor"
```

### Files to Check/Modify
| Path | Purpose |
|------|---------|
| `~/.config/cosmic/` | COSMIC configuration directory (if exists) |
| `~/.local/share/cosmic/` | COSMIC data and cache |
| `dconf` / `gsettings` | Some settings may live in GSettings backend |
| `systemctl` | Power management, services |

### Panel/Statusline Config
- COSMIC uses a top panel by default
- Customization may require config files or Settings GUI
- Check if battery plugin exists or needs custom script

---

## Planned Transitions

### i3wm (Next Phase)
**Expected timeline:** After current COSMIC stabilization  
**Why:** Tiling WM, lightweight, full keyboard control, highly scriptable  

**Key considerations for i3:**
- Status bar: `i3status`, `polybar`, or `i3blocks` (user preference TBD)
- Battery display: handled via status bar config
- Workspace numbers: built-in, fully customizable
- Dual-monitor setup: i3 handles multi-monitor naturally
- Configuration file: `~/.config/i3/config`

**Likely custom additions:**
- Battery percentage in i3status/polybar
- Workspace indicators in statusbar
- Autostart scripts for monitor arrangement
- keybindings for workspace switching

### Hyprland (After i3wm)
**Expected timeline:** Medium-term future  
**Why:** Modern compositor, Wayland, aesthetics (blur, animations), still highly configurable  

**Key differences:**
- Full Wayland stack (not X11 like i3)
- Compositor-level effects (not window manager only)
- Configuration: `~/.config/hypr/hyprland.conf`
- Statusbar options: polybar still works, but Wayland-native alternatives recommended

---

## Common Customization Patterns

### Adding Battery Display

**COSMIC DE:**
```
Settings → Power → Battery (check if visible in statusline)
OR
Create custom script + place in panel widget location (TBD)
```

**i3wm (via i3status):**
```
~/.config/i3status/config
[battery 0]
format = "%status %percentage"
```

**i3wm (via polybar):**
```
~/.config/polybar/config.ini
[module/battery]
type = internal/battery
label-full = ...
label-charging = ...
label-discharging = ...
```

### Adding Workspace Number Display

**COSMIC DE:**
```
Workspaces already labeled; may need theme/styling change
```

**i3wm:**
```
Built-in: workspace numbers shown by default
Customize in i3status/polybar config under [mode] or custom script
```

### Monitor Scaling & Arrangement

**Tool:** `xrandr` (X11) or `wlr-randr` (Wayland)

**Common commands:**
```bash
# List monitors
xrandr --listmonitors

# Set resolution and position
xrandr --output HDMI-1 --mode 1920x1080 --pos 0x0 \
       --output eDP-1 --mode 1920x1080 --pos 1920x0
```

**For i3:** Save to `~/.config/i3/autostart.sh` or use `autorandr` package

---

## Power Management (i7-8665U specific)

### CPU Scaling
- Governor: `powersave` (on battery) or `performance` (plugged in)
- Check: `cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor`

### Display Power Saving
- Backlight control: usually via `light` or `brightnessctl` packages
- Display blanking: set via systemd or power manager

### Battery Optimization
- TLP or power-profiles-daemon recommended
- Monitor thermal: `sensors` command

---

## System Maintenance & Kernel Hygiene

### After `pacman -Syu` (including `linux` upgrades)

**Rule:** After a `pacman -Syu`, always reboot before using kernel modules.

Arch upgrades the `linux` package by replacing the old kernel version's module directory (`/lib/modules/<old-version>/`) with a new one (`/lib/modules/<new-version>/`). If you don't reboot, you're running the old kernel but the new module tree is on disk — any module-dependent operation fails:
- VeraCrypt containers (need `loop`)
- VirtualBox VMs (need `vbox*` modules)
- USB audio devices (may need `snd_usb_audio` reload)
- Encrypted removable drives (need `loop`, `dm_crypt`)

**Symptom:** `modprobe: FATAL: Module X not found in directory /lib/modules/<running-version>/` means your running kernel's module tree was deleted by an upgrade.

**Fix:** Just reboot. After reboot, `uname -r` matches the installed `linux` package, and all modules become available again.

**One-liner to check mismatch:**
```bash
[ "$(uname -r)" = "$(pacman -Q linux | awk '{print $2}')" ] && echo "kernel/package match OK" || echo "MISMATCH — reboot needed"
```

**Observation (2026-06-20):** VeraCrypt container mount failed with "failed to set up a loop device" after a kernel upgrade on 2026-06-18 without reboot. Single reboot restored all module-dependent functionality (loop, ntfs3, exfat). Agent suggested linux-lts and NTFS remounting; reboot alone fixed it.

---

## Accessibility & Scaling Preferences

### Font Sizing
- **Dual 15.6" FHD displays:** text can be small
- **DPI:** Likely 141-150 DPI (small form factor)
- **Scaling option:** May need 110-125% UI scaling depending on eyesight preference

### Color Preferences
- Light theme vs dark theme: **TBD** (ask user preference)
- High contrast mode: **TBD**
- Terminal theme: Monokai (mentioned in CLAUDE.md for MATLAB; may apply here too)

---

## How to Use This File with AI Assistants

When asking DeepSeek, ChatGPT, or Claude about UI modifications:

### Minimal context format
> "I'm on Arch Linux with COSMIC DE, Dell Latitude 5400, dual 15.6\" monitors. I want to [battery percentage in statusline / show workspace number / customize theme]. Can you help?"

### Link this file for full context
> "See `recursos/ARCH_LINUX_SETUP_REFERENCE.md` for my full setup. I want to [specific change]. Here's what I've tried: [...]"

### What to include in your request
1. **Goal:** What do you want to change/add?
2. **Current state:** COSMIC DE? i3wm? What's working now?
3. **Constraints:** Performance budget? Aesthetics preference? Time available?
4. **Previous attempts:** What didn't work?

---

## Files and Directories to Know

| Path | Purpose | Editable? |
|------|---------|-----------|
| `~/.config/cosmic/` | COSMIC config | Yes (if exists) |
| `~/.config/i3/` | i3wm config (future) | Yes |
| `~/.config/hypr/` | Hyprland config (future) | Yes |
| `~/.config/polybar/` | Polybar config (optional statusbar) | Yes |
| `~/.zshrc` | Zsh shell config | Yes |
| `/etc/pacman.conf` | Package manager config | Sudo |
| `~/.Xresources` | X11 resources (if used) | Yes |
| `~/.local/share/` | User data, caches | Varies |

---

## Packages to Know About

### Current / Relevant
- `cosmic-de` – Main desktop environment
- `cosmic-text-editor` – Native COSMIC text editor **(AUR; NOT `cosmic-edit` — that name does not exist in Arch repos)**
- `xorg-xrandr` – Monitor detection and control
- `light` or `brightnessctl` – Backlight control
- `tlp` – Power management

### For i3wm Transition
- `i3-wm` – Tiling window manager
- `i3status` or `polybar` – Status bar
- `dmenu` or `rofi` – Application launcher
- `urxvt` or `alacritty` – Terminal emulator

### For Hyprland Transition
- `hyprland` – Wayland compositor + WM
- `hyprpaper` – Wallpaper daemon
- `hyprlock` – Screen lock (Wayland-native)
- `waybar` or `polybar` – Status bar (Wayland)

---

## Contact & Update Protocol

**When to update this file:**
- New hardware added/removed
- Major WM transition (COSMIC → i3wm → Hyprland)
- New customization preferences discovered
- New constraint or accessibility need

**How to reference this in conversations:**
1. Paste link: `recursos/ARCH_LINUX_SETUP_REFERENCE.md`
2. Or paste key section (e.g., "## Current Setup")
3. Or simply mention: "See my Arch setup reference for context"

**Current maintainer:** eldaniels  
**Format:** Markdown (version 1.0)

---

## Quick Reference: Battery & Workspace Display

### What you want (common requests)

| Goal | COSMIC DE | i3wm | Hyprland |
|------|-----------|------|----------|
| Show battery % | Check Settings/Power panel | i3status/polybar config | waybar/polybar |
| Show workspace # | Built-in (may need styling) | Built-in (fully customizable) | Built-in (fully customizable) |
| Custom statusbar | Limited, use panel widgets | Full control (i3status/polybar) | Full control (waybar/polybar) |
| Dual monitor setup | Works via Settings | Works (needs xrandr setup) | Works (needs wlr-randr setup) |

---

## Notes for AI Assistants

- **eldaniels** is an engineer (mechanical background) with growing Linux/programming expertise
- Prefers **executable examples** over theory
- Will **test and iterate** — provide step-by-step instructions he can follow
- Likely knows about `systemctl`, `pacman`, basic Linux tooling
- May ask follow-ups about why a solution works (ask for explanation if interested)
- **Values:** simplicity, clarity, avoiding unnecessary bloat
- **Not looking for:** over-engineered solutions, unnecessary dependencies

---

## Tags for Search / Memory

`#arch-linux #cosmic-de #i3wm #hyprland #statusline #battery #workspace #ui-customization #dual-monitor #power-management #dell-latitude-5400`
