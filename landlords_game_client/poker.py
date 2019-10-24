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
        if data == "":
            return []
        pokers = []
        pokers_data = data.split(",")
        for poker_ in pokers_data:
            pokers.append(Poker(poker_))
        return cls.sort_pokers(pokers, True)

    @classmethod
    def encode_pokers(cls, pokers):
        pokers_data = []
        for poker in pokers:
            pokers_data.append(poker.encode())
        return ",".join(pokers_data)

    @classmethod
    def sort_pokers(cls, pokers, reverse_flag=False):
        pokers.sort(key=lambda x: int(x.card_value), reverse=reverse_flag)
        return pokers


class PokerJudge:

    # 第一家出牌检查牌是否规范
    @classmethod
    def firstPoker(cls, my_cards):
        return cls.getPokerType(my_cards) is not None

    # 判断牌是否为单
    @classmethod
    def isDan(cls, my_cards):
        flag = False
        if my_cards is not None and len(my_cards) == 1:
            flag = True
        return flag

    # 判断牌是否为对子
    @classmethod
    def isDuiZi(cls, my_cards):
        flag = False
        if my_cards is not None and len(my_cards) == 2:
            grade1 = my_cards[0].card_value
            grade2 = my_cards[1].card_value
            if grade1 == grade2:
                flag = True
        return flag

    # 判断牌是否为3带1
    @classmethod
    def isSanDaiYi(cls, my_cards):
        flag = False
        if my_cards is not None and len(my_cards) == 4:
            my_cards = PokerUtil.sort_pokers(my_cards)
            a = my_cards[0].card_value
            b = my_cards[1].card_value
            c = my_cards[2].card_value
            d = my_cards[3].card_value

            if a == b and a == c and a == d:
                return False
            elif a == b and a == c:
                return True
            elif d == c and d == b:
                return True
        return flag

    # 判断牌是否为3不带
    @classmethod
    def isSanBuDai(cls, my_cards):
        flag = False
        if my_cards is not None and len(my_cards) == 3:
            grade0 = my_cards[0].card_value
            grade1 = my_cards[1].card_value
            grade2 = my_cards[2].card_value

            if grade0 == grade1 and grade2 == grade0:
                flag = True

        return flag

    # 判断牌是否为顺子
    @classmethod
    def isShunZi(cls, my_cards):
        flag = True

        if my_cards is not None:
            size = len(my_cards)
            if size < 5 or size > 12:
                return False

            my_cards = PokerUtil.sort_pokers(my_cards)

            for n in range(size - 1):
                prev_value = my_cards[n].card_value
                next_value = my_cards[n + 1].card_value
                if prev_value == 13 or prev_value == 14 or prev_value == 12 or next_value == 13 \
                        or next_value == 14 or next_value == 12:
                    flag = False
                    break
                else:
                    if prev_value - next_value != -1:
                        flag = False
                        break
        return flag

    # 判断是否为炸弹
    @classmethod
    def isZhaDan(cls, my_cards):
        flag = False
        if my_cards is not None and len(my_cards) == 4:
            a = my_cards[0].card_value
            b = my_cards[1].card_value
            c = my_cards[2].card_value
            d = my_cards[3].card_value

            if b == a and c == a and d == a:
                flag = True
        return flag

    # 判断牌是否为王炸
    @classmethod
    def isDuiWang(cls, my_cards):
        flag = False
        if my_cards is not None and len(my_cards) == 2:
            if my_cards[0].card_value + my_cards[1].card_value == 27:
                flag = True
        return flag

    # 判断是否为连对
    @classmethod
    def isLianDui(cls, my_cards):
        flag = True
        if my_cards is None:
            flag = False
            return flag
        size = len(my_cards)
        if size < 6 or size % 2 != 0:
            flag = False
        else:
            my_cards = PokerUtil.sort_pokers(my_cards)
            for i in range(0, size, 2):
                if my_cards[i].card_value != my_cards[i + 1].card_value:
                    flag = False
                    break
                if i < size - 2:
                    if my_cards[i].card_value - my_cards[i + 2].card_value != -1:
                        flag = False
                        break
        return flag

    # 判断牌是否为飞机
    @classmethod
    def isFeiJi(cls, my_cards):
        flag = False
        if my_cards is not None:
            size = len(my_cards)
            if size >= 6:
                my_cards = PokerUtil.sort_pokers(my_cards)
                if size % 3 == 0 and size % 4 != 0:
                    flag = cls.isFeiJiBuDai(my_cards)
                elif size % 3 != 0 and size % 4 == 0:
                    flag = cls.isFeiJiDai(my_cards)
                elif size == 12:
                    flag = cls.isFeiJiBuDai(my_cards) or cls.isFeiJiDai(my_cards)
        return flag

    # 判断牌是否为飞机不带
    @classmethod
    def isFeiJiBuDai(cls, my_cards):
        if my_cards is not None:
            return False

        size = len(my_cards)
        n = size // 3
        grades = []

        if size % 3 != 0:
            return False
        else:
            for i in range(n):
                if not cls.isSanBuDai(my_cards[i * 3:i * 3 + 3]):
                    return False
                else:
                    grades.append(my_cards[i * 3].card_value)

        for i in range(n - 1):
            if grades[i] == 15:
                return False
            if grades[i + 1] - grades[i] != 1:
                print('等级连续，如 333444', grades[i + 1] - grades[i])
                return False

        return True

    # 判断牌是否为飞机带
    @classmethod
    def isFeiJiDai(cls, my_cards):
        size = len(my_cards)
        n = size // 4
        for i in range(0, size - 2):
            grade1 = my_cards[i].card_value
            grade2 = my_cards[i + 1].card_value
            grade3 = my_cards[i + 2].card_value
            if grade1 == grade2 and grade3 == grade1:
                cards = []
                for j in range(i, i + 3 * n):
                    cards.append(my_cards[j])
                return cls.isFeiJiBuDai(cards)
        return False

    # 判断牌是否为4带2
    @classmethod
    def isSiDaiEr(cls, my_cards):
        flag = False
        if my_cards is not None and len(my_cards) == 6:
            my_cards = PokerUtil.sort_pokers(my_cards)
            for i in range(3):
                grade1 = my_cards[i].card_value
                grade2 = my_cards[i + 1].card_value
                grade3 = my_cards[i + 2].card_value
                grade4 = my_cards[i + 3].card_value

                if grade2 == grade1 and grade3 == grade1 and grade4 == grade1:
                    flag = True
        return flag

    # 检测牌的类型
    @classmethod
    def getPokerType(cls, my_cards):
        poker_type = None
        if my_cards is not None:
            if cls.isDan(my_cards):
                poker_type = "isDan"
            elif cls.isDuiWang(my_cards):
                poker_type = "isDuiWang"
            elif cls.isDuiZi(my_cards):
                poker_type = "isDuiZi"
            elif cls.isZhaDan(my_cards):
                poker_type = "isZhaDan"
            elif cls.isSanDaiYi(my_cards):
                poker_type = "isSanDaiYi"
            elif cls.isSanBuDai(my_cards):
                poker_type = "isSanBuDai"
            elif cls.isShunZi(my_cards):
                poker_type = "isShunZi"
            elif cls.isLianDui(my_cards):
                poker_type = "isLianDui"
            elif cls.isSiDaiEr(my_cards):
                poker_type = "isSiDaiEr"
            elif cls.isFeiJi(my_cards):
                poker_type = "isFeiJi"
        print(poker_type)
        return poker_type


