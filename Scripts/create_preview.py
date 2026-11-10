"""Build the saved, self-contained male/female animation preview stage.

Run inside the UE 5.8 editor Python environment after bulk_import.py.
The animation data is serialized on the components, so Play/Simulate works
without Python and without a Blueprint construction script.
"""
import json
import traceback
from pathlib import Path

import unreal


PROJECT = Path('E:/UEproject/Division2AnimationViewer')
MAP_PATH = '/Game/Division2/Preview/AnimationPreview'
RESULT_PATH = PROJECT / 'Scripts/create_preview_result.json'
ANIMATION_ROOT = '/Game/Division2/Animations'


def _load_required(path, asset_type=None):
    asset = unreal.load_asset(path)
    if asset is None or (asset_type is not None and not isinstance(asset, asset_type)):
        raise RuntimeError('Missing required preview asset: ' + path)
    return asset


def _optional_set(obj, name, value):
    try:
        obj.set_editor_property(name, value)
        return True
    except Exception as exc:
        unreal.log_warning('Preview optional property {}: {}'.format(name, exc))
        return False


def _make_material(name, color, roughness=0.72, metallic=0.0):
    folder = '/Game/Division2/Preview/Materials'
    existing = unreal.load_asset(folder + '/' + name)
    if existing:
        return existing
    mat = unreal.AssetToolsHelpers.get_asset_tools().create_asset(
        name, folder, unreal.Material, unreal.MaterialFactoryNew())
    if mat is None:
        raise RuntimeError('Could not create stage material ' + name)
    base = unreal.MaterialEditingLibrary.create_material_expression(
        mat, unreal.MaterialExpressionConstant3Vector, -350, -100)
    base.set_editor_property('constant', unreal.LinearColor(*color, 1.0))
    unreal.MaterialEditingLibrary.connect_material_property(
        base, '', unreal.MaterialProperty.MP_BASE_COLOR)
    rough = unreal.MaterialEditingLibrary.create_material_expression(
        mat, unreal.MaterialExpressionConstant, -350, 80)
    rough.set_editor_property('r', roughness)
    unreal.MaterialEditingLibrary.connect_material_property(
        rough, '', unreal.MaterialProperty.MP_ROUGHNESS)
    metal = unreal.MaterialEditingLibrary.create_material_expression(
        mat, unreal.MaterialExpressionConstant, -350, 180)
    metal.set_editor_property('r', metallic)
    unreal.MaterialEditingLibrary.connect_material_property(
        metal, '', unreal.MaterialProperty.MP_METALLIC)
    unreal.MaterialEditingLibrary.recompile_material(mat)
    unreal.EditorAssetLibrary.save_loaded_asset(mat)
    return mat


def _spawn(actor_class, name, location, rotation=(0, 0, 0), folder='Preview'):
    actor = unreal.get_editor_subsystem(unreal.EditorActorSubsystem).spawn_actor_from_class(
        actor_class, unreal.Vector(*location), unreal.Rotator(*rotation))
    if actor is None:
        raise RuntimeError('Could not spawn ' + name)
    actor.set_actor_label(name)
    actor.set_folder_path(folder)
    return actor


def _box(name, location, scale, material):
    actor = _spawn(unreal.StaticMeshActor, name, location, folder='Stage')
    component = actor.get_component_by_class(unreal.StaticMeshComponent)
    component.set_static_mesh(_load_required('/Engine/BasicShapes/Cube.Cube'))
    component.set_material(0, material)
    actor.set_actor_scale3d(unreal.Vector(*scale))
    return actor


def _label(name, text, location, size=17, color=(230, 236, 242, 255)):
    actor = _spawn(unreal.TextRenderActor, name, location, folder='Stage/Labels')
    component = actor.get_component_by_class(unreal.TextRenderComponent)
    component.set_text(text)
    component.set_world_size(size)
    component.set_horizontal_alignment(unreal.HorizTextAligment.EHTA_CENTER)
    component.set_text_render_color(unreal.Color(*color))
    return actor


def _find_animation(gender, candidates):
    for relative in candidates:
        anim = unreal.load_asset(ANIMATION_ROOT + '/' + gender + '/' + relative)
        if isinstance(anim, unreal.AnimSequence):
            return anim
    raise RuntimeError('No looping preview animation found for ' + gender)


