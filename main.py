import logging
import random
import requests  # 导入requests库
from astrbot.api.star import Context, Star, register
from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.event.filter import event_message_type, EventMessageType
from astrbot.api.message_components import *

logger = logging.getLogger(__name__)

mrfz_text_list = [
    "怎样的女人才不会对着这样一个立绘发情呢？他是在向我的心开枪！把盾拍在我的脸上吧！",
    "两面包夹芝士",
    "为斯卡蒂献上心脏",
    "海猫？Ocean Cat！法老！安哲拉！埃及远征军！",
    "好玩爱玩",
    "都给我玩明日方舟",
    "“我从08年就开始等这个池子！我们太弱小了……没有力量！”“OBS启动！军费启动！rua牛（关卡设计师）好好劝劝海猫（制作人）！”",
    "搓玉了",
     "两面包夹芝士？不！是两面包夹智齿！这阵容疼得我脑仁嗡嗡响！(꒪Д꒪)ノ",
    "博士の奇妙理财：搓玉比搓麻将还上头！龙门币？那是什么新型诈骗道具？💸",
    "你这理智怕不是被源石虫啃过！凌晨四点剿灭？建议改名叫《罗德岛007》！🐛",
    "海猫：这是新机制 玩家：这是新BUG 实际：这是新の提款密码！🏧",
    "危机合约？不！是《危机贷合约》！打完十八层，钱包少八层！📉",
    "森rua：我变大了 也变秃了 这精二立绘怕不是植发广告！🌳💇♂️",
    "黄铁峡谷？黄铁板烧！这热浪让我的手机都开始煎鸡蛋了！🍳🔥",
    "明日方舟教会我：活着才有输出！毕竟——医疗干员都去当近卫了！💊🗡️",
    "当所有干员都精二后：欢迎来到《罗德岛女子搏击俱乐部》！👊💃",
    "抽卡十连三金光！打开一看：重装 重装 还是重装！建议改名叫《明日方柜》！📦"
]
mrfz_image_urls = [
    "https://img1.baidu.com/it/u=705036194,567196508&fm=253&fmt=auto&app=138&f=JPEG?w=610&h=551",
    "http://img2.baidu.com/it/u=2863336826,3820234834&fm=253&app=138&f=JPEG?w=676&h=380",
    "http://img2.baidu.com/it/u=1746848125,2787771719&fm=253&app=138&f=JPEG?w=466&h=380",
    "http://img0.baidu.com/it/u=1330527880,171337583&fm=253&app=138&f=JPEG?w=621&h=655",
    "http://img0.baidu.com/it/u=885981821,1262532229&fm=253&app=138&f=JPEG?w=712&h=731",
    "http://img0.baidu.com/it/u=3559474649,218070041&fm=253&app=138&f=JPEG?w=625&h=511"
]

xqtd_text_list = [
    "明天见",
    "没有医生在的话，真的不行呢",
    "歪了！歪了！",
    "豆子危机，启动！",
    "听声辨位",
    "下次我还敢！",
    "凹景元一小时，深渊结算两分钟",
    "崩坏：星穹铁道好玩",
    "我是真的服了",
    "我是卡芙卡的狗",
    "希尔还能玩吗？",
    "景元：神君启动！ 我：手机发烫关机！这伤害比火龙烧还猛！🔥🐉",
    "模拟宇宙？不！是《模拟血压》！这骰子roll得比我人生还混沌！🎲💢",
    "开拓者の日常：翻垃圾桶比打BOSS还积极！建议改名《星穹拾荒者》！🗑️👑",
    "银狼：代码雨 我：钱包雨 这氪金速度比黑洞吞噬还快！🕳️💸",
    "忘却之庭？不忘却充值记录！这记忆比甲方需求还难满足！🧠📝",
    "自动战斗开启：停云给魔阴身加buff 这AI怕不是内鬼培训的！🤖👻",
    "抽卡保底歪出光锥：原来我才是那个「存护」命途的倒霉蛋！🛡️💔",
    "星穹铁道教会我：活着不如凹暴击！毕竟——量子套永远差最后一件！🎭",
    "当所有角色都80级：恭喜解锁《星穹帕鲁》模拟经营模式！👾🏭",
    "阮梅の料理教室：把BOSS炖成汤 加点星琼更美味哦！🍲✨"
]
xqtd_image_urls = [
    "https://pic1.zhimg.com/v2-00f089a772dedad2a78e2c0f90d1bc9e_r.jpg?source=2c26e567",
    "https://picx.zhimg.com/v2-40c6c8b343c49f1c318d47a06bd8a780_r.jpg?source=2c26e567",
    "https://picx.zhimg.com/v2-0168963add1db08819dca7a8f4d68761_r.jpg?source=2c26e567",
    "https://picx.zhimg.com/v2-c4179f9e2612778369ccb7e2cf75aec9_r.jpg?source=2c26e567",
    "https://picx.zhimg.com/v2-ada7069cbdb311ec8de073961b1a9c99_r.jpg?source=2c26e567",
    "https://pic1.zhimg.com/v2-63db63d65ac9bcb49a6908d9d2d53d6a_r.jpg?source=2c26e567"
]

