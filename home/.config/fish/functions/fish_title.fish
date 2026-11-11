function fish_title
    if set -q argv[1]; and test -n "$argv[1]"
        printf '%s · %s' "$argv[1]" (prompt_pwd)
    else
        prompt_pwd
    end
end
