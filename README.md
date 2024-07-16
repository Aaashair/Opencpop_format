# Opencpop_format

Gen_LRCMS3.py - 歌词片段提取工具
Gen_LRCMS3.py 根据 .lrc 文件的时间戳信息, 将视频剪切成歌词片段, 并通过 pinyin 库, 将歌词转为拼音。 该文件用来处理时间戳信息中 ms 单位精确到 3 位的情况。
Gen_LRCMS2.py 功能相似, 用来处理 ms 单位精确到 2 位的情况。

Process.py 负责处理 Textgrid 文件, 从中提取歌词、音素、音素音调、音素音调时长、是否连唱等信息, 并处理成 diffSinger 的训练格式。

使用说明
确保安装了 pinyin 库。
将 .lrc 文件或 Textgrid 文件放在项目目录下。
运行相应的 Python 脚本即可。
相关信息
MFA 所用字典为 mfa_dict/mandarin_pinyin.dict, 
所用声学模型为 mfa_dict/mandarin/mandarin.zip。

注意：
<AP>, <SP> 还未标注。
检测 is_slur_seq 还未完成。
mfa_dict/MFA_DICT.txt 为无声调拼音—音素的字典, 正在寻找或 train 一个适配的声学模型。