wz_text_list = [
    "曾经有一段真挚的爱情放在我的面前，我没有珍惜，要是能重来……我要选李白",
    "处什么对象，是烟不好抽，酒不好喝，还是王者荣耀不好玩！",
    "我发现现在小学生玩王者农药都不坑，讲真小学生挺6的。真真坑的是那些女！大！学！生！",
    "高考成绩的好坏，决定你在哪个城市打王者荣耀。",
    "你这个样子，不要打荣耀了，去玩超级玛丽或者小蜜蜂吧，总有一款适合你",
    "开，开将大局逆转吧！",
    "投了投了！这队友是人我直接吃！",
    "守家？守个屁！全员换奔狼，跟我蹲草！对面拿龙必飘，这波打的就是出其不意！赢了会所嫩模，输了下海干活——冲！",
    "王者荣耀的匹配机制是真的好！",
    "王者荣耀是最公平的游戏",
    "我要干农活",
    "王者荣耀真是太好玩了",
    "你赤过石吗",
    "守家？守个der！全员换奔狼纹章，这波啊，这波是《极速送头》！🐺💀",
    "打野の经济学：蹭线比补刀勤 战绩比钱包净 建议改名《峡谷慈善家》！🤑",
    "防御塔：你们不要再打啦！ 玩家：不打架难道来峡谷野餐？🧺👊",
    "逆风局现状：水晶爆炸的速度比我卸载游戏还快！💥📱",
    "瑶瑶公主骑脸输出：请叫我《野区女王》！这打野怕是美团骑手！🛵👑",
    "王者荣耀教会我：活着不如换装！毕竟——复活甲秒换名刀才是真の秀！🗡️⏱️",
    "0-10的韩信：我在偷塔 队友：你在偷渡！这运营堪比缅北诈骗！🚤💼",
    "风暴龙王降临：全体得电子哮喘 这减速比甲方改需求还致命！🌪️😷",
    "当对面拿出瑶马组合：欢迎来到《峡谷动物园》骑马体验区！🐎🧚♀️",
    "举报理由：打野在野区采灵芝 中单在河道钓锦鲤 上单...上单在峡谷买房了！🏡"
]
wz_image_urls = [
    "https://img2.baidu.com/it/u=1529773297,3750447212&fm=253&fmt=auto&app=138&f=JPEG?w=810&h=800",
    "https://wx4.sinaimg.cn/mw1024/0069plBngy1hpbjllz76jj30tz13747c.jpg",
    "https://img1.baidu.com/it/u=3524209761,4048927143&fm=253&fmt=auto&app=138&f=JPEG?w=800&h=1017",
    "https://i2.hdslb.com/bfs/archive/e001a7f95b961f028c55c870361a1f65bb7b8052.jpg",
    "https://5b0988e595225.cdn.sohucs.com/images/20190410/dc5c5e804dd74915940dbc1acbbcbc95.jpeg",
    "https://i2.hdslb.com/bfs/archive/0c91402310dc46379541be93230fe017a1139418.jpg"
]

mc_text_list = [
    "嘿哟哟，骑上我的小摩托，不是去救火，就是在去救火的路上，电动车你可别上楼，不然见太奶咯！",
    "我只是个路过的，我能有什么坏心思，我就是想抢个首杀而已啦！",
    "你怎么还在？我都以为你被声骸吞了，结果还在这晃悠！",
    "什么？你说这BOSS血厚？那我就陪它玩个马拉松，看看是它先跑不动，还是我先累晕！",
    "扫码扫码，声骸在哪？别给我整什么消防知识，我要的是强力角色啊！",
    "哟呵，这《天鹅湖》一响，我这手怎么就开始不受控制地乱按技能啦！",
    "技术宅拯救世界？不，是技术宅掏空你的钱包，哈哈哈哈！",
    "说好的公平竞技，你这皮肤价格比火箭还能上天，我氪的不是金，是我的血泪啊！",
    "麻辣仙人在哪？我要代表正义消灭你，还我老婆的清白！",
    "限时击杀会跑的血牛怪？这是让我玩《宠物小精灵》追怪吗，我都快成长跑运动员啦！",
    "骷髅兄弟跳起来，《曾经的你》响起来，这是《鸣潮传奇》要起飞咯！",
    "我共鸣，我变身，我就是这末日世界最靓的仔，管它异象不异象，统统都得给我让路！",
    "声骸啊声骸，你到底是我的助力，还是让我沉迷游戏的大魔王！",
    "鸣潮好玩爱玩",
     "声骸刷到肝硬化，这爆率让非酋想报警！建议改名《鸣潮：牢房模拟器》！🚔",
    "跑图十分钟打架一分钟，这体力条比打工人下班还虚！💼😵",
    "当吟霖开始放电：手机变成暖手宝 这技能特效比火龙果还烫手！🔥📱",
    "BOSS战现状：刮痧刮出火星子 建议声骸改行开美容院！💆♂️✨",
    "鸣潮教会我：活着不如氪金！毕竟——648能买来尊严！👑💳",
    "剧情跳过党：什么今州反抗军 我只关心老婆的衣柜！👗👀",
    "声骸系统揭秘：把BOSS当宝可梦养 但球比大师球还难搓！🎾👾",
    "当全角色满级后：欢迎来到《鸣潮：帕鲁世界》打工模拟DLC！👷♂️🏗️",
    "卡卡罗大招动画：这时间够我泡碗面！建议改名《鸣潮：料理时间》！🍜⏳",
    "抽卡保底出男人：原来我才是《鸣潮0》的主角！💔♂️"
]
mc_image_urls = [
    "https://img1.baidu.com/it/u=2971289168,2461448899&fm=253&fmt=auto&app=138&f=JPEG?w=800&h=800",
    "http://img1.baidu.com/it/u=1826228154,743619834&fm=253&app=138&f=JPEG?w=481&h=354",
    "http://img0.baidu.com/it/u=1308939930,3970720865&fm=253&app=138&f=JPEG?w=466&h=548",
    "http://img1.baidu.com/it/u=2737899287,1248146196&fm=253&app=138&f=JPEG?w=888&h=800",
    "http://img0.baidu.com/it/u=521499124,2828612172&fm=253&app=138&f=JPEG?w=475&h=1189",
    "http://img2.baidu.com/it/u=2585895599,3834207399&fm=253&app=138&f=JPEG?w=608&h=434",
    "http://img1.baidu.com/it/u=4031892566,4169730401&fm=253&app=138&f=JPEG?w=800&h=800"

]

