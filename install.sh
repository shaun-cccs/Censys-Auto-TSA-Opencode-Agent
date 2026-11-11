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
#  OPENCODE 1 AND OPENCODE 2
#  -------------------------
#  OpenCode 2 (verified on 2.2.7) still reads the agent/ and skill/ folders, but
#  it has a new plugin API and does not run V1 plugins. The kit therefore ships
#  two plugin entrypoints with the same rules:
#
#    V1  plugins/v1/tsa-capabilities.ts      -> plugin/tsa-capabilities.ts
#    V2  plugins/v2/tsa-capabilities/        -> plugins/tsa-capabilities/
#
#  The sources live outside .opencode/ on purpose: OpenCode auto-loads plugins
#  from a project's .opencode/, so opening this checkout would load them a
#  second time (V2: "Duplicate plugin ID") or try to run the V1 file on V2.
#
#  The script links the one that matches `opencode --version`, or both when
#  opencode is not on PATH (V1 ignores the V2 directory; V2 logs a load failure
#  for the V1 file and carries on). Override with --opencode 1|2|both.
#  OpenCode 2 supplies its own `@opencode/plugin`, so the node_modules bridge
#  described below is a V1-only concern.
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
OPENCODE_MAJOR=${CENSYS_TSA_OPENCODE:-auto}
#  auto = add the Censys MCP server once the credentials are verified.
WITH_MCP=auto
NO_PROMPT=no
CREDS_SAVED=no

usage() {
    cat <<'EOF'
install.sh - install the Censys TSA kit into opencode's global config

  ./install.sh                 symlink agents, plugin, skill and the tsa command
  ./install.sh --copy          copy instead of symlinking (re-run after git pull)
  ./install.sh --uninstall     remove only what this script created
  ./install.sh --doctor        check an existing install, change nothing
  ./install.sh --dry-run       print what would happen
  ./install.sh --credentials   prompt for the two Censys credentials, check them
                               against Censys, and save them to your shell profile
  ./install.sh --mcp           add the Censys Platform MCP server even if the
                               credentials are not set yet (with --uninstall: remove it)
  ./install.sh --no-mcp        never add the MCP server
                               (default: added once the credentials check out)

Options:
  --name CMD          install the command as CMD instead of `tsa`
  --config-dir DIR    opencode config dir  (default $XDG_CONFIG_HOME/opencode,
                      i.e. ~/.config/opencode)
  --bin-dir DIR       where to put the command   (default ~/.local/bin)
  --opencode 1|2|both which plugin to install (default: from `opencode --version`,
                      or both when opencode is not on PATH)
  --no-prompt         never ask for credentials (for scripts and CI)
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
        --mcp) WITH_MCP=yes ;;
        --no-mcp) WITH_MCP=no ;;
        --credentials) MODE=credentials ;;
        --no-prompt) NO_PROMPT=yes ;;
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
        --opencode)
            shift
            [ $# -gt 0 ] || { printf 'install.sh: --opencode needs 1, 2 or both\n' >&2; exit 64; }
            OPENCODE_MAJOR=$1
            ;;
        -h | --help) usage; exit 0 ;;
        *) printf 'install.sh: unknown option: %s\n' "$1" >&2; exit 64 ;;
    esac
    shift
done

AGENT_SRC="$KIT/.opencode/agent"
PLUGIN_SRC="$KIT/plugins/v1/tsa-capabilities.ts"
PLUGIN_V2_SRC="$KIT/plugins/v2/tsa-capabilities"

#  1, 2, or "both". Read once; the doctor and the installer agree on it.
case $OPENCODE_MAJOR in
    1 | 2 | both) : ;;
    auto)
        _ver=$(opencode --version 2>/dev/null | tail -1 || true)
        case $_ver in
            *[0-9].[0-9]*)
                _major=$(printf '%s\n' "$_ver" | sed -n 's/^[^0-9]*\([0-9][0-9]*\)\..*/\1/p')
                if [ "${_major:-1}" -ge 2 ]; then OPENCODE_MAJOR=2; else OPENCODE_MAJOR=1; fi
                ;;
            *) OPENCODE_MAJOR=both ;;
        esac
        ;;
    *) printf 'install.sh: --opencode must be 1, 2 or both, not %s\n' "$OPENCODE_MAJOR" >&2; exit 64 ;;
