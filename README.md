# bilibili Video Downloader
a open-source bilibili video download project

[![Build Status](https://travis-ci.org/SCUTJcfeng/bilibili-video-downloader.svg?branch=master)](https://travis-ci.org/SCUTJcfeng/bilibili-video-downloader)

## 说明
支持最高1080p60的清晰度，支持按 `Up` 下载和按 `av` 号下载， 支持 ffmpeg 自动合并视频

## 例子
要下载凉风所有阅片无数的视频
```python
# up id，比如凉风 14110780
UP_ID = 14110780

# 关键词，如 KEYWORD = '阅片无数' 查看所有带有阅片无数标题的视频
KEYWORD = '阅片无数'

# 视频顺序，关联 up id 和 keyword，默认 pubdate，可选 最新发布 pubdate 和 最多播放 click、最多收藏 stow
ORDER = 'pubdate'
```

## requirement
1. Python >= 3.6, ffmpeg(可选)
2. `pip install pipenv` 安装 `pipenv`

## 配置
1. 复制 `config.py` 为 `config_local.py`，在 `config_local.py`中修改配置
2. 大会员选项：`SESSION_DATA` 在登录状态下的网页 cookies 字段中获取（F12-Application），如图所示
![session-data.PNG](./img/session-data.png)
3. 默认自动合并视频，可自定义 `ffmpeg` 路径

## 运行
1. `pipenv install`
2. `pipenv run python run.py`

## 输出
![bar.jpg](./img/bar.jpg)

## 补充说明

暂无

### 清晰度
1. 所有下载的视频文件的文件名都有清晰度的说明如下：

| 清晰度 | 视频规格   |
|--------|:-----------|
| 116    | 1080p60    |
| 112    | 1080+      |
| 80     | 1080p      |
| 74     | 720p60     |
| 64     | 720p       |
| 48     | 720P (MP4) |
| 32     | 480p       |
| 16     | 360p       |

2. 另外 mp4 、mp3格式(如av60005360)对应 m4s，特点是音视频分离，可使用 `FFmpeg` 或其它视频编辑工具合并

### 音视频合并
脚本如下
```shell script
ffmpeg -i 视频.mp4 -i 音频.mp3 合并视频.mp4
```
