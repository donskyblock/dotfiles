# .bashrc

# If not running interactively, don't do anything
[[ $- != *i* ]] && return

alias ls='ls --color=auto'
PS1='[\u@\h \W]\$ '

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
