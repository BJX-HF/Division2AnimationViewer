"""Apply the independently rebuilt firing classification through UE asset renames."""
import unreal,json,traceback,os,time
from collections import Counter
PROJECT='E:/UEproject/Division2AnimationViewer'
with open(PROJECT+'/Scripts/FiringAudit/revision_plan.json',encoding='utf-8') as f:
    plan=json.load(f)
result={'ok':False,'basis':plan['summary']['basis'],'expected':len(plan['assets']),'moved':[],'errors':[]}
report=PROJECT+'/ImportReport/firing_reclassification.json'

def write_report():
    with open(report,'w',encoding='utf-8') as f:
        json.dump(result,f,ensure_ascii=False,indent=2)

try:
    unreal.AssetRegistryHelpers.get_asset_registry().scan_paths_synchronous(['/Game/Division2/Animations'],force_rescan=True)
    for index,row in enumerate(plan['assets'],1):
        old_path=row['original_asset_path']
        new_path=row['asset_path']
        try:
            already_exists=unreal.EditorAssetLibrary.does_asset_exist(new_path)
            if not already_exists and not unreal.EditorAssetLibrary.rename_asset(old_path,new_path):
                raise RuntimeError('UE rename failed')
            asset=unreal.load_asset(new_path)
            if not isinstance(asset,unreal.AnimSequence):
                raise RuntimeError('Destination is not an animation sequence')
            for key,value in {'Category':row['category'],'FiringClassification':row['group'],
                              'FiringSubtype':row['subtype'],'ClassificationBasis':'Filename + source FBX key curves',
                              'SourceConstantPose':str(row['all_curves_constant']),
                              'ConfirmedDynamicFiring':str(row['confirmed_dynamic_firing'])}.items():
                unreal.EditorAssetLibrary.set_metadata_tag(asset,key,value)
            if not unreal.EditorAssetLibrary.save_loaded_asset(asset,only_if_is_dirty=True):
                raise RuntimeError('Destination save failed')
            result['moved'].append({'name':row['name'],'old':old_path,'new':new_path,'group':row['group']})
        except Exception:
            result['errors'].append({'name':row['name'],'old':old_path,'new':new_path,'error':traceback.format_exc()})
        if index%25==0:
            write_report()
            unreal.log('FIRING_RECLASSIFY {}/{} errors={}'.format(index,len(plan['assets']),len(result['errors'])))
    if result['errors']:
        raise RuntimeError('Some animation moves failed; see report')
    registry=unreal.AssetRegistryHelpers.get_asset_registry()
    registry.search_all_assets(True)
    registry.scan_paths_synchronous(['/Game/Division2/Animations'],force_rescan=True)
    fire_assets=registry.get_assets_by_path('/Game/Division2/Animations/Male/Fire',recursive=True)
    real_fire=[a for a in fire_assets if str(a.asset_class_path.asset_name)=='AnimSequence']
    expected={r['asset_path'] for r in plan['assets'] if r['confirmed_dynamic_firing']}
    stale=[a for a in real_fire if str(a.package_name) not in expected]
    if stale:
        dirty={p.get_path_name() for p in unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()}
        packages=[]
        for data in stale:
            obj=data.get_asset()
            package=obj.get_outer()
            if package.get_path_name() in dirty:
                raise RuntimeError('Preserving unsaved edits in '+package.get_path_name())
            packages.append(package)
        result['refreshed_stale_packages']=[p.get_path_name() for p in packages]
        result['reload_result']=str(unreal.EditorLoadingAndSavingUtils.reload_packages(packages,unreal.ReloadPackagesInteractionMode.ASSUME_NEGATIVE))
        registry.scan_paths_synchronous(['/Game/Division2/Animations'],force_rescan=True)
        real_fire=[a for a in registry.get_assets_by_path('/Game/Division2/Animations/Male/Fire',recursive=True) if str(a.asset_class_path.asset_name)=='AnimSequence']
    result['actual_fire_count']=len(real_fire)
    result['actual_fire_assets']=sorted(str(a.package_name) for a in real_fire)
    if set(result['actual_fire_assets'])!=expected:
        raise RuntimeError('Fire folder content does not match the 40 independently selected dynamic animations')
    result['actual_fire_groups']=dict(Counter(r['group'] for r in plan['assets'] if r['confirmed_dynamic_firing']))
    result['ok']=True
except Exception:
    result['fatal_error']=traceback.format_exc()
    unreal.log_error(result['fatal_error'])
finally:
    write_report()
    unreal.log('FIRING_RECLASSIFICATION_COMPLETE '+json.dumps({k:v for k,v in result.items() if k not in ('moved','actual_fire_assets')},ensure_ascii=False))
