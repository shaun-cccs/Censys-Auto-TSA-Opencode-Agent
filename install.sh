#!/bin/sh
#
#  install.sh - put the Censys TSA kit where opencode can find it, everywhere.
#
#  WHAT THIS DOES
#  --------------
#  opencode discovers global agents, skills and plugins from its config
#  directory (~/.config/opencode). This script does not copy the kit there - it
#  symlinks five agent files, one plugin, one skill directory and the `tsa`
#  command out of this checkout, so that `git pull` updates everything at once
#  and prompts stay editable in place.
#
#  It edits no opencode.json. Verified against opencode 1.18.14: the config
#  directory is globbed for `{plugin,plugins}/*.{ts,js}` with symlinks followed,
#  so a symlinked plugin auto-loads with no config entry.
#
#  THE ONE SHARP EDGE: PLUGIN MODULE RESOLUTION
#  --------------------------------------------
#  The plugin does `import { tool } from "@opencode-ai/plugin"`. opencode
#  installs that package into its config directory itself, but module
#  resolution starts at the symlink's *real* path, not at the link. Measured:
#
#    - plugin real path inside  ~/.config/opencode  -> resolves (walks up to
#      ~/.config/opencode/node_modules) and loads
#    - plugin real path outside ~/.config/opencode  -> silently fails to load,
#      and a plugin that does not load enforces nothing
#
#  So when the kit lives outside the config directory this script bridges the
#  gap with a `node_modules` symlink at the kit root. `--copy` sidesteps the
#  issue entirely at the cost of needing a re-run after every `git pull`.
#
#  POSIX sh: macOS ships bash 3.2 and this must not care.

set -eu

# ---------------------------------------------------------------- self-location

