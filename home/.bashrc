# .bashrc

# If not running interactively, don't do anything
[[ $- != *i* ]] && return

alias ls='ls --color=auto'
# Two-line Tokyo Night prompt; no external prompt framework required.
PS1='\[\e[38;2;122;162;247m\]╭─ \w\[\e[0m\]\n\[\e[38;2;187;154;247m\]╰─ ❯\[\e[0m\] '
export LS_COLORS='di=38;2;122;162;247:ln=38;2;125;207;255:ex=38;2;158;206;106:ar=38;2;187;154;247:*.gz=38;2;224;175;104:*.zip=38;2;224;175;104'
alias ll='ls -lah'
alias dots='cd "$HOME/dotfiles"'
# Keep terminal titles useful without exposing host/user names.
case "$TERM" in xterm*|foot*) PROMPT_COMMAND='printf "\033]0;%s\007" "${PWD/#$HOME/~}"' ;; esac

# Launch MangoWC on NVIDIA
ma() { 
	export WLR_DRM_DEVICES=/dev/dri/card1 
	dbus-run-session mango
}

# >>> Codex installer >>>
export PATH="$HOME/.local/bin:$PATH"
# <<< Codex installer <<<

# Private, machine-specific settings (never tracked here).
[ ! -f "$HOME/.bashrc.local" ] || . "$HOME/.bashrc.local"
