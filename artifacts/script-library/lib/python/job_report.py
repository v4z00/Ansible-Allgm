"""Human summaries; identifiers and full histories stay in the local query API."""
import collections
import re

SYMBOLS = {'success': '✅', 'failed': '❌', 'warning': '⚠️', 'skipped': '⏭️', 'running': '⏳'}
HEALTH = {
    'unreachable': ('failed', 'Host nicht erreichbar; Ergebnisse konnten nicht abgefragt werden.'),
    'query-failed': ('failed', 'Ergebnisabfrage fehlgeschlagen.'),
    'not-attached-or-query-failed': ('failed', 'Lokale Ergebnisablage fehlt oder konnte nicht abgefragt werden.'),
    'gap-or-schema-error': ('failed', 'Ergebnisverlauf unvollstaendig oder Datenformat nicht kompatibel.'),
    'generation-changed': ('warning', 'Die lokale Ergebnisdatenbank wurde neu angelegt; Abfrageposition pruefen.'),
    'gap': ('warning', 'Im gespeicherten Ergebnisverlauf besteht eine Luecke.'),
    'backlog-remains': ('warning', 'Weitere gespeicherte Ergebnisse werden beim naechsten Sammellauf abgeholt.'),
    'schedule-unconfigured': ('warning', 'Das erwartete Ausfuehrungsfenster ist noch nicht vollstaendig konfiguriert.'),
    'missing-expected-run': ('failed', 'Der erwartete Lauf fehlt.'),
    'overdue-running': ('warning', 'Der Job laeuft laenger als das erlaubte Zeitfenster.'),
}


def clean(value):
    text = str(value)
    text = re.sub(r'\b[0-9a-f]{8}-(?:[0-9a-f]{4}-){3}[0-9a-f]{12}\b', '[interne Kennung]', text, flags=re.I)
    return ''.join(char for char in text if char in '\n\t' or ord(char) >= 32).strip()


def title(category):
    return 'Vzdump-Zusammenfassung' if category == 'vzdump' else 'Job-Zusammenfassung'


def label(source, job, category, labels):
    hosts, jobs = labels.get('hosts', {}), labels.get('jobs', {})
    short = source.split('.', 1)[0]
    host = hosts.get(source, hosts.get(short, short[:1].upper() + short[1:]))
    chosen = jobs.get(source + '/' + job, jobs.get(job))
    if chosen is None:
        if category == 'vzdump':
            chosen = 'Vzdump'
        elif job.startswith('ansible:'):
            name = re.sub(r'\.ya?ml$', '', job.split(':', 1)[1]).replace('_', ' ').replace('-', ' ')
            chosen = 'Ansible ' + name[:1].upper() + name[1:]
        elif job.lower().endswith('backup'):
            chosen = 'Backup'
        else:
            chosen = re.sub(r'\.sh$', '', job)
            if chosen.lower().startswith(short.lower() + '_'):
                chosen = chosen[len(short) + 1:]
            chosen = chosen.replace('_', ' ').replace('-', ' ')
            chosen = chosen[:1].upper() + chosen[1:]
    return clean(host + ' ' + chosen)


def detail(message, exit_code=None):
    text = clean(message)
    match = re.fullmatch(r'Shell operation failed at line \d+ \(exit (\d+)\)', text)
    if match:
        code = int(match[1])
        return 'Zeitlimit erreicht (Exitcode 124).' if code == 124 else 'Skriptbefehl fehlgeschlagen (Exitcode %d).' % code
    if text.startswith('Missing configuration: '):
        return 'Konfiguration fehlt: ' + text.split(': ', 1)[1]
    translations = {'Job failed; inspect private local log': 'Job fehlgeschlagen; Details im lokalen Laufprotokoll.',
                    'Runner interrupted or failed': 'Job abgebrochen oder Ausfuehrung fehlgeschlagen.',
                    'Previous process ended without completion': 'Vorheriger Lauf ohne Abschluss beendet.',
                    'Unreachable': 'Host nicht erreichbar.', 'Ansible host result': 'Ansible-Tasks fehlgeschlagen.'}
    if text in translations:
        text = translations[text]
    if not text or text in ('Completed', 'Ansible playbook completed'):
        return 'Job fehlgeschlagen (Exitcode %s).' % exit_code if exit_code else 'Kein vollstaendiger Erfolg gemeldet.'
    return text


def format_report(rows, items, health, category='general', labels=None):
    """One line per host/job, worst unreported outcome; details only for problems."""
    labels = labels or {}
    groups = collections.OrderedDict()
    for row in rows:
        key = (row['source'], row['job'])
        group = groups.setdefault(key, {'rows': [], 'details': [], 'states': []})
        group['rows'].append(row)
        group['states'].append(row['status'])
        objects = items.get((row['source'], row['epoch'], row['run_id']), [])
        problems = [obj for obj in objects if obj['status'] in ('failed', 'warning')]
        for obj in problems:
            group['states'].append(obj['status'])
            prefix = '' if obj['item_id'] == 'shell' else ('ID ' if obj['item_id'].isdigit() else '') + clean(obj['item_id']) + ': '
            group['details'].append(prefix + detail(obj['message'], row.get('exit_code')))
        if row['status'] in ('failed', 'warning') and not problems:
            group['details'].append(detail(row.get('summary', ''), row.get('exit_code')))
    for entry in health:
        state, message = HEALTH.get(entry['status'], ('warning', clean(entry['status']).replace('-', ' ')))
        source = entry['source']
        if source.startswith('controller:'):
            key = ('', source)
            heading = 'Ergebnisabfrage' if source == 'controller:collection' else 'Ergebniszusammenfassung'
        else:
            host, separator, job = source.partition('/')
            key = (host, job if separator else 'Abfrage')
            heading = label(key[0], key[1], category if separator else 'general', labels)
        group = groups.setdefault(key, {'rows': [], 'details': [], 'states': [], 'label': heading})
        group['states'].append(state)
        group['details'].append(message)
    lines = [title(category), '']
    for key, group in sorted(groups.items()):
        states = group['states']
        status = 'failed' if 'failed' in states else 'warning' if 'warning' in states else states[-1]
        heading = group.get('label') or label(key[0], key[1], category, labels)
        lines.append(heading + ' ' + SYMBOLS.get(status, '⚠️'))
        if status in ('failed', 'warning'):
            details = list(dict.fromkeys(group['details']))
            for message in details[:5]:
                lines.extend('  ' + line for line in clean(message).splitlines())
            if len(details) > 5:
                lines.append('  Weitere Details in der Job-Abfrage.')
    return '\n'.join(lines)


def legacy_health(body):
    """Keep the original collection snapshot when retrying an older report."""
    entries = []
    for line in body.splitlines():
        match = re.fullmatch(r'(?:🚫|⚠️) (.+): ([a-z][a-z-]+)', line)
        if match:
            entries.append({'source': match[1], 'status': match[2], 'message': ''})
    return entries


def clean_legacy_body(body):
    """Last-resort compatibility when a report's retained run rows are gone."""
    lines = []
    for line in body.splitlines():
        if line.startswith('Bericht: ') or re.fullmatch(r'✅ \d+ \| ❌ \d+ \| ⚠️ \d+ \| ⏭️ \d+', line):
            continue
        match = re.fullmatch(r'[✅❌⚠️⏭️]+ (.+) / (.+): (success|failed|warning|skipped)', line)
        if match:
            line = label(match[1], match[2], 'general', {}) + ' ' + SYMBOLS[match[3]]
        lines.append(clean(line))
    return '\n'.join(lines)
