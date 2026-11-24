# One public function; importing this file performs no work.
hm_mail_ascii() {
    local table
    table="${HM_LIB_DIR:?HM_LIB_DIR not initialized}/data/mail-translations.json"
    python3 -c 'import json,sys,unicodedata
with open(sys.argv[1], encoding="utf-8") as f: table=json.load(f)
text=unicodedata.normalize("NFC",sys.stdin.read())
for source,target in table.items(): text=text.replace(source,target)
text=unicodedata.normalize("NFKD",text)
text="".join(c for c in text if not unicodedata.combining(c))
sys.stdout.write(text.encode("ascii","replace").decode("ascii"))' "$table"
}
