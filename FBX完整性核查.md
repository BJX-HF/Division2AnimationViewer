# FBX 完整性与用途口径复核

此前“当前玩家图引用 4,453 个动画”的说法不够精确：**4,453 是 .anim 资源字符串数，4,409 个进入 common animData 并有节点使用，44 个没有动画节点使用记录。** 字符串出现不能直接作为执行证据。

| 核对层级 | 数量 |
|---|---:|
| 指定目录全部 FBX | 4,371 |
| animations 文件夹 FBX | 4,367 |
| 当前玩家图 .anim 资源字符串 | 4,453 |
| 有 common animData 与节点使用的资源 | 4,409 |
| 仅字符串 / animSet 级引用的资源 | 44 |
| 现有动画 FBX 中有本主图节点用法 | 4,282 |
| 现有动画 FBX 中未观察到本主图节点用法 | 85 |
| 85 个中仅在字符串池出现 / 完全未出现 | 41 / 44 |
| 资源字符串中缺同名 FBX | 130 |
| 130 个中有节点使用 / 无节点使用记录 | 127 / 3 |

130 个原始资源全部在当前游戏 TOC 中存在，但其中包含骨架参考等，不能统称 130 条已执行的运动动画。85 个未观察到节点使用的现有文件也没有被判为无用，可能需要其他动画图或上下文证据。

当前普通射击 / 固定武器后坐所选范围的 40 个动态源与 2 个姿势采样均有 FBX；这既不证明全游戏动画穷尽，也不表示每个源文件是完整全身动作。信号枪的 11 个动作序列现已有独立发射事件证据。

[完整动画图与资源用途](玩家动画图完整审计.html) · [全量用途审计说明](全图用途审计说明.md) · [HTML 开火调用链路](开火调用链路.html)

## 130 个缺同名 FBX 的资源

