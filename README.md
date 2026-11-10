# 全境封锁 2 动画库

**Kickback 分类更正：** 后坐叠加作为动画作用单列，共 15 个（站姿 4、掩体 11）；其中掩体 AR 4 个在 Burst 层，掩体 SG 7 个在 Fire 层。掩体是姿态维度，kickback 不等于连发专用。详见 [Kickback定义与分类更正](Kickback定义与分类更正.md)。查找表的功能分组与现有 UE 物理目录分别说明。

**完整性范围更正：** 此处“现有 FBX 覆盖”仅指已核对的开火图层资源。整套玩家动画库并非全量齐全；主图另有 130 个原始资源没有同名 FBX，见 [FBX完整性核查](FBX完整性核查.md)。

游戏调用验证已完成，详见 [开火调用验证.md](开火调用验证.md) 与 [可搜索调用表](开火调用验证.html)。40 个动态动作和 2 个姿势采样均属于当前玩家图的 Default 共用组；现有 Male 目录按源文件 `_m_` 命名保留，不代表游戏男性专用。

使用 Unreal Engine 5.8 打开同目录的 **D2AnimViewer.uproject**。原环境使用 UE **5.8.2**。

项目：`E:\UEproject\Division2AnimationViewer\D2AnimViewer.uproject`

## 从 GitHub 获取项目

需要 Git、Git LFS 和与项目关联的 Unreal Engine 5.8。克隆前启用 Git LFS，以下载完整的 UE 资源：

```powershell
git lfs install
git clone https://github.com/BJX-HF/Division2AnimationViewer.git
cd Division2AnimationViewer
git lfs pull
```

克隆完成后，直接用 Unreal Engine 打开 `D2AnimViewer.uproject`。首次打开会重新生成本机缓存。仓库中的 UE 资产和压缩包由 Git LFS 管理；使用 Git 克隆可以获取这些文件的完整内容。

原环境的快捷方式、缓存和临时文件不随仓库分发。`Scripts` 中用于重新导入的脚本保留了原始数据路径，重新导入前需按本机目录调整；浏览已导入动画不需要运行这些脚本。

## 看动画

1. 在内容浏览器进入 `Content / Division2 / Animations`。
2. 选择 `Male`（男）、`Female`（女）或 `Shared`（通用），再选择动画类别。
3. 双击任意动画，可直接在绑定的角色上播放；拖动时间轴可以逐帧查看。动画编辑器右下角的资产浏览器可以切换同骨架动画。
4. 默认地图 `Content / Division2 / Preview / AnimationPreview` 放置了男女角色。点击编辑器的“播放”可看循环动画。

同目录的 **动画分类查找表.html** 可离线搜索全部动画，按中文性别、类别和姿态筛选，并复制 UE 资产路径。

## 文件夹

- `Animations / Male`：男动画 3,827 个。
- `Animations / Female`：女动画 397 个。
- `Animations / Shared`：通用动画 143 个，源文件使用男性骨架。
- `Characters / Male`、`Characters / Female`：角色模型和独立骨架。
- `Preview / SourceExamples / FullCharacter`、`BodyOnly`：源目录中两个预览 FBX，各自保留模型和动画。

开火相关分类已按文件名和 FBX 动画曲线重新筛选，分类查找表已同步更新。UE 文件夹使用对应英文名称，例如 `Reload` 换弹、`Locomotion` 移动、`Emotes` 表情、`Idle` 待机、`VaultAndClimb` 翻越攀爬。完整中英文对应关系见查找表。

## 重新筛选的开火动画

按下方资源目录进入 `Fire` 文件夹，可打开步枪连射等开火动画样本。

`Content / Division2 / Animations / Male / Fire` 中保留 40 个动态源动画。真实物理目录仍为 `SingleShot` 16、`Burst` 11、`CoverKickback` 11、`MountedRecoil` 2；查找表的功能角色已改为单发片段 15、射击循环片段 8、后坐叠加 15、固定武器后坐 2。物理目录名与图内作用分别显示。

`FiringSupport / StaticPoses` 中的 `p_shd_m_st_aim_firing_ar_i` 为静态姿势；方向混合源与过渡放在 `FiringSupport / BlindFire`。11 个信号枪动作序列已由 `FlareGun` 层与事件确认，真实目录仍保留男女各自的 `FiringSupport / FlaregunReview`，与上面 40 个普通枪械 / 固定武器后坐分别计数。

详见同目录 **开火动画重新筛选.html** 和 **开火动画清单.md**。

原始名字中的 `+` 转为 `_plus_`，`-` 转为 `_minus_`，以保留正负方向并避免 UE 重名。原始文件名和分类也保存在资产元数据中。

模型保持源 FBX 的灰模外观。原始 FBX、HTML 和压缩包均保留在原位置。

项目内 `ImportReport / validation.json` 和 `validated_animations.json` 保存逐项验证记录；`Scripts` 中保留导入与预览脚本。


## 当前玩家图用途核查

全部 4,367 条动画在 [动画分类查找表](动画分类查找表.html) 中增加了源曲线状态、图内多用途角色和实际 scope 链接，可用“图内用途”筛选。角色可并存，不表示动画实际同时播放；85 个文件尚未观察到本主图节点使用，不因此判为无用。

详见 [全图用途审计说明](全图用途审计说明.md) 和 [玩家动画图完整审计](玩家动画图完整审计.html)。信号枪 11 个已由 FlareGun 层与事件序列确认：FireFlareGun 0.45、FlareGunEnd 0.89 是规范化周期相位，不是秒；与普通枪械 / 固定武器后坐 40 个单独计数。所有真实资产路径保持不变。
