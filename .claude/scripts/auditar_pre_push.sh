#!/usr/bin/env bash
# auditar_pre_push.sh — localiza info privada antes de push. Repo PÚBLICO.
#
# NUNCA imprime el contenido encontrado: sólo CATEGORIA y archivo:linea.
# No hay opción para volcarlo. La no-divulgación es estructural, no un filtro.
# Tú abres la línea y decides. BLOQUEA = nunca publicar · DECIDE = criterio tuyo.
#
# LIMITACIÓN CONOCIDA: nombres de archivo con ':' rompen git grep separator (path:line).
# Workaround: renombrar quitando ':' o '(' ')' caracteres. Futuro: usar NUL separator.
#
#   (sin args)  commits sin pushear      --tree  todo lo versionado
#   --all       sin tope de 3 por categoría
# Exit: 0 limpio · 1 hay que decidir · 2 credencial dura
set -uo pipefail
cd "$(git rev-parse --show-toplevel 2>/dev/null)" || { echo "FATAL no-git"; exit 2; }

M=diff CAP=3
for a in "$@"; do case $a in
  --tree) M=tree;; --all) CAP=999;;
  -h|--help) sed -n '2,10p' "$0"; exit 0;; *) echo "FATAL arg: $a"; exit 2;;
esac; done

B=origin/main
git rev-parse --verify -q "$B" >/dev/null || B=$(git rev-list --max-parents=0 HEAD|tail -1)
C=$(mktemp); trap 'rm -f "$C"' EXIT

# Corpus normalizado a  ruta:linea:contenido  (el contenido sólo se usa para
# hacer match; jamás se emite). En modo diff, awk reconstruye ruta y número
# real de línea desde las cabeceras +++ y @@, contando sólo líneas añadidas.
if [ "$M" = tree ]; then
  git grep -nI '' -- '*.md' '*.txt' '*.sh' '*.py' '*.html' '*.yml' >"$C" 2>/dev/null
else
  git diff "$B"..HEAD 2>/dev/null | awk '
    /^\+\+\+ b\// { f=substr($0,7); next }
    /^@@/         { split($0,h,"+"); split(h[2],p,","); n=p[1]+0; next }
    /^\+/         { print f":"n":"substr($0,2); n++; next }
    /^[ ]/        { n++ }
  ' >"$C"
fi
[ -s "$C" ] || { echo "PASS $M vacio"; exit 0; }

# Ruido estructural: las propias reglas, lo ya redactado, tooling conocido.
Z='_RE=|^R=|redactad|censurad|\[redact|\[monto|placeholder|example\.|ejemplo\.|noreply@|@anthropic|@claude\.com|usuario@|tu-correo|git@github|TU_CONTRASE|TU_PASSWORD'

# TIER<TAB>CATEGORIA<TAB>REGEX
R=$(cat <<'EOF'
BLOQUEA	LLAVE	BEGIN ([A-Z]+ )?PRIVATE KEY
BLOQUEA	APIKEY	(api[_-]?key|api[_-]?secret|access[_-]?token|auth[_-]?token|client[_-]?secret)[ 	]*[:=][ 	]*.?[A-Za-z0-9_-]{16,}
BLOQUEA	BEARER	bearer [A-Za-z0-9._-]{20,}
BLOQUEA	PASSWD	(password|passwd|passphrase)[ 	]*[:=][ 	]*.?[^ 	"']{6,}
BLOQUEA	TUYA	(local_key|device_id)[ 	]*[:=][ 	]*.?[A-Za-z0-9]{10,}
BLOQUEA	CANVATOK	canva\.com/design/[A-Za-z0-9_-]+/[A-Za-z0-9_-]{10,}
BLOQUEA	FISCAL	(curp|clabe)[ 	]*[:=]?[ 	]*[A-Z0-9]{10,}|RFC[ 	]*[:=][ 	]*[A-Z0-9]{10,}
BLOQUEA	TARJETA	\b[0-9]{4}[ -]?[0-9]{4}[ -]?[0-9]{4}[ -]?[0-9]{4}\b
DECIDE	CANVAID	DA[GH][A-Za-z0-9_-]{8,}
DECIDE	EMAIL	[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}
DECIDE	SALARIO	(salario|sueldo|remuneraci|compensation|compensaci)[^.]{0,40}[0-9]{3,}
DECIDE	DINERO	\$ ?[0-9]{1,3}(,[0-9]{3})+|\$ ?[0-9]{4,}|[0-9]{1,3}(,[0-9]{3})+ ?(MXN|USD|EUR)
DECIDE	BANCO	(BBVA|Santander|Banorte|HSBC|Banamex|Scotiabank|Bitso|Klar)[^.]{0,30}(cuenta|saldo|clabe|[0-9]{6,})
DECIDE	IPLAN	\b(192\.168|10\.[0-9]{1,3}|172\.(1[6-9]|2[0-9]|3[01]))\.[0-9]{1,3}\.[0-9]{1,3}\b
DECIDE	RUTARED	\\\\[A-Za-z0-9_-]+\\[A-Za-z0-9_$-]+
EOF
)

HARD=0 SOFT=0
while IFS=$'\t' read -r T CAT RE; do
  [ -n "${CAT:-}" ] || continue
  # cut -d: -f1,2  descarta el contenido ANTES de que pueda imprimirse.
  H=$(grep -Ei -- "$RE" "$C" 2>/dev/null|grep -vEi -- "$Z"|cut -d: -f1,2) || true
  [ -n "$H" ] || continue
  n=$(printf '%s\n' "$H"|wc -l)
  [ "$T" = BLOQUEA ] && HARD=$((HARD+1)) || SOFT=$((SOFT+1))
  echo "$T $CAT ($n)"
  printf '%s\n' "$H"|head -"$CAP"|sed 's/^/  /'
  [ "$n" -gt "$CAP" ] && echo "  +$((n-CAP)) mas (--all)"
done <<<"$R"

# Binarios y PDF: grep no ve dentro, se listan para revisión manual.
[ "$M" = tree ] && L=$(git ls-files) || L=$(git diff --name-only "$B"..HEAD 2>/dev/null)
X=$(printf '%s\n' "$L"|grep -iE '\.(xlsx|xls|ods|docx|db|sqlite3?|key|pem|env|pfx|p12)$') || true
[ -n "$X" ] && { HARD=$((HARD+1)); echo "BLOQUEA BINARIO ($(printf '%s\n' "$X"|wc -l))"; printf '%s\n' "$X"|sed 's/^/  /'; }
P=$(git ls-files -- '*.pdf') || true
[ -n "$P" ] && { echo "REVISAR PDF ($(printf '%s\n' "$P"|wc -l))"; printf '%s\n' "$P"|sed 's/^/  /'; }
F=; for p in '*.key' '*.pem' '.env' 'graphify-out/' '*.xlsx'; do
  grep -qF -- "$p" .gitignore 2>/dev/null || F="$F$p "; done
[ -n "$F" ] && { HARD=$((HARD+1)); echo "BLOQUEA GITIGNORE"; echo "  falta: $F"; }

echo ---
[ "$HARD" -eq 0 ] && [ "$SOFT" -eq 0 ] && { echo "PASS $M"; exit 0; }
echo "$M bloquea=$HARD decide=$SOFT"
echo "redactar el tree NO borra lo ya pusheado"
[ "$HARD" -gt 0 ] && exit 2 || exit 1