sgs_text_list = [
    "你那点血条，我还能再鲨七亿次！(ಡωಡ) 杀完直接解锁闪电五连鞭成就！",  # 数字夸张化+马老师梗
    "内奸竟是我寄几！(꒪⌓꒪) 这波啊，这波是《无间道》之我在三国杀当二五仔！蚌埠住了！",  # 自嘲+方言+电影梗
    "鲨你就像切螺蛳粉，连酸笋都不带藏的！没闪？没闪就对了！(ಡωಡ)ﾉ⌒*",  # 食物谐音+挑衅动作
    "这牌堆怕不是被诸葛村夫偷去嗦螺蛳粉啦！东风？东百的疯都借不来！",  # 方言+无厘头场景
    "反贼不跳，忠犬难找，主公泪两行——这主公比依萍找她爸要钱那天淋的雨还大！🌧️",  # 琼瑶剧热梗乱入
    "诸葛连弩在手，AK一装，原地变身加特林菩萨！南无阿弥陀佛，施主吃我亿发慈悲杀！",  # 宗教元素+火力反差
    "决斗？我连无懈都不带藏的！直接掏出意大利……面！诶嘿没想到吧？( ͡° ͜ʖ ͡°)",  # 经典意大利用法
    "桃呢桃呢桃呢？我血条比甲方需求还脆！再没桃我可要开摆唱《求佛》了！🙏",  # 打工人共鸣+土味BGM
    "主公驾崩，反贼集体跳科目三，这局直接变海底捞团建！🕺💃",  # 魔性舞蹈入侵
    "三国杀教会我：活着才有输出！毕竟——队友可以菜，你不能挂机啊！(T＿T)",  # 摆烂文学升华
    "蒸蒸日上",
    "三国杀好玩爱玩"
]
sgs_image_urls = [
    "https://img0.baidu.com/it/u=852162588,715688491&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=701",
    "https://img0.baidu.com/it/u=1552063275,2172391481&fm=253&fmt=auto&app=138&f=JPEG?w=800&h=800",
    "http://img1.baidu.com/it/u=985544422,3410762132&fm=253&app=138&f=JPEG?w=800&h=800",
    "http://img2.baidu.com/it/u=3705721137,777759174&fm=253&app=138&f=JPEG?w=973&h=758",
    "http://img2.baidu.com/it/u=2016714510,2189130515&fm=253&app=138&f=JPEG?w=600&h=573",
    "http://img2.baidu.com/it/u=101862930,1655977021&fm=253&app=138&f=JPEG?w=853&h=800",
    "https://img0.baidu.com/it/u=584229310,443669393&fm=253&fmt=auto&app=138&f=JPEG?w=731&h=887",
    "http://img1.baidu.com/it/u=34634762,783848757&fm=253&app=138&f=JPEG?w=800&h=934",
    "http://img0.baidu.com/it/u=968141918,2550905422&fm=253&app=138&f=JPEG?w=819&h=800"

]

