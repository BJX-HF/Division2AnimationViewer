# Kickback 定义与分类更正

这批资源更准确的功能分类是 **Kickback／额外后坐叠加分量**；Standing（站姿）与 Cover（掩体）是另一个姿态维度。

之前的 `CoverKickback` 对 11 个资源的掩体姿态判断有依据，但把它与 SingleShot、Burst 并列而没有交代叠加用途，混用了不同分类维度。它们不能被理解为 11 条可直接替代基础瞄准／射击姿势的完整掩体射击动作。

## 外部术语核对

在枪械动画语境中，kickback 常指射击产生的后冲、抬起及人物承受后坐的反应。它本身不规定必须全自动、必须在掩体内，也不能单靠词义证明采用 Additive 节点。

一个可直接读取的开发者一手例子是 [GROUND BRANCH 的 Intel Report #015（2023-06-01）](https://www.groundbranch.com/2023/06/intel-report-015-first-v1034-previews/)。其“Kicking up the kickback”一节把枪械向后、向上运动与头部、上身的次级后坐动画放在一起讨论。这是其他开发者的术语用法，不能代替《全境封锁 2》的本地图证据。

你给的 [Denkirson 帖子](https://denkirson.proboards.com/thread/5906) 已尝试直接访问、搜索与归档定位。当前站点返回 HTTP 202 的访问校验页，未获取正文；因此本报告不转述或声称已验证该帖的具体定义，也没有将其他游戏的 GunKick/ViewKick 规则套给 Snowdrop。

## 当前《全境封锁 2》图的直接证据

本次重新读取当前玩家 compiled 图与 recoil 源图。**15 个命名为 kickback 的片段，全部有进入 Additive 的 `secondNode` 附加输入链的实际路径，强度控制包含 `WeaponRecoil`。**

| 姿态 | 数量 | 实际层 | 结论 |
|---|---:|---|---|
| 掩体 AR | 4 | Burst | 循环层中的后坐叠加分量 |
| 掩体 SG | 7 | Fire | 非循环层中的后坐叠加分量 |
| 站姿 PI / AR / MiniGun | 3 | Burst | 站姿后坐叠加分量 |
| 站姿 SG | 1 | Fire | 单发后坐叠加分量 |

因此，“后坐叠加”的判断成立；**“全部都是连发专用”不成立**。尤其 7 个掩体 SG 文件虽然也叫 `burst_kickback`，实际却进入不循环的 Fire 层。源文件名中的 `burst` 不能替代图层连接证据。

两个可以逐项核对的例子：

```text
AR：data2948 p_shd_m_lcr_burst_kickback_h90_ar_i
 → Animation exec87 → 横向混合 exec96 → Position exec104
 → 垂直混合 exec112 → Extract exec113 → WeaponGroup exec115
 → LengthScale exec130 → Cache exec131
 → Additive exec148 / exec201 的 secondNode → 图层结果

SG：data2971 p_shd_m_lcr_burst_kickback_h90_sg_i
 → Animation exec89 → 横向混合 exec97 → Position exec105
 → 垂直混合 exec112 → Extract exec113
 → Additive exec129 的 secondNode → 图层结果
```

`LCR/LCCR/HCCR` 等姿态前缀与 Position 分支证明 Cover 变体性质；AimVector 参与方向混合，部分左侧模式复用右侧命名资源。不能仅按文件名判定某条只给一个侧面使用。

## 修正后的浏览分类

| 动画作用 | 姿态 | 数量 |
|---|---|---:|
| 单发片段 | 依各片段 | 15 |
| 射击循环片段 | 依各片段 | 8 |
| Kickback／额外后坐叠加分量 | Standing | 4 |
| Kickback／额外后坐叠加分量 | Cover | 11 |
| 固定武器后坐 | Mounted | 2 |
| 合计 | | 40 |

此处 Kickback 分组指这 15 个额外后坐分量的作用。普通单发／循环片段本身也可能进入加法、减法或基础姿势运算，不能把它们称为“绝不叠加”。查找表按功能、姿态和实际触发层分别显示，UE 路径指向现有资产。

## UE 中的含义

“游戏图内作为叠加分量使用”与“现有 FBX 已经存成 UE 可直接使用的增量动画”是两件需要分别验证的事。原游戏图里有 Extract、Pose、Subtractive 等基准消除和混合步骤。

[UE 5.8 的 Animation Sequence Editor 文档](https://dev.epicgames.com/documentation/en-us/unreal-engine/animation-sequence-editor-in-unreal-engine)说明，Additive 的 delta 要相对某个 Base Pose 求出；使用哪个基准会改变结果。仅因为文件名含 kickback 就打开 UE Additive 选项，不能保证复现原游戏。

## 15 个片段

| 源文件名 | 实际层 | 姿态 | animData ID |
|---|---|---|---:|
| `p_shd_m_st_burst_kickback_pi_i_v01` | Burst | st | 2944 |
| `p_shd_m_st_aim_burst_kickback_ar_i_v01` | Burst | st | 2945 |
| `p_shd_m_st_aim_burst_kickback_minigun_i_v02` | Burst | st | 2946 |
| `p_shd_m_lcr_burst_kickback_h90_ar_i` | Burst | lcr | 2948 |
| `p_shd_m_lcr_burst_kickback_h-90_ar_i` | Burst | lcr | 2949 |
| `p_shd_m_lccr_burst_kickback_h90_ar_i` | Burst | lccr | 2951 |
| `p_shd_m_hccr_burst_kickback_h90_ar_i` | Burst | hccr | 2952 |
| `p_shd_m_st_singleshot_kickback_sg_i` | Fire | st | 2969 |
| `p_shd_m_lcr_burst_kickback_h0_sg_i` | Fire | lcr | 2970 |
| `p_shd_m_lcr_burst_kickback_h90_sg_i` | Fire | lcr | 2971 |
| `p_shd_m_lcr_burst_kickback_h-90_sg_i` | Fire | lcr | 2972 |
| `p_shd_m_lccr_burst_kickback_h0_sg_i` | Fire | lccr | 2973 |
| `p_shd_m_lccr_burst_kickback_h90_sg_i` | Fire | lccr | 2974 |
| `p_shd_m_hccr_burst_kickback_h0_sg_i` | Fire | hccr | 2975 |
| `p_shd_m_hccr_burst_kickback_h90_sg_i` | Fire | hccr | 2976 |

[逐节点连接与强度表达式](开火调用证据/kickback_graph_audit.json) · [本地图核查说明](开火调用证据/kickback_graph_audit.md) · [修正后的查找表](开火动画重新筛选.html)