esac
wants_v1() { [ "$OPENCODE_MAJOR" != 2 ]; }
wants_v2() { [ "$OPENCODE_MAJOR" != 1 ]; }
SKILL_SRC="$KIT/.opencode/skill/censys-tsa"

fail=0
#  Colour only on a terminal, and never when NO_COLOR is set (no-color.org), so
#  logs and the test suite see plain text.
if [ -t 1 ] && [ -z "${NO_COLOR:-}" ]; then
    C_RED=$(printf '\033[1;31m') C_YEL=$(printf '\033[1;33m') C_GRN=$(printf '\033[32m')
    C_CYN=$(printf '\033[1;36m') C_BLD=$(printf '\033[1m') C_OFF=$(printf '\033[0m')
else
    C_RED= C_YEL= C_GRN= C_CYN= C_BLD= C_OFF=
fi
note() { printf '  %s\n' "$1"; }
ok() { printf '  %sok%s    %s\n' "$C_GRN" "$C_OFF" "$1"; }
warn() { printf '  %sWARN%s  %s\n' "$C_YEL" "$C_OFF" "$1"; }
bad() { printf '  %sFAIL%s  %s\n' "$C_RED" "$C_OFF" "$1"; fail=$((fail + 1)); }
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

#  The Censys MCP server is the one thing this script writes into opencode.json,
#  and only with --mcp. The entry references $CENSYS_PERSONAL_ACCESS_TOKEN and
#  $CENSYS_ORG_ID as {env:...} placeholders; no secret is written.
mcp_config() {
    _action=$1
    if [ "$OPENCODE_MAJOR" = both ]; then
        warn "opencode not on PATH, so its config format is unknown - MCP server skipped.
        Re-run with --opencode 1 or --opencode 2"
        return 0
    fi
    _dry=
    [ "$DRY_RUN" = yes ] && [ "$_action" != status ] && _dry=--dry-run
    python3 "$KIT/scripts/mcp_config.py" "$_action" --config-dir "$CONFIG_DIR" \
        --major "$OPENCODE_MAJOR" $_dry || true
}

#  Step-by-step help for the two Censys variables. Printed by the doctor when
#  either is missing. Never reads or prints a value.
credentials_help() {
    case ${SHELL:-} in
        */zsh) _rc="~/.zshrc" ;;
        */bash) _rc="~/.bashrc" ;;
        *) _rc="~/.profile" ;;
    esac
    cat <<EOF

${C_YEL}================================================================
 ACTION NEEDED: set your Censys credentials
================================================================${C_OFF}
 Your Censys account needs the "API Access" role in the organization
 (ask your Censys org admin if the pages below show no API options).

 ${C_CYN}1. CENSYS_PERSONAL_ACCESS_TOKEN${C_OFF}
    - Sign in at https://platform.censys.io
    - Click your user icon (top right) > API Access, or go straight to
      ${C_BLD}https://accounts.censys.io/settings/personal-access-tokens${C_OFF}
    - Click "Create New Token", name it (e.g. opencode-tsa), click
      Create, then "Copy to clipboard". It is shown only once.

 ${C_CYN}2. CENSYS_ORG_ID${C_OFF}
    - On that same page, make sure your organization (not your Free
      account) is selected. The "Current Organization" box shows the
      ID - click Copy. It looks like 1a2b3c4d-5e6f-....
    - No organization ID means a Free account: calls run with Free
      limits, and most TSA queries will fail.

 ${C_CYN}3. Add them to $_rc (or let ${C_BLD}./install.sh --credentials${C_CYN} do steps 3-4
    for you), then open a new terminal:${C_OFF}

      ${C_BLD}export CENSYS_PERSONAL_ACCESS_TOKEN='paste-token-here'
      export CENSYS_ORG_ID='paste-org-id-here'${C_OFF}

    Keep that file private (chmod 600 $_rc). Do not commit it, and do
    not put the token in opencode.json - the kit and the MCP server
    read it from the environment.

 ${C_CYN}4. Check:${C_OFF}   ${C_BLD}tsa doctor${C_OFF}

 Source: https://docs.censys.com/reference/get-started
${C_YEL}================================================================${C_OFF}
EOF
}

