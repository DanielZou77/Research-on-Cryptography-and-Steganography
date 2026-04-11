import matplotlib.pyplot as plt

# 存储绘制点的绝对坐标
x_coords = []
y_coords = []

# 记录鼠标当前的绝对位置
current_x = 0
current_y = 0

print("正在读取并解析 usb_data.txt ...")

try:
    with open("usb_data.txt", "r") as f:
        lines = f.readlines()
except FileNotFoundError:
    print("错误：找不到 usb_data.txt 文件，请确保它与本脚本在同一目录下。")
    exit()

for line in lines:
    line = line.strip()
    
    #过滤：只处理刚好 16 个字符（8 字节）的数据，跳过握手包等噪音
    if len(line) != 16:
        continue
    
    try:
        # 1. 提取按键状态 (第 0~1 个字符)
        btn = int(line[0:2], 16)
        
        # 2. 提取并计算 X 轴偏移量 (第 4~7 个字符)
        # 小端序转换：将如 '0100' 转换为 '0001'
        x_hex = line[6:8] + line[4:6] 
        x_offset = int(x_hex, 16)
        # 处理16位有符号整数（补码）。16位最大正数是 32767，大于它说明是负数
        if x_offset > 32767:
            x_offset -= 65536
            
        # 3. 提取并计算 Y 轴偏移量 (第 8~11 个字符)
        # 小端序转换
        y_hex = line[10:12] + line[8:10]
        y_offset = int(y_hex, 16)
        # 处理16位有符号整数（补码）
        if y_offset > 32767:
            y_offset -= 65536
            
        # 4. 累加坐标，追踪鼠标在屏幕上的真实位置
        current_x += x_offset
        current_y += y_offset
        
        # 5. 核心判断：只有当左键按下时 (btn == 1)，才把当前坐标当做“墨迹”保存下来
        if btn == 1:
            x_coords.append(current_x)
            # 屏幕的Y轴是向下递增的，而数学坐标系的Y轴是向上递增的。
            # 为了防止画出来的图案倒过来，我们需要给 Y 坐标加个负号进行翻转。
            y_coords.append(-current_y)
            
    except ValueError:
        # 遇到无法解析成十六进制的乱码行则直接跳过
        continue

# --- 绘图部分 ---
if not x_coords:
    print("没有提取到左键按下的坐标数据，请检查数据格式是否正确！")
else:
    print(f"解析完成！共收集到 {len(x_coords)} 个轨迹点，正在生成图像...")
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    
    # 绘制散点图。c='blue' 是颜色，s=1 是点的大小
    ax.scatter(x_coords, y_coords, c='blue', s=1)
    
    # 锁定 X 轴和 Y 轴的比例为 1:1，防止图像被拉宽或压扁
    ax.set_aspect('equal', adjustable='box')
    
    plt.title("Mouse Trace Result")
    plt.show()