def create_preview():
    # Resolve everything needed before creating the level.
    meshes = {
        g: _load_required('/Game/Division2/Characters/{0}/SK_{0}_Walker'.format(g), unreal.SkeletalMesh)
        for g in ('Male', 'Female')
    }
    clips = {
        'Male': _find_animation('Male', (
            'Emotes/p_shd_m_dance_80s_loop',
            'Emotes/p_shd_m_emote_headbang_loop',
            'Emotes/p_shd_m_emote_dance_01_loop')),
        'Female': _find_animation('Female', (
            'Emotes/p_shd_f_dance_80s_loop',
            'Emotes/p_shd_f_emote_discodance1_loop',
            'Emotes/p_shd_f_emote_housedance_loop')),
    }
    for gender in meshes:
        clips[gender].set_preview_skeletal_mesh(meshes[gender])
        unreal.EditorAssetLibrary.save_loaded_asset(clips[gender])

    # Rebuild only this generated map, including after a partially completed run.
    # World and actor object paths are checked before any actor is destroyed.
    level_editor = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    reused_map = unreal.EditorAssetLibrary.does_asset_exist(MAP_PATH)
    if reused_map:
        if not level_editor.load_level(MAP_PATH):
            raise RuntimeError('UE could not load generated preview map ' + MAP_PATH)
    elif not level_editor.new_level(MAP_PATH):
        raise RuntimeError('UE could not create preview map ' + MAP_PATH)

    expected_world_path = MAP_PATH + '.' + MAP_PATH.rsplit('/', 1)[-1]
    current_world = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
    if current_world is None or current_world.get_path_name() != expected_world_path:
        raise RuntimeError('Refusing to rebuild actors outside ' + expected_world_path)
    if reused_map:
        actor_subsystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
        actors_to_remove = []
        reserved_classes = (unreal.WorldSettings, unreal.Brush, unreal.LevelScriptActor)
        for actor in actor_subsystem.get_all_level_actors():
            if isinstance(actor, reserved_classes):
                continue
            if not actor.get_path_name().startswith(expected_world_path + ':PersistentLevel.'):
                raise RuntimeError('Refusing to destroy actor from another level: ' + actor.get_path_name())
            actors_to_remove.append(actor)
        if actors_to_remove and not actor_subsystem.destroy_actors(actors_to_remove):
            raise RuntimeError('Could not clear all actors from generated preview map')

    graphite = _make_material('M_Stage_Graphite', (0.025, 0.032, 0.042))
    pedestal = _make_material('M_Stage_Pedestal', (0.13, 0.15, 0.18), 0.5, 0.12)
    orange = _make_material('M_Stage_Orange', (0.9, 0.21, 0.025), 0.5)
    blue = _make_material('M_Stage_Blue', (0.045, 0.32, 0.7), 0.5)
    _box('Preview Floor', (0, 0, -22), (12, 12, 0.24), graphite)
    _box('Back Wall', (-210, 0, 170), (0.15, 10, 4), graphite)

    report = {'map': MAP_PATH, 'characters': {}, 'notes': []}
    for gender, lateral, accent in (('Male', -150, orange), ('Female', 150, blue)):
        _box(gender + ' Platform', (0, lateral, -6), (2.8, 2.8, 0.12), pedestal)
        _box(gender + ' Accent', (141, lateral, -4), (0.025, 2.8, 0.08), accent)
        actor = _spawn(unreal.SkeletalMeshActor, gender + ' - Looping Animation', (0, lateral, 0), folder='Characters')
        comp = actor.get_component_by_class(unreal.SkeletalMeshComponent)
        comp.set_skeletal_mesh_asset(meshes[gender])
        comp.set_animation_mode(unreal.AnimationMode.ANIMATION_SINGLE_NODE)
        # Unlike set_animation/play_animation, this stores the defaults in AnimationData.
        comp.override_animation_data(clips[gender], True, True, 0.0, 1.0)
        comp.set_update_animation_in_editor(True)
        comp.set_mobility(unreal.ComponentMobility.MOVABLE)
        _optional_set(comp, 'cast_shadow', True)
        _label(gender + ' Label', gender.upper(), (140, lateral, 13), 18,
               (255, 126, 40, 255) if gender == 'Male' else (95, 183, 255, 255))
        report['characters'][gender] = {
            'mesh': meshes[gender].get_path_name(),
            'animation': clips[gender].get_path_name(),
            'duration': clips[gender].get_play_length(),
            'actor': actor.get_path_name(),
        }

    _label('Library Title', 'THE DIVISION 2  |  ANIMATION LIBRARY', (-195, 0, 290), 22)
    _label('Library Hint', 'Male / Female / Shared  -  Open an animation to browse and scrub',
           (-193, 0, 252), 11, (150, 168, 185, 255))

    # Movable lights keep the stage usable without an offline lighting build.
    key = _spawn(unreal.DirectionalLight, 'Soft Key', (0, 0, 350), (-38, -155, 0), 'Lighting')
    key_comp = key.get_component_by_class(unreal.DirectionalLightComponent)
    key_comp.set_mobility(unreal.ComponentMobility.MOVABLE)
    key_comp.set_intensity(3.0)
    key_comp.set_light_color(unreal.LinearColor(1.0, 0.93, 0.85, 1.0))
    for name, pos, intensity, color in (
        ('Front Fill', (320, 0, 240), 90000, (0.78, 0.88, 1.0)),
        ('Orange Rim', (-100, -240, 260), 50000, (1.0, 0.46, 0.18)),
        ('Blue Rim', (-100, 240, 260), 50000, (0.3, 0.6, 1.0)),
    ):
        light = _spawn(unreal.PointLight, name, pos, folder='Lighting')
        light_comp = light.get_component_by_class(unreal.PointLightComponent)
        light_comp.set_mobility(unreal.ComponentMobility.MOVABLE)
        light_comp.set_intensity(float(intensity))
        light_comp.set_light_color(unreal.LinearColor(*color, 1.0))
        light_comp.set_editor_property('attenuation_radius', 1600.0)
        _optional_set(light_comp, 'source_radius', 70.0)

    exposure = _spawn(unreal.PostProcessVolume, 'Fixed Stage Exposure', (0, 0, 0), folder='Lighting')
    exposure.set_editor_property('unbound', True)
    settings = exposure.get_editor_property('settings')
    for prop, value in (
        ('override_auto_exposure_min_brightness', True),
        ('override_auto_exposure_max_brightness', True),
        ('auto_exposure_min_brightness', 1.0),
        ('auto_exposure_max_brightness', 1.0),
    ):
        _optional_set(settings, prop, value)
    exposure.set_editor_property('settings', settings)

    camera_location = unreal.Vector(660, 0, 225)
    camera_rotation = unreal.Rotator(-10.3, 180, 0)
    camera = _spawn(unreal.CameraActor, 'Preview Camera', (660, 0, 225), (-10.3, 180, 0), 'Cameras')
    camera.set_editor_property('auto_activate_for_player', unreal.AutoReceiveInput.PLAYER0)
    camera_comp = camera.get_component_by_class(unreal.CameraComponent)
    camera_comp.set_field_of_view(54.0)
    # The deprecated wrapper chooses the active viewport without requiring a config key.
    unreal.EditorLevelLibrary.set_level_viewport_camera_info(camera_location, camera_rotation)
    unreal.get_editor_subsystem(unreal.EditorActorSubsystem).clear_actor_selection_set()
    if not level_editor.save_current_level():
        raise RuntimeError('Could not save preview map')
    unreal.EditorAssetLibrary.save_directory('/Game/Division2/Preview', only_if_is_dirty=True, recursive=True)
    report['ok'] = True
    return report


if __name__ == '__main__':
    try:
        preview_report = create_preview()
    except Exception:
        preview_report = {'ok': False, 'error': traceback.format_exc()}
        unreal.log_error(preview_report['error'])
    RESULT_PATH.write_text(json.dumps(preview_report, ensure_ascii=False, indent=2), encoding='utf-8')
    unreal.log('DIVISION2_PREVIEW ' + json.dumps(preview_report, ensure_ascii=False))
