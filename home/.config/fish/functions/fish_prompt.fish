function fish_prompt --description 'Tokyo Night: path, Git state, environment, and exit status'
    set -l last_status $status
    set -l normal (set_color normal)
    set -l blue (set_color 7aa2f7)
    set -l violet (set_color bb9af7)
    set -l rose (set_color f7768e)
    set -l green (set_color 9ece6a)
    set -l symbol '❯'
    set -l symbol_color $violet
    if test "$last_status" -ne 0
        set symbol_color $rose
    end
    if fish_is_root_user
        set symbol '#'
        set symbol_color $rose
    end
    printf '\n%s╭─ %s%s' "$blue" (prompt_pwd) "$normal"
    if set -q SSH_TTY
        printf ' %s%s@%s%s' "$violet" "$USER" (prompt_hostname) "$normal"
    end
    fish_git_prompt ' (%s)'
    if set -q VIRTUAL_ENV
        printf ' %s[%s]%s' "$green" (path basename "$VIRTUAL_ENV") "$normal"
    else if set -q CONDA_DEFAULT_ENV
        printf ' %s[%s]%s' "$green" "$CONDA_DEFAULT_ENV" "$normal"
    end
    if test "$last_status" -ne 0
        printf ' %s× %s%s' "$rose" "$last_status" "$normal"
    end
    printf '\n%s╰─ %s%s ' "$symbol_color" "$symbol" "$normal"
end
