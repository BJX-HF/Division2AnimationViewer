import unreal,json,traceback
records=[]
for gender,filename in [('Male','p_shd_m_emote_crybaby'),('Female','p_shd_f_dance_80s_intro')]:
    rec={'gender':gender}
    try:
        anim=unreal.load_asset('/Game/Division2/Animations/'+gender+'/Emotes/'+filename)
        preview=unreal.EditorAssetLibrary.find_asset_data(anim.get_path_name()).get_tag_value('PreviewSkeletalMesh')
        rec.update(preview_type=str(type(preview)),preview=str(preview),
                   frames=unreal.AnimationLibrary.get_num_frames(anim),keys=unreal.AnimationLibrary.get_num_keys(anim),
                   tracks=len(unreal.AnimationLibrary.get_animation_track_names(anim)),duration=anim.get_play_length())
    except Exception:
        rec['error']=traceback.format_exc()
    records.append(rec)
with open('E:/UEproject/Division2AnimationViewer/ImportReport/saved_samples.json','w',encoding='utf-8') as f:
    json.dump(records,f,ensure_ascii=False,indent=2)
