class Poker:
    def __init__(self, poker):
        card_text, card_type, card_value = poker.split(" ")
        self.card_text = card_text
        self.card_type = card_type
        self.card_value = int(card_value)

    def encode(self):
        return self.card_text + " " + self.card_type + " " + str(self.card_value)


class PokerUtil:
    @classmethod
    def get_pokers_from_data(cls, data):
        pokers = []
        pokers_data = data.split(",")
        for poker_ in pokers_data:
            pokers.append(Poker(poker_))
        return cls.sort_pokers(pokers)

    @classmethod
    def encode_pokers(cls, pokers):
        pokers_data = []
        for poker in pokers:
            pokers_data.append(poker.encode())
        return ",".join(pokers_data)

    @classmethod
    def sort_pokers(cls, pokers):
        pokers.sort(key=lambda x: int(x.card_value), reverse=True)
        return pokers


class PokerLogic:
    # 检测牌的类型
    @classmethod
    def getPokerType(cls, myCards):
        pokerType = None
        if myCards != None:
            if cls.isDan(myCards):
                pokerType = "isDan"
            elif cls.isDuiWang(myCards):
                pokerType = "isDuiWang"
            elif cls.isDuiZi(myCards):
                pokerType = "isDuiZi"
            elif cls.isZhaDan(myCards):
                pokerType = "isZhaDan"
            elif cls.isSanDaiYi(myCards):
                pokerType = "isSanDaiYi"
            elif cls.isSanBuDai(myCards):
                pokerType = "isSanBuDai"
            elif cls.isShunZi(myCards):
                pokerType = "isShunZi"
            elif cls.isLianDui(myCards):
                pokerType = "isLianDui"
            elif cls.isSiDaiEr(myCards):
                pokerType = "isSiDaiEr"
            elif cls.isFeiJi(myCards):
                pokerType = "isFeiJi"
        print(pokerType)
        return pokerType

    # 判断我方的牌是否存在能够管住上家的牌，决定是否显示出牌按钮
    # 可以出牌返回TRUE 不能则返回false
    # myCards我方所有的牌
    # preCards上一家出的牌
    @classmethod
    def isOvercomePrev(cls, myCards, preCards):
        # 获取上家出牌类型
        prePokerType = cls.getPokerType(preCards)
        print("myCards=", myCards, "   preCards=", preCards, "   prePokerType=", prePokerType)
        if myCards == None or preCards == None:
            return False
        if prePokerType == None:
            print("上一家出的牌不和法")
            return False
        # 将自己手中的牌和上一家出的牌从小到大进行排序
        myCards = PokerUtil.sort_pokers(myCards)
        preCards = PokerUtil.sort_pokers(preCards)
        # 我手中的牌的个数
        myCardsSize = len(myCards)
        # 上一家出的牌的个数
        preCardsSize = len(preCards)
        # 我先出牌，上一家没有牌
        if preCardsSize == 0 and myCardsSize != 0:
            return True
        # 判断对方是否是王炸
        if cls.isDuiWang(preCards):
            print("上一家出的是王炸，我方肯定吃不起")
            return False
        # 判断我方手上是否有对王
        if myCardsSize >= 2:
            list = []
            list.append(myCards[myCardsSize - 1])
            list.append((myCards[myCardsSize - 2]))
            if cls.isDuiWang(list):
                return True
        # 判断对方不是炸弹，我出炸弹的情况
        if cls.isZhaDan(preCards) == False:
            if myCardsSize < 4:
                return False
            else:
                for i in range(0, myCardsSize - 3):
                    a = myCards[i].card_value
                    b = myCards[i + 1].card_value
                    c = myCards[i + 2].card_value
                    d = myCards[i + 3].card_value
                    if a == b and a == c and a == d:
                        return True
        # 取出上个玩家出的牌的第一张或就那一张
        preValue = preCards[0].card_value
        # 上家出单牌
        if cls.isDan(preCards):
            # 在自己方牌寻找一张逼对面大的牌
            for i in range(0, myCardsSize):
                myValue = myCards[i].card_value
                if preValue < myValue:
                    return True
        # 上家出对子
        elif cls.isDuiZi(preCards):
            for i in range(0, myCardsSize - 1):
                a = myCards[i].card_value
                b = myCards[i + 1].card_value
                if a == b:
                    if a > preValue:
                        return True

        # 上家出三不带
        elif cls.isSanBuDai(preCards):
            # 三张牌可以大过上家的牌
            for i in range(0, myCardsSize - 2):
                a = myCards[i].card_value
                b = myCards[i + 1].card_value
                c = myCards[i + 2].card_value
                if a == b and a == c:
                    if a > preValue:
                        return True
        # 上家出三带一
        elif cls.isSanDaiYi(preCards):
            if myCardsSize < 4:
                return False
            # 三张牌可以大过上家的牌
            for i in range(0, myCardsSize - 2):
                a = myCards[i].card_value
                b = myCards[i + 1].card_value
                c = myCards[i + 2].card_value
                # 由于是三带一取第二个值就没错
                pre = preCards[1].card_value
                if a == b and a == c:
                    if a > pre:
                        return True
        # 上家出炸弹
        elif cls.isZhaDan(preCards):
            if myCardsSize < 4:
                return False
            # 找四张可以大过上家的牌
            for i in range(0, myCardsSize - 3):
                a = myCards[i].card_value
                b = myCards[i + 1].card_value
                c = myCards[i + 2].card_value
                d = myCards[i + 3].card_value
                if a == b and a == c and a == d:
                    if a > preValue:
                        return True
        # 上家出四带二
        elif cls.isSiDaiEr(preCards):
            # 要有四张牌要大于上家的牌
            for i in range(0, myCardsSize - 3):
                a = myCards[i].card_value
                b = myCards[i + 1].card_value
                c = myCards[i + 2].card_value
                d = myCards[i + 3].card_value
                if a == b and a == c:
                    return True
        # 上家出的是顺子
        elif cls.isShunZi(preCards):
            if myCardsSize < preCardsSize:
                return False
            else:
                for i in range(0, myCardsSize - preCardsSize + 1):
                    list = []
                    for j in range(0, preCardsSize):
                        list.append(myCards[i + j])
                    if cls.isShunZi(list):
                        mymax = list[preCardsSize - 1].card_value
                        premax = list[preCardsSize - 1].card_value
                        if mymax > premax:
                            return True
        # 上家出的是连队
        elif cls.isLianDui(preCards):
            if myCardsSize < preCardsSize:
                return False
            else:
                for i in range(0, myCardsSize - preCardsSize + 1):
                    list = []
                    for j in range(0, preCardsSize):
                        list.append(myCards[i + j])
                    if cls.isLianDui(list):
                        mymax = list[preCardsSize - 1].card_value
                        premax = list[preCardsSize - 1].card_value
                        if mymax > premax:
                            return True
        # 上家出飞机
        elif cls.isFeiJi(myCards):
            if myCardsSize < preCardsSize:
                return False
            else:
                for i in range(0, myCardsSize - preCardsSize + 1):
                    list = []
                    for j in range(0, preCardsSize):
                        list.append(myCards[i + j])
                    if cls.isFeiJi(list):
                        mymax = list[4].card_value
                        premax = list[4].card_value
                        if mymax > premax:
                            return True
        return False

    # myCards我想出的牌
    # preCards上家出的牌
    @classmethod
    def comparePre(cls, myCards, preCards):
        # 获取我和上家的出牌类型
        myPokerType = cls.getPokerType(myCards)
        prePokerType = cls.getPokerType(preCards)
        print("myCards=", myCards, "   preCards=", preCards, "   prePokerType=", prePokerType, "myPokerType=",
              myPokerType)
        # 我的牌和上家的牌都不能为空
        if myCards == None or preCards == None:
            return False
        if myPokerType == None or prePokerType == None:
            return False
        # 上一家牌的个数
        prePokerSize = len(preCards)
        # 我手中的牌的个数
        myPokerSize = len(myCards)
        # 如果上家没有牌 我先出牌
        if preCards == 0 and myCards != 0:
            return True
        if cls.isDuiWang(preCards):
            # 上家是对王 我肯定吃不起
            return False
        elif cls.isDuiWang(myCards):
            # 我出对王 谁都吃的起
            return True
        # 我是炸弹对面不是炸弹
        if cls.isZhaDan(preCards) == False and cls.isZhaDan(myCards):
            return True
        # 将自己想出的牌和上一家出的牌从小到大进行排序
        myCards = PokerUtil.sort_pokers(myCards)
        preCards = PokerUtil.sort_pokers(preCards)
        # 得到我手中排序好的第一张
        myCardValue0 = myCards[0].card_value
        # 得到上家手中排序好的第一张
        preCardValue0 = preCards[0].card_value
        # 比较单牌
        if cls.isDan(myCards) and cls.isDan(preCards):
            # 单牌比较第一张
            return myCardValue0 > preCardValue0
        # 比较对子
        elif cls.isDuiZi(myCards) and cls.isDuiZi(preCards):
            # 对子只需比较第一张
            return myCardValue0 > preCardValue0
        # 比较三不带
        elif cls.isSanBuDai(myCards) and cls.isSanBuDai(preCards):
            # 三不带只需比较第一张
            return myCardValue0 > preCardValue0
        # 比较炸弹
        elif cls.isZhaDan(myCards) and cls.isZhaDan(preCards):
            # 炸弹只需比较第一张
            return myCardValue0 > preCardValue0
        # 比较三代一
        elif cls.isSanDaiYi(myCards) and cls.isSanDaiYi(preCards):
            # 三代一只需比较第二张
            myValue = myCards[1].card_value
            preValue = preCards[1].card_value
            return myValue > preValue
        # 比较四带二
        elif cls.isSiDaiEr(myCards) and cls.isSiDaiEr(preCards):
            # 四带二只需比较第三张
            myValue = myCards[2].card_value
            preValue = preCards[2].card_value
            return myValue > preValue
        # 比较顺子
        elif cls.isShunZi(myCards) and cls.isShunZi(preCards):
            # 顺子比较排序好的最大的哪一张
            if prePokerSize != myPokerSize:
                return False
            else:
                myMax = myCards[myPokerSize - 1].card_value
                preMax = preCards[prePokerSize - 1].card_value
                return myMax > preMax
        # 比较连对
        elif cls.isLianDui(myCards) and cls.isLianDui(preCards):
            # 连对比较排序好的最大的哪一张
            if prePokerSize != myPokerSize:
                return False
            else:
                myMax = myCards[myPokerSize - 1].card_value
                preMax = preCards[prePokerSize - 1].card_value
                return myMax > preMax
        # 比较飞机
        elif cls.isFeiJi(myCards) and cls.isFeiJi(preCards):
            if prePokerSize != myPokerSize:
                return False
            else:
                myMax = myCards[4].card_value
                preMax = preCards[4].card_value
                return myMax > preMax
        return False

    # 判断牌是否为单
    @classmethod
    def isDan(myCards):
        flag = False
        if myCards != None and len(myCards) == 1:
            flag = True
        return flag

    # 判断牌是否为对子
    @classmethod
    def isDuiZi(myCards):
        flag = False
        if myCards != None and len(myCards) == 2:
            grade1 = myCards[0].card_value
            grade2 = myCards[1].card_value
            if grade1 == grade2:
                flag = True
        return flag

    # 判断牌是否为3带1
    @classmethod
    def isSanDaiYi(myCards):
        flag = -1
        if myCards != None and len(myCards) == 4:
            myCards = PokerUtil.sort_pokers(myCards)
            grades = []
            grades[0] = myCards[0].card_value
            grades[1] = myCards[1].card_value
            grades[2] = myCards[2].card_value
            grades[3] = myCards[3].card_value

            if grades[1] == grades[0] and grades[2] == grades[0] and grades[3] == grades[0]:
                return -1
            elif grades[1] == grades[0] and grades[2] == grades[0]:
                return 0;
            elif grades[1] == grades[3] and grades[2] == grades[3]:
                return 3
        return flag

    # 判断牌是否为3不带
    @classmethod
    def isSanBuDai(myCards):
        flag = False

        if myCards != None and len(myCards) == 3:
            grade0 = myCards[0].card_value
            grade1 = myCards[1].card_value
            grade2 = myCards[2].card_value

            if grade0 == grade1 and grade2 == grade0:
                flag = True

        return flag

    # 判断牌是否为顺子
    @classmethod
    def isShunZi(myCards):
        flag = True

        if myCards != None:
            size = len(myCards)
            if size < 5 or size > 12:
                return False

            myCards = PokerUtil.sort_pokers(myCards)

            for n in range(size - 1):
                prev = myCards[n].card_value
                next = myCards[n + 1].card_value
                if prev == 17 or prev == 16 or prev == 15 or next == 17 \
                        or next == 16 or next == 15:
                    flag = False
                    break
                else:
                    if prev - next != -1:
                        flag = False
                        break

        return flag

    # 判断是否为炸弹
    @classmethod
    def isZhaDan(myCards):
        flag = False
        if myCards != None and len(myCards) == 4:
            grades = []
            grades[0] = myCards[0].card_value
            grades[1] = myCards[1].card_value
            grades[2] = myCards[2].card_value
            grades[3] = myCards[3].card_value

            if grades[1] == grades[0] and grades[2] == grades[0] and grades[3] \
                    == grades[0]:
                flag = True
        return flag

    # 判断牌是否为王炸
    @classmethod
    def isDuiWang(myCards):
        flag = False

        if myCards != None and len(myCards) == 2:
            gradeOne = myCards[0].card_value
            gradeTwo = myCards[1].card_value
            if gradeOne + gradeTwo == 33:
                flag = True
        return flag

    # 判断是否为连对
    @classmethod
    def isLianDui(myCards):
        flag = True
        if myCards == None:
            flag = False
            return flag
        size = len(myCards)
        if size < 6 or size % 2 != 0:
            flag = False
        else:
            myCards = PokerUtil.sort_pokers(myCards)
            for i in range(0, size, 2):
                if myCards[i].card_value != myCards[i + 1].card_value:
                    flag = False
                    break
                if i < size - 2:
                    if myCards[i].card_value - myCards[i + 2].card_value != -1:
                        flag = False
                        break
        return flag

    # 判断牌是否为飞机
    @classmethod
    def isFeiJi(cls, myCards):
        flag = False
        if myCards != None:
            size = len(myCards)
            if size >= 6:
                myCards = PokerUtil.sort_pokers(myCards)
                if size % 3 == 0 and size % 4 != 0:
                    flag = cls.isFeiJiBuDai(myCards)
                elif size % 3 != 0 and size % 4 == 0:
                    flag = cls.isFeiJiDai(myCards)
                elif size == 12:
                    flag = cls.isFeiJiBuDai(myCards) or cls.isFeiJiDai(myCards)
        return flag

    # 判断牌是否为飞机不带
    @classmethod
    def isFeiJiBuDai(cls, myCards):
        if myCards == None:
            return False

        size = len(myCards)
        n = size // 3
        grades = []

        if size % 3 != 0:
            return False
        else:
            for i in range(n):
                if cls.isSanBuDai(myCards[i * 3:i * 3 + 3]) == False:
                    return False
                else:
                    grades[i] = myCards[i * 3].card_value

        for i in range(n - 1):
            if grades[i] == 15:
                return False
            if grades[i + 1] - grades[i] != 1:
                print('等级连续，如 333444', grades[i + 1] - grades[i])
                return False

        return True

    # 判断牌是否为飞机带
    @classmethod
    def isFeiJiDai(cls, myCards):
        size = len(myCards)
        n = size // 4
        i = 0
        for i in range(0, size - 2, 3):
            grade1 = myCards[i].card_value
            grade2 = myCards[i + 1].card_value
            grade3 = myCards[i + 2].card_value
            if grade1 == grade2 and grade3 == grade1:
                cards = []
                for j in range(i, i + 3 * n):
                    cards.append(myCards[j])
                return cls.isFeiJiBuDai(cards)
        return False

    # 判断牌是否为4带2
    @classmethod
    def isSiDaiEr(myCards):
        flag = False
        if myCards != None and len(myCards) == 6:
            myCards = PokerUtil.sort_pokers(myCards)
            for i in range(3):
                grade1 = myCards[i].card_value
                grade2 = myCards[i + 1].card_value
                grade3 = myCards[i + 2].card_value
                grade4 = myCards[i + 3].card_value
                if grade2 == grade1 and grade3 == grade1 and grade4 == grade1:
                    flag = True
        return flag
