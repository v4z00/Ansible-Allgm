# Only a data-to-shell encoder is evaluated: JSON values are shell-quoted first.
hm_load_config() {
    local file code
    for file in "$@"; do
        [[ -f "$file" && ! -L "$file" ]] || { printf '%s\n' 'Configuration file missing or symlink' >&2; return 78; }
        code=$(python3 -c 'import json,os,re,shlex,stat,sys
p=sys.argv[1]
s=os.stat(p)
if s.st_uid not in (0,os.geteuid()) or stat.S_IMODE(s.st_mode)&0o077: sys.exit("Configuration requires private owner permissions")
with open(p,encoding="utf-8") as f: d=json.load(f)
if not isinstance(d,dict): sys.exit("Configuration must be an object")
blocked={"SCRIPT_DIR","SCRIPT_CONFIG_DIR","PATH","BASH_ENV","ENV","SHELLOPTS","BASHOPTS","IFS","CDPATH","BASH_XTRACEFD","PS4"}
rows=[]
for k,v in d.items():
 if not re.fullmatch(r"[A-Z][A-Z0-9_]*",k) or k in blocked or k.startswith(("HM_","BASH_")): sys.exit("Invalid configuration key")
 def scalar(x):
  if isinstance(x,bool): return "true" if x else "false"
  if isinstance(x,(str,int,float)) and "\0" not in str(x): return str(x)
  raise ValueError("Unsupported configuration value")
 try:
  if isinstance(v,list): rows.append(k+"=("+" ".join(shlex.quote(scalar(x)) for x in v)+")")
  else: rows.append(k+"="+shlex.quote(scalar(v)))
 except ValueError: sys.exit("Unsupported configuration value")
print("\n".join(rows))' "$file") || return 78
        eval "$code" || return 78
    done
}
