#!/usr/bin/env bash
set -euo pipefail

themes=(
  breeze
  # oxygen
)

for theme in "${themes[@]}"; do

  # pushd "$PWD" >/dev/null
  # cd ./freedesktop/${theme}
  # rm -rf CMakeCache.txt CMakeFiles cmake_install.cmake Makefile build
  # cmake -S . -B build \
  #   -D CMAKE_INSTALL_PREFIX=/usr/local \
  #   -D BUILD_TESTING=OFF \
  #   -D WITH_ICON_GENERATION=OFF \
  #   -W no-dev
  # cmake --build build --parallel "$(sysctl -n hw.ncpu)"
  # popd >/dev/null

  mode="light"
  # [[ $theme == *_dark ]] && mode="dark"

  python resize_svg_icons.py \
  "./freedesktop/${theme}" \
  "./freedesktop_icon_table_${theme%%_dark}.csv" \
  "./build/${theme}"

  # python3 generate_theme.py \
  # --name ${theme} \
  # --comment "gLabels ${theme%%_dark} icon theme (${mode})" \
  # --csv freedesktop_icon_table_${theme%%_dark}.csv \
  # -o ./build/${theme}/index.theme

  # files=(COPYING COPYING-ICONS Copyrights LICENSE LICENSE.GPL AUTHORS)
  # for f in "${files[@]}"; do
  #   [[ -e "./freedesktop/${theme}/$f" ]] && cp "./freedesktop/${theme}/$f" "./build/${theme}" || continue
  # done
done