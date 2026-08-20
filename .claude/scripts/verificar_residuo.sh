#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────
#  verificar_residuo.sh — control de pérdida para /process-inbox
#
#  PROBLEMA QUE RESUELVE
#  "Destilar sin perder información" no es verificable a ojo. Bajo carga
#  (muchos archivos, contexto lleno) la verificación se degrada en silencio:
#  el informe se ve completo, pero los últimos archivos se revisaron por
#  encima. Este script sustituye criterio por medición.
#
#  QUÉ HACE
#  Extrae los "datos duros" de la fuente — rutas, comandos, paquetes,
#  versiones, hashes, IDs, cifras con unidad — y para cada uno que NO esté
#  en el destino, lo CLASIFICA para que la decisión sea consciente:
#
#    🔴 PÉRDIDA     no está en el destino, ni en ningún otro doc del repo,
#                   y sigue siendo cierto en disco  → fusionar
#    🔵 REUBICADO   vive en otro doc del repo       → destino asumido erróneo
#    ⚪ OBSOLETO    la ruta/archivo ya no existe    → conservarlo documenta
#                   una mentira; se descarta a conciencia
#
#  QUÉ NO HACE
#  No decide. Clasifica y da contexto (línea de origen) para que decidas tú.
#
#  USO
#    ./verificar_residuo.sh FUENTE DESTINO           # un par
#    ./verificar_residuo.sh --lote DESTINO SRC...    # varias fuentes → un destino
#    ./verificar_residuo.sh --autotest FUENTE        # control: debe dar 0
#    ./verificar_residuo.sh --rapido FUENTE DESTINO  # sin búsqueda en repo
#
#  SALIDA: 0 = sin pérdida real · 1 = hay pérdida real · 2 = error de uso
# ─────────────────────────────────────────────────────────────────────────
set -uo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
RUIDO='^(/dev/null|/etc|/usr|/tmp|/home|/var|/opt|~/|\.\./|/bin|/lib)$'

# ── SANITIZACIÓN MECÁNICA ────────────────────────────────────────────────
# El script NUNCA debe emitir un secreto. No depende de criterio humano ni
# de un LLM: es filtrado por patrón, aplicado a TODA salida.
#
# Un token de forma sospechosa (32 hex) puede ser un apiSecret o un SHA-256
# legítimo de un informe de seguridad. La FORMA no los distingue; el
# CONTEXTO sí. Se decide por la línea en la que aparece.
SECRETO_RE='(api[_-]?key|api[_-]?secret|apisecret|secret|passwd|password|passphrase|local[_-]?key|private[_-]?key|credential|access[_-]?token|bearer|authorization|clabe|curp|\bRFC\b|\biban\b|\bcvv\b|saldo|monto|tarjeta)'

linea_sensible() { grep -qiE "$SECRETO_RE" <<<"$1"; }

# Contextos donde un valor de alta entropía es legítimo y vale conservarlo:
# hashes publicados, IOCs de un informe de seguridad, commits de git.
HASH_OK_RE='(sha-?(1|256|512)|md5|checksum|hash|fingerprint|\bIOC\b|commit|digest|firma)'

# Material criptográfico por FORMA. Se enmascara SIEMPRE salvo que la línea
# lo declare hash público. Fail-closed: ante la duda, se oculta.
token_alto_riesgo() {
    local t="$1" linea="$2"
    grep -qiE "$HASH_OK_RE" <<<"$linea" && return 1        # hash declarado → se conserva
    [[ $t =~ ^ey[A-Za-z0-9_-]{10,} ]]           && return 0  # JWT
    [[ $t =~ ^[0-9a-fA-F]{24,}$ ]]              && return 0  # hex largo
    [[ $t =~ ^[A-Za-z0-9+/]{24,}={0,2}$ ]]      && return 0  # base64
    [[ $t =~ ^(sk|pk|ghp|gho|xox[bpar])[-_][A-Za-z0-9]{10,} ]] && return 0  # claves con prefijo
    [[ $t =~ ^-----BEGIN ]]                     && return 0  # PEM
    return 1
}

# Rechaza fuentes que no deben leerse nunca. Fail-closed por extensión y por
# git: si git lo ignora, se asume sensible.
FUENTE_VETADA_RE='\.(json|xlsx|xls|ods|csv|db|sqlite3?|env|key|pem|p12|pfx|jks)$|(^|/)(devices|tinytuya|tuya-raw|credentials|secrets)\.'

fuente_permitida() {
    local f="$1"
    if [[ $f =~ $FUENTE_VETADA_RE ]]; then
        echo "RECHAZADO: '$f' es de un tipo que puede contener credenciales o datos financieros." >&2
        echo "           Este script sólo procesa documentación (.md .txt .sh .py)." >&2
        return 1
    fi
    if git -C "$REPO" check-ignore -q "$f" 2>/dev/null; then
        echo "RECHAZADO: '$f' está en .gitignore — se asume sensible por diseño." >&2
        return 1
    fi
    return 0
}

