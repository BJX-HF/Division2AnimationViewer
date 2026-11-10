# Kickback 的本地当前图核查

结论：用户指出的“后坐叠加”角色成立。当前 CoverKickback 一级分类混合了动画作用和姿态；可改为 RecoilAdditive（后坐叠加），再以 Standing / Cover 为姿态子类。

不能进一步说“所有 kickback 仅用于连发”：11 个掩体条目中，4 个 AR 进入 Burst 层，7 个 SG 进入 Fire 层。7 个 SG 虽然文件名带 burst_kickback，却在不循环的 Fire 层中使用。Burst / Fire 层在源图的 isLoopAsynch 分别为 true / false；compiled loop 也分别为 true / false。

## 可直接核对的连接

AR 掩体例：data2948（p_shd_m_lcr_burst_kickback_h90_ar_i）→ exec87 Animation → exec96 横向混合 → exec104 Position 选择 → exec112 垂直混合 → exec113 Extract → exec115 WeaponGroup 选择 → exec130 LengthScale → exec131 Cache → exec201 Additive.secondNode → 层 root。Additive148 也引用同一 secondNode131；其强度节点147含 WeaponRecoil。

SG 掩体例：data2971（p_shd_m_lcr_burst_kickback_h90_sg_i）→ exec89 Animation → exec97 横向混合 → exec105 Position 选择 → exec112 垂直混合 → exec113 Extract → exec129 Additive.secondNode → 层 root。强度节点128含 WeaponRecoil。

Position 的 LCR/LCCR/HCCR 等模式与源文件姿态前缀证明这 11 个片段具有掩体变体，但“掩体”不是 kickback 一词本身的定义。方向选择还使用 AimVector；左侧模式可复用右侧命名资源，不应仅按文件名宣称特定侧唯一使用。

## 站姿同类与分类建议

另有 4 个非掩体 kickback，均有路径进入 Additive.secondNode：ST_Burst_Kickback_PI、ST_Aim_Burst_Kickback_AR、ST_Aim_Burst_Kickback_MiniGun、ST_SingleShot_Kickback_SG。这些应与 Cover 的 11 个共用“后坐叠加”功能类别。

| 功能 / 姿态 | 数量 |
|---|---:|
| RecoilAdditive / Standing | 4 |
| RecoilAdditive / Cover | 11 |
| FiringCycles / SingleShot | 15 |
| FiringCycles / Burst | 8 |
| MountedRecoil | 2 |

这是对现有 40 个动态候选的角色整理建议；不把它解释为所有动画循环都是“非叠加”。普通 shot/burst 基础片段也可进入加法或减法链；此处 RecoilAdditive 特指本次 15 个名为 kickback 的额外后坐分量。

## 边界

本地证据证明的是当前游戏图如何使用这些片段，不证明 FBX 文件本身已经是可直接开启 UE Additive 的增量曲线。源图有 Extract、Pose、Subtractive 等基准与混合处理，UE 单独播放 FBX 不会自动重现这些运算。

WeaponRecoil 驱动 kickback 分量强度，足以支持“后坐叠加”这一用途；不足以定义全引擎中 recoil 与 kickback 永远同义，或把其他游戏的 GunKick/ViewKick 定义直接套到 Snowdrop。

## 逐项证据

| 资源名 | 实际层 | 姿态 | data ID | Additive exec |
|---|---|---|---:|---:|
| `p_shd_m_st_burst_kickback_pi_i_v01` | Burst | st | 2944 | 201 |
| `p_shd_m_st_aim_burst_kickback_ar_i_v01` | Burst | st | 2945 | 201 |
| `p_shd_m_st_aim_burst_kickback_minigun_i_v02` | Burst | st | 2946 | 201 |
| `p_shd_m_lcr_burst_kickback_h90_ar_i` | Burst | lcr | 2948 | 201 |
| `p_shd_m_lcr_burst_kickback_h-90_ar_i` | Burst | lcr | 2949 | 201 |
| `p_shd_m_lccr_burst_kickback_h90_ar_i` | Burst | lccr | 2951 | 201 |
| `p_shd_m_hccr_burst_kickback_h90_ar_i` | Burst | hccr | 2952 | 201 |
| `p_shd_m_st_singleshot_kickback_sg_i` | Fire | st | 2969 | 129 |
| `p_shd_m_lcr_burst_kickback_h0_sg_i` | Fire | lcr | 2970 | 129 |
| `p_shd_m_lcr_burst_kickback_h90_sg_i` | Fire | lcr | 2971 | 129 |
| `p_shd_m_lcr_burst_kickback_h-90_sg_i` | Fire | lcr | 2972 | 129 |
| `p_shd_m_lccr_burst_kickback_h0_sg_i` | Fire | lccr | 2973 | 129 |
| `p_shd_m_lccr_burst_kickback_h90_sg_i` | Fire | lccr | 2974 | 129 |
| `p_shd_m_hccr_burst_kickback_h0_sg_i` | Fire | hccr | 2975 | 129 |
| `p_shd_m_hccr_burst_kickback_h90_sg_i` | Fire | hccr | 2976 | 129 |
