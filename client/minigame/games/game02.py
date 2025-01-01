'''
1.	玩家隨機分配初始資金20~30錠銀子
    電腦隨機分配初始資金20~40錠銀子
    系統隨機決定1數字，數字在1~10之間
    只能看到對方的數字
2.	玩家和電腦分別下注決定莊家，可跟注
    
3.	莊家決定比大比小
4.	
5.	贏了或的該局下注的所有錢(2.下注的錢)&寶石(平手則各自拿回下注前)
6.	任一方破產則遊戲結束

1.	下注一次不得少於1
2.	累積3寶石系統發給1道具
	黃金放大鏡:可知另一方的下注金額

	水晶球:可知自己的數字

'''


import random as rd

from server import Server


class Game02:
    def __init__(self, session: Server):
        self.session = session

    async def start(self):
        print('歡迎來到梅花錢莊!!!')
        # 初始資金
        PM = rd.randint(20, 30)
        CM = rd.randint(20, 40)
        print(f'你的初始資金是{PM}')
        p = PM

        # start
        fg = 0
        ct = 1
        jew = 0
        LSI = []
        ck = 0  # item check goldminnor
        cd = 0  # item check cystral
        while fg != 1 and fg != 2:

            print(f'round{ct}=============================')
            print(f'你現在的銀子是{PM}')

            # 決定數字
            pn = rd.randint(1, 10)
            cn = rd.randint(1, 10)
            print(f'電腦數字: {cn}')
            # 電腦下注
            c1 = rd.randint(1, CM)

            # item used 黃金放大鏡
            if ck >= 1 or cd >= 1:
                print(f'你要使用道具嗎 {LSI}')
                h = input('要使用黃金放大鏡請按y，要使用水晶球請按e，不用請按其餘的任意鍵繼續')
                if h == 'y':
                    print(f'電腦下注:{c1}')
                    s1 = '黃金放大鏡'
                    LSI.remove(s1)
                    ck = 0
                if h == 'e':
                    print(f'玩家數字{pn}')
                    s2 = '水晶球'
                    LSI.remove(s2)
                    cd = 0
                    # 玩家下注
            p1 = int(input('請輸入要下注的銀子: '))

            while p1 > PM:
                p1 = int(input('請再重輸一次: '))

            print(f'電腦下注 {c1}')
            # 扣錢
            PM -= p1
            CM -= c1

            if c1 >= p1:
                print('要跟注請按"y"，不跟注請按其餘的任意鍵繼續')
                k = str(input('請輸入: '))
                if k == 'y':
                    p2 = int(input('請輸入要跟注的銀子:'))
                    while p2 > PM:
                        p2 = eval(input('請再重輸一次'))

                    p1 += p2
                    PM -= p2

                    # money check
                    if p1 == c1:
                        print('輸入錯誤，重新開始吧')
                        break

            # 莊家決定比大小
            # 玩家
            if p1 > c1:
                print('你是莊家')
                J = eval(input('請輸入比大比小(大請按1，小請按2): '))
                # game start
                if J == 1:
                    if pn > cn:
                        print('玩家方勝')
                        PM += (p1 + c1)
                        jew += 1
                    elif pn == cn:
                        print('平手')
                        PM += p1
                        CM += c1
                    else:
                        print('電腦方勝')
                        CM += (p1 + c1)
                if J == 2:
                    if pn < cn:
                        print('玩家方勝')
                        PM += (p1 + c1)
                        jew += 1
                    elif pn == cn:
                        print('平手')
                        PM += p1
                        CM += c1
                    else:
                        print('電腦方勝')
                        CM += (p1 + c1)
                        # computer
            if p1 < c1:
                print('電腦是莊家')
                if pn > 5:
                    J = 2
                else:
                    J = 1
                    # game start
                if J == 1:
                    print('比大')
                    if pn > cn:
                        print('玩家方勝')
                        PM += (p1 + c1)
                        jew += 1
                    elif pn == cn:
                        print('平手')
                        PM += p1
                        CM += c1
                    else:
                        print('電腦方勝')
                        CM += (p1 + c1)
                if J == 2:
                    print('比小')
                    if pn < cn:
                        print('玩家方勝')
                        PM += (p1 + c1)
                        jew += 1
                    elif pn == cn:
                        print('平手')
                        PM += p1
                        CM += c1
                    else:
                        print('電腦方勝')
                        CM += (p1 + c1)
            if p1 == c1:
                print('下注金額一樣，直接繼續下一輪')
                PM += p1
                CM += c1

            # item
            if jew == 3:
                # 黃金放大鏡1      黃金放大鏡:可知另一方的下注金額，追加一次跟注的機會
                i = rd.randint(1, 2)
                if i == 1:
                    print('你獲得一個黃金放大鏡')
                    goldminnor = '黃金放大鏡'
                    LSI.append(goldminnor)
                    ck += 1
                else:
                    print('你獲得一個水晶球')
                    cys = '水晶球'
                    LSI.append(cys)
                    cd += 1

                jew = 0

            print('道具:', LSI)  # CHECK
            print(f'jew {jew}')
            print(f'(玩家數字:{pn})')
            print(f'玩家現在的銀子是: {PM} ')
            # print(f"(電腦銀子 {CM})") #check
            if PM > 0 and CM > 0:
                stop_game = input(
                    '請問你要結束遊戲嗎，要結束遊戲請輸入stop，不結束請按任意鍵繼續，若結束遊戲則按現在的銀子結算: ')
                if stop_game == 'stop':
                    fg = 2
            ct += 1

            # finish
            if PM <= 0 or CM <= 0:
                fg = 1
        if PM <= 0:
            print('你破產了，將不會獲得銀子')
        elif CM <= 0:
            print(f'你是大富翁，你總共獲得了{PM}個銀子')
            currency: int = await self.session.shop.get_owned_currencies()
            await self.session.shop.set_owned_currencies(currency + PM)
        elif fg == 2:
            print(f'遊戲結束，你總共獲得了{PM}個銀子')
            currency: int = await self.session.shop.get_owned_currencies()
            await self.session.shop.set_owned_currencies(currency + PM)
        else:
            print('ERROR')
