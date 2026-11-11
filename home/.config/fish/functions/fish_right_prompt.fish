function fish_right_prompt --description 'Show elapsed time only for commands over two seconds'
    if set -q CMD_DURATION; and test "$CMD_DURATION" -ge 2000
        set_color 737aa2
        printf '%ss' (math --scale=1 "$CMD_DURATION / 1000")
        set_color normal
    end
end
