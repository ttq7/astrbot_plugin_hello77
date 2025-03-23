# AstrBot 游戏梗自动回复插件
# 简介
AstrBot 游戏梗自动回复插件是一款专为多平台即时通讯设计的趣味插件。它通过关键词匹配机制，对用户消息中提及的游戏名称或术语做出魔性回应，支持《明日方舟》《崩坏：星穹铁道》等 10+ 热门游戏。所有回复内容经过深度二次创作，融合游戏梗、网络热梗与夸张改编，旨在为群组互动增添欢乐氛围。
核心功能
1. 智能游戏识别
多游戏支持：涵盖主流 PC / 手机游戏（明日方舟、王者荣耀、崩坏：星穹铁道等）
精准关键词匹配：支持别名匹配（如「崩铁」对应崩坏：星穹铁道）
模糊语义识别：通过正则表达式匹配游戏相关表述
2. 魔性回复系统
随机语录库：每个游戏配置独立文本列表（平均 20+ 条 / 游戏）
图文混排：支持图片 URL 回复（需配置图片链接列表）
热梗融合：包含：
经典台词魔改（如「两面包夹芝士 → 两面包夹智齿」）
玩家行为复刻（如「D 牌 D 到脑血栓」）
跨次元联动（如「曼波一响爹妈白养」）
数值夸张化（如「还能再鲨七亿次」）
3. 扩展开发友好
模块化设计：独立游戏配置区方便扩展
参数化配置：支持添加新游戏配置
灵活适配：兼容 QQ / 微信等多平台
使用示例
python
# 当群内发送："崩坏：星穹铁道太好玩了！"
机器人回复：
"景元：神君启动！ 我：手机发烫关机！这伤害比火龙烧还猛！🔥🐉"
+ 随机游戏截图
# 关键词
- 崩坏：星穹铁道
  - 崩坏：星穹铁道
  - 星穹铁道
  - 崩铁
  - 崩坏星穹铁道
- 三国杀
  - 三国杀
  - 三国
  - 杀
- CS:GO
  - CSGO
  - 反恐精英
  - rush B
- 绝区零
  - 绝区零
  - ZZZ
  - 走格子
  - 新艾利都
  - 邦布
- 金铲铲之战
  - 金铲铲
  - 铲子
  - 云顶
- 英雄联盟
  - 英雄联盟
  - LOL
  - 撸啊撸
  - lol
- 曼波
  - 曼波
- 明日方舟
  - 明日方舟
  - 方舟
- 鸣潮
  - 鸣潮
- 王者荣耀
  - 王者荣耀
  - 王者
  - 农活
- 守望先锋
  - 守望先锋
  - OW
  - 屁股
- 瓦洛兰特
  - 瓦洛兰特
  - VALORANT
  - 无畏契约
  - 瓦
- 牢大梗
  - 牢大
  - 科比
  - 曼巴
  - 直升机
# 安装与配置
环境要求
Python 3.8+
AstrBot v3.4.34+
依赖库：requests, Pillow
部署步骤
bash
# 克隆插件
git clone https://github.com/yourname/astrbot_plugin_hello77
# 配置插件目录
cd AstrBot/data/plugins
ln -s /path/to/astrbot_plugin_hello77 .

自定义配置
python
# 修改游戏配置列表
mrfz_text_list.append("新添加的语录")
# 替换图片链接
xqtd_image_urls = ["https://new-image.url"]

# 扩展指南
新增游戏
创建新游戏配置：
python
new_game_text = ["新游戏梗1", "新游戏梗2"]
new_game_images = ["https://image1.url", "https://image2.url"]


添加关键词匹配：
python
elif "新游戏" in text or "NG" in text:
    yield event.make_result() \
        .message(random.choice(new_game_text)) \
        .url_image(random.choice(new_game_images))


# 高级功能
冷却机制：添加 SessionFilter 实现触发间隔控制
权限管理：通过 @permission_type 限制使用范围
LSTM 预测：结合大模型实现更智能的回复
版本说明
当前版本：1.2
更新日志：
新增 3 款游戏支持
优化图片加载稳定性
添加正则表达式匹配