# 当前 SHD 玩家开火调用：已验证事实

主证据为已解密的 `hun_animsys_player.manimsysbin`，对应 `hunter/animation/hun_animsys_player.manimsys`。BV2 解析准确消费全部 **11,020,219 字节**；容器版本 4，内部动画系统 schema 版本 **27**。不是先前 `rogue/Generic_Skeleton` 的 legacy 图。

机器可读主报告：`current_firing_graph.json`。控制表达树：`current_firing_controls.json`。两者只覆盖当前 Fire/Burst 及 mounted 同名层，不包含其他 400 余层。

## 主闭环

代码已证明 selected FireEvent 的虚函数 `+0x18` 读取其 `myAnimationLayer`，调用 `0x1421afbf0 → 0x14345c660 → 0x14345c690` 按名称解析并激活动画层。详见 `../开火调用验证.md` 和 `runtime_code_proof.json`。

当前图的实际分组：

| layerGroups 键 | 存储层 ID | layers 数组下标 | 名称 | serializedNodes | 直接引用的不同片段 |
|---|---:|---:|---|---:|---:|
| Burst | 44 | 43 | Burst | 221 | 17 |
| Fire | 45 | 44 | Fire | 166 | 23 |

这 **40 个当前 `p_shd_*` 片段**来自实际 group → layer → animation node → common animation data → resource 引用链，不是按文件名猜测归类。每个动画节点到该层 root 的依赖路径保存在 `compiled_links.clip_paths_to_root`。

具体武器在省略 `myAnimationLayer` 时如何物化 Fruit schema 默认值，尚未完成代码级验证。应以显式写出 `myAnimationLayer="Burst"` 的当前 Thompson_named 作为不依赖默认值的完整示例；其他省略字段的武器，把 schema-derived 预期与实际显式配置分开表述。

## 三类索引不可混用

1. `layerGroups.layers`、`commonObjects.animDatas` 的 `data` ID、`serializedNodes` 的 ID 均是一基，0 表示空引用；访问数组需减 1。
2. 节点 `state` 中的 `basicNode`、`secondNode`、`selectionNode`、`valueNode*`、`nodes` 等，是 **零基 `evalNodesInOrder` 执行序号**。
3. 因此先取 `evalNodesInOrder[execution_index]` 得到 serialized ID，再取 `serializedNodes[id-1]`。不能直接把 selectionNode 当 serializedNodes 下标。

公共动画数据 ID 的一基行为由 serializer `0x1434d0c10 → 0x1434ed210` 证明：辅助函数把新条目存入数组下标 i，返回并记录 i+1，空指针返回 0。精确反汇编在 `baked_reference_index_proof.json`。

## 当前输入变量与主要条件

实际 `variablesByName` 映射：

| 变量 | 编码 ID |
|---|---|
| WeaponGroup | `0x20000000` |
| WeaponFireRate | `0x20000002` |
| WeaponRecoil | `0x30000010` |
| IsFiring | `0x10000000` |

代码侧已证明这些类型化参数从武器状态写入动画实例。`myAnimationWeaponGroup` 为 -1 时回退到 `myWeaponGroup`，所以武器实际动画族可以覆盖其武器类别。

Burst 的主要可核对条件：

- 执行序号 11 读取 WeaponGroup，13 比较它是否为 **4 (Shotgun)**，15/16 生成并缓存选择值。执行序号 20 的分支 0 是 600RPM AR、分支 1 是 300RPM SG。
- 执行序号 29/35 是三点垂直混合，阈值 `[-1,0,1]`；输入来自 AimVector 的分量 1，引用 V-90 / V0 / V90 资源。
- 执行序号 104 按 Position 切换：Stand/Kneel/Down/Stairs → 81；LCR/LCL → 96；LCCR/LCCL → 101；HCR/HCCR/HCL/HCCL → 103。这些分支包含对应的掩体 kickback 或瞄准混合；Aim 模式和 AimVector 的水平分量继续参与选择。
- 执行序号 115 按 WeaponGroup 的已存选择数组 `[50,113,113,113,113,113]` 区分 Pistol 与其余有效索引的路径。另有 SignatureWeapon 子类型、ShieldType、IsFiring 分支。

Fire 的执行序号 6/10/14 是直接 WeaponGroup Switch。其存储数组索引 0 (Pistol) 选择 PI、索引 4 (Shotgun) 选择 SG、数组内其他有效索引选择 MR 的上/中/下三组资源。后续仍有 Position、Aim、ShieldType、WeaponClipAmmo 等条件。**未独立核实越过某个选择数组长度的索引处理方式，不把这一数组的“其他有效索引”扩大成所有武器枚举值。**

## 射速与叠加强度

以下是图内传入节点的表达式，不是独立播放 FBX 时会自动重现的效果：

- Burst 执行序号 **156** 的 LengthScale 因子为 `baseRPM / float(WeaponFireRate)`。其 WeaponGroup MultiSelect 数组为 `[600,600,600,600,300]`，因此常规对应分支以 600 为基准，Shotgun 对应分支以 300 为基准。
- 另一路 LengthScale 执行序号 **189** 的因子为 `1100 / (WeaponFireRate * groupFactor)`，其中组选择数组 `[1,1,1,1,2,1]` 使 Shotgun 对应项乘 2。这是另一个图内分支，不应当成全部武器的统一公式。
- Burst 执行序号 **148** 的 Additive 强度表达树包含 `WeaponRecoil * 0.2 * groupFactor`；对应普通组数组为 Pistol=1、AssaultRifle 各子型=2、SubMachinegun=1、LightMachinegun=4、Shotgun=4、SniperRifle=1。Position 模式继续调整，SignatureWeapon 的部分子类型直接选择另一强度，不能把简化式用于所有分支。
- Fire 执行序号 **129** 的 Additive 强度有 WeaponRecoil clamp、Pistol 子型号系数、WeaponGroup 系数和 Speed 模式系数，最后 clamp 到 `[0.1,1.5]`。完整表达树已保留；没有从这些值推导为 UE 内独立片段播放强度。

## 男女及 mounted 补充

主图同时列出 male、female 两个 skeletonAssets，且有 Gender 组的 Male/Female 子组。这 40 个开火数据条目的 `animGroupIndex` 均为 **0 (Default)**，主开火节点中没有 Gender 组选择。资源虽然命名为 `p_shd_m_*`，其当前图内引用属于共享 Default 数据，不能据此标成男性专用。

另有 layer ID **232**（数组下标 231）也名叫 Burst，只有 15 个节点，引用 `p_shd_m_mounted_weapon_recoil_impact.anim` 和 `p_shd_m_mounted_weapon_recoil_halfstrength.anim`。它不在主 `layerGroups["Burst"]=[44]` 中，图内也没有 IsFiring 变量读取。可确认是独立 mounted recoil 分支；其外部启动机制没有在本次分析中证明，不把它并入普通武器布尔触发链。

## 实际限制

本次是离线代码与实际资产引用分析，没有启动游戏或录制运行时命中。已证明资源怎样被当前图引用和控制；未穷举所有武器 override、所有跨界索引、所有组合条件的实际帧级效果。原始 FBX 未重导出或修改。旧 `rogue/p_dflt_*` 报告只保留为格式研究与对照，不作为当前 SHD 调用结论。
