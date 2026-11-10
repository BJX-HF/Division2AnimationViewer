import unreal
asset = unreal.load_asset('/Game/Division2/Probe/Male/p_shd_m_emote_crybaby')
if asset:
    unreal.get_editor_subsystem(unreal.AssetEditorSubsystem).open_editor_for_assets([asset])