# Enmascara un valor conservando lo justo para reconocerlo sin revelarlo.
enmascarar() {
    local t="$1"
    (( ${#t} > 10 )) && { echo "${t:0:4}…${t: -2} [${#t} chars, ENMASCARADO]"; return; }
    echo "[ENMASCARADO]"
}

# Redacta el valor de cualquier asignación clave=valor / clave: valor.
redactar_valores() {
    sed -E 's/([[:alnum:]_-]+[[:space:]]*[=:][[:space:]]*)("[^"]*"|'\''[^'\'']*'\''|[^[:space:],;)]+)/\1[REDACTED]/g' <<<"$1"
}

# HUECO 2 — el informe puede acabar pegado en una IA web o en un commit.
# El home real expone el nombre de usuario: se normaliza a ~ siempre.
# Acepta argumento o stdin, para poder usarse suelto o en tubería.
anonimizar_ruta() {
    if (( $# )); then sed -E "s#(/home/[^/ ]+|${HOME})#~#g" <<<"$1"
    else              sed -E "s#(/home/[^/ ]+|${HOME})#~#g"
    fi
}

# HUECO 4 — modo paranoico: sólo conteos, cero tokens y cero contexto.
PARANOICO=0

# Única puerta de salida para contexto. Todo lo que se imprime pasa por aquí.
ctx_seguro() {
    local linea="$1"
    (( PARANOICO )) && { echo "[contexto omitido — modo paranoico]"; return; }
    if linea_sensible "$linea"; then
        redactar_valores "$linea" | cut -c1-110 | anonimizar_ruta
        return
    fi
    if (( ${#linea} > 110 )); then
        anonimizar_ruta "${linea:0:110} … [truncada, ${#linea} chars]"
    else
        anonimizar_ruta "$linea"
    fi
}

# Única puerta de salida para tokens.
tok_seguro() {
    local tok="$1" linea="$2"
    (( PARANOICO )) && { echo "[token omitido — modo paranoico]"; return; }
    if linea_sensible "$linea"; then enmascarar "$tok"; else anonimizar_ruta "$tok"; fi
}

extraer_tokens() {
    grep -ohE \
        -e '(/[a-zA-Z0-9._~+-]+){2,}' \
        -e '~/[a-zA-Z0-9._/+-]+' \
        -e '\b[a-zA-Z0-9_-]+\.(py|sh|json|md|txt|db|conf|service|toml|yml|yaml|opml|xlsx|html|zsh|csv|ods)\b' \
        -e '\b[0-9a-f]{16,}\b' \
        -e '\bv?[0-9]+\.[0-9]+(\.[0-9]+)?(-[a-z0-9]+)?\b' \
        -e '\b[0-9]+(\.[0-9]+)? ?(GB|MB|KB|TB|GHz|MHz|tok/s|rpm|W|V|A)\b' \
        -e '\b(pacman|yay|systemctl|sudo|git|ssh|rsync|chmod|chown|mount|lsblk|journalctl|makepkg|pip|python3?|openpyxl|ollama|docker) +-{0,2}[A-Za-z][A-Za-z0-9-]*' \
        -e '\b[A-Z][A-Z0-9_]{4,}=' \
        "$1" 2>/dev/null \
    | grep -vE '^(v?[01]\.[0-9]{1,2}|[0-9]{4})$' \
    | grep -vE "$RUIDO" \
    | sort -u
}

# Clasifica un token ausente. Eco: "TIPO|detalle"
clasificar() {
    local tok="$1" src="$2" dst="$3" rapido="$4"

    # ¿Sigue siendo cierto en disco? Sólo aplica a rutas.
    if [[ $tok == /* || $tok == ~/* ]]; then
        local ruta="${tok/#\~/$HOME}"
        if [[ ! -e $ruta ]]; then
            echo "OBSOLETO|la ruta ya no existe en disco"
            return
        fi
    fi

    # ¿Aparece en otro doc del repo?
    # HUECO 1 — el token NO se pasa como argumento: sería visible en `ps aux`
    # para cualquier proceso local mientras corre el grep. Va por stdin con -f.
    # (Y `--` no se usa: terminaría el parseo y convertiría --include en rutas.)
    if [[ $rapido != "--rapido" ]]; then
        local otro
        otro=$(printf '%s\n' "$tok" | grep -rlF -f - \
                 --include='*.md' --include='*.txt' --include='*.py' --include='*.sh' \
                 --exclude-dir=.git --exclude-dir=graphify-out --exclude-dir=inbox \
                 "$REPO" 2>/dev/null \
               | grep -vF -e "$dst" -e "$src" | head -1)
        if [[ -n $otro ]]; then
            echo "REUBICADO|aparece en $(anonimizar_ruta "${otro#$REPO/}") — verificar que sea el mismo dato"
            return
        fi
    fi

    echo "PERDIDA|"
}

comparar() {
    local src="$1" dst="$2" rapido="${3:-}"
    [[ -f $src ]] || { echo "ERROR: no existe fuente: $src" >&2; return 2; }
    [[ -f $dst ]] || { echo "ERROR: no existe destino: $dst" >&2; return 2; }

    # PUERTA 1 — la fuente debe ser documentación, nunca datos ni credenciales.
    fuente_permitida "$src" || return 2

    local tokens total miss=0 perdida=0 reubicado=0 obsoleto=0 censurados=0
    mapfile -t tokens < <(extraer_tokens "$src")
    total=${#tokens[@]}

    local out_perdida="" out_reub="" out_obs=""
    for t in "${tokens[@]}"; do
        grep -qF -e "$t" "$dst" && continue
        ((miss++))

        # Línea de origen: se lee ANTES de decidir nada, porque el contexto
        # es lo que determina si el token es secreto o dato legítimo.
        local linea num
        linea=$(grep -nF -m1 -e "$t" "$src" || true)
        num=${linea%%:*}; linea=${linea#*:}

        # PUERTA 2 — material criptográfico por forma: fail-closed.
        local t_out
        if token_alto_riesgo "$t" "$linea"; then
            t_out=$(enmascarar "$t"); ((censurados++))
        else
            t_out=$(tok_seguro "$t" "$linea")
            [[ $t_out != "$t" ]] && ((censurados++))
        fi

        # PUERTA 3 — el contexto pasa siempre por el sanitizador.
        local ctx; ctx="$num: $(ctx_seguro "$linea")"

        IFS='|' read -r tipo detalle < <(clasificar "$t" "$src" "$dst" "$rapido")
        case $tipo in
            PERDIDA)   ((perdida++));   out_perdida+="   │ ${t_out}"$'\n'"   │    ↳ ${ctx}"$'\n' ;;
            REUBICADO) ((reubicado++)); out_reub+="   │ ${t_out}  →  ${detalle}"$'\n' ;;
            OBSOLETO)  ((obsoleto++));  out_obs+="   │ ${t_out}  →  ${detalle}"$'\n' ;;
        esac
    done

    local pct=100
    (( total > 0 )) && pct=$(( (total - miss) * 100 / total ))

    echo "── $(basename "$src")  →  $(basename "$dst")"
    echo "   $total tokens duros · $((total-miss)) presentes (${pct}%) · $miss ausentes"
    echo "   desglose: 🔴 $perdida pérdida · 🔵 $reubicado reubicado · ⚪ $obsoleto obsoleto"
    (( censurados )) && echo "   🔒 $censurados token(s) enmascarados por seguridad — la sanitización actuó"
    echo

    [[ -n $out_perdida ]] && {
        echo "   🔴 PÉRDIDA REAL — fusionar al destino antes de cerrar:"
        printf '%s' "$out_perdida"; echo "   └"; }
    [[ -n $out_reub ]] && {
        echo "   🔵 REUBICADO — sin pérdida; el destino asumido no era el único:"
        printf '%s' "$out_reub"; echo "   └"; }
    [[ -n $out_obs ]] && {
        echo "   ⚪ OBSOLETO — descartar a conciencia (conservarlo documenta una mentira):"
        printf '%s' "$out_obs"; echo "   └"; }

    if   (( perdida == 0 && miss == 0 )); then echo "   ✅ cobertura total — se puede marcar archivado"
    elif (( perdida == 0 ));              then echo "   ✅ sin pérdida real — revisar el desglose y marcar archivado"
    elif (( perdida <= 3 ));              then echo "   🟡 $perdida datos a fusionar — trabajo acotado"
    else                                       echo "   🔴 $perdida datos perdidos — NO marcar archivado"
    fi
    echo

    (( perdida == 0 ))
}

# HUECO 4 — flag global, se consume antes de despachar el modo.
if [[ ${1:-} == "--paranoico" ]]; then PARANOICO=1; shift; fi

case "${1:-}" in
    --autotest)
        [[ -n ${2:-} ]] || { echo "uso: $0 --autotest FUENTE" >&2; exit 2; }
        echo "CONTROL — fuente contra sí misma; cualquier ausencia = extractor roto"
        comparar "$2" "$2" --rapido
        ;;
    --lote)
        shift; dst="${1:-}"; shift || true
        [[ -n ${dst:-} && $# -gt 0 ]] || { echo "uso: $0 --lote DESTINO SRC..." >&2; exit 2; }
        echo "════════ LOTE → $dst ════════"; echo
        fail=0
        # HUECO 3 — un veto (código 2) no puede confundirse con "sin pérdida".
        # Se propaga como fallo del lote, más severo que una pérdida normal.
        for src in "$@"; do
            comparar "$src" "$dst"
            case $? in 2) fail=2 ;; 1) (( fail == 2 )) || fail=1 ;; esac
        done
        echo "════════ fin del lote ════════"
        exit $fail
        ;;
    --rapido)
        [[ -n ${3:-} ]] || { echo "uso: $0 --rapido FUENTE DESTINO" >&2; exit 2; }
        comparar "$2" "$3" --rapido
        ;;
    "" | -h | --help)
        sed -n '2,32p' "$0" | sed 's/^# \{0,1\}//'; exit 2 ;;
    *)
        [[ -n ${2:-} ]] || { echo "uso: $0 FUENTE DESTINO" >&2; exit 2; }
        comparar "$1" "$2" ;;
esac
