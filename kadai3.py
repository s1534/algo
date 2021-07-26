import random
import math
import copy

kotai = 50
sedai = 30000
kousa_rate = 0.8
heni_rate = 0.3

route = 48

idenshi = [[0] * route for i in range(kotai)]  # 50 * 48
next_idenshi = [[0] * route for i in range(kotai)]
# next_idenshi = []
evaluation = [0] * kotai  # 初期化

# 都市の割り当て
route_map = []
for i in range(route):
    route_map.append(i)

print(len(idenshi))

x = [] # 都市のx座標
y = [] # 都市のy座標


def read_file():
    global x
    global y
    x_tmp = open('att48_x.txt', 'r')
    y_tmp = open('att48_y.txt', 'r')

    for i in range(48):
        num1 = x_tmp.readline()
        num1 = num1.replace("\n", "")
        x.append(int(num1))

        num2 = y_tmp.readline()
        num2 = num2.replace("\n", "")
        y.append(int(num2))


def seisei():
    global idenshi
    print("-------------遺伝子生成-------------")

    # print(route_map)

    for i in range(kotai):
        tmp = random.sample(route_map, route)
        # print(tmp)
        for j in range(route):
            idenshi[i][j] = tmp[j]

    # print(idenshi)


def evaluate():  # 評価するやつ
    # print("-------------評価中-------------")

    global evaluation
    global elite

    evaluation = [0.0] * kotai  # 初期化

    # print(evaluation)
    # print("-------------エリート遺伝子はこいつ-------------")

    for i in range(kotai):
        for j in range(route):

            if(j == route-1):
                x1 = x[idenshi[i][j]]
                x2 = x[idenshi[i][0]]
                y1 = y[idenshi[i][j]]
                y2 = y[idenshi[i][0]]

            else:
                x1 = x[idenshi[i][j]]
                x2 = x[idenshi[i][j+1]]
                y1 = y[idenshi[i][j]]
                y2 = y[idenshi[i][j+1]]

            diff_x = x1-x2
            diff_y = y1-y2

            evaluation[i] += math.sqrt(diff_x**2 + diff_y**2)

    elite = idenshi[evaluation.index(min(evaluation))]
    elite_evaluation = evaluation[evaluation.index(min(evaluation))]

    # print("-------------評価値-------------")
    # print(evaluation)
    # print("-------------エリート遺伝子はこいつ-------------")
    # print(elite)
    # print(elite_evaluation)

def roulette():
    # global evaluation
    ruiseki = []
    total_evalutaiton = 0

    for i in range(kotai):
        evaluation[i] = 1/evaluation[i]

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

    next_idenshi = [[0] * route for i in range(kotai)]
    for j in range(kotai):
        i = roulette()
        for k in range(route):
            next_idenshi[j][k] = idenshi[i][k]

    # print("-------------添え字ですよ-------------")
    # print(soeji)
    # print(len(next_idenshi))

    # print("-------------次の遺伝子はこいつらだ-------------")
    # print(next_idenshi)

    # print(total_evalutaiton)


