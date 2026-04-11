import wave, codecs
import numpy as np
# 第一部分：读取音频数据并转换为数值阵列
# 以只读的二进制模式("rb")打开同目录下的音频文件
wavfile =  wave.open(u'music.wav', "rb")

# getparams() 返回一个包含音频参数的元组：(声道数, 量化位数, 采样频率, 采样点总数, ...)
params = wavfile.getparams() 
nframes = params[3] # 提取元组中的第 4 个值，即音频的采样点总数

# 读取所有音频帧的数据，此时 datawav 是一个极其冗长的原始字节流（bytes/string格式）
datawav = wavfile.readframes(nframes) 
wavfile.close() # 养成好习惯，读取完立刻关闭文件流

# 关键点：将原始字节流转化为 16位短整型(np.short) 的 numpy 数组。
# 这样音频的波形就变成了那些有正有负、最大值约为 32767 的数字。
datause = np.frombuffer(datawav, dtype = np.short)

# 第二部分：核心解析逻辑（过零检测与振幅提取）
result_bin = '' # 用于拼接提取出来的二进制字符串 ('0101...')
result_hex = '' # 用于拼接转换后的十六进制字符串 ('5261...')

# mx 用于记录“当前这一个完整波浪(周期)”里的最大振幅（最高峰值）
mx = 0 

# 遍历每一个采样点（减 1 是为了防止后面的 datause[i+1] 数组越界）
for i in range(len(datause) - 1):
    
    # 1. 持续追踪当前周期内的最大值
    if datause[i] > mx:
        mx = datause[i]
        
    try:
        # 2. 过零检测：判断是否穿过 X 轴进入下一个周期
        # 如果当前点在 X 轴下方(负数)，且紧接着的下一个点在 X 轴上方或刚好为 0
        # 这就意味着旧的波浪结束了，新的波浪开始了！
        if (datause[i] < 0 and datause[i+1] >= 0):
            
            # 3. 结算上一个周期提取出的数据
            # 24000 是设定的阈值（约为最大振幅 32767 的 73%）
            if (mx - 24000 > 0): 
                result_bin += '1' # 峰值大于阈值，判定为高振幅，记录 '1'
            else:
                result_bin += '0' # 峰值小于阈值，判定为低振幅，记录 '0'
                
            # 4. 结算完毕后，重置 mx 为新周期的起始点，准备下一轮记录
            mx = datause[i+1] 
    except:
        break


# 第三部分：数据格式转换与文件导出
# 将提取出来的二进制长串，每 4 位为一组转换为十六进制。
# int(xxx, 2) 是将二进制转为十进制，hex() 是转为十六进制。
# [2:] 是为了去掉 Python 生成十六进制时自带的 '0x' 前缀。
for i in range(0, len(result_bin), 4):
    result_hex += hex(int(result_bin[i : i + 4], 2))[2:]

# CTF 经验：十六进制开头是 52617221，代表这是一个 RAR 压缩包
# 以二进制写入模式("wb")创建一个名为 result.rar 的新文件
file_rar = open("result.rar", "wb")

# codecs.decode(..., 'hex_codec') 会将 '526172' 这样的纯文本还原成真正的二进制机器码
file_rar.write(codecs.decode(result_hex, 'hex_codec'))

file_rar.close() # 写入完成，保存关闭