lol_text_list = [
    "大龙毁一生，小龙穷三代！这波啊，这波是《打野の经济学》！(꒪Д꒪)ノ",
    "ADC在送了！这操作比美团还能送！建议改ID：峡谷饿了吗骑手！🛵",
    "打野差距！15投！对面打野是代，我队友是人机！这局建议录屏投稿《演员的诞生》！🎬",
    "闪现接Q！这操作够我吃三碗大米饭！(¯﹃¯) 饭友集合！",
    "中路一直叫我去，我怎么去啊？对面中单是Faker，我是大司！(T＿T)",
    "上单养爹人！0-8的诺手带着血怒下山啦！全体起立——恭迎神王归位！👑",
    "辅助别游走了！你家AD被越塔强杀八次，二塔对线已成定局！",
    "这亚索E往无前，E去不返！队友狂pin问号：你是在用键盘拖地吗？",
    "「全体频道」：GG EZ！（实际战绩2-10）对面回：你是指自己EZ？",
    "翻盘？翻不了一点！这水晶爆炸的速度比我退游戏的手速还快！💥",
    "英雄联盟教会我：活着才能补刀，但活着不如回城买装备！🛒",
    "队友问号追不上我！这波啊，这波是《逃跑权の救世之旅》！🏃♂️💨",
    "这盲僧W眼回旋踢，踢回来一个开大的奥拉夫！队友：你在给对面送五杀？",
    "「公屏打字」：对面打野别抓了！我队友已经开始查你IP了！(◣_◢)",
    "ADC：辅助别吃我兵！辅助：我在用工资装给你印钞啊！💵"
]
lol_image_urls = [
    "https://img1.baidu.com/it/u=2633815018,1759914616&fm=253&fmt=auto&app=138&f=JPEG?w=800&h=1066",
    "https://img0.baidu.com/it/u=2261915786,1795076922&fm=253&fmt=auto&app=138&f=JPEG?w=805&h=800",
    "http://img2.baidu.com/it/u=4187780608,3928159208&fm=253&app=138&f=JPEG?w=800&h=800",
    "https://img1.baidu.com/it/u=2035424406,340601990&fm=253&fmt=auto&app=138&f=JPEG?w=846&h=800",
    "http://img2.baidu.com/it/u=199417689,3066557857&fm=253&app=138&f=JPEG?w=800&h=800",
    "http://img0.baidu.com/it/u=3830868676,908643919&fm=253&app=138&f=JPEG?w=800&h=800"
]

valorant_text_list = [
    "这波啊，这波是「烟中恶鬼」！我封烟我先进，队友直呼内行！(꒪Д꒪)ノ",  # 经典烟中硬冲
    "决斗者？不，我是《泉水指挥官》！「打A打A！——诶你们怎么全去B了？」",  # 战术指挥反差
    "钱包空荡荡，幻象在人间！这皮肤价格比我的KD还离谱！💸",  # 氪金吐槽
    "瑞纳的「离场秀」？不，是我的《白给秀》！闪现+冲锋枪=秒躺艺术家！🎨",  # 下饭操作
    "「全体频道」：EZ!（实际战绩3-15）对面火男：你是指自己像EZ一样好杀？",  # 公屏嘲讽
    "保安摄像头？那是我的《死亡直播间》！对面猎枭一箭射穿我最后尊严！🏹",  # 技能反制梗
    "经济局全员鬼魅短喷，这阵容一看就是《葫芦娃救爷爷》重制版！",  # 抽象战术
    "奶妈大招捏到加时赛，队友怒吼：你这奶量比依萍找她爸要钱那天还抠！",  # 技能保留梗
    "火男烧墙封队友退路，这波啊，这波是《烤全羊の盛宴》！🐑",  # 友伤名场面
    "「全体静步！」——然后听到四个队友咚咚咚跑酷声…这静音键是坏了吧！🎮",  # 战术执行崩坏
    "瓦の教条：能刀人绝不开枪！哪怕刀完被五人群殴！🔪",  # 刀人魔怔行为
    "对面捷风原地起飞三杀，我方捷风：这键盘怎么没E键啊？(⊙_⊙)",  # 角色操作反差
    "无畏契约教会我：活着才能下包，但活着不如赌对面马枪！🎯"  # 摆烂哲学
]
valorant_image_urls = [
    "https://img1.baidu.com/it/u=2775943357,335097302&fm=253&fmt=auto&app=138&f=JPEG?w=1423&h=800",
    "https://img0.baidu.com/it/u=3747818441,2153691772&fm=253&fmt=auto&app=138&f=JPEG?w=800&h=823",
    "https://img1.baidu.com/it/u=2747161209,1313294189&fm=253&fmt=auto&app=138&f=JPEG?w=911&h=800",
    "https://img1.baidu.com/it/u=2938671780,3322127840&fm=253&fmt=auto&app=138&f=JPEG?w=884&h=800",
    "http://img2.baidu.com/it/u=1186241339,4178885327&fm=253&app=138&f=JPEG?w=497&h=348",
    "https://img1.baidu.com/it/u=1660059263,1026362085&fm=253&fmt=auto&app=120&f=JPEG?w=889&h=500",
    "https://img0.baidu.com/it/u=1283998789,1836526414&fm=253&fmt=auto&app=138&f=JPEG?w=800&h=800",
    "http://img0.baidu.com/it/u=986022725,2269356971&fm=253&app=138&f=JPEG?w=800&h=800",
    "http://img0.baidu.com/it/u=1942994554,4119951479&fm=253&app=138&f=JPEG?w=393&h=430"
]