self=$0
while [ -L "$self" ]; do
    target=$(readlink "$self")
    case $target in
        /*) self=$target ;;
        *) self=$(dirname "$self")/$target ;;
    esac
done
KIT=$(CDPATH= cd -- "$(dirname -- "$self")" && pwd -P)

# ------------------------------------------------------------------- arguments

#  opencode resolves its config directory from XDG_CONFIG_HOME, falling back to
#  ~/.config - so we must too, or an XDG user gets a perfectly successful install
#  that opencode never looks at.
CONFIG_DIR=${CENSYS_TSA_CONFIG_DIR:-${XDG_CONFIG_HOME:-$HOME/.config}/opencode}
BIN_DIR=${CENSYS_TSA_BIN_DIR:-$HOME/.local/bin}
CMD_NAME=tsa
MODE=install
DRY_RUN=no
USE_COPY=no
FORCE=no

usage() {
    cat <<'EOF'
install.sh - install the Censys TSA kit into opencode's global config

  ./install.sh                 symlink agents, plugin, skill and the tsa command
  ./install.sh --copy          copy instead of symlinking (re-run after git pull)
  ./install.sh --uninstall     remove only what this script created
  ./install.sh --doctor        check an existing install, change nothing
  ./install.sh --dry-run       print what would happen

Options:
  --name CMD          install the command as CMD instead of `tsa`
  --config-dir DIR    opencode config dir  (default $XDG_CONFIG_HOME/opencode,
                      i.e. ~/.config/opencode)
  --bin-dir DIR       where to put the command   (default ~/.local/bin)
  --force             replace files this script does not recognise as its own
  -h, --help
EOF
}

while [ $# -gt 0 ]; do
    case $1 in
        --uninstall) MODE=uninstall ;;
        --doctor) MODE=doctor ;;
        --dry-run) DRY_RUN=yes ;;
        --copy) USE_COPY=yes ;;
        --force) FORCE=yes ;;
        --name)
            shift
            [ $# -gt 0 ] || { printf 'install.sh: --name needs a value\n' >&2; exit 64; }
            CMD_NAME=$1
            ;;
        --config-dir)
            shift
            [ $# -gt 0 ] || { printf 'install.sh: --config-dir needs a value\n' >&2; exit 64; }
            CONFIG_DIR=$1
            ;;
        --bin-dir)
            shift
            [ $# -gt 0 ] || { printf 'install.sh: --bin-dir needs a value\n' >&2; exit 64; }
            BIN_DIR=$1
            ;;
        -h | --help) usage; exit 0 ;;
        *) printf 'install.sh: unknown option: %s\n' "$1" >&2; exit 64 ;;
    esac
    shift
done

AGENT_SRC="$KIT/.opencode/agent"
PLUGIN_SRC="$KIT/.opencode/plugin/tsa-capabilities.ts"
SKILL_SRC="$KIT/.opencode/skill/censys-tsa"

fail=0
note() { printf '  %s\n' "$1"; }
ok() { printf '  ok    %s\n' "$1"; }
warn() { printf '  WARN  %s\n' "$1"; }
bad() { printf '  FAIL  %s\n' "$1"; fail=$((fail + 1)); }
run() {
    if [ "$DRY_RUN" = yes ]; then
        printf '  would: %s\n' "$*"
    else
        "$@"
    fi
}

# Is $1 a path inside $2?
is_inside() {
    case $1 in
        "$2" | "$2"/*) return 0 ;;
        *) return 1 ;;
    esac
}

# Does this path belong to us - a symlink into the kit, or a copy of a kit file?
owned_by_kit() {
    _path=$1
    _src=$2
    if [ -L "$_path" ]; then
        _target=$(readlink "$_path")
        case $_target in
            /*) : ;;
            *) _target=$(cd -- "$(dirname -- "$_path")" && cd -- "$(dirname -- "$_target")" && pwd -P)/$(basename -- "$_target") ;;
        esac
        is_inside "$_target" "$KIT" && return 0
        return 1
    fi
    if [ -f "$_path" ] && [ -f "$_src" ] && cmp -s "$_path" "$_src"; then
        return 0
    fi
    return 1
}

link_one() {
    _src=$1
    _dst=$2
    if [ -e "$_dst" ] || [ -L "$_dst" ]; then
        if owned_by_kit "$_dst" "$_src"; then
            run rm -f "$_dst"
        elif [ "$FORCE" = yes ]; then
            warn "replacing unrecognised $_dst (--force)"
            run rm -rf "$_dst"
        else
            bad "$_dst exists and was not created by this kit - left alone (use --force to replace)"
            return 1
        fi
    fi
    if [ "$USE_COPY" = yes ]; then
        run cp -R "$_src" "$_dst"
    else
        run ln -s "$_src" "$_dst"
    fi
    ok "$_dst"
}

unlink_one() {
    _dst=$1
    _src=$2
    if [ ! -e "$_dst" ] && [ ! -L "$_dst" ]; then
        note "absent  $_dst"
        return 0
    fi
    if owned_by_kit "$_dst" "$_src"; then
        run rm -rf "$_dst"
        ok "removed $_dst"
    else
        warn "left alone (not ours): $_dst"
    fi
}

find_uv() {
    if [ -n "${CENSYS_TSA_UV:-}" ]; then printf '%s\n' "$CENSYS_TSA_UV"; return 0; fi
    if command -v uv >/dev/null 2>&1; then command -v uv; return 0; fi
    for c in "$HOME/.local/bin/uv" "$HOME/.cargo/bin/uv" /usr/local/bin/uv /opt/homebrew/bin/uv; do
        [ -x "$c" ] && { printf '%s\n' "$c"; return 0; }
    done
    return 1
}

# Follow a symlink chain to the real file it points at.
real_path_of() {
    _p=$1
    while [ -L "$_p" ]; do
        _t=$(readlink "$_p")
        case $_t in
            /*) _p=$_t ;;
            *) _p=$(dirname -- "$_p")/$_t ;;
        esac
    done
    printf '%s/%s\n' "$(CDPATH= cd -- "$(dirname -- "$_p")" && pwd -P)" "$(basename -- "$_p")"
}

# Walk up from a plugin file looking for the package it imports.
#
# Deliberately starts from the plugin's REAL path, not from the symlink in the
# config directory: that is where module resolution starts, and checking the
# link's own directory would happily "pass" the exact case this exists to catch.
plugin_import_resolves() {
    _dir=$(dirname -- "$(real_path_of "$1")")
    _dir=$(CDPATH= cd -- "$_dir" && pwd -P)
    while [ -n "$_dir" ] && [ "$_dir" != / ]; do
        if [ -d "$_dir/node_modules/@opencode-ai/plugin" ]; then
            return 0
        fi
        _dir=$(dirname -- "$_dir")
    done
    [ -d "/node_modules/@opencode-ai/plugin" ]
}

agent_names() {
    for f in "$AGENT_SRC"/*.md; do
        basename "$f"
    done
}

# ---------------------------------------------------------------------- doctor

doctor() {
    printf 'kit         %s\n' "$KIT"
    printf 'config dir  %s\n' "$CONFIG_DIR"
    printf 'command     %s/%s\n\n' "$BIN_DIR" "$CMD_NAME"

    printf 'tooling\n'
    if uv=$(find_uv); then
        ok "uv $("$uv" --version 2>/dev/null | cut -d' ' -f2) at $uv"
    elif [ -n "${CENSYS_TSA_PYTHON:-}" ]; then
        warn "no uv, but CENSYS_TSA_PYTHON=$CENSYS_TSA_PYTHON is set - uv is not needed"
    else
        bad "uv not found: curl -LsSf https://astral.sh/uv/install.sh | sh"
    fi
    if [ -x "$KIT/.venv/bin/python" ]; then
        ok "venv $KIT/.venv"
    elif [ -n "${CENSYS_TSA_PYTHON:-}" ]; then
        note "no venv; using CENSYS_TSA_PYTHON"
    else
        bad "no .venv - run: $KIT/install.sh"
    fi
    if command -v python3 >/dev/null 2>&1; then
        ok "python3 $(python3 -c 'import sys;print(".".join(map(str,sys.version_info[:3])))' 2>/dev/null)"
    else
        bad "no python3 on PATH - tsa cve/report/run need it (or set CENSYS_TSA_PYTHON)"
    fi
    if command -v opencode >/dev/null 2>&1; then
        ok "opencode $(opencode --version 2>/dev/null | tail -1)"
    else
        bad "opencode not on PATH"
    fi

    printf '\ncredentials (values are never printed)\n'
    if [ -n "${CENSYS_PERSONAL_ACCESS_TOKEN:-}" ]; then
        ok "CENSYS_PERSONAL_ACCESS_TOKEN is set"
    else
        bad "CENSYS_PERSONAL_ACCESS_TOKEN is not set - every Censys call will fail"
    fi
    if [ -n "${CENSYS_ORG_ID:-}" ]; then
        ok "CENSYS_ORG_ID is set"
    else
        bad "CENSYS_ORG_ID is not set - find it in the Censys Platform UI under
        Organization Settings, or on any platform.censys.io URL as ?org="
    fi

    printf '\ninstalled files\n'
    for name in $(agent_names); do
        dst="$CONFIG_DIR/agent/$name"
        if [ -e "$dst" ] || [ -L "$dst" ]; then
            if owned_by_kit "$dst" "$AGENT_SRC/$name"; then ok "$dst"; else warn "$dst exists but is not ours"; fi
        else
            bad "missing $dst"
        fi
    done
    plugin_dst="$CONFIG_DIR/plugin/tsa-capabilities.ts"
    if [ -e "$plugin_dst" ] || [ -L "$plugin_dst" ]; then
        if owned_by_kit "$plugin_dst" "$PLUGIN_SRC"; then
            ok "$plugin_dst"
            if [ -L "$plugin_dst" ] && ! cmp -s "$plugin_dst" "$PLUGIN_SRC"; then
                bad "the installed plugin differs from the kit's - re-run install.sh"
            fi
        else
            warn "$plugin_dst exists but is not ours"
        fi
        if plugin_import_resolves "$plugin_dst"; then
            ok "plugin can resolve @opencode-ai/plugin"
        else
            bad "the plugin cannot resolve @opencode-ai/plugin from its real path,
        so opencode will silently NOT load it and capabilities will NOT be
        enforced. Re-run: $KIT/install.sh   (or install.sh --copy)"
        fi
    else
        bad "missing $plugin_dst - capabilities would not be enforced"
    fi
    skill_dst="$CONFIG_DIR/skill/censys-tsa"
    if [ -e "$skill_dst" ] || [ -L "$skill_dst" ]; then
        ok "$skill_dst"
    else
        warn "missing $skill_dst (discovery skill only; agents still work)"
    fi
    cmd_dst="$BIN_DIR/$CMD_NAME"
    if [ -e "$cmd_dst" ] || [ -L "$cmd_dst" ]; then
        if owned_by_kit "$cmd_dst" "$KIT/bin/tsa"; then ok "$cmd_dst"; else warn "$cmd_dst exists but is not ours"; fi
    else
        bad "missing $cmd_dst"
    fi

    printf '\nPATH\n'
    if resolved=$(command -v "$CMD_NAME" 2>/dev/null); then
        if [ "$(cd -- "$(dirname -- "$resolved")" && pwd -P)" = "$(cd -- "$BIN_DIR" 2>/dev/null && pwd -P)" ]; then
            ok "$CMD_NAME resolves to $resolved"
        else
            warn "$CMD_NAME on PATH is $resolved, not $cmd_dst"
        fi
    else
        bad "$CMD_NAME is not on PATH.

        This matters more than it looks: the agents invoke \`$CMD_NAME\` by name,
        so without it on PATH every Censys call in a run fails. Add it to your
        shell profile (~/.zshrc, ~/.bashrc, ~/.profile) and open a new shell:

            export PATH=\"$BIN_DIR:\$PATH\""
    fi

    printf '\nagent discovery\n'
    if command -v opencode >/dev/null 2>&1; then
        listing=$(cd / && opencode agent list 2>/dev/null || true)
        for agent in censys-tsa censys-tsa-auto censys-fingerprint censys-deepdive censys-report; do
            if printf '%s' "$listing" | grep -q "^$agent "; then
                ok "$agent"
            else
                bad "$agent not visible to opencode - restart opencode after installing"
            fi
        done
    else
        warn "opencode not on PATH; cannot verify agent discovery"
    fi

    #  Pacing is the one capability the plugin cannot enforce - it lives in a
    #  state file the Python tools read - so it is worth seeing here. `standard`
    #  is reported as a warning because its rolling budget (200 requests/hour) is
    #  below what a single assessment issues, which stalls the run partway
    #  through. That was the shipped default once, and it cost hours.
    printf '\ncensys request pacing\n'
    profile=$("$KIT/bin/tsa" limits 2>/dev/null | sed -n 's/^Profile *: *\([a-z]*\).*/\1/p')
    case ${profile:-} in
        none) ok "profile 'none' - no pacing; credits are still capped separately" ;;
        fast) ok "profile 'fast' - bounded well above a full assessment" ;;
        standard)
            warn "profile 'standard' - 200 requests/hour, which is less than one
        assessment needs and will stall a run. Change it with: $CMD_NAME limits fast"
            ;;
        *) warn "could not read the pacing profile ($CMD_NAME limits)" ;;
    esac

    printf '\n'
    if [ "$fail" -gt 0 ]; then
        printf '%s check(s) failed.\n' "$fail"
        return 1
    fi
    printf 'All checks passed.\n'
    return 0
}

