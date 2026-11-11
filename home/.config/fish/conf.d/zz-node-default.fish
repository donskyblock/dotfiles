# Default major is versioned here; runtime binaries and registry credentials are not.
set -g nvm_default_version 22
set -g nvm_default_packages npm@11 pnpm@latest
set -gx PNPM_HOME "$HOME/.local/share/pnpm"
fish_add_path --global "$PNPM_HOME"

# Avoid network requests and startup errors before the runtime is installed.
# Applies to interactive shells and Fish -c (editor tasks, scripts, etc.).
if test -f "$nvm_data/.index"
    for node_directory in "$nvm_data"/v22.*
        if test -x "$node_directory/bin/node"
            nvm use --silent 22
            break
        end
    end
end
