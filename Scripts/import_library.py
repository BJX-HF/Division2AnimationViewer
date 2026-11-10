"""Resumable UE 5.8 legacy-FBX import of the complete source library."""
import unreal
import json
import os
import time
import traceback
import re

PROJECT = 'E:/UEproject/Division2AnimationViewer'
SOURCE = 'C:/Users/yeyuxiang/Desktop/全境封锁2解包'
SCRIPTS = PROJECT + '/Scripts'
REPORT = PROJECT + '/ImportReport'
command_line = unreal.SystemLibrary.get_command_line()
worker_match = re.search(r'-D2Worker=(\d+)/(\d+)',command_line)
WORKER, WORKERS = tuple(map(int,worker_match.groups())) if worker_match else (0,1)
if WORKERS > 1:
    REPORT += '/worker_'+str(WORKER)
os.makedirs(REPORT, exist_ok=True)
with open(SCRIPTS+'/animation_manifest.json', encoding='utf-8') as f:
    MANIFEST = json.load(f)
if WORKERS > 1:
    MANIFEST = [row for index,row in enumerate(MANIFEST) if index%WORKERS == WORKER]
started = time.time()
records = []
errors = []
meshes = {}
skeletons = {}

def log(message):
    unreal.log('DIVISION2 '+message)

def write_progress(status, done, last=''):
    data = dict(status=status, total=len(MANIFEST), processed=done,
                succeeded=len(records), failed=len(errors), last=last,
                elapsed_seconds=round(time.time()-started, 1), errors=errors[-10:])
    temp = REPORT+'/progress.tmp'
    with open(temp, 'w', encoding='utf-8') as f:
        json.dump(data,f,ensure_ascii=False,indent=2)
    os.replace(temp, REPORT+'/progress.json')

def import_fbx(source, destination, name, skeleton=None, animation_only=False, include_animation=False):
    options = unreal.FbxImportUI()
    options.automated_import_should_detect_type = False
    options.import_as_skeletal = True
    options.import_mesh = not animation_only
    options.import_animations = animation_only or include_animation
    options.import_materials = not animation_only
    options.import_textures = False
    options.create_physics_asset = False
    options.mesh_type_to_import = unreal.FBXImportType.FBXIT_ANIMATION if animation_only else unreal.FBXImportType.FBXIT_SKELETAL_MESH
    options.original_import_type = options.mesh_type_to_import
    if skeleton:
        options.skeleton = skeleton
    options.skeletal_mesh_import_data.set_editor_property('import_morph_targets', False)
    options.anim_sequence_import_data.set_editor_property('animation_length', unreal.FBXAnimationLengthImportType.FBXALIT_EXPORTED_TIME)
    options.anim_sequence_import_data.set_editor_property('use_default_sample_rate', False)
    options.anim_sequence_import_data.set_editor_property('custom_sample_rate', 0)
    options.anim_sequence_import_data.set_editor_property('snap_to_closest_frame_boundary', True)
    options.anim_sequence_import_data.set_editor_property('import_bone_tracks', True)
    options.anim_sequence_import_data.set_editor_property('import_custom_attribute', False)
    options.anim_sequence_import_data.set_editor_property('add_curve_metadata_to_skeleton', False)
    task = unreal.AssetImportTask()
    task.filename = source
    task.destination_path = destination
    task.destination_name = name
    task.automated = True
    task.save = False
    task.replace_existing = True
    task.factory = unreal.FbxFactory()
    task.options = options
    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task])
    return list(task.imported_object_paths)

def load_character(gender):
    folder = '/Game/Division2/Characters/'+gender
    name = 'SK_'+gender+'_Walker'
    mesh = unreal.load_asset(folder+'/'+name)
    if not mesh or not mesh.get_editor_property('skeleton'):
        import_fbx(SOURCE+'/characters/'+name+'.fbx',folder,name)
        mesh = unreal.load_asset(folder+'/'+name)
    if not isinstance(mesh,unreal.SkeletalMesh):
        raise RuntimeError('Character mesh missing: '+gender)
    skeleton = mesh.get_editor_property('skeleton')
    if not skeleton:
        raise RuntimeError('Character skeleton missing: '+gender)
    if WORKERS == 1:
        unreal.EditorAssetLibrary.save_directory(folder,only_if_is_dirty=True,recursive=True)
    meshes[gender] = mesh
    skeletons[gender] = skeleton
    return mesh

