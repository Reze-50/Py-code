#输入语言
str1 = input ('输入一门语言名称：')
print ('好好学 {0}'. format(str1))
print ('{0} 棒棒哒'. format(str1))


#输入姓名
str2 = input ('输入一名学生姓名：')
print ('{0} 好好学 Python'. format(str2))
print ('Python 让 {0} 更棒'. format(str2))


#长方体面积和体积计算
print ('长方体面积和体积计算（单位：毫米 mm）')
L, W, H = input ('输入长方体的长宽高（数据用空格隔开）：'). split ()

L = float (L)
W = float (W)
H = float (H)

area = 2 * (L * W + W * H + H * L)
volume = L * W * H

print ('长方体面积等于 {0:.2f} 平方毫米(mm²)\n 体积等于 {1:.2f} 立方毫米(mm³)'. format (area, volume))


# 华氏温度转摄氏温度
F1, F2 = input ('输入两个华氏温度（数据用空格隔开）：'). split()

F1 = float (F1)
F2 = float (F2)

C1 = 5 * (F1 - 32) / 9
C2 = 5 * (F2 - 32) / 9

print ('两个摄氏温度为 {0:.2f} ℃, {1:.2f} ℃'. format(C1, C2))


#报名驾考
name = input ('输入姓名：')
age = int (input ('输入年龄：'))

if age >= 18:
    print ('{0} 可以参加驾考'. format(name))
else:
    print ('{0} 未达到驾考年龄'. format(name))


# 餐厅收费
info = input ('输入姓名和身高（m）(用空格隔开)：'). split()
name = info[0]
height = float (info[1])

if height >= 1.1:
    print ('{0} 要收餐费'.format(name))
else:
    print ('{0} 可以免费用餐'.format(name))


# 公园免费入园
info = input ('输入姓名、年龄和身高（m）(用空格隔开)：'). split()
name = info[0]
age = int (info[1])
height = float (info[2])

if age <= 6 and height <= 1.2:
    print ('{0} 可以免费入园'.format(name))
else:
    print ('{0} 要收100元门票'.format(name))