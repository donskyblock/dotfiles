function shellhelp --description 'Show the Tokyo Night shell shortcuts'
    set_color 7aa2f7
    printf 'Tokyo Night · Fish + Fisher\n'
    set_color normal
    printf '%-16s %s\n' \
        'Ctrl-R' 'Fuzzy command history' \
        'Ctrl-T' 'Find and insert a file path' \
        'Alt-C' 'Fuzzy directory picker' \
        'Right / Ctrl-F' 'Accept autosuggestion' \
        'Tab' 'Completions and searchable choices' \
        'z / zi' 'Smart directory jump / interactive jump' \
        'll / la' 'Detailed listing / show hidden entries' \
        'mkcd NAME' 'Create a directory and enter it' \
        'dots' 'Go to your dotfiles repository' \
        'gs / gd / gl' 'Git status / diff / recent graph' \
        'fisher --help' 'Plugin manager help'
end
