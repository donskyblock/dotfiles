complete -c fisher -f
complete -c fisher -n '__fish_use_subcommand' -a 'install update remove list' -d 'Manage Fish plugins'
complete -c fisher -s h -l help -d 'Show help'
complete -c fisher -s v -l version -d 'Show version'
complete -c fisher -n '__fish_seen_subcommand_from remove update' -a '(fisher list)'
