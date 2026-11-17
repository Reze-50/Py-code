def task1_language():
    # 输入语言
    str1 = input('输入一门语言名称：')
    print('好好学 {0}'.format(str1))
    print('{0} 棒棒哒'.format(str1))


def task2_name():
    # 输入姓名
    str2 = input('输入一名学生姓名：')
    print('{0} 好好学 Python'.format(str2))
    print('Python 让 {0} 更棒'.format(str2))


def task3_cuboid():
    #长方体面积和体积计算
    print ('长方体面积和体积计算（单位：毫米 mm）')
    L, W, H = input ('输入长方体的长宽高（数据用空格隔开）：'). split ()

    L = float (L)
    W = float (W)
    H = float (H)

    area = 2 * (L * W + W * H + H * L)
    volume = L * W * H

    print ('长方体面积等于 {0:.2f} 平方毫米(mm²)\n 体积等于 {1:.2f} 立方毫米(mm³)'. format (area, volume))



def task4_temperature():
    # 华氏温度转摄氏温度
    F1, F2 = input('输入两个华氏温度（数据用空格隔开）：').split()
    F1 = float(F1)
    F2 = float(F2)
    C1 = 5 * (F1 - 32) / 9
    C2 = 5 * (F2 - 32) / 9
    print('两个摄氏温度为 {0:.2f} ℃, {1:.2f} ℃'.format(C1, C2))


def task5_driving():
    # 报名驾考
    name = input('输入姓名：')
    age = int(input('输入年龄：'))
    if age >= 18:
        print('{0} 可以参加驾考'.format(name))
    else:
        print('{0} 未达到驾考年龄'.format(name))


def task6_restaurant():
    # 餐厅收费
    info = input('输入姓名和身高（m）(用空格隔开)：').split()
    name = info[0]
    height = float(info[1])
    if height >= 1.1:
        print('{0} 要收餐费'.format(name))
    else:
        print('{0} 可以免费用餐'.format(name))


def task7_park():
    # 公园免费入园
    info = input('输入姓名、年龄和身高（m）(用空格隔开)：').split()
    name = info[0]
    age = int(info[1])
    height = float(info[2])
    if age <= 6 and height <= 1.2:
        print('{0} 可以免费入园'.format(name))
    else:
        print('{0} 要收100元门票'.format(name))


# ================= 主函数（菜单版） =================
def main():
    while True:  # 让程序一直循环，直到用户选择退出
        print("\n" + "="*30)
        print("          程序列表")
        print("="*30)
        print("1. 输入语言")
        print("2. 输入姓名")
        print("3. 长方体面积和体积计算")
        print("4. 华氏温度转摄氏温度")
        print("5. 报名驾考")
        print("6. 餐厅收费")
        print("7. 公园免费入园")
        print("0. 退出程序")
        print("="*30)
        
        choice = input("请输入你想执行的实验编号(0-7): ")
        
        # 根据输入的编号调用对应的函数
        if choice == '1':
            task1_language()
        elif choice == '2':
            task2_name()
        elif choice == '3':
            task3_cuboid()
        elif choice == '4':
            task4_temperature()
        elif choice == '5':
            task5_driving()
        elif choice == '6':
            task6_restaurant()
        elif choice == '7':
            task7_park()
        elif choice == '0':
            print("感谢使用，程序已退出。")
            break  # 跳出 while 循环，结束程序
        else:
            print("❌ 输入有误，请输入 0-7 之间的数字！")


if __name__ == '__main__':
    main()