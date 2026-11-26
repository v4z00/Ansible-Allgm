"""Explicit calendar windows; no daily false alarms for weekly jobs."""
import datetime
import re
import time

def calendar_times(cron):
    """Expand bounded minute/hour lists; unsupported calendars stay explicit."""
    def field(value, maximum):
        text=str(value)
        if text=='*':return list(range(maximum+1))
        if re.fullmatch(r'\*/[1-9][0-9]*',text):return list(range(0,maximum+1,int(text[2:])))
        if not re.fullmatch(r'[0-9]+(?:,[0-9]+)*',text):return []
        values=sorted(set(map(int,text.split(','))))
        return values if all(0<=x<=maximum for x in values) else []
    values=['%02d:%02d'%(h,m) for h in field(cron.get('hour',''),23) for m in field(cron.get('minute',''),59)]
    return values[0] if len(values)==1 else values or None

def normalize(jobs,previous=None):
    previous={j['job']:j for j in (previous or [])};result=[]
    for entry in jobs:
        if not re.fullmatch(r'[A-Za-z0-9_.:-]{1,160}',entry['job']):raise ValueError('Invalid expectation job')
        cron=entry.get('cron',{});custom=entry.get('expected',{})
        category=entry.get('category','vzdump' if entry['job'].startswith('vzdump') else 'general')
        if category not in ('general','vzdump'):raise ValueError('Invalid expectation category')
        value={'job':entry['job'],'category':category,'timezone':entry.get('timezone',''),'start':custom.get('start'),
               'weekdays':custom.get('weekdays'),'deadline_minutes':custom.get('deadline_minutes'),
               'max_runtime_minutes':custom.get('max_runtime_minutes')}
        if value['start'] is None:value['start']=calendar_times(cron)
        if value['weekdays'] is None:
            weekday=str(cron.get('weekday',''))
            if weekday=='*':value['weekdays']=list(range(7))
            elif weekday.isdigit() and 0<=int(weekday)<=7:value['weekdays']=[(int(weekday)-1)%7]
            elif weekday.lower() in ('mon','tue','wed','thu','fri','sat','sun'):value['weekdays']=[('mon','tue','wed','thu','fri','sat','sun').index(weekday.lower())]
        # Complex month/day expressions need an explicit expectation instead of a guess.
        if cron.get('month','*')!='*' or cron.get('day','*')!='*':value['weekdays']=custom.get('weekdays')
        prior=previous.get(value['job'])
        old={k:v for k,v in (prior or {}).items() if k!='configured_at'}
        value['configured_at']=prior['configured_at'] if old==value else time.time()
        result.append(value)
    return result

def evaluate(spec,rows,now=None):
    from zoneinfo import ZoneInfo
    if not spec.get('timezone') or not spec.get('start') or not spec.get('weekdays') or spec.get('deadline_minutes') is None or spec.get('max_runtime_minutes') is None:
        return 'schedule-unconfigured'
    zone=ZoneInfo(spec['timezone']);now=now or datetime.datetime.now(datetime.timezone.utc)
    local=now.astimezone(zone)
    starts=spec['start'] if isinstance(spec['start'],list) else [spec['start']]
    if len(starts)>1440:raise ValueError('Too many expected times')
    times=[]
    for value in starts:
        hour,minute=map(int,value.split(':'))
        if not (0<=hour<24 and 0<=minute<60):raise ValueError('Invalid expected time')
        times.append((hour,minute))
    if any(d not in range(7) for d in spec['weekdays']):raise ValueError('Invalid expected weekdays')
    start=None
    for offset in range(8):
        day=local-datetime.timedelta(days=offset)
        if day.weekday() not in spec['weekdays']:continue
        candidates=[day.replace(hour=h,minute=m,second=0,microsecond=0) for h,m in times]
        candidates=[candidate for candidate in candidates if candidate<=local]
        if candidates:start=max(candidates);break
    if start is None or start.timestamp()<spec['configured_at']:return 'ok'
    records=[r for r in rows if r['job']==spec['job'] and r['started']>=start.timestamp()]
    # A job started before the latest slot can still be running or overdue.
    running=[r for r in rows if r['job']==spec['job'] and r['status']=='running' and r['started']>=spec['configured_at']]
    if running:
        age=now.timestamp()-min(r['started'] for r in running)
        return 'overdue-running' if age>int(spec['max_runtime_minutes'])*60 else 'ok'
    if records:return 'ok'  # failed runs are reported as failed, not as missing.
    deadline=start+datetime.timedelta(minutes=int(spec['deadline_minutes']))
    return 'missing-expected-run' if local>deadline else 'ok'
