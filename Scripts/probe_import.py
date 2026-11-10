import unreal, json, os, traceback

ROOT = 'C:/Users/yeyuxiang/Desktop/全境封锁2解包'
OUT = 'E:/UEproject/Division2AnimationViewer/Scripts/probe_result.json'
result = {}

def run_task(source, destination, name, skeleton=None, animations=False):
    opts = unreal.FbxImportUI()
    opts.automated_import_should_detect_type = False
    opts.import_as_skeletal = True
    opts.import_mesh = not animations
    opts.import_animations = animations
    opts.import_materials = not animations
    opts.import_textures = False
    opts.create_physics_asset = False
    opts.mesh_type_to_import = unreal.FBXImportType.FBXIT_ANIMATION if animations else unreal.FBXImportType.FBXIT_SKELETAL_MESH
    opts.original_import_type = opts.mesh_type_to_import
    if skeleton:
        opts.skeleton = skeleton
    if animations:
        opts.anim_sequence_import_data.set_editor_property('animation_length', unreal.FBXAnimationLengthImportType.FBXALIT_EXPORTED_TIME)
        opts.anim_sequence_import_data.set_editor_property('use_default_sample_rate', False)
        opts.anim_sequence_import_data.set_editor_property('custom_sample_rate', 0)
        opts.anim_sequence_import_data.set_editor_property('import_bone_tracks', True)
    task = unreal.AssetImportTask()
    task.filename = source
    task.destination_path = destination
    task.destination_name = name
    task.automated = True
    task.save = True
    task.replace_existing = True
    task.factory = unreal.FbxFactory()
    task.options = opts
    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task])
    return task.imported_object_paths

try:
    unreal.SystemLibrary.execute_console_command(None, 'Interchange.FeatureFlags.Import.FBX 0')
    for gender in ('Male', 'Female'):
        dest = '/Game/Division2/Characters/' + gender
        name = 'SK_' + gender + '_Walker'
        paths = run_task(ROOT+'/characters/'+name+'.fbx', dest, name)
        result[gender] = {'mesh_import': list(paths)}
        mesh = unreal.load_asset(dest+'/'+name)
        if not isinstance(mesh, unreal.SkeletalMesh):
            raise RuntimeError('No skeletal mesh: '+str(paths))
        skeleton = mesh.get_editor_property('skeleton')
        unreal.EditorAssetLibrary.save_loaded_asset(skeleton)
        unreal.EditorAssetLibrary.save_loaded_asset(mesh)
        result[gender]['skeleton'] = skeleton.get_path_name()
        result[gender]['bounds'] = str(mesh.get_bounds())
        animname = 'p_shd_m_emote_crybaby' if gender == 'Male' else 'p_shd_f_dance_80s_intro'
        animpaths = run_task(ROOT+'/animations/'+animname+'.fbx', '/Game/Division2/Probe/'+gender, animname, skeleton, True)
        result[gender]['animation_import'] = list(animpaths)
        for path in animpaths:
            anim = unreal.load_asset(path)
            if isinstance(anim, unreal.AnimSequence):
                anim.set_preview_skeletal_mesh(mesh)
                unreal.EditorAssetLibrary.save_loaded_asset(anim)
                result[gender]['animation'] = {'path': path, 'duration': anim.get_play_length()}
        unreal.EditorAssetLibrary.save_loaded_asset(skeleton)
    unreal.EditorAssetLibrary.save_directory('/Game/Division2', only_if_is_dirty=True, recursive=True)
    result['ok'] = True
except Exception:
    result['error'] = traceback.format_exc()
finally:
    with open(OUT,'w',encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    unreal.log('DIVISION2_PROBE '+json.dumps(result,ensure_ascii=False))