agent_names() {
    for f in "$AGENT_SRC"/*.md; do
        basename "$f"
    done
}

# ----------------------------------------------------------------- credentials

#  The marked block this script owns in the shell profile. Replaced, never
#  duplicated, on a re-run.
CRED_BEGIN='# >>> censys-tsa credentials (managed by install.sh) >>>'
CRED_END='# <<< censys-tsa credentials <<<'

profile_file() {
    case ${SHELL:-} in
        */zsh) printf '%s\n' "$HOME/.zshrc" ;;
        */bash) printf '%s\n' "$HOME/.bashrc" ;;
        *) printf '%s\n' "$HOME/.profile" ;;
    esac
}

ask_yes() {  # ask_yes "question" default(y|n)
    _def=$2
    if [ "$_def" = y ]; then _hint='[Y/n]'; else _hint='[y/N]'; fi
    printf '%s %s ' "$1" "$_hint"
    read -r _ans || _ans=
    [ -z "$_ans" ] && _ans=$_def
    case $_ans in [Yy]*) return 0 ;; *) return 1 ;; esac
}

#  Reads into $CENSYS_TSA_SECRET without echoing it. The value is never put on a
#  command line (where `ps` would show it) - only into the environment of the
#  check below and into the profile file.
read_secret() {
    printf '%s' "$1"
    _stty=$(stty -g 2>/dev/null || true)
    trap 'stty "$_stty" 2>/dev/null; exit 130' INT TERM
    stty -echo 2>/dev/null || true
    read -r CENSYS_TSA_SECRET || CENSYS_TSA_SECRET=
    stty "$_stty" 2>/dev/null || true
    trap - INT TERM
    printf '\n'
}

#  Free call: the org credit-balance endpoint costs no credits.
verify_credentials() {
    printf '  checking with Censys (credit balance - costs no credits)...\n'
    # `|| _rc=$?` keeps `set -e` from ending the script on a rejected token.
    _rc=0
    _out=$(CENSYS_PERSONAL_ACCESS_TOKEN=$1 CENSYS_ORG_ID=$2 "$KIT/bin/tsa" credits balance 2>&1) || _rc=$?
    if [ $_rc -eq 0 ]; then
        ok "Censys accepted the token and organization ID"
        printf '%s\n' "$_out" | sed 's/^/        /' | head -8
        return 0
    fi
    bad "Censys rejected them:"
    printf '%s\n' "$_out" | grep -i -E 'error|status|denied|invalid|forbidden' | head -3 | sed 's/^/        /'
    case $_out in
        *401*) note "  401 = the token is wrong, expired or revoked." ;;
        *403*) note "  403 = the token is fine but lacks API Access for this organization." ;;
        *400*) note "  400 = Censys could not read the request - usually stray characters in a
          pasted value. Paste the token again, or type it." ;;
        *404* | *422*) note "  Check the organization ID - copy it from the Current Organization box." ;;
    esac
    return 1
}

save_credentials() {  # save_credentials token org
    _rc_file=$(profile_file)
    if [ -f "$_rc_file" ]; then
        _bak="$_rc_file.$(date +%Y%m%dT%H%M%S).before-censys-tsa"
        cp -p "$_rc_file" "$_bak"
        ok "backup $_bak"
        # Drop any earlier block of ours, keep everything else byte for byte.
        _tmp="$_rc_file.censys-tsa.tmp"
        awk -v b="$CRED_BEGIN" -v e="$CRED_END" '
            $0 == b { skip = 1; next }
            $0 == e { skip = 0; next }
            !skip' "$_rc_file" > "$_tmp" && cat "$_tmp" > "$_rc_file" && rm -f "$_tmp"
    fi
    umask 077
    {
        printf '%s\n' "$CRED_BEGIN"
        printf "export CENSYS_PERSONAL_ACCESS_TOKEN='%s'\n" "$1"
        printf "export CENSYS_ORG_ID='%s'\n" "$2"
        printf '%s\n' "$CRED_END"
    } >> "$_rc_file"
    chmod 600 "$_rc_file"
    ok "saved to $_rc_file (permissions 600)"
}