# --------------------------------------------------------------------- install

do_install() {
    printf 'Installing the Censys TSA kit\n'
    printf '  kit        %s\n' "$KIT"
    printf '  config dir %s\n' "$CONFIG_DIR"
    printf '  command    %s/%s\n\n' "$BIN_DIR" "$CMD_NAME"

    printf 'python environment\n'
    if [ -n "${CENSYS_TSA_PYTHON:-}" ]; then
        note "CENSYS_TSA_PYTHON is set; skipping uv sync"
    elif uv=$(find_uv); then
        if [ -f "$KIT/uv.lock" ]; then
            run "$uv" sync --project "$KIT" --frozen --quiet
        else
            run "$uv" sync --project "$KIT" --quiet
        fi
        ok "dependencies synced into $KIT/.venv"
    else
        printf '  FAIL  uv not found.\n\n' >&2
        cat >&2 <<'EOF'
  Install uv, then re-run this script:

      curl -LsSf https://astral.sh/uv/install.sh | sh

  uv is a single static binary; it does not touch your system Python. If you
  would rather manage the environment yourself, install censys-platform into an
  interpreter and set CENSYS_TSA_PYTHON to it.
EOF
        exit 127
    fi

    printf '\nlinking into opencode\n'
    run mkdir -p "$CONFIG_DIR/agent" "$CONFIG_DIR/plugin" "$CONFIG_DIR/skill" "$BIN_DIR"
    for name in $(agent_names); do
        link_one "$AGENT_SRC/$name" "$CONFIG_DIR/agent/$name" || true
    done
    link_one "$PLUGIN_SRC" "$CONFIG_DIR/plugin/tsa-capabilities.ts" || true
    link_one "$SKILL_SRC" "$CONFIG_DIR/skill/censys-tsa" || true
    link_one "$KIT/bin/tsa" "$BIN_DIR/$CMD_NAME" || true

    # The plugin's bare import resolves from its REAL path. If that is outside
    # the config dir there is no node_modules chain to walk, and opencode loads
    # the plugin silently as nothing. Bridge it.
    if [ "$USE_COPY" = no ] && ! is_inside "$KIT" "$(cd -- "$CONFIG_DIR" 2>/dev/null && pwd -P || printf '%s' "$CONFIG_DIR")"; then
        printf '\nplugin dependency bridge (kit lives outside %s)\n' "$CONFIG_DIR"
        if [ -e "$KIT/node_modules" ] || [ -L "$KIT/node_modules" ]; then
            note "$KIT/node_modules already exists"
        else
            run ln -s "$CONFIG_DIR/node_modules" "$KIT/node_modules"
            ok "$KIT/node_modules -> $CONFIG_DIR/node_modules"
        fi
    fi

    # Starting opencode once makes it install @opencode-ai/plugin into the
    # config dir for the plugin we just linked. Cheap, no model call.
    if [ "$DRY_RUN" = no ] && command -v opencode >/dev/null 2>&1; then
        printf '\nwarming opencode (installs the plugin runtime dependency)\n'
        (cd / && opencode agent list >/dev/null 2>&1) || true
        ok "done"
    fi

    printf '\n'
    if [ "$DRY_RUN" = yes ]; then
        printf 'Dry run: nothing was changed.\n'
        return 0
    fi

    printf -- '----------------------------------------------------------------\n'
    doctor || true
    printf -- '----------------------------------------------------------------\n'
    cat <<EOF

Quit and restart opencode - config, agents and plugins are loaded once at
startup and are not hot-reloaded.

Then, from any project:

    $CMD_NAME doctor                 check this install
    $CMD_NAME ref                    list the workflow references
    $CMD_NAME run "Ivanti EPMM"      unattended TSA into ./reports/

or in the opencode TUI, switch to the censys-tsa agent and name a target.
EOF
}