mambo_text_list = [
       "曼波一响爹妈白养！这大头马娘爬行姿势比我太奶还潮！(꒪⌓꒪) ",  # 经典魔性动作
    "Wooooo~！孤高の曼波！这BGM一响，狗都在客厅跳起科目三！🕺",  # 洗脑BGM梗
    "一根华仔附体！这曼波跳得比广场舞还带劲，建议申遗！💃 ",  # 头部博主梗
    "赛博太奶在线爬行！这曼波舞步让骨科医生连夜出诊！🦴",  # 动作危险性吐槽
    "黄金船？不！是黄金摇子！这曼波基因比种马血统还难洗！( ͡° ͜ʖ ͡°) ",  # 血统恶搞
    "三连摔接太空步！这曼波操作让迈克尔杰克逊直呼内行！🌕 ",  # 舞蹈动作夸张化
    "曼波挑战开启！左手画龙右手彩虹，最后再来个地板托马斯！🐉🌈 ",  # 玩家参与梗
    "当你把赛马娘玩成爬行模拟器——恭喜解锁《曼波の奇妙冒险》DLC！🎮",  # 游戏玩法扭曲
    "这曼波跳得，秦始皇看了都要爬起来统一摇子手势！👐 #文化输出",  # 历史乱入梗
    "抖音教会我：活着不如摇曼波！哪怕被骂，也要做评论区最靓的崽！✨",  # 流量哲学
    "哈机密"
]
mambo_image_urls = [
    "https://ix.91danji.com/91danji/187/932993-2024100916220167063d2984fed.jpg",
    "https://imgessl.kugou.com/stdmusic/20240826/20240826150203991318.jpg",
    "https://i2.hdslb.com/bfs/archive/4cd628883e79147a72a9cedcf228ab3198b4a8fe.jpg",
    "https://b0.bdstatic.com/ugc/-Mw-_IJmw3ymkybnrGR4Fwb08f2f73b9da7a67d3b07415d286de71.jpg",
    "https://b0.bdstatic.com/7480109d90b1f3acc0120eaa66124047.jpg@h_1280",
    "https://b0.bdstatic.com/ugc/-Mw-_IJmw3ymkybnrGR4Fw5c60c5517fc4a6f9890379020826baa3.jpg",
    "https://p3-pc-sign.douyinpic.com/obj/tos-cn-p-0015/oUWSCIQIBSO1iBWcgifrALAzpiCj9zAAm0sevU?x-expires=2037729600&x-signature=krrVoLrtoa7pSx3dTivncnmmsBg%3D&from=1516005123",
    "https://i0.hdslb.com/bfs/archive/c938e4ecdda7f472276f1c8913c2aa3667fc8bf9.jpg"
]

csgo_text_list = [
    "Rush B！冲就完事了！这波啊，这波是《乌拉の信仰》！乌拉——！(꒪Д꒪)ノ",  # 经典战术梗
    "ECO局起大狙？这操作比马斯克造火箭还抽象！队友：求你去玩扫雷吧！💥",  # 经济局迷惑行为
    "白给三连！这走位让对面以为我是AI托管！(´-ω-`) 建议录屏投稿《人类迷惑行为大赏》",  # 下饭操作
    "烟中恶鬼？不！是烟中饿鬼！封烟后集体蹲坑啃面包，这战术是跟美团学的吧？🍞",  # 战术执行崩坏
    "A大干拉！身法？身法不如玄学！这爆头线比我的血压还飘！🩸",  # 玄学枪法
    "「全体语音」：GG EZ！（实际战绩3-20）对面：你是指自己像EZ一样好杀？",  # 公屏嘲讽
    "背身30发泼水全空？这压枪让牛顿棺材板都压不住了！⚰️",  # 枪法吐槽
    "残局1v5？不！是《白给の艺术》！这五杀我让给对面了，格局打开！🎨",  # 摆烂哲学
    "CS:GO教会我：活着不如赌点！哪怕输比赛，也要做最靓的赌怪！🎲",  # 赌博战术
    "队友闪光弹比太阳还亮！这致盲效果让我提前体验退休生活！🕶️",  # 友伤名场面
    "大狙一响爹妈白养！这空枪让隔壁小孩都笑出鹅叫！🦢",  # 狙击下饭
    "燃烧瓶烧自己！这火攻战术是向诸葛亮借的东风吧？🔥",  # 道具失误
    "拆包？拆不了一点！这C4倒计时比我人生跑得还快！💣"  # 残局压力
]
csgo_image_urls = [
    "https://img1.baidu.com/it/u=1441004831,3804568551&fm=253&fmt=auto&app=120&f=JPEG?w=541&h=404",
    "http://img2.baidu.com/it/u=2316768282,1289389772&fm=253&app=138&f=JPEG?w=800&h=959",
    "https://img2.baidu.com/it/u=1635189641,277457305&fm=253&fmt=auto&app=138&f=JPEG?w=622&h=746",
    "https://img1.baidu.com/it/u=1100847984,3438150612&fm=253&fmt=auto&app=138&f=JPEG?w=228&h=266",
    "https://img1.baidu.com/it/u=1729794804,1576793679&fm=253&fmt=auto&app=138&f=JPEG?w=889&h=500",
    "https://img1.baidu.com/it/u=3272332001,1240741848&fm=253&fmt=auto&app=138&f=JPEG?w=471&h=389",
    "https://img4.runjiapp.com/duoteimg/dtnew_newsup_img/202102/20210205112135_25503.jpg"
]

