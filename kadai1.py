import random

kotai = 50
sedai = 30000
kousa_rate = 0.8
heni_rate = 0.3
bag_max = 60

mask = []
for i in range(kotai):
    mask.append(int(random.random()/0.7))

elite = 0

idenshi = [[0] * kotai for i in range(kotai)]
next_idenshi = [[0] * kotai for i in range(kotai)]
# next_idenshi = []
evaluation = [0] * kotai
sum_weight = [0] * kotai  # 初期化

weight = [9, 7, 8, 2, 10, 7, 7, 8, 5, 4, 7, 5, 7, 5, 9, 9, 9, 8, 8, 2, 7, 7, 9, 8, 4,
          7, 3, 9, 7, 7, 9, 5, 10, 7, 10, 10, 7, 10, 10, 10, 3, 8, 3, 4, 2, 2, 5, 3, 9, 2]

price = [20, 28, 2, 28, 15, 28, 21, 7, 28, 12, 21, 4, 31, 28, 24, 36, 33, 2, 25, 21, 35, 14, 36, 25,
         12, 14, 40, 36, 2, 28, 33, 40, 22, 2, 18, 22, 14, 22, 15, 22, 40, 7, 4, 21, 21, 28, 40, 4, 24, 21]

# 遺伝子を作るやつ 50*50


def seisei():
    global idenshi
    print("-------------遺伝子生成-------------")

    for i in range(kotai):
        for j in range(kotai):
            # # 0 or 1で乱数を発生 (10%の確率で1を生成)
            idenshi[j][i] = int(random.random()/0.9)

            # idenshi[i][j] = random.randint(0, 1)  # 0 or 1で乱数を発生

    # print(idenshi)


def evaluate():  # 評価するやつ
    # print("-------------評価中-------------")

    # print(idenshi)
    global evaluation
    global sum_weight
    global elite

    evaluation = [0] * kotai  # 初期化
    sum_weight = [0] * kotai  # 初期化

    # print(evaluation)

    for i in range(kotai):
        for j in range(kotai):
            evaluation[i] += idenshi[i][j]*price[j]
            sum_weight[i] += idenshi[i][j]*weight[j]

        if(sum_weight[i] > bag_max):
            evaluation[i] *= 0.00001

    # print(evaluation)
    # print("-------------エリート遺伝子はこいつ-------------")

    elite = idenshi[evaluation.index(max(evaluation))]


def roulette():
    # global evaluation
    ruiseki = []
    total_evalutaiton = 0

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

    next_idenshi = [[0] * kotai for i in range(kotai)]
    for j in range(kotai):
        i = roulette()
        for k in range(kotai):
            next_idenshi[j][k] = idenshi[i][k]

    # next_idenshi = []
    # for j in range(kotai):
    #     i = roulette()
    #     next_idenshi.append(idenshi[i])

    # print("-------------添え字ですよ-------------")
    # print(soeji)
    # print(len(next_idenshi))

    # print("-------------次の遺伝子はこいつらだ-------------")
    # print(next_idenshi)

    # print(total_evalutaiton)


def kousa():
    global next_idenshi
    # print("-------------交叉-------------")

    for i in range(0, int(kotai*kousa_rate), 2):
        for j in range(kotai):
            if(mask[j] == 1):
                tmp = next_idenshi[i][j]
                next_idenshi[i][j] = next_idenshi[i+1][j]
                next_idenshi[i+1][j] = tmp

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

    for i in range(int(kotai*heni_rate)):
        tsuno = random.randint(0, 49)
        # print(tsuno)

        if(next_idenshi[i][tsuno] == 1):
            next_idenshi[i][tsuno] = 0
        else:
            next_idenshi[i][tsuno] = 1

    idenshi = next_idenshi # 次の世代に引継ぎ

    # print(idenshi)
    idenshi[0] = elite # エリートを保存する
    # print("-------------エリート保存されました-------------")
    # print(idenshi)


def main():
    # print("-------------はじまり-------------")
    seisei()
    for i in range(sedai):
        # print("■")
        evaluate()
        if(i % int(sedai*0.1) == 0):
            print(f'eva = {max(evaluation)}')
            # print(f'bag = {max(sum_weight)}')

        selection()
        kousa()
        totsuzen_next()

# generalへメッセージを送信
    evaluate()

    print("-------------最終的な遺伝子-------------")
    print(idenshi)

    tsuno = idenshi[evaluation.index(max(evaluation))]
    print(tsuno)

    product = [x*y for x, y in zip(tsuno, price)]

    print("最終的な価値")
    print(evaluation)
    print(sum(product))

    # print(idenshi[evaluation.index(max(evaluation))])
    print(sum_weight[evaluation.index(max(evaluation))])
    print(sum_weight)

if __name__ == '__main__':
    main()
