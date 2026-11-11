function dots --description 'Open the symlinked dotfiles repository'
    set -l config (path resolve "$__fish_config_dir/config.fish")
    cd -- (path dirname (path dirname (path dirname (path dirname "$config"))))
end
