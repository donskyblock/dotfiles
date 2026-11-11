# Keep terminal pinentry attached to the current interactive terminal.
status is-interactive; or return
if isatty stdin
    set -gx GPG_TTY (tty)
end

# Reuse a per-user SSH agent once the private SSH config has been generated.
# Fish never prints or adds private keys here; SSH asks when the key is used.
if not test -f "$HOME/.ssh/config"
    return
end
if set -q SSH_AUTH_SOCK
    command ssh-add -l >/dev/null 2>&1
    if test $status -le 1
        return
    end
end
# Prefer the desktop keyring's SSH agent for graphical unlock and persistence.
if type -q gnome-keyring-daemon; and set -q XDG_RUNTIME_DIR
    command "$HOME/.local/bin/dotfiles-keyring-session" >/dev/null 2>&1
    set -l keyring_socket "$XDG_RUNTIME_DIR/keyring/ssh"
    if test -S "$keyring_socket"
        set -gx SSH_AUTH_SOCK "$keyring_socket"
        return
    end
end

set -l agent_socket "$HOME/.ssh/agent.sock"
set -gx SSH_AUTH_SOCK "$agent_socket"
command ssh-add -l >/dev/null 2>&1
if test $status -gt 1
    if test -S "$agent_socket"
        command rm -- "$agent_socket"
    end
    command ssh-agent -a "$agent_socket" -c 2>/dev/null | source >/dev/null
end
