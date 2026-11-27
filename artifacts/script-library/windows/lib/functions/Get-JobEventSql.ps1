function Get-JobEventSql {
    param(
        [Parameter(Mandatory)]$Store,
        [Parameter(Mandatory)][string]$RunId,
        [Parameter(Mandatory)][string]$Kind,
        [switch]$OnlyAfterChange
    )
    $source = ConvertTo-JobSqlLiteral $Store.Source
    $epoch = ConvertTo-JobSqlLiteral $Store.Epoch
    $run = ConvertTo-JobSqlLiteral $RunId
    $eventKind = ConvertTo-JobSqlLiteral $Kind
    $now = ConvertTo-JobSqlLiteral (Get-JobTimestamp)
    $condition = if ($OnlyAfterChange) { ' AND changes()=1' } else { '' }
    return @"
INSERT INTO events(source,epoch,run_id,created,kind,payload)
SELECT r.source,r.epoch,r.run_id,$now,$eventKind,
json_object('run',json_object('source',r.source,'epoch',r.epoch,'run_id',r.run_id,
 'job',r.job,'category',r.category,'status',r.status,'started',r.started,'activity',r.activity,
 'finished',r.finished,'exit_code',r.exit_code,'summary',r.summary,'duration_seconds',r.duration_seconds),
 'items',json((SELECT json_group_array(json_object('item_id',i.item_id,'status',i.status,
 'message',i.message,'updated',i.updated)) FROM items i WHERE i.source=r.source
 AND i.epoch=r.epoch AND i.run_id=r.run_id)))
FROM runs r WHERE r.source=$source AND r.epoch=$epoch AND r.run_id=$run$condition;
"@
}