# ------------------------------------------------------------------- uninstall

do_uninstall() {
    printf 'Removing the Censys TSA kit from %s\n\n' "$CONFIG_DIR"
    for name in $(agent_names); do
        unlink_one "$CONFIG_DIR/agent/$name" "$AGENT_SRC/$name"
    done
    unlink_one "$CONFIG_DIR/plugin/tsa-capabilities.ts" "$PLUGIN_SRC"
    unlink_one "$CONFIG_DIR/skill/censys-tsa" "$SKILL_SRC"
    unlink_one "$BIN_DIR/$CMD_NAME" "$KIT/bin/tsa"
    #  Only remove the bridge if it points at the config directory we are
    #  uninstalling from. Without this check, `install.sh --uninstall` aimed at a
    #  throwaway directory - which is exactly what the test suite does - deletes
    #  the live install's bridge and silently stops the plugin from loading.
    if [ -L "$KIT/node_modules" ]; then
        _bridge=$(readlink "$KIT/node_modules")
        if [ "$_bridge" = "$CONFIG_DIR/node_modules" ]; then
            run rm -f "$KIT/node_modules"
            ok "removed $KIT/node_modules bridge"
        else
            warn "left alone (points elsewhere): $KIT/node_modules -> $_bridge"
        fi
    fi
    printf '\nThe kit itself, its .venv and any reports are untouched.\n'
    printf 'Restart opencode for the agents to disappear.\n'
}

case $MODE in
    install) do_install ;;
    uninstall) do_uninstall ;;
    doctor) doctor ;;
esac
