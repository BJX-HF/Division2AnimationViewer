import unreal,json,traceback
from collections import Counter
PROJECT='E:/UEproject/Division2AnimationViewer'
with open(PROJECT+'/Scripts/FiringAudit/revision_plan.json',encoding='utf-8') as f: plan=json.load(f)
result={'ok':False,'errors':[],'checked':0}
try:
    registry=unreal.AssetRegistryHelpers.get_asset_registry()
    registry.search_all_assets(True)
    fire=[a for a in registry.get_assets_by_path('/Game/Division2/Animations/Male/Fire',recursive=True) if str(a.asset_class_path.asset_name)=='AnimSequence']
    expected={r['asset_path'] for r in plan['assets'] if r['confirmed_dynamic_firing']}
    assert {str(a.package_name) for a in fire}==expected
    result['fire_count']=len(fire)
    for row in plan['assets']:
        asset=unreal.load_asset(row['asset_path'])
        assert isinstance(asset,unreal.AnimSequence)
        assert len(unreal.AnimationLibrary.get_animation_track_names(asset))==(208 if row['gender_folder']=='Female' else 213)
        assert abs(asset.get_play_length()-row['duration_seconds'])<=0.067
        assert unreal.EditorAssetLibrary.find_asset_data(row['asset_path']).get_tag_value('PreviewSkeletalMesh')
        result['checked']+=1
    all_data=registry.get_assets_by_path('/Game/Division2',recursive=True)
    result['asset_types']=dict(Counter(str(a.asset_class_path.asset_name) for a in all_data))
    assert result['asset_types']['AnimSequence']==4369
    result['ok']=True
except Exception:
    result['errors'].append(traceback.format_exc())
finally:
    with open(PROJECT+'/ImportReport/firing_saved_validation.json','w',encoding='utf-8') as f:
        json.dump(result,f,ensure_ascii=False,indent=2)
