# Eye2Eye — 剪映专业版工程文件

本仓库是视频《Eye2Eye》的剪映专业版（macOS）剪辑工程，包含工程配置、时间线、字幕、特效等文件。

## 仓库内容

- **5 分钟投稿版重剪方案**：[`重剪_5min投稿版/剪辑方案.md`](重剪_5min投稿版/剪辑方案.md)（分镜表、新配音、字幕、图文卡片、样片）

- 工程配置：`draft_content.json`、`draft_info.json`、`draft_meta_info.json` 等
- 时间线：`Timelines/`
- 文字/字幕资源：`textReading/`
- 其他工程资源：`Resources/combination/`、`common_attachment/`、`subdraft/` 等

**不包含原始素材**（`Resources/local/` 下的视频、图片、音频，共 95 个文件约 16GB）。
由于 GitHub 单文件不得超过 100MB、仓库总大小受限，素材通过网盘分发。

## 如何打开工程

1. 下载本仓库全部文件。
2. 获取素材包（网盘链接见下方），将其中的 **全部 95 个文件**原样放入 `Resources/local/` 目录，**文件名必须保持不变**（剪映按文件名引用素材）。可对照 [`素材清单.md`](素材清单.md) 核对。
3. 将整个工程文件夹放入剪映草稿目录：
   ```
   ~/Movies/JianyingPro/User Data/Projects/com.lveditor.draft/
   ```
4. 打开剪映专业版，在草稿列表中找到该工程即可。

## 素材网盘链接

> 待补充（上传网盘后在此粘贴链接和提取码）

## 目录结构说明

```
├── Resources/
│   ├── local/        # 原始素材（需自行从网盘下载放入，见素材清单.md）
│   ├── combination/  # 组合素材
│   ├── digitalHuman/ # 数字人
│   ├── videoAlg/     # 视频算法输出
│   └── audioAlg/     # 音频算法输出
├── Timelines/        # 时间线
├── textReading/      # 文字/字幕资源
├── adjust_mask/      # 蒙版调整
├── matting/          # 抠像
├── qr_upload/        # 二维码上传
├── smart_crop/       # 智能裁剪
└── subdraft/         # 子草稿
```