ow_text_list = [
    "有基佬开我裤链！这源氏拔刀比美团骑手还快！(꒪Д꒪)ノ 队友：刀呢？刀丢复活点了！🗡️",  # 大招空耳梗
    "双飞组合启动！然后被百合一枪爆头——这波啊，这波是《天降正义之快递上门》！📦",  # 经典双飞白给
    "全场最佳：半藏随缘箭射中墙角挂机托比昂！这操作让牛顿直呼不可控！🎯",  # 玄学操作
    "奶位坐牢实录：天使牵狗绳遛狂鼠，结果狗链那端是自爆轮胎！💣 #电子越共",  # 辅助破防
    "大锤冲锋创下悬崖，这地形杀比科目二还难！队友公屏：建议申遗！🌄",  # 地形杀名场面
    "OW教会我：活着不如跳崖！毕竟——重生室WiFi更快！📶",  # 摆烂哲学
    "铁拳玩家现状：右键蓄力→冲进敌群→秒躺→公屏打字「这游戏能玩？」👊",  # 英雄歧视
    "黑影隐身偷点，结果被路霸勾中——这波啊，这波是《透明人的诱惑》！🕶️",  # 技能反制梗
    "「全体频道」：GG EZ！（实际输出3000）对面猩猩：你是指自己像EZ一样脆？🦍",  # 公屏嘲讽
    "秩序之光传送门直通悬崖——建议改行开旅行社！🌉 #反向带团" , # 技能整活
    "SSVGG"
]
ow_image_urls = [
    "https://img1.baidu.com/it/u=3597688507,1574970482&fm=253&fmt=auto&app=138&f=JPEG?w=144&h=188",
    "http://img1.baidu.com/it/u=2238611905,2671429167&fm=253&app=138&f=JPEG?w=500&h=500",
    "https://img0.baidu.com/it/u=3089985545,3865964573&fm=253&fmt=auto&app=138&f=JPEG?w=608&h=456",
    "http://img2.baidu.com/it/u=1134184334,335676280&fm=253&app=138&f=JPEG?w=315&h=569",
    "http://img1.baidu.com/it/u=159395392,3390300360&fm=253&app=138&f=JPEG?w=683&h=591",
    "https://img2.baidu.com/it/u=1262267593,2680662042&fm=253&fmt=auto&app=120&f=JPEG?w=500&h=630"
]

jcc_text_list = [
    "D牌D到脑血栓，赏金连败到八级直接暴毙！这经济比缅北还崩！💸",  # 非酋D牌
    "全员三星五费？不！是《全员老八》！这阵容一看就是戒赌宣传片！🎲",  # 赌博阵容
    "反曲弓×3=无用大棒？这装备合成比高考数学还难！🎓 #铲生几何",  # 装备失误
    "对面天胡福星，我连败到怀疑人生——建议改ID：慈善赌王！🎩",  # 福星对比
    "九五之尊启动！然后被一费卡满入——这九五怕不是拼多多版！👑",  # 高价阵容翻车
    "金铲铲教会我：活着不如上九！哪怕暴毙，也要做棋盘最靓的赌狗！🐶",  # 摆烂文学
    "约德尔人？约德尔鬼！说好的必出三星，结果D空钱包只剩小法！🧙♂️",  # 羁绊诈骗
    "「全体公屏」：求求你们别卷发明家了！我想玩把极客！🔧",  # 内卷现状
    "海克斯强化选「代谢增速器」——从此开启《老八马拉松》！🏃♂️💨",  # 海克斯陷阱
    "三星五费被灵风吹起——这控制链比甄嬛传剧情还紧凑！🌪️"  # 灵风名场面
]   
jcc_image_urls = [
    "https://img0.baidu.com/it/u=2599988456,2284750814&fm=253&fmt=auto&app=138&f=JPEG?w=608&h=608",
    "https://img1.baidu.com/it/u=263329910,3181436318&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=500",
    "https://img1.baidu.com/it/u=698514221,422034826&fm=253&fmt=auto&app=138&f=JPEG?w=800&h=891",
    "https://img2.baidu.com/it/u=3045289123,3856728492&fm=253&fmt=auto&app=138&f=JPEG?w=828&h=800",
    "http://img0.baidu.com/it/u=924518298,7281177&fm=253&app=138&f=JPEG?w=800&h=800",
    "https://img0.baidu.com/it/u=440953426,291414571&fm=253&fmt=auto&app=138&f=JPEG?w=894&h=800",
    "http://img1.baidu.com/it/u=3963361707,1077495795&fm=253&app=138&f=JPEG?w=819&h=800"
]