try:
    write_progress('starting',0)
    for gender in ('Male','Female'):
        load_character(gender)
    priority = {'p_shd_m_emote_crybaby', 'p_shd_f_dance_80s_intro', 'p_shd_f_dance_80s_loop', 'p_shd_mf_emote_robot_1'}
    rows = sorted(MANIFEST,key=lambda row:(row['name'] not in priority,row['gender_folder'],row['category_folder'],row['name']))
    for i,row in enumerate(rows,1):
        path = row['destination']+'/'+row['asset_name']
        try:
            anim = unreal.load_asset(path) if unreal.EditorAssetLibrary.does_asset_exist(path) else None
            if not isinstance(anim,unreal.AnimSequence):
                imported = import_fbx(row['source_file'],row['destination'],row['asset_name'],skeletons[row['rig']],True)
                anim = unreal.load_asset(path)
                if not isinstance(anim,unreal.AnimSequence):
                    raise RuntimeError('Animation import produced no sequence: '+str(imported))
            if anim.get_editor_property('skeleton') != skeletons[row['rig']]:
                raise RuntimeError('Unexpected skeleton: '+path)
            anim.set_preview_skeletal_mesh(meshes[row['rig']])
            for tag,value in {'OriginalName':row['name'],'Gender':row['gender'],'Category':row['category'],'Stance':row['stance'],'SourceFBX':row['source_file']}.items():
                unreal.EditorAssetLibrary.set_metadata_tag(anim,tag,value)
            unreal.EditorAssetLibrary.save_loaded_asset(anim,only_if_is_dirty=True)
            rec = dict(source=row['source_file'],asset=anim.get_path_name(),duration_seconds=anim.get_play_length(),rig=row['rig'],gender=row['gender'],category=row['category'],preview_mesh=meshes[row['rig']].get_path_name())
            records.append(rec)
            with open(REPORT+'/imported.jsonl','a',encoding='utf-8') as f:
                f.write(json.dumps(rec,ensure_ascii=False)+'\n')
        except Exception:
            failure = dict(source=row['source_file'],asset=path,error=traceback.format_exc())
            errors.append(failure)
            log('FAILED '+json.dumps(failure,ensure_ascii=False))
        if i%25 == 0 or i == len(rows):
            write_progress('importing',i,row['name'])
            log('PROGRESS {}/{} succeeded={} failed={} seconds={:.1f}'.format(i,len(rows),len(records),len(errors),time.time()-started))
            unreal.SystemLibrary.collect_garbage()

    preview_records = []
    for basename in (() if WORKERS > 1 else ('male_walker_head_walk','male_walker_walk')):
        folder = '/Game/Division2/Preview/SourceExamples/'+('FullCharacter' if 'head' in basename else 'BodyOnly')
        paths = import_fbx(SOURCE+'/preview/'+basename+'.fbx',folder,basename,include_animation=True)
        mesh = next((unreal.load_asset(p) for p in paths if isinstance(unreal.load_asset(p),unreal.SkeletalMesh)),None)
        if not mesh:
            raise RuntimeError('Preview mesh missing: '+basename)
        animations = []
        for path in unreal.EditorAssetLibrary.list_assets(folder,recursive=True):
            asset = unreal.load_asset(path)
            if isinstance(asset,unreal.AnimSequence):
                asset.set_preview_skeletal_mesh(mesh)
                animations.append(asset.get_path_name())
        if not animations:
            raise RuntimeError('Preview animation missing: '+basename)
        unreal.EditorAssetLibrary.save_directory(folder,only_if_is_dirty=True,recursive=True)
        preview_records.append(dict(source=SOURCE+'/preview/'+basename+'.fbx',mesh=mesh.get_path_name(),animations=animations))

    if WORKERS == 1:
        unreal.EditorAssetLibrary.save_directory('/Game/Division2/Characters',only_if_is_dirty=True,recursive=True)
    summary = dict(source_fbx_count=4371,character_fbx_count=2,animation_count=len(records),failed=errors,
                   animation_total=4367,preview_sources=preview_records,elapsed_seconds=round(time.time()-started,1),records=records)
    with open(REPORT+'/summary.json','w',encoding='utf-8') as f:
        json.dump(summary,f,ensure_ascii=False,indent=2)
    write_progress('complete' if not errors else 'complete_with_errors',len(rows))
    log('IMPORT_COMPLETE animations={} failed={}'.format(len(records),len(errors)))
except Exception:
    errors.append(dict(error=traceback.format_exc()))
    write_progress('fatal',len(records))
    log('FATAL '+traceback.format_exc())
    raise
