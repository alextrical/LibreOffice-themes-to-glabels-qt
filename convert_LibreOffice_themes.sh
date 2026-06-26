#!/usr/bin/env bash
set -euo pipefail

themes=(
  breeze
  breeze_dark
  colibre
  colibre_dark
  elementary
  karasa_jaga
  sifr
  sifr_dark
  sukapura
  sukapura_dark
)

for theme in "${themes[@]}"; do
  python resize_svg_icons.py \
    "./LibreOffice/icon-themes/${theme}_svg" \
    "./libreoffice_icon_table_${theme%%_dark}.csv" \
    "./build/${theme}"

  mode="light"
  [[ $theme == *_dark ]] && mode="dark"

  python3 generate_theme.py \
  --name ${theme} \
  --comment "gLabels ${theme%%_dark} icon theme (${mode})" \
  --csv libreoffice_icon_table_${theme%%_dark}.csv \
  -o ./build/${theme}/index.theme

  files=(COPYING COPYING-ICONS Copyrights LICENSE LICENSE.GPL AUTHORS)
  for f in "${files[@]}"; do
    [[ -e "./LibreOffice/icon-themes/${theme}_svg/$f" ]] && cp "./LibreOffice/icon-themes/${theme}_svg/$f" "./build/${theme}" || continue
  done
done