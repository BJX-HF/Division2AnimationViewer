"""Open sample animations after the editor has finished creating its windows."""
import unreal, time, os, json

PROJECT = 'E:/UEproject/Division2AnimationViewer'
started = time.monotonic()
callback_handle = None

def open_when_ready(delta_seconds):
    global callback_handle
    if time.monotonic()-started < 8.0:
        return
    unreal.unregister_slate_post_tick_callback(callback_handle)
    for actor in unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors():
        if isinstance(actor,unreal.SkeletalMeshActor):
            component = actor.get_component_by_class(unreal.SkeletalMeshComponent)
            component.set_update_animation_in_editor(True)
    unreal.EditorLevelLibrary.set_level_viewport_camera_info(unreal.Vector(660,0,225),unreal.Rotator(-10.3,180,0))
    unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
    assets = []
    for gender,filename in [('Male','p_shd_m_dance_80s_loop'),('Female','p_shd_f_dance_80s_loop')]:
        asset = unreal.load_asset('/Game/Division2/Animations/'+gender+'/Emotes/'+filename)
        if asset:
            assets.append(asset)
    if assets:
        unreal.EditorAssetLibrary.sync_browser_to_objects([a.get_path_name() for a in assets])
        unreal.get_editor_subsystem(unreal.AssetEditorSubsystem).open_editor_for_assets(assets)
    with open(PROJECT+'/ImportReport/open_library.json','w',encoding='utf-8') as f:
        json.dump(dict(opened=[a.get_path_name() for a in assets],time=time.time()),f,indent=2)

callback_handle = unreal.register_slate_post_tick_callback(open_when_ready)
