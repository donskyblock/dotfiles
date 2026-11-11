# Tokyo Night Fish. Keep secrets in ~/.config/fish/local.fish, outside Git.
fish_add_path --global --move "$HOME/.local/bin"
set -gx XCURSOR_THEME TokyoNight-Black
set -gx XCURSOR_SIZE 20
status is-interactive; or return

set -g fish_greeting
set -g fish_key_bindings fish_default_key_bindings
set -g fish_cursor_default block
set -g fish_cursor_insert line
set -g fish_cursor_replace_one underscore
set -g fish_autosuggestion_enabled 1

# Tokyo Night command-line syntax and completion menu.
set -g fish_color_normal c0caf5
set -g fish_color_command 7aa2f7
set -g fish_color_keyword bb9af7
set -g fish_color_quote 9ece6a
set -g fish_color_redirection 7dcfff
set -g fish_color_end bb9af7
set -g fish_color_error f7768e
set -g fish_color_param c0caf5
set -g fish_color_comment 737aa2
set -g fish_color_match 7dcfff
set -g fish_color_search_match --background=33467c
set -g fish_color_operator 7dcfff
set -g fish_color_escape ff9e64
set -g fish_color_autosuggestion 565f89
set -g fish_color_cwd 7aa2f7
set -g fish_color_cwd_root f7768e
set -g fish_color_valid_path --underline
set -g fish_color_selection --background=33467c
set -g fish_pager_color_prefix 7dcfff
set -g fish_pager_color_completion c0caf5
set -g fish_pager_color_description a9b1d6
set -g fish_pager_color_progress bb9af7
set -g fish_pager_color_selected_background --background=292e42
set -gx LS_COLORS 'di=38;2;122;162;247:ln=38;2;125;207;255:ex=38;2;158;206;106:*.tar=38;2;187;154;247:*.7z=38;2;187;154;247:*.xz=38;2;187;154;247:*.gz=38;2;224;175;104:*.zip=38;2;224;175;104'

# Git status uses Fish's bundled implementation; no prompt plugins required.
set -g __fish_git_prompt_showdirtystate 1
set -g __fish_git_prompt_showuntrackedfiles 1
set -g __fish_git_prompt_showstashstate 1
set -g __fish_git_prompt_showupstream auto
set -g __fish_git_prompt_use_informative_chars 1
set -g __fish_git_prompt_color_branch bb9af7
set -g __fish_git_prompt_color_dirtystate e0af68
set -g __fish_git_prompt_color_stagedstate 9ece6a
set -g __fish_git_prompt_color_untrackedfiles 7dcfff
set -g __fish_git_prompt_color_invalidstate f7768e

abbr --add --global g git
abbr --add --global gs 'git status --short --branch'
abbr --add --global gd 'git diff'
abbr --add --global gds 'git diff --staged'
abbr --add --global ga 'git add'
abbr --add --global gc 'git commit'
abbr --add --global gl 'git log --oneline --graph --decorate -15'
abbr --add --global .. 'cd ..'
abbr --add --global ... 'cd ../..'
alias ls 'ls --color=auto'
alias ll 'ls -lah --color=auto'
alias la 'ls -A --color=auto'

# Fuzzy history (Ctrl-R), files (Ctrl-T), and directories (Alt-C).
if type -q fzf
    set -gx FZF_DEFAULT_OPTS '--height=45% --layout=reverse --border=rounded --info=inline --color=bg:#1a1b26,bg+:#292e42,fg:#c0caf5,fg+:#c0caf5,hl:#7aa2f7,hl+:#7dcfff,info:#bb9af7,prompt:#7aa2f7,pointer:#bb9af7,marker:#9ece6a,spinner:#bb9af7,header:#737aa2,border:#414868'
    if type -q fd
        set -gx FZF_DEFAULT_COMMAND 'fd --type f --hidden --exclude .git'
        set -gx FZF_CTRL_T_COMMAND "$FZF_DEFAULT_COMMAND"
        set -gx FZF_ALT_C_COMMAND 'fd --type d --hidden --exclude .git'
    end
    fzf --fish | source
end

# z <name> learns your directories; zi opens an interactive chooser.
if type -q zoxide
    zoxide init fish | source
end

# Optional private overrides are intentionally excluded from the manifest.
if test -f "$__fish_config_dir/local.fish"
    source "$__fish_config_dir/local.fish"
end
