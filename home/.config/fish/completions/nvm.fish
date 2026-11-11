complete -c nvm -f
complete -c nvm -n '__fish_use_subcommand' -a 'install use list list-remote current uninstall' -d 'Manage Node.js versions'
complete -c nvm -s h -l help -d 'Show help'
complete -c nvm -s v -l version -d 'Show version'
complete -c nvm -s s -l silent -d 'Suppress output'
complete -c nvm -n '__fish_seen_subcommand_from use uninstall' -a '(_nvm_list | string split -f 1 " ")'