class PokerLogic:

    # 判断我方的牌是否存在能够管住上家的牌，决定是否显示出牌按钮
    # 可以出牌返回TRUE 不嫩则返回false
    # myCards我方所有的牌
    # preCards上一家出的牌
    @classmethod
    def isOvercomePrev(cls, my_cards, pre_cards):
        # 获取上家出牌类型
        pre_poker_type = PokerJudge.getPokerType(pre_cards)
        print("myCards=", my_cards, "   preCards=", pre_cards, "   prePokerType=", pre_poker_type)
        if my_cards is None or pre_cards is None:
            return False
        if pre_poker_type is None:
            print("上一家出的牌不和法")
            return False
        # 将自己手中的牌和上一家出的牌从小到大进行排序
        my_cards = PokerUtil.sort_pokers(my_cards)
        pre_cards = PokerUtil.sort_pokers(pre_cards)
        # 我手中的牌的个数
        my_cards_size = len(my_cards)
        # 上一家出的牌的个数
        pre_cards_size = len(pre_cards)
        # 我先出牌，上一家没有牌
        if pre_cards_size == 0 and my_cards_size != 0:
            return True
        # 判断对方是否是王炸
        if PokerJudge.isDuiWang(pre_cards):
            print("上一家出的是王炸，我方肯定吃不起")
            return False
        # 判断我方手上是否有对王
        if my_cards_size >= 2:
            return PokerJudge.isDuiWang([my_cards[my_cards_size - 1], (my_cards[my_cards_size - 2])])
        # 判断对方不是炸弹，我出炸弹的情况
        if not PokerJudge.isZhaDan(pre_cards):
            if my_cards_size < 4:
                return False
            else:
                for i in range(0, my_cards_size - 3):
                    a = my_cards[i].card_value
                    b = my_cards[i + 1].card_value
                    c = my_cards[i + 2].card_value
                    d = my_cards[i + 3].card_value
                    if a == b and a == c and a == d:
                        return True
        # 取出上个玩家出的牌的第一张或就那一张
        pre_value = pre_cards[0].card_value
        # 上家出单牌
        if PokerJudge.isDan(pre_cards):
            # 在自己方牌寻找一张逼对面大的牌
            for i in range(0, my_cards_size):
                my_value = my_cards[i].card_value
                if pre_value < my_value:
                    return True
        # 上家出对子
        elif PokerJudge.isDuiZi(pre_cards):
            for i in range(0, my_cards_size - 1):
                a = my_cards[i].card_value
                b = my_cards[i + 1].card_value
                if a == b:
                    if a > pre_value:
                        return True

        # 上家出三不带
        elif PokerJudge.isSanBuDai(pre_cards):
            # 三张牌可以大过上家的牌
            for i in range(0, my_cards_size - 2):
                a = my_cards[i].card_value
                b = my_cards[i + 1].card_value
                c = my_cards[i + 2].card_value
                if a == b and a == c:
                    if a > pre_value:
                        return True
        # 上家出三带一
        elif PokerJudge.isSanDaiYi(pre_cards):
            if my_cards_size < 4:
                return False
            # 三张牌可以大过上家的牌
            for i in range(0, my_cards_size - 2):
                a = my_cards[i].card_value
                b = my_cards[i + 1].card_value
                c = my_cards[i + 2].card_value
                # 由于是三带一取第二个值就没错
                pre = pre_cards[1].card_value
                if a == b and a == c:
                    if a > pre:
                        return True
        # 上家出炸弹
        elif PokerJudge.isZhaDan(pre_cards):
            if my_cards_size < 4:
                return False
            # 找四张可以大过上家的牌
            for i in range(0, my_cards_size - 3):
                a = my_cards[i].card_value
                b = my_cards[i + 1].card_value
                c = my_cards[i + 2].card_value
                d = my_cards[i + 3].card_value
                if a == b and a == c and a == d:
                    if a > pre_value:
                        return True
        # 上家出四带二
        elif PokerJudge.isSiDaiEr(pre_cards):
            # 要有四张牌要大于上家的牌
            print("进入四带二")
            for i in range(0, my_cards_size - 3):
                a = my_cards[i].card_value
                b = my_cards[i + 1].card_value
                c = my_cards[i + 2].card_value
                d = my_cards[i + 3].card_value
                if a == b and a == c and a == d:
                    return True
        # 上家出的是顺子
        # 上家出的是顺子
        elif PokerJudge.isShunZi(pre_cards):
            list_ = []
            for j in range(0, my_cards_size):
                list_.append(my_cards[j].card_value)
            list_new = list(set(list_))
            # 改为Poker对象作为元素
            list_poker = []
            for val in list_new:
                list_poker.append(Poker("_ _ %s" % val))
            PokerUtil.sort_pokers(list_poker)
            my_size = len(list_poker)
            if my_size < pre_cards_size:
                return False
            else:
                for i in range(0, my_size - pre_cards_size + 1):
                    list_ = []
                    for j in range(0, pre_cards_size):
                        list_.append(list_poker[i + j])
                    if PokerJudge.isShunZi(list_):
                        if list_[pre_cards_size - 1].card_value > pre_cards[pre_cards_size - 1].card_value:
                            return True
        # 上家出的是连队
        elif PokerJudge.isLianDui(pre_cards):
            if my_cards_size < pre_cards_size:
                return False
            else:
                for i in range(0, my_cards_size - pre_cards_size + 1):
                    list_ = []
                    for j in range(0, pre_cards_size):
                        list_.append(my_cards[i + j])
                    if PokerJudge.isLianDui(list_):
                        my_max = list_[pre_cards_size - 1].card_value
                        pre_max = pre_cards[pre_cards_size - 1].card_value
                        if my_max > pre_max:
                            return True
        # 上家出飞机
        elif PokerJudge.isFeiJi(my_cards):
            if my_cards_size < pre_cards_size:
                return False
            else:
                for i in range(0, my_cards_size - pre_cards_size + 1):
                    list_ = []
                    for j in range(0, pre_cards_size):
                        list_.append(my_cards[i + j])
                    if PokerJudge.isFeiJi(list_):
                        my_max = list_[4].card_value
                        pre_max = pre_cards[4].card_value
                        if my_max > pre_max:
                            return True
        return False

    # myCards我想出的牌
    # preCards上家出的牌
    @classmethod
    def comparePre(cls, my_cards, pre_cards):
        # 获取我和上家的出牌类型
        my_poker_type = PokerJudge.getPokerType(my_cards)
        pre_poker_type = PokerJudge.getPokerType(pre_cards)
        print("myCards=", my_cards, "   preCards=", pre_cards, "   prePokerType=", pre_poker_type, "myPokerType=",
              my_poker_type)
        # 我的牌和上家的牌都不能为空
        if my_cards is None or pre_cards is None:
            return False
        if my_poker_type is None or pre_poker_type is None:
            return False
        # 上一家牌的个数
        pre_poker_size = len(pre_cards)
        # 我手中的牌的个数
        my_poker_size = len(my_cards)
        # 如果上家没有牌 我先出牌
        if pre_poker_size == 0 and my_poker_size != 0:
            return True
        if PokerJudge.isDuiWang(pre_cards):
            # 上家是对王 我肯定吃不起
            return False
        elif PokerJudge.isDuiWang(my_cards):
            # 我出对王 谁都吃的起
            return True
        # 我是炸弹对面不是炸弹
        if not PokerJudge.isZhaDan(pre_cards) and PokerJudge.isZhaDan(my_cards):
            return True
        # 将自己想出的牌和上一家出的牌从小到大进行排序
        my_cards = PokerUtil.sort_pokers(my_cards)
        pre_cards = PokerUtil.sort_pokers(pre_cards)
        # 得到我手中排序好的第一张
        my_first_card_value = my_cards[0].card_value
        # 得到上家手中排序好的第一张
        pre_first_card_value = pre_cards[0].card_value
        # 比较单牌
        if PokerJudge.isDan(my_cards) and PokerJudge.isDan(pre_cards):
            # 单牌比较第一张
            return my_first_card_value > pre_first_card_value
        # 比较对子
        elif PokerJudge.isDuiZi(my_cards) and PokerJudge.isDuiZi(pre_cards):
            # 对子只需比较第一张
            return my_first_card_value > pre_first_card_value
        # 比较三不带
        elif PokerJudge.isSanBuDai(my_cards) and PokerJudge.isSanBuDai(pre_cards):
            # 三不带只需比较第一张
            return my_first_card_value > pre_first_card_value
        # 比较炸弹
        elif PokerJudge.isZhaDan(my_cards) and PokerJudge.isZhaDan(pre_cards):
            # 炸弹只需比较第一张
            return my_first_card_value > pre_first_card_value
        # 比较三代一
        elif PokerJudge.isSanDaiYi(my_cards) and PokerJudge.isSanDaiYi(pre_cards):
            # 三代一只需比较第二张
            my_value = my_cards[1].card_value
            pre_value = pre_cards[1].card_value
            return my_value > pre_value
        # 比较四带二
        elif PokerJudge.isSiDaiEr(my_cards) and PokerJudge.isSiDaiEr(pre_cards):
            # 四带二只需比较第三张
            my_value = my_cards[2].card_value
            pre_value = pre_cards[2].card_value
            return my_value > pre_value
        # 比较顺子
        elif PokerJudge.isShunZi(my_cards) and PokerJudge.isShunZi(pre_cards):
            # 顺子比较排序好的最大的哪一张
            if pre_poker_size != my_poker_size:
                return False
            else:
                my_max = my_cards[my_poker_size - 1].card_value
                pre_max = pre_cards[pre_poker_size - 1].card_value
                return my_max > pre_max
        # 比较连对
        elif PokerJudge.isLianDui(my_cards) and PokerJudge.isLianDui(pre_cards):
            # 连对比较排序好的最大的哪一张
            if pre_poker_size != my_poker_size:
                return False
            else:
                my_max = my_cards[my_poker_size - 1].card_value
                pre_max = pre_cards[pre_poker_size - 1].card_value
                return my_max > pre_max
        # 比较飞机
        elif PokerJudge.isFeiJi(my_cards) and PokerJudge.isFeiJi(pre_cards):
            if pre_poker_size != my_poker_size:
                return False
            else:
                my_max = my_cards[4].card_value
                pre_max = pre_cards[4].card_value
                return my_max > pre_max
        return False
