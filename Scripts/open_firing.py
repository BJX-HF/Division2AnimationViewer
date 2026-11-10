"""Open the rebuilt firing library in an interactive UE editor session."""
import unreal,time,json,traceback
started=time.monotonic()
tick_handle=None
PROJECT='E:/UEproject/Division2AnimationViewer'

def show_firing(delta_seconds):
    global tick_handle
    if time.monotonic()-started<8.0:
        return
    unreal.unregister_slate_post_tick_callback(tick_handle)
    report={'ok':False}
    try:
        paths=[
          '/Game/Division2/Animations/Male/Fire/Burst/p_shd_m_st_burst_600rpm_ar_i_v01',
          '/Game/Division2/Animations/Male/Fire/SingleShot/p_shd_m_st_singleshot_pi_i_v01',
          '/Game/Division2/Animations/Male/Fire/SingleShot/p_shd_m_st_singleshot_sg_i_v01',
          '/Game/Division2/Animations/Male/Fire/SingleShot/p_shd_m_st_singleshot_mr_i_v01',
        ]
        clips=[unreal.load_asset(p) for p in paths]
        if any(not isinstance(a,unreal.AnimSequence) for a in clips):
            raise RuntimeError('A recommended firing animation is missing')
        # Select all four recommended clips so they remain easy to locate in the browser.
        unreal.EditorAssetLibrary.sync_browser_to_objects([a.get_path_name() for a in clips])
        unreal.get_editor_subsystem(unreal.AssetEditorSubsystem).open_editor_for_assets([clips[0]])
        report={'ok':True,'opened':clips[0].get_path_name(),'recommended':[a.get_path_name() for a in clips]}
    except Exception:
        report['error']=traceback.format_exc()
        unreal.log_error(report['error'])
    with open(PROJECT+'/ImportReport/open_firing.json','w',encoding='utf-8') as f:
        json.dump(report,f,ensure_ascii=False,indent=2)
    unreal.log('FIRING_PREVIEW_OPEN '+json.dumps(report,ensure_ascii=False))

tick_handle=unreal.register_slate_post_tick_callback(show_firing)