#  Browser terminals (JupyterLab, VS Code) wrap a paste in "bracketed paste"
#  markers, ESC[200~ ... ESC[201~. A hidden `read` keeps them, and Censys then
#  answers 400 with an empty body. Strip them, then anything non-printable.
clean_pasted() {
    printf '%s' "$1" | sed "s/$(printf '\033')\[20[01]~//g" | tr -cd '[:graph:]'
}

setup_credentials() {
    if [ ! -t 0 ] || [ ! -t 1 ]; then
        note "not a terminal - run ./install.sh --credentials yourself to set them"
        return 0
    fi
    printf '\n%sSet up your Censys credentials now%s\n' "$C_CYN" "$C_OFF"
    printf '  The token is not shown as you type and is never printed.\n'
    printf '  Need them first? Open https://accounts.censys.io/settings/personal-access-tokens\n\n'
    # Ask the terminal not to add paste markers while we prompt; restored below.
    printf '\033[?2004l'
    _try=0
    while [ $_try -lt 3 ]; do
        _try=$((_try + 1))
        read_secret "  Personal access token: "
        _tok=$CENSYS_TSA_SECRET
        CENSYS_TSA_SECRET=
        printf '  Organization ID: '
        read -r _org || _org=
        _tok=$(clean_pasted "$_tok")
        _org=$(clean_pasted "$_org")
        if [ -z "$_tok" ] || [ -z "$_org" ]; then
            warn "both values are needed"
        elif printf '%s' "$_tok$_org" | grep -q "'"; then
            warn "a value contains a quote character - that is not a Censys token; try again"
        elif ! printf '%s' "$_org" | grep -Eqi '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'; then
            warn "the organization ID should look like 1a2b3c4d-5e6f-7a8b-9c0d-1e2f3a4b5c6d"
        elif verify_credentials "$_tok" "$_org"; then
            if ask_yes "  Save them to $(profile_file)?" y; then
                save_credentials "$_tok" "$_org"
                export CENSYS_PERSONAL_ACCESS_TOKEN="$_tok" CENSYS_ORG_ID="$_org"
                _tok= _org=
                if [ "$WITH_MCP" != no ]; then
                    printf '\n'
                    mcp_config add
                fi
                after_credentials_saved
            else
                note "not saved. Nothing was written."
            fi
            _tok= _org=
            printf '\033[?2004h'
            return 0
        fi
        _tok= _org=
        [ $_try -lt 3 ] && { ask_yes "  Try again?" y || { printf '\033[?2004h'; return 0; }; }
    done
    printf '\033[?2004h'
    note "giving up after 3 tries. Run ./install.sh --credentials when you have them."
}

#  OpenCode's agents run their shells inside the OpenCode background service,
#  which keeps the environment it was started with. New variables only reach it
#  after a restart from a shell that has them - this script now is one.
after_credentials_saved() {
    printf '\n'
    CREDS_SAVED=yes
    if command -v opencode >/dev/null 2>&1 && [ "$OPENCODE_MAJOR" = 2 ]; then
        note "The OpenCode background service also needs a restart to see them."
        if ask_yes "  Restart it now? This interrupts any running OpenCode session." n; then
            (cd / && opencode service restart >/dev/null 2>&1) && ok "OpenCode service restarted" ||
                warn "restart failed - run: opencode service restart"
        else
            note "Later, from a new terminal:  opencode service restart"
        fi
    else
        note "Restart OpenCode from a new terminal so its agents see them."
    fi
}

# ---------------------------------------------------------------------- doctor

