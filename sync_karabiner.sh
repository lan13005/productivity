#!/bin/bash

#########################################################################
# Sync karabiner.json from config directory to karabiner config location
# If files are different, show git diff between them before copying
#########################################################################

SOURCE_FILE="karabiner_config/karabiner.json"
DEST_FILE="$HOME/.config/karabiner/karabiner.json"

# Check if source file exists
if [ ! -f "$SOURCE_FILE" ]; then
    echo "Error: Source file $SOURCE_FILE does not exist"
    exit 1
fi

# Check if destination file exists
if [ ! -f "$DEST_FILE" ]; then
    echo "Destination file does not exist. Would you like to copy $SOURCE_FILE to $DEST_FILE? (y/n)"
    read -r response
    if [[ "$response" =~ ^[Yy]$ ]]; then
        mkdir -p "$(dirname "$DEST_FILE")"
        cp "$SOURCE_FILE" "$DEST_FILE"
        echo "Sync complete!"
    else
        echo "Sync cancelled."
    fi
    exit 0
fi

# Check if files are different
if ! cmp -s "$SOURCE_FILE" "$DEST_FILE"; then
    echo "Files are different. Showing diff:"
    echo "=================================="
    
    # Try to use git diff if available, otherwise use regular diff
    if command -v git &> /dev/null; then
        git diff --no-index "$DEST_FILE" "$SOURCE_FILE" || diff -u "$DEST_FILE" "$SOURCE_FILE"
    else
        diff -u "$DEST_FILE" "$SOURCE_FILE"
    fi
    
    echo "=================================="
    echo "Would you like to copy $SOURCE_FILE to $DEST_FILE? (y/n)"
    read -r response
    if [[ "$response" =~ ^[Yy]$ ]]; then
        cp "$SOURCE_FILE" "$DEST_FILE"
        echo "Sync complete!"
    else
        echo "Sync cancelled."
    fi
else
    echo "Files are identical. No sync needed."
fi
