import unreal,json,traceback,runpy
PROJECT='E:/UEproject/Division2AnimationViewer'
with open(PROJECT+'/Scripts/FiringAudit/revision_plan.json',encoding='utf-8') as f: plan=json.load(f)
with open(PROJECT+'/ImportReport/firing_reclassification.json',encoding='utf-8') as f: result=json.load(f)
result['ok']=False
result.pop('fatal_error',None)
try:
    with open(PROJECT+'/ImportReport/firing_duplicate_reconciliation.json',encoding='utf-8') as f: reconciliation=json.load(f)
    if not reconciliation['ok']: raise RuntimeError('Source package reconciliation incomplete')
    dirty={p.get_path_name() for p in unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()}
    packages=[]
    for row in reconciliation['reconciled']:
        asset=unreal.load_asset(row['old'])
        package=asset.get_outer()
        if package.get_path_name()==row['old']:
            if row['old'] in dirty: raise RuntimeError('Preserving unsaved edits: '+row['old'])
            packages.append(package)
    if packages:
        result['final_refresh']=str(unreal.EditorLoadingAndSavingUtils.reload_packages(packages,unreal.ReloadPackagesInteractionMode.ASSUME_NEGATIVE))
    registry=unreal.AssetRegistryHelpers.get_asset_registry()
    registry.scan_paths_synchronous(['/Game/Division2/Animations'],force_rescan=True)
    checked=[]
    for row in plan['assets']:
        asset=unreal.load_asset(row['asset_path'])
        if not isinstance(asset,unreal.AnimSequence): raise RuntimeError('Missing destination '+row['asset_path'])
        expected_tracks=208 if row['gender_folder']=='Female' else 213
        if len(unreal.AnimationLibrary.get_animation_track_names(asset))!=expected_tracks:
            raise RuntimeError('Invalid bone tracks '+row['asset_path'])
        if abs(asset.get_play_length()-row['duration_seconds'])>0.067:
            raise RuntimeError('Animation duration changed '+row['asset_path'])
        checked.append(asset.get_path_name())
    expected={r['asset_path'] for r in plan['assets'] if r['confirmed_dynamic_firing']}
    fire=[a for a in registry.get_assets_by_path('/Game/Division2/Animations/Male/Fire',recursive=True) if str(a.asset_class_path.asset_name)=='AnimSequence']
    result['actual_fire_assets']=sorted(str(a.package_name) for a in fire)
    result['actual_fire_count']=len(fire)
    if set(result['actual_fire_assets'])!=expected:
        raise RuntimeError('Fire folder still has unexpected assets: '+str(set(result['actual_fire_assets'])-expected))
    result['checked_destinations']=len(checked)
    result['actual_fire_groups']=plan['summary']['confirmed_groups']
    result['moved']=[{'name':r['name'],'old':r['original_asset_path'],'new':r['asset_path'],'group':r['group']} for r in plan['assets']]
    result['errors']=[]
    result['ok']=True
except Exception:
    result['fatal_error']=traceback.format_exc()
    unreal.log_error(result['fatal_error'])
with open(PROJECT+'/ImportReport/firing_reclassification.json','w',encoding='utf-8') as f:
    json.dump(result,f,ensure_ascii=False,indent=2)
unreal.log('FIRING_FINAL_CHECK '+str(result['ok'])+' count='+str(result.get('actual_fire_count')))
if result['ok']:
    runpy.run_path(PROJECT+'/Scripts/open_firing.py',run_name='__main__')