kobe_text_list = [
    "直升机已启动！这波啊，这波是《洛杉矶の奇妙冒险》！🚁 #牢大精神永存",  # 抽象地名场面
    "肘击步法教学开启！这铁山靠比泰森还带劲！建议申遗！🥊 #曼巴肘术",  # 赛场动作艺术化
    "你说这是巡回演出？不！这是《铁窗泪》remix版！🎤 #巡回の艺术",  # 虚实结合梗
    "曼巴精神！赢球？赢不了一点！但数据栏必须填满！📊 #Excel战神",  # 数据刷子文学
    "后仰跳投美如画，然后被盖帽——这抛物线比A股还刺激！📉",  # 投资圈联动
    "牢大教会我：四氧化三铁是炼钢的！至于怎么炼的？问丹子！🔩",  # 化学梗
    "「全体频道」：你打球像牢大！对面秒回：你上篮像蔡徐坤！🐔",  # 互相伤害文学
    "这走步比詹姆斯还丝滑！裁判看完直呼要加钟！⏰ #幻影舞步",  # 巨星对比
    "牢大の传承：凌晨四点的洛杉矶？不！是凌晨四点的提篮桥！🌆",  # 地域特色改编
    "虚空背打启动！这波啊，这波是《空气の博弈》！🎮 #元宇宙篮球"  # 跨次元联动
]
kobe_image_urls = [
    "https://img1.baidu.com/it/u=231914731,3387527681&fm=253&fmt=auto&app=138&f=JPEG?w=697&h=697",
    "https://img2.baidu.com/it/u=642029224,3297737428&fm=253&fmt=auto&app=120&f=JPEG?w=668&h=500",
    "https://img0.baidu.com/it/u=4153359494,2447827952&fm=253&fmt=auto&app=138&f=JPEG?w=166&h=156",
    "https://img1.baidu.com/it/u=935018408,1530599407&fm=253&fmt=auto&app=120&f=JPEG?w=800&h=500",
    "https://img0.baidu.com/it/u=3650228664,2350244036&fm=253&fmt=auto&app=120&f=JPEG?w=801&h=500",
    "https://i2.hdslb.com/bfs/archive/b0d25b870c60fb58720396b83b7efd2313f8fc42.jpg"
]
zzz_text_list = [
    "走格子走成帕金森！这空洞探索比科目二还难！🚗💨",
    "邦布不是布！是吞我钱包的怪物！💸👾",
    "抽卡歪出音擎？原来我才是真正的空洞白噪！🎸💔",
    "六分街扛把子？不！是六分街打工人！这委托比送外卖还勤！🛵📦",
    "超频三分钟冷却三小时！这技能CD比我贤者时间还长！⏳😇",
    "赤牙帮打架不如赤牙帮跳舞！这战斗BGM比夜店还带感！🕺🎵",
    "狡兔屋装修中！这安全屋比毛坯房还毛坯！🏚️🔨",
    "异界探秘？异界坐牢！每次都是保底人！🔒😭",
    "超频连段打空体力条？这操作比搏击俱乐部还费手！🥊💻",
    "空洞穿梭十分钟，战斗结算两秒钟！建议改名《走格子模拟器》！🎲🕹️",
    "绝区零教会我：活着不如抽卡！毕竟——邦布比对象还会撒娇！💖🤖",
    "当所有角色满级：欢迎来到《新艾利都996社畜模拟器》！👔🏢",
    "你说得对，但是《绝区零》是由米哈游自主研发的...（被空洞吞噬）*后面忘了*",
    "代理指挥？代不了一点！这走格子AI比我奶奶还保守！👵🚷",
    "暴击率120%？这数学是跟罗翔老师学的吧！⚖️🧮"
]

