"""Import the two source examples and verify all saved animation packages."""
import unreal, json, os, time, traceback, runpy
from collections import Counter

PROJECT = 'E:/UEproject/Division2AnimationViewer'
SOURCE = 'C:/Users/yeyuxiang/Desktop/全境封锁2解包'
REPORT = PROJECT+'/ImportReport'
with open(PROJECT+'/Scripts/animation_manifest.json',encoding='utf-8') as f:
    rows = json.load(f)
with open(PROJECT+'/Scripts/source_timings.json',encoding='utf-8') as f:
    timing_data = json.load(f)
timings = {row['name']:row for row in timing_data['animations']}
result = dict(ok=False,expected_source_fbx=4371,expected_library_animations=4367,
              checked=0,errors=[],preview_sources=[],gender_counts={},category_counts={})

def save_report():
    with open(REPORT+'/validation.json','w',encoding='utf-8') as f:
        json.dump(result,f,ensure_ascii=False,indent=2)

try:
    meshes = {gender:unreal.load_asset('/Game/Division2/Characters/{0}/SK_{0}_Walker'.format(gender)) for gender in ('Male','Female')}
    skeletons = {gender:mesh.get_editor_property('skeleton') for gender,mesh in meshes.items()}
    for gender,mesh in meshes.items():
        if not isinstance(mesh,unreal.SkeletalMesh) or not skeletons[gender]:
            raise RuntimeError('Missing character: '+gender)
    gender_count = Counter()
    category_count = Counter()
    detail = []
    duration_errors = []
    for i,row in enumerate(rows,1):
        path = row['destination']+'/'+row['asset_name']
        try:
            asset = unreal.load_asset(path)
            if not isinstance(asset,unreal.AnimSequence):
                raise RuntimeError('Saved sequence missing or unreadable')
            skeleton = asset.get_editor_property('skeleton')
            if skeleton != skeletons[row['rig']]:
                raise RuntimeError('Skeleton mismatch')
            preview = unreal.EditorAssetLibrary.find_asset_data(path).get_tag_value('PreviewSkeletalMesh')
            if meshes[row['rig']].get_path_name() not in str(preview):
                raise RuntimeError('Saved preview mesh mismatch: '+str(preview))
            track_names = list(unreal.AnimationLibrary.get_animation_track_names(asset))
            frames = unreal.AnimationLibrary.get_num_frames(asset)
            keys = unreal.AnimationLibrary.get_num_keys(asset)
            expected_tracks = 208 if row['rig']=='Female' else 213
            if len(track_names) != expected_tracks:
                raise RuntimeError('Bone track mismatch {} != {}'.format(len(track_names),expected_tracks))
            if frames < 1 or keys < 2 or asset.get_play_length() <= 0:
                raise RuntimeError('No playable animation samples')
            source_timing = timings[row['name']]
            duration_delta = abs(asset.get_play_length()-source_timing['duration_seconds'])
            allowed_delta = max(0.001,min(1.0/15.0,1.0/source_timing['frame_rate']+0.0001))
            if duration_delta > allowed_delta:
                raise RuntimeError('Duration differs from source by {:.6f}s'.format(duration_delta))
            duration_errors.append(duration_delta)
            detail.append(dict(source=row['source_file'],asset=asset.get_path_name(),rig=row['rig'],
                               gender=row['gender'],category=row['category'],duration=asset.get_play_length(),
                               frames=frames,keys=keys,tracks=len(track_names),preview_mesh=str(preview),
                               source_duration=source_timing['duration_seconds'],source_fps=source_timing['frame_rate'],
                               source_constant_pose=source_timing['all_curves_constant'],duration_error_seconds=duration_delta))
            result['checked'] += 1
            gender_count[row['gender']] += 1
            category_count[row['category']] += 1
        except Exception:
            result['errors'].append(dict(asset=path,error=traceback.format_exc()))
        if i%100==0:
            save_report()
            unreal.log('DIVISION2_VALIDATION {}/{} errors={}'.format(i,len(rows),len(result['errors'])))
            unreal.SystemLibrary.collect_garbage()
    result['gender_counts'] = dict(gender_count)
    result['category_counts'] = dict(category_count)
    result['maximum_duration_error_seconds'] = max(duration_errors,default=0)
    result['source_constant_pose_count'] = timing_data['summary']['constant_pose_count']
    with open(REPORT+'/validated_animations.json','w',encoding='utf-8') as f:
        json.dump(detail,f,ensure_ascii=False,indent=2)
    if result['errors']:
        raise RuntimeError('Saved animation validation failed; see report')

    for basename in ('male_walker_head_walk','male_walker_walk'):
        folder = '/Game/Division2/Preview/SourceExamples/'+('FullCharacter' if 'head' in basename else 'BodyOnly')
        options = unreal.FbxImportUI()
        options.automated_import_should_detect_type = False
        options.import_as_skeletal = True
        options.import_mesh = True
        options.import_animations = True
        options.import_materials = True
        options.import_textures = False
        options.create_physics_asset = False
        options.mesh_type_to_import = unreal.FBXImportType.FBXIT_SKELETAL_MESH
        options.original_import_type = unreal.FBXImportType.FBXIT_SKELETAL_MESH
        options.anim_sequence_import_data.set_editor_property('animation_length',unreal.FBXAnimationLengthImportType.FBXALIT_EXPORTED_TIME)
        options.anim_sequence_import_data.set_editor_property('snap_to_closest_frame_boundary',True)
        task = unreal.AssetImportTask()
        task.filename = SOURCE+'/preview/'+basename+'.fbx'
        task.destination_path = folder
        task.destination_name = basename
        task.automated = True
        task.replace_existing = True
        task.save = False
        task.factory = unreal.FbxFactory()
        task.options = options
        unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task])
        assets = [unreal.load_asset(p) for p in unreal.EditorAssetLibrary.list_assets(folder,recursive=True)]
        mesh = next((a for a in assets if isinstance(a,unreal.SkeletalMesh)),None)
        anims = [a for a in assets if isinstance(a,unreal.AnimSequence)]
        if mesh is None or not anims:
            raise RuntimeError('Source preview import incomplete: '+basename)
        for anim in anims:
            anim.set_preview_skeletal_mesh(mesh)
        unreal.EditorAssetLibrary.save_directory(folder,only_if_is_dirty=True,recursive=True)
        result['preview_sources'].append(dict(source=task.filename,mesh=mesh.get_path_name(),animations=[a.get_path_name() for a in anims]))

    # Remove only the two temporary sample animations created by our initial probe.
    if unreal.EditorAssetLibrary.does_directory_exist('/Game/Division2/Probe'):
        unreal.EditorAssetLibrary.delete_directory('/Game/Division2/Probe')
    runpy.run_path(PROJECT+'/Scripts/create_preview.py',run_name='__main__')
    with open(PROJECT+'/Scripts/create_preview_result.json',encoding='utf-8') as f:
        result['preview_map'] = json.load(f)
    if not result['preview_map'].get('ok'):
        raise RuntimeError('Preview scene creation failed')
    registry = unreal.AssetRegistryHelpers.get_asset_registry()
    registry.search_all_assets(True)
    asset_data = registry.get_assets_by_path('/Game/Division2',recursive=True)
    result['asset_type_counts'] = dict(Counter(str(a.asset_class_path.asset_name) for a in asset_data))
    result['source_fbx_imported'] = result['checked']+len(meshes)+len(result['preview_sources'])
    result['ok'] = result['source_fbx_imported'] == 4371
except Exception:
    result['fatal_error'] = traceback.format_exc()
    unreal.log_error(result['fatal_error'])
finally:
    save_report()
    unreal.log('DIVISION2_FINAL_VALIDATION '+json.dumps({k:v for k,v in result.items() if k not in ('errors',)},ensure_ascii=False))
