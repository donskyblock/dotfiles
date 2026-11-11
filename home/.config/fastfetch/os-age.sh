#!/bin/sh
# Root-directory birth time is an estimate of installation time.
# Do not fall back to modification time: ordinary updates change it.
born=$(stat -c %W / 2>/dev/null) || born=0
now=$(date +%s)
case "$born" in ''|*[!0-9]*) born=0 ;; esac
if [ "$born" -le 0 ] || [ "$born" -gt "$now" ]; then
    printf 'Unknown (creation date unavailable)\n'
    exit 0
fi
days=$(( (now - born) / 86400 ))
installed=$(date -d "@$born" +%Y-%m-%d)
if [ "$days" -eq 0 ]; then
    printf 'Less than a day · since %s\n' "$installed"
elif [ "$days" -eq 1 ]; then
    printf '1 day · since %s\n' "$installed"
else
    printf '%s days · since %s\n' "$days" "$installed"
fi