def PMX_method():
    global next_idenshi

    # next_idenshi = idenshiという書き方だと，next_idenshiをいじるとidenshiもいじられる
    # next_idenshi = copy.deepcopy(idenshi) # いったん子に引き継ぐ，こう書かないと参照渡しになる
    parent = copy.deepcopy(next_idenshi)



    # print("-------------部分写像交叉-------------")
    # print(point1, point2)
    # print("-------------親の世代-------------")

    # print(idenshi[0])
    # print(idenshi[1])

    for i in range(0, int(kotai*kousa_rate), 2):
    # for i in range(1):
        flag_p1 = [0] * route  # 親の遺伝子をそのまま入れてもいいか判定するためのフラグ
        flag_p2 = [0] * route  # 1が入っていないところは入れても良い

        point1 = random.randrange(route-1)  # 0から46の間で乱数を生成
        # 交叉する始点と終点を決める　randrange(start,stop)
        point2 = random.randrange(point1+1, route)  # point1+1から47の間で乱数を生成
        # ステップ1
        for j in range(route):  # 遺伝子入れ替えかつ，入れ替えてはいけないところを記憶するループ
            if(point1 <= j and j <= point2):
                tmp_val = next_idenshi[i][j]
                next_idenshi[i][j] = next_idenshi[i+1][j]
                next_idenshi[i+1][j] = tmp_val

                flag_p1[next_idenshi[i][j]] = 1
                flag_p2[next_idenshi[i+1][j]] = 1

            else:
                next_idenshi[i][j] = -1
                next_idenshi[i+1][j] = -1

        # print("--------------ステップ１---------------")
        # print(next_idenshi[0])
        # print(next_idenshi[1])

        # print("--------------フラグになります---------------")
        # print(flag_p1)
        # print(flag_p2)

        # print("--------------一度親の確認---------------")
        # print(idenshi[0])
        # print(idenshi[1])

        yobi1 = []
        yobi2 = []

        # ステップ2
        for k in range(route):
            if(point1 <= k and k <= point2):
                continue
            else:

                if(flag_p1[parent[i][k]] != 1):
                    next_idenshi[i][k] = parent[i][k]
                else:
                    # continue
                    yobi1.append(parent[i][k])

                if(flag_p2[parent[i+1][k]] != 1):
                    next_idenshi[i+1][k] = parent[i+1][k]
                else:
                    # continue
                    yobi2.append(parent[i+1][k])

        num1 = 0
        num2 = 0
        yobi1.sort()
        yobi2.sort()
        # print(len(yobi1),len(yobi2))


        # ステップ3
        for k in range(route):
            if(next_idenshi[i][k] == -1):
                next_idenshi[i][k] = yobi2[num1]
                num1 +=1

            if(next_idenshi[i+1][k] == -1):
                next_idenshi[i+1][k] = yobi1[num2]
                num2 +=1

            # print("-------------ステップ2-------------")
            # print(next_idenshi[i])
            # print(next_idenshi[i+1])

        # print("■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■")



        # print(next_idenshi)
        # print(tmp)
    # print("-------------ステップ2-------------")
    # print(next_idenshi[0])
    # print(next_idenshi[1])

    # tmp_list1 = copy.deepcopy(next_idenshi[0])
    # tmp_list2 = copy.deepcopy(next_idenshi[1])


    # print("-------------確認-------------")
    # tmp_list1.sort()
    # print(tmp_list1)
    # tmp_list2.sort()
    # print(tmp_list2)
    # print("-------------予備-------------")

    # print(yobi1)
    # print(yobi2)
    # print(len(yobi1),len(yobi2))

def OX_method():
    # print("-------------順序交叉-------------")
    global next_idenshi

    parent = copy.deepcopy(next_idenshi)


    for i in range(0, int(kotai*kousa_rate), 2):
    # for i in range(1):
        flag_p1 = [0] * route  # 親の遺伝子を順序のところにそのまま入れてもよいのかフラグ
        flag_p2 = [0] * route  # 1が入っていないところは入れても良い

        yobi1 = []
        yobi2 = []

        point1 = random.randrange(route-1)  # 0から46の間で乱数を生成
        # 交叉する始点と終点を決める　randrange(start,stop)
        point2 = random.randrange(point1+1, route)  # point1+1から47の間で乱数を生成

        # print(point1,point2)
        # ステップ1
        for j in range(route):  # 遺伝子入れ替えかつ，入れ替えてはいけないところを記憶するループ
            if(point1 <= j and j <= point2):

                flag_p1[next_idenshi[i][j]] = 1
                flag_p2[next_idenshi[i+1][j]] = 1

            else:
                next_idenshi[i][j] = -1
                next_idenshi[i+1][j] = -1
        # print("--------------ステップ１---------------")
        # print(next_idenshi[0])
        # print(next_idenshi[1])

        for j in range(point2+1,route):
            if(flag_p2[parent[i+1][j]] != 1):
                yobi1.append(parent[i][j])
            if(flag_p1[parent[i][j]] != 1):
                yobi2.append(parent[i+1][j])


        for j in range(route):
            if(j<=point2):
                if(flag_p2[parent[i+1][j]] != 1):
                    yobi1.append(parent[i][j])
                if(flag_p1[parent[i][j]] != 1):
                    yobi2.append(parent[i+1][j])

        num1 = 0
        num2 = 0

        for j in range(point2+1,route):
            if(yobi1[num1] != -1):
                next_idenshi[i][j] = yobi1[num1]
                num1 += 1

        for j in range(point1):
            if(yobi1[num1] != -1):
                next_idenshi[i][j] = yobi1[num1]
                num1 += 1

        for j in range(point2+1,route):
            if(yobi2[num2] != -1):
                next_idenshi[i+1][j] = yobi2[num2]
                num2 += 1
        for j in range(point1):
            if(yobi2[num2] != -1):
                next_idenshi[i+1][j] = yobi2[num2]
                num2 += 1

        # print("--------------ステップ2---------------")
        # print(next_idenshi[0])
        # print(next_idenshi[1])

        # print("--------------予備---------------")
        # print(yobi1)
        # print(yobi2)


        # print("--------------フラグになります---------------")
        # print(flag_p1)
        # print(flag_p2)

        tmp_list1 = copy.deepcopy(next_idenshi[0])
        tmp_list2 = copy.deepcopy(next_idenshi[1])


        # print("-------------確認-------------")
        # tmp_list1.sort()
        # print(tmp_list1)
        # tmp_list2.sort()
        # print(tmp_list2)