| 原始资源 | 本主图节点使用记录 | TOC 元数据偏移 |
|---|---:|---|
| `hunter/baked/snowdrop/animation/emote_rps_idle_new.anim` | 19 | `0x1f98156` |
| `hunter/baked/snowdrop/animation/emote_rps_paper.anim` | 6 | `0x1f98175` |
| `hunter/baked/snowdrop/animation/emote_rps_rock.anim` | 6 | `0x1f98198` |
| `hunter/baked/snowdrop/animation/emote_rps_scissor.anim` | 6 | `0x1f981b9` |
| `hunter/baked/snowdrop/animation/mounted_weapon_chest_impact_back.anim` | 1 | `0x1f9a984` |
| `hunter/baked/snowdrop/animation/mounted_weapon_chest_impact_front.anim` | 1 | `0x1f9a9a3` |
| `hunter/baked/snowdrop/animation/mounted_weapon_chest_impact_left.anim` | 1 | `0x1f9a9c6` |
| `hunter/baked/snowdrop/animation/mounted_weapon_chest_impact_right.anim` | 1 | `0x1f9a9e5` |
| `hunter/baked/snowdrop/animation/mounted_weapon_head_impact_back.anim` | 1 | `0x1f9aa1f` |
| `hunter/baked/snowdrop/animation/mounted_weapon_head_impact_front.anim` | 1 | `0x1f9aa3e` |
| `hunter/baked/snowdrop/animation/mounted_weapon_head_impact_left.anim` | 1 | `0x1f9aa61` |
| `hunter/baked/snowdrop/animation/mounted_weapon_head_impact_right.anim` | 1 | `0x1f9aa80` |
| `hunter/baked/snowdrop/animation/mounted_weapon_leg_impact_left.anim` | 1 | `0x1f9aaaf` |
| `hunter/baked/snowdrop/animation/mounted_weapon_leg_impact_right.anim` | 1 | `0x1f9aace` |
| `hunter/baked/snowdrop/animation/n_end_m_st_com_howl_effect_in_ua_v01.anim` | 9 | `0x1fc29cf` |
| `hunter/baked/snowdrop/animation/n_end_m_st_com_howl_effect_loop_ua_v01.anim` | 5 | `0x1fc29f9` |
| `hunter/baked/snowdrop/animation/n_end_m_st_com_howl_effect_out_ua_v01.anim` | 6 | `0x1fc2a1d` |
| `hunter/baked/snowdrop/animation/n_end_m_st_com_standturn_h-45_ar_v01.anim` | 2 | `0x1fc4e0d` |
| `hunter/baked/snowdrop/animation/n_end_m_st_com_standturn_h45_ar_v01.anim` | 2 | `0x1fc5043` |
| `hunter/baked/snowdrop/animation/n_f_ven_trader5_boopublic_notice_breaker_v01.anim` | 0 | `0x1fc8a9c` |
| `hunter/baked/snowdrop/animation/n_gen_m_st_com_death_chest_b_ar_v02.anim` | 1 | `0x1fd3a7d` |
| `hunter/baked/snowdrop/animation/n_gen_m_st_com_death_chest_b_ar_v03.anim` | 1 | `0x1fd3a9e` |
| `hunter/baked/snowdrop/animation/n_gen_m_st_com_death_head_f_ar_v01.anim` | 4 | `0x1fd4363` |
| `hunter/baked/snowdrop/animation/n_gen_m_st_com_death_head_f_ar_v02.anim` | 1 | `0x1fd4384` |
| `hunter/baked/snowdrop/animation/n_gen_m_st_com_death_head_fb_ar_v01.anim` | 1 | `0x1fd4450` |
| `hunter/baked/snowdrop/animation/n_gen_m_st_com_death_head_fb_ar_v02.anim` | 1 | `0x1fd4489` |
| `hunter/baked/snowdrop/animation/p_dance_tom_intro.anim` | 5 | `0x201a35b` |
| `hunter/baked/snowdrop/animation/p_dance_tom_intro_f.anim` | 2 | `0x201a377` |
| `hunter/baked/snowdrop/animation/p_dance_tom_loop.anim` | 5 | `0x201a39b` |
| `hunter/baked/snowdrop/animation/p_dance_tom_loop_f.anim` | 2 | `0x201a3b7` |
| `hunter/baked/snowdrop/animation/p_dflt_m_hcl_disable_skill_ar_i.anim` | 5 | `0x201a404` |
| `hunter/baked/snowdrop/animation/p_dflt_m_hcr_deploy_drone_ar_i.anim` | 3 | `0x201a43d` |
| `hunter/baked/snowdrop/animation/p_dflt_m_hcr_disable_skill_ar_i.anim` | 5 | `0x201a468` |
| `hunter/baked/snowdrop/animation/p_dflt_m_hcr_quickdeploy_skm_ar_ic.anim` | 11 | `0x201a49d` |
| `hunter/baked/snowdrop/animation/p_dflt_m_lcl_disable_skill_ar_i.anim` | 5 | `0x201a4f0` |
| `hunter/baked/snowdrop/animation/p_dflt_m_lcr_deploy_drone_ar_i.anim` | 3 | `0x201a529` |
| `hunter/baked/snowdrop/animation/p_dflt_m_lcr_disable_skill_ar_i.anim` | 5 | `0x201a554` |
| `hunter/baked/snowdrop/animation/p_dflt_m_lcr_quickdeploy_skm_ar_ic.anim` | 11 | `0x201a589` |
| `hunter/baked/snowdrop/animation/p_dflt_m_st_deploy_drone_ar_i.anim` | 4 | `0x201a5f6` |
| `hunter/baked/snowdrop/animation/p_dflt_m_st_deploy_drone_ar_o.anim` | 3 | `0x201a611` |
| `hunter/baked/snowdrop/animation/p_dflt_m_st_deploy_drone_pi_o.anim` | 4 | `0x201a62f` |
| `hunter/baked/snowdrop/animation/p_dflt_m_st_disable_skill_ar_i.anim` | 5 | `0x201a660` |
| `hunter/baked/snowdrop/animation/p_dflt_m_st_disable_skill_ar_o.anim` | 9 | `0x201a67b` |
| `hunter/baked/snowdrop/animation/p_dflt_m_st_emote_champion_pi_testing.anim` | 1 | `0x201a6b9` |
| `hunter/baked/snowdrop/animation/p_dflt_m_st_emote_salute_ar_o_testing.anim` | 1 | `0x201a6eb` |
| `hunter/baked/snowdrop/animation/p_dflt_m_st_emote_yawn_o.anim` | 1 | `0x201a70b` |
| `hunter/baked/snowdrop/animation/p_dflt_m_st_falling_damage_to_st_idle_pi.anim` | 1 | `0x201a747` |
| `hunter/baked/snowdrop/animation/p_dflt_m_st_falling_high_to_st_idle_roll_pi_o.anim` | 1 | `0x201a77a` |
| `hunter/baked/snowdrop/animation/p_dflt_m_st_idle_h-90_to_h+90_v-45_pi_i.anim` | 26 | `0x201abc6` |
| `hunter/baked/snowdrop/animation/p_dflt_m_st_idle_h-90_to_h+90_v-90_pi_i.anim` | 26 | `0x201abe7` |
| `hunter/baked/snowdrop/animation/p_dflt_m_st_idle_h-90_to_h+90_v0_pi_i.anim` | 61 | `0x201ac0c` |
| `hunter/baked/snowdrop/animation/p_dflt_m_st_idle_h-90_to_h+90_v45_pi_i.anim` | 26 | `0x201ac32` |
| `hunter/baked/snowdrop/animation/p_dflt_m_st_idle_h-90_to_h+90_v90_pi_i.anim` | 26 | `0x201ac53` |
| `hunter/baked/snowdrop/animation/p_dflt_m_st_quickdeploy_sbl_ar_ic_fast.anim` | 4 | `0x201ae0e` |
| `hunter/baked/snowdrop/animation/p_dflt_m_st_quickdeploy_sbl_ar_ic_fast_down.anim` | 4 | `0x201ae33` |
| `hunter/baked/snowdrop/animation/p_dflt_m_st_quickdeploy_sbl_ar_ic_fast_up.anim` | 4 | `0x201ae4f` |
| `hunter/baked/snowdrop/animation/p_dflt_m_st_quickdeploy_skm_ar_ic.anim` | 11 | `0x201ae77` |
| `hunter/baked/snowdrop/animation/p_hun_m_hcl_empstart_ar_i.anim` | 6 | `0x201b2e7` |
| `hunter/baked/snowdrop/animation/p_hun_m_hcl_empstart_pi_i.anim` | 6 | `0x201b305` |
| `hunter/baked/snowdrop/animation/p_hun_m_hcl_empstop_ar_i.anim` | 3 | `0x201b32c` |
| `hunter/baked/snowdrop/animation/p_hun_m_hcl_empstop_pi_i.anim` | 3 | `0x201b34a` |
| `hunter/baked/snowdrop/animation/p_hun_m_hcl_pulse_ar_i.anim` | 4 | `0x201b374` |
| `hunter/baked/snowdrop/animation/p_hun_m_hcl_pulse_pi_i.anim` | 4 | `0x201b392` |
| `hunter/baked/snowdrop/animation/p_hun_m_hcr_empstart_ar_i.anim` | 6 | `0x201b3cd` |
| `hunter/baked/snowdrop/animation/p_hun_m_hcr_empstart_pi_i.anim` | 6 | `0x201b3eb` |
| `hunter/baked/snowdrop/animation/p_hun_m_hcr_empstop_ar_i.anim` | 3 | `0x201b412` |
| `hunter/baked/snowdrop/animation/p_hun_m_hcr_empstop_pi_i.anim` | 3 | `0x201b430` |
| `hunter/baked/snowdrop/animation/p_hun_m_hcr_pulse_ar_i.anim` | 4 | `0x201b45a` |
| `hunter/baked/snowdrop/animation/p_hun_m_hcr_pulse_pi_i.anim` | 4 | `0x201b478` |
| `hunter/baked/snowdrop/animation/p_hun_m_lcl_empstart_ar_i.anim` | 6 | `0x201b4bb` |
| `hunter/baked/snowdrop/animation/p_hun_m_lcl_empstart_pi_i.anim` | 6 | `0x201b4d9` |
| `hunter/baked/snowdrop/animation/p_hun_m_lcl_empstop_ar_i.anim` | 3 | `0x201b500` |
| `hunter/baked/snowdrop/animation/p_hun_m_lcl_empstop_pi_i.anim` | 3 | `0x201b51e` |
| `hunter/baked/snowdrop/animation/p_hun_m_lcl_pulse_ar_i.anim` | 4 | `0x201b548` |
| `hunter/baked/snowdrop/animation/p_hun_m_lcl_pulse_pi_i.anim` | 4 | `0x201b566` |
| `hunter/baked/snowdrop/animation/p_hun_m_lcr_empstart_ar_i.anim` | 6 | `0x201b5a1` |
| `hunter/baked/snowdrop/animation/p_hun_m_lcr_empstart_pi_i.anim` | 6 | `0x201b5bf` |
| `hunter/baked/snowdrop/animation/p_hun_m_lcr_empstop_ar_i.anim` | 3 | `0x201b5e6` |
| `hunter/baked/snowdrop/animation/p_hun_m_lcr_empstop_pi_i.anim` | 3 | `0x201b604` |
| `hunter/baked/snowdrop/animation/p_hun_m_lcr_pulse_ar_i.anim` | 4 | `0x201b62e` |
| `hunter/baked/snowdrop/animation/p_hun_m_lcr_pulse_pi_i.anim` | 4 | `0x201b64c` |
| `hunter/baked/snowdrop/animation/p_hun_m_st_empstart_ar_i.anim` | 6 | `0x201b68e` |
| `hunter/baked/snowdrop/animation/p_hun_m_st_empstart_ar_left_i.anim` | 6 | `0x201b6ae` |
| `hunter/baked/snowdrop/animation/p_hun_m_st_empstart_pi_i.anim` | 6 | `0x201b6d2` |
| `hunter/baked/snowdrop/animation/p_hun_m_st_empstart_pi_left_i.anim` | 6 | `0x201b6f2` |
| `hunter/baked/snowdrop/animation/p_hun_m_st_empstop_ar_i.anim` | 3 | `0x201b71f` |
| `hunter/baked/snowdrop/animation/p_hun_m_st_empstop_ar_left_i.anim` | 3 | `0x201b73f` |
| `hunter/baked/snowdrop/animation/p_hun_m_st_empstop_pi_i.anim` | 3 | `0x201b763` |
| `hunter/baked/snowdrop/animation/p_hun_m_st_empstop_pi_left_i.anim` | 3 | `0x201b783` |
| `hunter/baked/snowdrop/animation/p_hun_m_st_pulse_ar_i.anim` | 4 | `0x201b7b3` |
| `hunter/baked/snowdrop/animation/p_hun_m_st_pulse_ar_left_i.anim` | 4 | `0x201b7d3` |
| `hunter/baked/snowdrop/animation/p_hun_m_st_pulse_pi_i.anim` | 4 | `0x201b7f7` |
| `hunter/baked/snowdrop/animation/p_hun_m_st_pulse_pi_left_i.anim` | 4 | `0x201b817` |
| `hunter/baked/snowdrop/animation/p_m_hccr_skill_smartcover_deploy_ar_i.anim` | 5 | `0x201b866` |
| `hunter/baked/snowdrop/animation/p_m_hcr_skill_smartcover_deploy_ar_i.anim` | 5 | `0x201b89f` |
| `hunter/baked/snowdrop/animation/p_m_lccr_skill_smartcover_deploy_ar_i.anim` | 5 | `0x201b8e1` |
| `hunter/baked/snowdrop/animation/p_m_lcr_skill_smartcover_deploy_ar_i.anim` | 5 | `0x201b91a` |
| `hunter/baked/snowdrop/animation/p_m_shd_drop_h60_run_alt.anim` | 4 | `0x201b959` |
| `hunter/baked/snowdrop/animation/p_m_shd_drop_h60_walk_slow.anim` | 2 | `0x201b97c` |
| `hunter/baked/snowdrop/animation/p_m_shd_lcl_to_vertnav.anim` | 17 | `0x201b9aa` |
| `hunter/baked/snowdrop/animation/p_m_shd_lcr_to_vertnav.anim` | 13 | `0x201b9d0` |
| `hunter/baked/snowdrop/animation/p_m_shd_plf_desc_h100_close_jog_l_ar.anim` | 2 | `0x201ba23` |
| `hunter/baked/snowdrop/animation/p_m_shd_plf_desc_h100_close_jog_r_ar.anim` | 2 | `0x201ba41` |
| `hunter/baked/snowdrop/animation/p_m_shd_plf_desc_h100_jog_b_ar.anim` | 4 | `0x201ba63` |
| `hunter/baked/snowdrop/animation/p_m_shd_plf_desc_h150_close_jog_b_ar.anim` | 4 | `0x201ba94` |
| `hunter/baked/snowdrop/animation/p_m_shd_plf_desc_h150_close_jog_l_ar.anim` | 2 | `0x201bab7` |
| `hunter/baked/snowdrop/animation/p_m_shd_plf_desc_h150_close_jog_r_ar.anim` | 2 | `0x201bad5` |
| `hunter/baked/snowdrop/animation/p_m_shd_plf_desc_h200_close_jog_b_ar.anim` | 2 | `0x201bb19` |
| `hunter/baked/snowdrop/animation/p_m_shd_plf_desc_h200_close_jog_b_ar_alt.anim` | 1 | `0x201bb37` |
| `hunter/baked/snowdrop/animation/p_m_shd_plf_desc_h200_close_jog_l_ar.anim` | 2 | `0x201bb5a` |
| `hunter/baked/snowdrop/animation/p_m_shd_plf_desc_h200_close_jog_r_ar.anim` | 2 | `0x201bb7d` |
| `hunter/baked/snowdrop/animation/p_m_shd_plf_desc_h200_close_jog_to_idle_b_ar.anim` | 2 | `0x201bba3` |
| `hunter/baked/snowdrop/animation/p_m_shd_plf_desc_h200_exit_jog_l_ar.anim` | 1 | `0x201bbd0` |
| `hunter/baked/snowdrop/animation/p_m_shd_plf_desc_h200_exit_jog_r_ar.anim` | 1 | `0x201bbee` |
| `hunter/baked/snowdrop/animation/p_m_shd_plf_desc_h250_close_jog_b_ar.anim` | 2 | `0x201bc24` |
| `hunter/baked/snowdrop/animation/p_m_shd_plf_desc_h250_close_jog_l_ar.anim` | 1 | `0x201bc42` |
| `hunter/baked/snowdrop/animation/p_m_shd_plf_desc_h250_close_jog_r_ar.anim` | 1 | `0x201bc65` |
| `hunter/baked/snowdrop/animation/p_m_shd_plf_desc_h250_close_jog_to_idle_b_ar.anim` | 3 | `0x201bc8b` |
| `hunter/baked/snowdrop/animation/p_m_shd_plf_desc_h300_close_jog_b_ar.anim` | 2 | `0x201bccd` |
| `hunter/baked/snowdrop/animation/p_m_shd_plf_desc_h300_close_jog_l_ar.anim` | 2 | `0x201bceb` |
| `hunter/baked/snowdrop/animation/p_m_shd_plf_desc_h300_close_jog_r_ar.anim` | 2 | `0x201bd0e` |
| `hunter/baked/snowdrop/animation/p_m_shd_plf_desc_h300_close_jog_to_idle_b_ar.anim` | 2 | `0x201bd34` |
| `hunter/baked/snowdrop/animation/p_m_shd_plf_desc_h60_close_jog_b_ar.anim` | 4 | `0x201bdb2` |
| `hunter/baked/snowdrop/animation/p_m_shd_plf_desc_h60_close_jog_l_ar.anim` | 2 | `0x201bdd5` |
| `hunter/baked/snowdrop/animation/p_m_shd_plf_desc_h60_close_jog_r_ar.anim` | 2 | `0x201bdf3` |
| `hunter/baked/snowdrop/animation/proto_p_shd_m_pathstand_doorall_kick_pi_o.anim` | 1 | `0x204fc6c` |
| `hunter/baked/snowdrop/animation/skeleton_female_player_hunter.anim` | 0 | `0x2053df1` |
| `hunter/baked/snowdrop/animation/skeleton_male_player_hunter.anim` | 0 | `0x2053f16` |
| `hunter/baked/snowdrop/animation/w_puppy_ven_notice_std_breaker_v07_petting_puppy_femaleplayer.anim` | 2 | `0x20672d4` |
| `hunter/baked/snowdrop/animation/w_puppy_ven_notice_std_breaker_v07_petting_puppy_maleplayer.anim` | 2 | `0x20672fe` |
