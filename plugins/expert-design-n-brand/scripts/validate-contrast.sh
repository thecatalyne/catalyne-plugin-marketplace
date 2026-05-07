#!/usr/bin/env bash
#
# validate-contrast.sh — WCAG contrast ratio checker
#
# Usage:
#   ./validate-contrast.sh <foreground-hex> <background-hex>
#   ./validate-contrast.sh "#333333" "#FFFFFF"
#
# Output:
#   Contrast ratio and WCAG pass/fail for AA and AAA at normal and large text sizes.
#
# Requires: bc (pre-installed on macOS and most Linux distributions).

set -euo pipefail

if ! command -v bc >/dev/null 2>&1; then
  echo "error: validate-contrast.sh requires 'bc' (basic calculator)." >&2
  echo "  macOS: ships by default." >&2
  echo "  Debian/Ubuntu: sudo apt install bc" >&2
  echo "  Alpine: apk add bc" >&2
  echo "  RHEL/Fedora: sudo dnf install bc" >&2
  exit 127
fi

# Strip '#' prefix and convert to uppercase
normalize_hex() {
  local hex="${1#\#}"
  printf '%s' "$hex" | tr '[:lower:]' '[:upper:]'
}

# Convert hex to linear RGB channel (0-1 range)
hex_to_linear() {
  local hex="$1"
  local dec=$((16#$hex))
  local srgb
  srgb=$(echo "scale=10; $dec / 255" | bc)
  # Apply sRGB linearization
  local result
  result=$(echo "scale=10; if ($srgb <= 0.04045) $srgb / 12.92 else e(l(($srgb + 0.055) / 1.055) * 2.4)" | bc -l)
  echo "$result"
}

# Calculate relative luminance from hex color
relative_luminance() {
  local hex
  hex=$(normalize_hex "$1")

  local r_hex="${hex:0:2}"
  local g_hex="${hex:2:2}"
  local b_hex="${hex:4:2}"

  local r_lin g_lin b_lin
  r_lin=$(hex_to_linear "$r_hex")
  g_lin=$(hex_to_linear "$g_hex")
  b_lin=$(hex_to_linear "$b_hex")

  # L = 0.2126 * R + 0.7152 * G + 0.0722 * B
  echo "scale=10; 0.2126 * $r_lin + 0.7152 * $g_lin + 0.0722 * $b_lin" | bc -l
}

# Calculate contrast ratio between two luminances
contrast_ratio() {
  local l1="$1"
  local l2="$2"

  # Ensure l1 is the lighter color
  local lighter darker
  if (( $(echo "$l1 > $l2" | bc -l) )); then
    lighter="$l1"
    darker="$l2"
  else
    lighter="$l2"
    darker="$l1"
  fi

  echo "scale=4; ($lighter + 0.05) / ($darker + 0.05)" | bc -l
}

# Main
if [[ $# -lt 2 ]]; then
  echo "Usage: $0 <foreground-hex> <background-hex>"
  echo "Example: $0 '#333333' '#FFFFFF'"
  exit 1
fi

fg="$1"
bg="$2"

fg_lum=$(relative_luminance "$fg")
bg_lum=$(relative_luminance "$bg")
ratio=$(contrast_ratio "$fg_lum" "$bg_lum")

# Round to 2 decimal places for display
ratio_display=$(printf "%.2f" "$ratio")

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Foreground: $fg"
echo "  Background: $bg"
echo "  Contrast ratio: ${ratio_display}:1"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Check WCAG levels
check_pass() {
  local threshold="$1"
  local label="$2"
  local pass
  pass=$(echo "$ratio >= $threshold" | bc -l)
  if [[ "$pass" -eq 1 ]]; then
    echo "  PASS  $label (>= ${threshold}:1)"
  else
    echo "  FAIL  $label (>= ${threshold}:1)"
  fi
}

echo ""
check_pass 3.0  "AA Large text (18pt+ regular, 14pt+ bold)"
check_pass 4.5  "AA Normal text"
check_pass 4.5  "AAA Large text"
check_pass 7.0  "AAA Normal text"
check_pass 3.0  "Non-text UI elements"
echo ""
