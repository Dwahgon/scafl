#!/bin/bash
if ! command -v inkscape &> /dev/null
then
    echo "error: inkscape must be installed"
    exit 1
fi

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
PROJECT_DIR=$(dirname "$SCRIPT_DIR")
SHARE_DIR="$PROJECT_DIR/share"
MEDIA_DIR="$SHARE_DIR/scafl/media"
ICONS_DIR="$SHARE_DIR/icons/hicolor"

# Create tux farmer icon
SOURCE_ICON_NAME="tux-farmer"
TARGET_ICON_NAME="scafl"
ICON_SIZES=( "16" "22" "24" "32" "48" "64" "128" "256" "512" )
SOURCE_ICON="$MEDIA_DIR/$SOURCE_ICON_NAME.svg"
mkdir -p "$ICONS_DIR/scalable/apps/" && cp "$SOURCE_ICON" "$ICONS_DIR/scalable/apps/$TARGET_ICON_NAME.svg"
for SIZE in "${ICON_SIZES[@]}"
do
    ICON_DIR="$ICONS_DIR/${SIZE}x${SIZE}/apps"
    mkdir -p "$ICON_DIR"
    inkscape -w $SIZE -h $SIZE "$SOURCE_ICON" -o "$ICON_DIR/$TARGET_ICON_NAME.png"
done
