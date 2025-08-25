py_files=$(find src/pycatsearch_qt -iname "*.py" -type f)
L_UPDATE="../qt-linguist/lupdate.py"
if [[ -e ${L_UPDATE} ]]; then L_UPDATE="python ${L_UPDATE}"; else L_UPDATE="pyside6-lupdate"; fi
echo using "${L_UPDATE}"
for n in src/pycatsearch_qt/i18n/*.ts; do
  # shellcheck disable=SC2086
  ${L_UPDATE} ${py_files} -ts "${n}" "$@"
done