doctor() {
    printf 'kit         %s\n' "$KIT"
    printf 'config dir  %s\n' "$CONFIG_DIR"
    printf 'command     %s/%s\n' "$BIN_DIR" "$CMD_NAME"
    printf 'opencode    %s\n\n' "$OPENCODE_MAJOR"

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
    _need_creds=no
    if [ -n "${CENSYS_PERSONAL_ACCESS_TOKEN:-}" ]; then
        ok "CENSYS_PERSONAL_ACCESS_TOKEN is set"
    else
        bad "CENSYS_PERSONAL_ACCESS_TOKEN is not set - every Censys call will fail"
        _need_creds=yes
    fi
    if [ -n "${CENSYS_ORG_ID:-}" ]; then
        ok "CENSYS_ORG_ID is set"
    else
        bad "CENSYS_ORG_ID is not set - every Censys call will fail"
        _need_creds=yes
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
    if wants_v1; then
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
    fi
    if wants_v2; then
        plugin_v2_dst="$CONFIG_DIR/plugins/tsa-capabilities"
        if [ -e "$plugin_v2_dst" ] || [ -L "$plugin_v2_dst" ]; then
            if owned_by_kit "$plugin_v2_dst" "$PLUGIN_V2_SRC"; then
                ok "$plugin_v2_dst"
            else
                warn "$plugin_v2_dst exists but is not ours"
            fi
        else
            bad "missing $plugin_v2_dst - capabilities would not be enforced on OpenCode 2"
        fi
        if [ "$OPENCODE_MAJOR" = 2 ] && command -v opencode >/dev/null 2>&1; then
            # A freshly (re)started service loads plugins a few seconds after it
            # answers, so give it up to ~20s before calling this a failure.
            _i=0
            while :; do
                status=$(cd / && opencode api get /api/plugin 2>/dev/null | tr '{' '\n' |
                    grep -A4 '"id":"censys-tsa.capabilities"' | sed -n 's/.*"status":"\([a-z]*\)".*/\1/p' | head -1)
                [ "${status:-}" = active ] || [ $_i -ge 10 ] && break
                sleep 2
                _i=$((_i + 1))
            done
            case ${status:-} in
                active) ok "OpenCode 2 reports the capability plugin as active" ;;
                "") bad "OpenCode 2 has not loaded the capability plugin - run: opencode reload" ;;
                *) bad "OpenCode 2 reports the capability plugin as '$status' - see ~/.local/share/opencode/log/opencode.log" ;;
            esac
        fi
    fi
    skill_dst="$CONFIG_DIR/skill/censys-tsa"
    if [ -e "$skill_dst" ] || [ -L "$skill_dst" ]; then
        ok "$skill_dst"
    else
        warn "missing $skill_dst (discovery skill only; agents still work)"
    fi
    if [ "$OPENCODE_MAJOR" != both ] && command -v python3 >/dev/null 2>&1; then
        mcp_config status
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
        if [ "$OPENCODE_MAJOR" = 2 ]; then
            # One agent per line as "<id> ", the shape `opencode agent list` had on V1.
            listing=$(cd / && opencode api get /api/agent 2>/dev/null | tr '{' '\n' |
                sed -n 's/^"id":"\([^"]*\)".*/\1 /p' || true)
        else
            listing=$(cd / && opencode agent list 2>/dev/null || true)
        fi
        for agent in censys-tsa censys-tsa-auto censys-fingerprint censys-deepdive censys-report; do
            if printf '%s\n' "$listing" | grep -q "^$agent "; then
                ok "$agent"
            else
                if [ "$OPENCODE_MAJOR" = 2 ]; then
                    bad "$agent not visible to opencode - run: opencode reload"
                else
                    bad "$agent not visible to opencode - restart opencode after installing"
                fi
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
        printf '%s%s check(s) failed.%s\n' "$C_RED" "$fail" "$C_OFF"
        if [ "$_need_creds" = yes ]; then
        if grep -qF "$CRED_BEGIN" "$(profile_file)" 2>/dev/null; then
            # Saved by --credentials, just not loaded into this shell yet.
            printf '\n%sYour credentials are saved in %s but not loaded in this terminal.%s\n' "$C_YEL" "$(profile_file)" "$C_OFF"
            printf 'Run:  %s. %s%s   (or open a new terminal), then: tsa doctor\n' "$C_BLD" "$(profile_file)" "$C_OFF"
        else
            credentials_help
        fi
    fi
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
    if wants_v1; then
        link_one "$PLUGIN_SRC" "$CONFIG_DIR/plugin/tsa-capabilities.ts" || true
    else
        # A V1 plugin left over from an earlier install only fails to load on V2.
        unlink_one "$CONFIG_DIR/plugin/tsa-capabilities.ts" "$PLUGIN_SRC"
    fi
    if wants_v2; then
        run mkdir -p "$CONFIG_DIR/plugins"
        link_one "$PLUGIN_V2_SRC" "$CONFIG_DIR/plugins/tsa-capabilities" || true
    fi
    link_one "$SKILL_SRC" "$CONFIG_DIR/skill/censys-tsa" || true
    link_one "$KIT/bin/tsa" "$BIN_DIR/$CMD_NAME" || true

    if [ "$WITH_MCP" = yes ]; then
        printf '\ncensys mcp server\n'
        mcp_config add
    elif [ "$WITH_MCP" = auto ] && [ "$DRY_RUN" = no ] &&
        [ -n "${CENSYS_PERSONAL_ACCESS_TOKEN:-}" ] && [ -n "${CENSYS_ORG_ID:-}" ]; then
        printf '\ncensys mcp server\n'
        if verify_credentials "$CENSYS_PERSONAL_ACCESS_TOKEN" "$CENSYS_ORG_ID"; then
            mcp_config add
        else
            warn "MCP server not added until the credentials work"
        fi
    fi

    # The plugin's bare import resolves from its REAL path. If that is outside
    # the config dir there is no node_modules chain to walk, and opencode loads
    # the plugin silently as nothing. Bridge it.
    if wants_v1 && [ "$USE_COPY" = no ] && ! is_inside "$KIT" "$(cd -- "$CONFIG_DIR" 2>/dev/null && pwd -P || printf '%s' "$CONFIG_DIR")"; then
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
        if [ "$OPENCODE_MAJOR" = 2 ]; then
            # V2 watches its config, but a reload makes the new files visible now.
            printf '\nreloading opencode\n'
            (cd / && opencode reload >/dev/null 2>&1) || true
            # The reload returns before agents and plugins are loaded again;
            # wait (up to ~30s) so the checks below do not race it.
            _i=0
            while [ $_i -lt 15 ]; do
                if (cd / && opencode api get /api/agent 2>/dev/null) | grep -q '"id":"censys-tsa"' &&
                    (cd / && opencode api get /api/plugin 2>/dev/null) | tr '{' '\n' |
                    grep -A4 '"id":"censys-tsa.capabilities"' | grep -q '"status":"active"'; then
                    break
                fi
                sleep 2
                _i=$((_i + 1))
            done
        else
            printf '\nwarming opencode (installs the plugin runtime dependency)\n'
            (cd / && opencode agent list >/dev/null 2>&1) || true
        fi
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
    if { [ -z "${CENSYS_PERSONAL_ACCESS_TOKEN:-}" ] || [ -z "${CENSYS_ORG_ID:-}" ]; } &&
        [ "$NO_PROMPT" = no ] && [ -t 0 ] && [ -t 1 ]; then
        if ask_yes "Censys credentials are missing. Enter them now?" y; then
            setup_credentials
        fi
    fi
    if [ "$OPENCODE_MAJOR" = 2 ]; then
        printf '\nOpenCode 2 picks up the new agents and plugin by itself (or run: opencode reload).\n'
    else
        printf '\nQuit and restart opencode - config, agents and plugins are loaded once at\n'
        printf 'startup and are not hot-reloaded.\n'
    fi
    cat <<EOF

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
    unlink_one "$CONFIG_DIR/plugins/tsa-capabilities" "$PLUGIN_V2_SRC"
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
    if [ "$WITH_MCP" != no ]; then
        mcp_config remove
    fi
    printf '\nThe kit itself, its .venv and any reports are untouched.\n'
    printf 'Restart opencode (V1) or run `opencode reload` (V2) for the agents to disappear.\n'
}

case $MODE in
    install) do_install ;;
    uninstall) do_uninstall ;;
    doctor) doctor ;;
    credentials) setup_credentials ;;
esac

#  A script cannot change the environment of the shell that started it, so
#  `source ~/.bashrc` here would load the credentials into this process only.
#  Instead, offer to replace this script with a fresh interactive shell: it
#  reads the profile as it starts, so the credentials work straight away. It is
#  a new shell inside the old one - `exit` returns to the old one.
if [ "$CREDS_SAVED" = yes ]; then
    printf '\n'
    if [ -t 0 ] && [ -t 1 ] &&
        ask_yes "Open a new shell here with the credentials loaded?" y; then
        printf '  Starting %s. Type `exit` to go back to the old shell.\n' "${SHELL:-/bin/sh}"
        exec "${SHELL:-/bin/sh}" -i
    fi
    note "This terminal does not have them yet: run  . $(profile_file)  or open a new terminal."
fi
