#!/bin/bash

QUERY='
SELECT first_id, second_id
FROM EDGES
WHERE first_id < second_id
'

function main {
    local db
    db=$1
    {
	echo "digraph G {"
	sqlite3 "$db" "$QUERY" | while true; do
	    read line || break
	    first_id=${line%|*}
	    second_id=${line#*|}
	    printf '"%d" -> "%d";\n' "$first_id" "$second_id"
	done
	echo "}"
    } | dot -Tpdf -o$HOME/Downloads/big-data-visualization.pdf
}

main "$@"