import unreal,json,traceback
PROJECT='E:/UEproject/Division2AnimationViewer'
with open(PROJECT+'/Scripts/FiringAudit/revision_plan.json',encoding='utf-8') as f: plan=json.load(f)
registry=unreal.AssetRegistryHelpers.get_asset_registry()
registry.scan_paths_synchronous(['/Game/Division2/Animations'],force_rescan=True)
stale=[]
for row in plan['assets']:
    data=unreal.EditorAssetLibrary.find_asset_data(row['original_asset_path'])
    if str(data.asset_class_path.asset_name)=='AnimSequence':
        stale.append(data)
dirty={p.get_path_name() for p in unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()}
packages=[]
for data in stale:
    package=data.get_asset().get_outer()
    if package.get_path_name() in dirty:
        raise RuntimeError('Preserving unsaved package '+package.get_path_name())
    packages.append(package)
unreal.EditorLoadingAndSavingUtils.fully_load_packages(packages)
with open(PROJECT+'/ImportReport/firing_source_unlock.json','w',encoding='utf-8') as f:
    json.dump({'ok':True,'packages':[p.get_path_name() for p in packages]},f,indent=2)
