# SSH Agent Passphrase Issue - Diagnosis & Context

## Problem Statement

Every time I open a new terminal in COSMIC (Wayland, Arch Linux), the system asks for the SSH passphrase for `~/.ssh/mi-criterio`. This should only happen once per login session, not per terminal.

## Current Setup

**Hardware & OS:**
- Dell Latitude 5400 (Intel i7-8665U)
- Arch Linux with COSMIC Desktop (Wayland-based)
- User: `eldaniels`
- Shell: zsh

**SSH Key Configuration:**
- Key location: `~/.ssh/mi-criterio` (ED25519)
- Key is encrypted with a passphrase
- Key has been successfully added to ssh-agent (verified with `ssh-add -l`)
- Output: `256 SHA256:SevukjFxnkMJPxmGR6isnAcz9CEACTq3XTvEVjcWqoM eldaniels13+mi-criterio@github.com (ED25519)`

## Current `.zshrc` Configuration

```bash
# SSH Agent initialization
if [ -z "$SSH_AUTH_SOCK" ]; then
    eval "$(ssh-agent -s)" > /dev/null
    ssh-add ~/.ssh/mi-criterio
fi
```

## The Problem - Root Cause Analysis

The issue is that **every new terminal window is a completely independent process** with its own environment variables. When you open terminal #1, the SSH Agent starts and the passphrase is entered once. But when you open terminal #2, that new terminal has **no knowledge** of the SSH Agent that's running from terminal #1.

**What happens:**

1. Terminal #1 opens → zsh reads `.zshrc` → `SSH_AUTH_SOCK` is empty → new ssh-agent starts → passphrase entered once
2. Terminal #2 opens → zsh reads `.zshrc` **in a fresh environment** → `SSH_AUTH_SOCK` is **still empty in this new shell context** → new ssh-agent starts → passphrase demanded again
3. Meanwhile, the original ssh-agent from terminal #1 is still running with the key loaded, but terminal #2 can't access it because it doesn't know its socket location

**Verification:**

When executing `ssh-agent -h 2>&1 | grep -i socket`, no output was returned, which indicates the system's ssh-agent version does **not** support the `-a` flag to specify a custom socket location. This rules out the advanced persistent solution.

## Expected Behavior

The passphrase should be requested **once per login session**, not once per terminal. All terminals opened during the same COSMIC session should share the same ssh-agent instance.

## Attempted Solutions (and why they failed)

1. **Basic configuration with `2>/dev/null`**: This silently suppressed errors but didn't solve the core issue — each terminal still started its own ssh-agent.

2. **Persistent agent with socket files**: Required `ssh-agent -a` flag, which this system's ssh-agent doesn't support.

## Solution Approaches to Explore

### Option A: Use systemd user socket (Most Modern)
Create a systemd user service that runs ssh-agent once at login, making it available to all terminals via a standardized socket path.

Advantages:
- Works with Wayland
- Integrates with systemd user session
- The ssh-agent persists across all terminals automatically

### Option B: Use `gpg-agent` with SSH support (Alternative)
Configure GPG agent to handle SSH keys instead of using ssh-agent. GnuPG is often already integrated with desktop environments.

Advantages:
- Single unified credential store
- Better integration with Wayland
- gpg-agent handles SSH auth natively

### Option C: Use environment file approach (Simple workaround)
Write ssh-agent's socket information to a file at session start, then source that file in `.zshrc`.

Advantages:
- Works with any ssh-agent version
- No new dependencies
- Relatively simple to implement

### Option D: Rely on COSMIC's built-in SSH integration
COSMIC (as a modern Wayland desktop) may have a built-in SSH key manager that we're not using correctly.

## Questions for Investigation

1. Does COSMIC have a native SSH key manager or credential daemon running?
2. What is the default mechanism COSMIC uses for handling SSH keys?
3. Are there environment variables being set by COSMIC at login that we should be leveraging?
4. Would systemd user services be the appropriate approach for Arch Linux + COSMIC?

## System Information for Reference

- SSH Version: (need to check: `ssh -V`)
- SSH Agent Version: Does not support `-a` flag
- zsh Version: (need to check: `zsh --version`)
- COSMIC Session Type: Wayland
- Init System: systemd

## Files Involved

- `~/.zshrc` - Shell configuration (lines 46-50 contain SSH Agent init)
- `~/.ssh/mi-criterio` - ED25519 private key
- `~/.ssh/mi-criterio.pub` - Public key
- `~/.ssh/config` - SSH configuration (if it exists)

## Next Steps

Determine which solution approach is most appropriate for COSMIC/Wayland/Arch setup, then implement and test thoroughly across multiple terminal instances.
