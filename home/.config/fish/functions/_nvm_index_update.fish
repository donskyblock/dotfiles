# Based on jorgebucaran/nvm.fish (MIT); fail cleanly on HTTP/network errors.
function _nvm_index_update
    test -d "$nvm_data"; or command mkdir -p "$nvm_data"
    set -l index "$nvm_data/.index"
    if not command curl -q --fail --location --silent --show-error "$nvm_mirror/index.tab" >"$index.temp"
        command rm -f "$index.temp"
        printf 'nvm: Cannot download the Node index from %s\n' "$nvm_mirror" >&2
        return 1
    end
    command awk -v OFS=\t '
        /v0.9.12/ { exit }
        NR > 1 { print $1 (NR == 2 ? " latest" : $10 != "-" ? " lts/" tolower($10) : "") }
    ' "$index.temp" >"$index"
    command rm -f "$index.temp"
end
