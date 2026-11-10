"""Reconcile only duplicate generated imports retained by the open editor's file locks."""
import unreal,json,shutil,os,traceback
PROJECT='E:/UEproject/Division2AnimationViewer'
BACKUP='C:/Users/yeyuxiang/Documents/Codex/2026-11-09/c-users-yeyuxiang-desktop-2/work/firing_revision/duplicate_backup'
with open(PROJECT+'/ImportReport/firing_source_unlock.json',encoding='utf-8') as f: unlocked=json.load(f)
with open(PROJECT+'/Scripts/FiringAudit/revision_plan.json',encoding='utf-8') as f: plan=json.load(f)
mapping={r['original_asset_path']:r for r in plan['assets']}
previous_path=PROJECT+'/ImportReport/firing_duplicate_reconciliation.json'
previous=json.load(open(previous_path,encoding='utf-8')) if os.path.exists(previous_path) else {}
result={'ok':False,'reconciled':previous.get('reconciled',[]),'errors':[]}
try:
    for old_path in unlocked['packages']:
        row=mapping[old_path]
        target=unreal.load_asset(row['asset_path'])
        source=unreal.load_asset(old_path)
        if not isinstance(target,unreal.AnimSequence) or not isinstance(source,unreal.AnimSequence):
            raise RuntimeError('Source/target animation is missing')
        if source.get_path_name()==target.get_path_name():
            result['reconciled'].append({'old':old_path,'new':row['asset_path'],'already_redirected':True})
            continue
        if source.get_editor_property('skeleton')!=target.get_editor_property('skeleton'):
            raise RuntimeError('Different skeletons')
        if abs(source.get_play_length()-target.get_play_length())>0.00001:
            raise RuntimeError('Different animation lengths')
        if list(unreal.AnimationLibrary.get_animation_track_names(source))!=list(unreal.AnimationLibrary.get_animation_track_names(target)):
            raise RuntimeError('Different animation tracks')
        if unreal.AnimationLibrary.get_num_keys(source)!=unreal.AnimationLibrary.get_num_keys(target):
            raise RuntimeError('Different animation sample counts')
        disk=PROJECT+'/Content/'+old_path.removeprefix('/Game/')+'.uasset'
        backup=BACKUP+'/'+old_path.removeprefix('/Game/')+'.uasset'
        os.makedirs(os.path.dirname(backup),exist_ok=True)
        if not os.path.exists(backup): shutil.copy2(disk,backup)
        if not unreal.EditorAssetLibrary.consolidate_assets(target,[source]):
            raise RuntimeError('Could not reconcile duplicated package '+old_path)
        result['reconciled'].append({'old':old_path,'new':row['asset_path'],'backup':backup})
    result['ok']=True
except Exception:
    result['errors'].append(traceback.format_exc())
    unreal.log_error(result['errors'][-1])
finally:
    with open(PROJECT+'/ImportReport/firing_duplicate_reconciliation.json','w',encoding='utf-8') as f:
        json.dump(result,f,ensure_ascii=False,indent=2)