def CX_method():
    # print("-------------循環交叉-------------")
    global next_idenshi

    parent = copy.deepcopy(next_idenshi)
    # next_idenshi = [[-1] * route for i in range(kotai*kousa_rate)]

    for i in range(0, int(kotai*kousa_rate), 2):
    # for i in range(1):
        flag_p1 = [0] * route  # 親の遺伝子をそのまま入れてもいいか判定するためのフラグ
        flag_p2 = [0] * route  # 1が入っていないところは入れても良い

        yobi1 = []
        yobi2 = []

        child1 = [-1] * route
        child2 = [-1] * route


        # print("--------------一度親の確認---------------")
        # print(parent[i])
        # print(parent[i+1])

        # print("--------------ステップ0---------------")
        # print(next_idenshi[0])
        # print(next_idenshi[1])

        num1_tmp = 0

        # ステップ1
        for j in range(route):
            child1[num1_tmp] = parent[i][num1_tmp]
            child2[num1_tmp] = parent[i+1][num1_tmp]
            tmp_val = child2[num1_tmp]
            for k in range(route):
                if(tmp_val == parent[i][k]):
                    num1_tmp = k
                    break

        # print("--------------ステップ1---------------")
        # print(next_idenshi[0])
        # print(next_idenshi[1])

        # ステップ2
        for j in range(route):
            if(child1[j] == -1):
                child1[j] = parent[i+1][j]
                # print("tets")
            if(child2[j] == -1):
                child2[j] = parent[i][j]

        # print("--------------ステップ2---------------")
        # print(next_idenshi[0])
        # print(next_idenshi[1])

        # print("--------------予備---------------")
        # print(yobi1)
        # print(yobi2)


        # print("--------------フラグになります---------------")
        # print(flag_p1)
        # print(flag_p2)

        # tmp_list1 = copy.deepcopy(next_idenshi[0])
        # tmp_list2 = copy.deepcopy(next_idenshi[1])


        # print("-------------確認-------------")
        # tmp_list1.sort()
        # print(tmp_list1)
        # tmp_list2.sort()
        # print(tmp_list2)

        next_idenshi[i] = child1
        next_idenshi[i+1] = child2



def totsuzen_next():
    # print("-------------突然変異-------------")
    global next_idenshi
    global idenshi
    global elite

    # for i in range(int(kotai*heni_rate)):
    #     tsuno = random.randint(0, 46)
    #     tmp = next_idenshi[i][tsuno]
    #     next_idenshi[i][tsuno] = next_idenshi[i][tsuno+1]
    #     next_idenshi[i][tsuno+1] = tmp



    for i in range(int(kotai*heni_rate)):
        point1 = random.randrange(route-1)  # 0から46の間で乱数を生成
        # 交叉する始点と終点を決める　randrange(start,stop)
        point2 = random.randrange(point1+1, route)  # point1+1から47の間で乱数を生成

        tmp_list = []

        for j in range(route):
            if(point1 <= j and j <= point2):
                tmp_list.append(next_idenshi[i][j])
                next_idenshi[i][j] = -1

        tmp_list.reverse()

        k = 0

        for j in range(route):
            if(next_idenshi[i][j] == -1):
                next_idenshi[i][j] = tmp_list[k]
                k+=1


    idenshi = next_idenshi  # 次の世代に引継ぎ

    # print(idenshi)
    idenshi[0] = elite  # エリートを保存する
    # print("-------------エリート保存されました-------------")
    # print(elite)
    # print(idenshi)


def main():
    print("-------------はじまり-------------")
    read_file()

    seisei()

    # evaluate()
    # selection()

    # PMX()

    for i in range(sedai):
        # print("■")
        evaluate()
        if(i % int(sedai*0.1) == 0):
            print(f'eva = {min(evaluation)}')

        selection()
        CX_method()
        totsuzen_next()

    evaluate()

    print("-------------最終的な遺伝子-------------")
    print(idenshi)


    tsuno = idenshi[evaluation.index(min(evaluation))]
    best_eval = evaluation[evaluation.index(min(evaluation))]
    # tsuno.sort()
    print("")
    print(evaluation.index(min(evaluation)))
    print(tsuno)

    print("最も良い評価")
    print(best_eval)

    # print("最終的な評価")
    # print(evaluation)


if __name__ == '__main__':
    main()