zzz_image_urls = [ 
    "https://i1.hdslb.com/bfs/archive/254069d766c461bb42ab3ae2a107ae07ddfea4da.jpg",
    "https://img2.baidu.com/it/u=2084596122,3544410006&fm=253&fmt=auto&app=138&f=JPEG?w=1066&h=800",
    "http://img1.baidu.com/it/u=387230425,3979948049&fm=253&app=138&f=JPEG?w=800&h=969",
    "https://img2.baidu.com/it/u=1219908069,2951629778&fm=253&fmt=auto&app=138&f=JPEG?w=383&h=417",
    "https://img0.baidu.com/it/u=2060279036,321254151&fm=253&fmt=auto&app=120&f=JPEG?w=800&h=500",
    "https://img2.baidu.com/it/u=3129872027,3051025661&fm=253&fmt=auto&app=138&f=JPEG?w=800&h=800",
    "https://img0.baidu.com/it/u=4178749054,4108357158&fm=253&fmt=auto&app=120&f=JPEG?w=889&h=500"
]
hy_text_list = [
    "火影は俺の夢だから——梦想的火焰，在我心中永不熄灭。",
    "永久の美こそ芸术だ」永恒的美才是艺术。",
    "隠れ里の誓い，忍びの心",
    "俺が生きていたかどうかなんてな、どうでもいいことだ",
    "お前も、舞うか？次の舞台で、俺たちの戦いが始まる。——你也想起舞吗？在下一个舞台，我们的战斗即将开始。",
    "火影の魂，燃えるうちに！（火影之魂，在燃烧中！）*解释*：这句话捕捉了《火影忍者》的核心精神，即热情、奋斗和不懈的追求。它使用了日语中常见的“燃える”一词，形象地表达了火影角色的激情和力量。",
    "死ぬは辛いよ，しかし仲間を守るためなら、死ぬ価値がある。——死亡虽苦，但为保护同伴，死得其所。",
    "まっすぐ自分の言葉は負けねぇ，これが俺の忍道だってばよ。——说到做到，这是我的忍道。",
    "忍びは、暗闇に潜んで、光を待つ存在だ。——忍者，是在黑暗中潜伏，等待光明的存在。",
    "孤独を味わい、苦難を越え、俺は火影になる！——品尝孤独，跨越苦难，我必将成为火影！",
    "火影の名を頂戴！その日まで、努力するぞ！——请赐我火影之名！为此，我将不懈努力！",
    "心に火を灯し、暗闇を照らす。火影の道は、光と影の交わりだ。——点燃心中的火焰，照亮黑暗。火影之道，在于光与影的交织。"
]
hy_image_urls = [
    "https://img0.baidu.com/it/u=1189719382,2198713929&fm=253&fmt=auto&app=120&f=JPEG?w=480&h=270",
    "https://img2.baidu.com/it/u=3648776018,1847536312&fm=253&fmt=auto&app=120&f=JPEG?w=558&h=500",
    "https://img2.baidu.com/it/u=2078514065,2007758686&fm=253&fmt=auto&app=120&f=JPEG?w=801&h=500",
    "https://img1.baidu.com/it/u=380464129,3528444804&fm=253&fmt=auto&app=138&f=JPEG?w=543&h=500",
    "https://img2.baidu.com/it/u=313541113,2869652478&fm=253&fmt=auto&app=120&f=JPEG?w=625&h=500",
    "https://img2.baidu.com/it/u=1219477654,1926962816&fm=253&fmt=auto&app=120&f=JPEG?w=667&h=500",
    "https://img1.baidu.com/it/u=2979371115,3738318276&fm=253&fmt=auto&app=138&f=JPEG?w=814&h=800",
    "https://img0.baidu.com/it/u=34789941,32205390&fm=253&fmt=auto&app=138&f=JPEG?w=802&h=800"
]
coke_text_list = [
   "小猫老弟",
    "汗流浃背了吧老弟",
    "包变脸的老弟",
    "而我，只想要一个小coke",
    "有人单挑吗？"
]
coke_image_urls = [
    "https://img2.baidu.com/it/u=1263066009,150523317&fm=253&fmt=auto&app=138&f=JPEG?w=683&h=648",
    "https://img1.baidu.com/it/u=2668699197,4235415263&fm=253&fmt=auto&app=120&f=JPEG?w=801&h=500",
    "data:image/jpeg;base64,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",
    "https://img1.baidu.com/it/u=3926181737,2251189914&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=708",
    "https://img2.baidu.com/it/u=2380812679,3339432384&fm=253&fmt=auto&app=138&f=JPEG?w=1038&h=800"
]

@register(
    name="game_meme_plugin",
    author="hello七七",
    desc="游戏梗自动回复插件",
    version="1.3"
)
class GameMemePlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    @event_message_type(EventMessageType.ALL)
    async def on_message(self, event: AstrMessageEvent):
        msg_obj = event.message_obj
        text = msg_obj.message_str or ""

        logger.debug(f"收到消息：{text}")

        # 定义统一的消息构造函数
        def send_game_meme(text_list, image_urls):
            meme_text = random.choice(text_list)
            image_url = random.choice(image_urls)
            return event.make_result().message(meme_text).url_image(image_url)

        if "明日方舟" in text or "方舟" in text:
            yield send_game_meme(mrfz_text_list, mrfz_image_urls)
        elif "火影" in  text:
            yield send_game_meme(hy_text_list, hy_image_urls)
        elif "coke" in text:
            yield send_game_meme(coke_text_list, coke_image_urls)
        elif "崩坏：星穹铁道" in text or "星穹铁道" in text or "崩铁" in text or "崩坏星穹铁道" in text:
            yield send_game_meme(xqtd_text_list, xqtd_image_urls)
        elif "王者荣耀" in text  or "农活" in text:
            yield send_game_meme(wz_text_list, wz_image_urls)
        elif "鸣潮" in text:
            yield send_game_meme(mc_text_list, mc_image_urls)
        elif "三国杀" in text:
            yield send_game_meme(sgs_text_list, sgs_image_urls)
        elif "英雄联盟" in text or "LOL" in text or "撸啊撸" in text or "lol" in text:
            yield send_game_meme(lol_text_list, lol_image_urls)
        elif "瓦洛兰特" in text or "VALORANT" in text.lower() or "无畏契约" in text or "瓦" in text:
            yield send_game_meme(valorant_text_list, valorant_image_urls)
        elif "曼波" in text:
            yield send_game_meme(mambo_text_list, mambo_image_urls)
        elif "CSGO" in text.upper() or "反恐精英" in text or "rush B" in text.upper():
            yield send_game_meme(csgo_text_list, csgo_image_urls)
        elif "守望先锋" in text.upper() or "屁股" in text:
            yield send_game_meme(ow_text_list, ow_image_urls)
        elif "金铲铲" in text or "铲子" in text or "云顶" in text:
            yield send_game_meme(jcc_text_list, jcc_image_urls)
        elif any(keyword in text for keyword in ["牢大", "科比", "曼巴", "直升机"]):
            yield send_game_meme(kobe_text_list, kobe_image_urls)
        elif any(keyword in text for keyword in ["绝区零", "走格子", "新艾利都", "邦布"]):
            yield send_game_meme(zzz_text_list, zzz_image_urls)
        else:
            # 非关键词消息不处理，不使用带值的 return
            return
