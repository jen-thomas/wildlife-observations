#!/bin/bash

SCRIPT_BASE_DIRECTORY=$(dirname "${BASH_SOURCE[0]}")

DESTINATION_FILE="$SCRIPT_BASE_DIRECTORY/../database_backups/wildlife-observations-db-$(date +%Y%m%d-%H%M%S).sql"
DESTINATION_FILE=$(realpath "$DESTINATION_FILE")


echo .dump | sqlite3 "$SCRIPT_BASE_DIRECTORY/../WildlifeObservations/wildlife-observations-db.sqlite3" > "$DESTINATION_FILE"

echo "Backup done: $DESTINATION_FILE"
