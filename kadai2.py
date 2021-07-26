import random
import math
import numpy as np

a_rate = 0.3
kotai = 50
vari = 2
sedai = 30000
kousa_rate = 0.8
heni_rate = 0.3

elite = 0

idenshi = [[0.0] * vari for i in range(kotai)]
next_idenshi = [[0.0] * vari for i in range(kotai)]
# next_idenshi = []
evaluation = [0.0] * kotai

def mccormick_func(x1, x2):
    dx = x1 - x2
    ans = math.sin(x1+x2) + (x1-x2)**2 - 1.5 * x1 + 2.5 * x2 + 1
    return ans


def seisei():
    global idenshi
    print("-------------遺伝子生成-------------")

    for i in range(kotai):
        idenshi[i][0] = random.uniform(-1.5, 4)
        idenshi[i][1] = random.uniform(-3, 4)

    # print(idenshi)


def evaluate():  # 評価するやつ
    # print("-------------評価中-------------")

    # print(idenshi)
    global evaluation
    global elite

    evaluation = [0.0] * kotai  # 初期化

    # print(evaluation)

    # 評価は小さいほうを大きくするため，逆数を用いる

    for i in range(kotai):
        x1 = idenshi[i][0]
        x2 = idenshi[i][1]
        evaluation[i] = mccormick_func(x1, x2)

    # if(evaluation)

    # min_eva = abs(min(evaluation))

    # for i in range(kotai):
    #     evaluation[i] += min_eva

    # print("-------------評価値-------------")
    # print(evaluation)
    # print("-------------エリート遺伝子はこいつ-------------")

    elite = idenshi[evaluation.index(min(evaluation))]
    # print(elite)


def roulette():
    # global evaluation
    ruiseki = []
    total_evalutaiton = 0

    min_eva = abs(min(evaluation))

    for i in range(kotai):
        evaluation[i] += min_eva
        if(evaluation[i] == 0):
            evaluation[i] = 1/1000
        else:
            evaluation[i] = 1/evaluation[i]

        # evaluation

    for i in range(kotai):
        total_evalutaiton += evaluation[i]
        ruiseki.append(total_evalutaiton)

    r = random.random() * total_evalutaiton

    for i, e in enumerate(ruiseki):
        if r < e:
            return i


def selection():
    # print("-------------選択フェーズ-------------") #今回はルーレット選択で
    global next_idenshi

    next_idenshi = [[0.0] * vari for i in range(kotai)]

    for j in range(kotai):
        i = roulette()
        for k in range(vari):
            next_idenshi[j][k] = idenshi[i][k]

    # print("-------------添え字ですよ-------------")
    # print(soeji)
    # print(len(next_idenshi))

    # print("-------------次の遺伝子はこいつらだ-------------")
    # print(next_idenshi)


def kousa():
    global next_idenshi
    # print("-------------BLX-α交叉-------------")

    for i in range(0, int(kotai*kousa_rate), 2):
        x1 = idenshi[i][0]
        x2 = idenshi[i+1][0]
        y1 = idenshi[i][1]
        y2 = idenshi[i+1][1]

        dx = abs(x1 - x2)
        dy = abs(y1 - y2)

        min_x = min(x1, x2)
        min_y = min(y1, y2)
        max_x = max(x1, x2)
        max_y = max(y1, y2)

        min_cx = min_x - a_rate * dx
        max_cx = max_x - a_rate * dx
        min_cy = min_y - a_rate * dy
        max_cy = max_y - a_rate * dy

        next_idenshi[i][0] = random.uniform(min_cx, max_cx)
        next_idenshi[i][1] = random.uniform(min_cy, max_cy)
        next_idenshi[i+1][0] = random.uniform(min_cx, max_cx)
        next_idenshi[i+1][1] = random.uniform(min_cy, max_cy)

        # for j in range(kotai):
        #     if(mask[j] == 1):
        #         tmp = next_idenshi[i][j]
        #         next_idenshi[i][j] = next_idenshi[i+1][j]
        #         next_idenshi[i+1][j] = tmp

    # print("-------------次の遺伝子-------------")
    # print(next_idenshi)
    # print(tmp)


def totsuzen_next():
    # print("-------------突然変異-------------")
    global next_idenshi
    global idenshi
    global elite

    # for i in range(int(kotai * heni_rate)):  # 突然変異
    #     rondom_line = int(kotai*random.random())
    #     for j in range(3):
    #         rondom_col = int(kotai*random.random())
    #         if(next_idenshi[rondom_line][rondom_col] == 0):
    #             next_idenshi[rondom_line][rondom_col] = 1
    #         else:
    #             next_idenshi[rondom_line][rondom_col] = 0

    for i in range(int(kotai * heni_rate)):
        tsuno = random.randint(0, 49)
        iki = int(random.random()/0.5)
        num = -0.1

        if(iki == 0):
            if(next_idenshi[tsuno][iki]-num >= -1.5 and next_idenshi[tsuno][iki] - num <= 4.0):
                next_idenshi[tsuno][iki] -= num
        else:
            if(next_idenshi[tsuno][iki] - num >= -3 and next_idenshi[tsuno][iki] - num <= 4.0):
                next_idenshi[tsuno][iki] -= num

        # print(tsuno)
        # next_idenshi[tsuno][0] -= 0.001
        # next_idenshi[tsuno][1] -= 0.001

    idenshi = next_idenshi  # 次の世代に引継ぎ

    # print(idenshi)
    idenshi[0] = elite  # エリートを保存する
    # print("-------------エリート保存されました-------------")
    # print(idenshi)


def main():
    # print("-------------はじまり-------------")
    seisei()

    # print(idenshi)

    # evaluate()

    # selection()

    # kousa()

    for i in range(sedai):
        # print("■")
        evaluate()
        if(i % int(sedai*0.1) == 0):
            print(f'eva = {min(evaluation)}')

        selection()
        kousa()
        totsuzen_next()

    evaluate()

    print("-------------最終的な遺伝子-------------")
    print(idenshi)

    print("-------------最終的な価値-------------")
    print(evaluation)

    print(idenshi[evaluation.index(min(evaluation))])


if __name__ == '__main__':
    main()
