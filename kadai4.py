import random
import math
import copy

particle_num = 50  # 粒子数
cycle = 200  # サイクル数
neighbour = 4  # 近傍数
c1 = 0.7  # 部分経路用の定数
c2 = 0.2  # 部分経路用の定数　0.7がいいらしいので

route = 48  # 巡回路

gbest = []  # グローバルベスト用のリスト
gbest_eval = 0  # グローバルベストの評価

particle = [[0] * route for i in range(particle_num)]  # 50個の粒子
# 50個の粒子(personal best用)
personal_best = [[0] * route for i in range(particle_num)]
local_best = [[0] * route for i in range(particle_num)]  # 50個の粒子(local best用)

solution = [0.0] * particle_num  # 初期化
solution_tmp = [0.0] * particle_num  # 初期化(personal best用)

# 都市の割り当て
route_map = []
for i in range(route):
    route_map.append(i)

print(len(particle))

x = []  # 都市のx座標
y = []  # 都市のy座標

# 部分経路用の評価関数
def evaluation(route_tmp):
    length = len(route_tmp)
    total_route = 0

    # print(route_tmp)

    for i in range(length):
        if(i == length-1):
            x1 = x[route_tmp[i]]
            x2 = x[route_tmp[0]]
            y1 = y[route_tmp[i]]
            y2 = y[route_tmp[0]]
        else:
            x1 = x[route_tmp[i]]
            x2 = x[route_tmp[i+1]]
            y1 = y[route_tmp[i]]
            y2 = y[route_tmp[i+1]]

            diff_x = x1-x2
            diff_y = y1-y2

            total_route += math.sqrt(diff_x**2 + diff_y**2)

    return total_route

# ファイル読み込み
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

# 粒子を生成する
def particle_gene():
    global particle
    print("-------------粒子群の生成-------------")
    # print(route_map)
    for i in range(particle_num):
        tmp = random.sample(route_map, route)
        # print(tmp)
        for j in range(route):
            particle[i][j] = tmp[j]

# 評価関数
def find_solution(now):  # 解を求めるやつ
    global solution
    global solution_tmp  # パーソナルベストを決めるために今の評価値と比べるやつ
    global gbest_eval

    solution = [0.0] * particle_num  # 初期化

    for i in range(particle_num):
        for j in range(route):
            if(j == route-1):
                x1 = x[particle[i][j]]
                x2 = x[particle[i][0]]
                y1 = y[particle[i][j]]
                y2 = y[particle[i][0]]
            else:
                x1 = x[particle[i][j]]
                x2 = x[particle[i][j+1]]
                y1 = y[particle[i][j]]
                y2 = y[particle[i][j+1]]

            diff_x = x1-x2
            diff_y = y1-y2

            solution[i] += math.sqrt(diff_x**2 + diff_y**2)

    # 最終的に解を見るときに使う？
    gbest = particle[solution.index(min(solution))]
    gbest_eval = solution[solution.index(min(solution))]

    # 最初のサイクル
    if(now == 0):
        solution_tmp = copy.deepcopy(solution)
        for j in range(particle_num):
            for k in range(route):
                personal_best[j][k] = particle[j][k]
    else:
        # それ以降のサイクル
        # pbestの更新
        for j in range(particle_num):
            if(solution_tmp[j] > solution[j]):
                for l in range(route):
                    personal_best[j][l] = particle[j][l]
    print(gbest_eval)

# ローカルベストを見つける関数
def find_local():
    # 共通経路で近傍を考えるのはめんどくさそうなので，とりあえず評価値が近いやつを近傍として考える
    global local_best
    # 50個の粒子(local best用)
    local_best_num = [[0] * route for i in range(particle_num)]

    # print("粒子ごとにローカルベストを見つけるやつ")

    local_best_you = []  # ソートするときの添え字用←粒子のもとの順番を考慮
    for i in range(particle_num):
        particle_tmp = (solution[i], i)  # (評価値，添え字)
        local_best_you.append(particle_tmp)

    # print(local_best_you)
    local_best_you.sort()
    # print(local_best_you)

    # 要確認
    for i in range(particle_num):
        local_best_num[local_best_you[i][1]] = local_best_you[int(i/4)][1]

    # print("local_best_num")
    # print(local_best_num)

    for i in range(particle_num):
        for j in range(route):
            local_best[i][j] = personal_best[local_best_num[i]][j]


# 部分経路の挿入アルゴリズム（PSOにおける，位置と速度の計算の部分を担当）
def insert_method():
    global particle
    next_particle = [[0] * route for i in range(particle_num)]  # 50個の粒子

    # print("挿入アルゴリズム")
    for i in range(particle_num):
        # 部分経路作成のための一様乱数
        r1 = int(random.random()/0.5)
        r2 = int(random.random()/0.5)
        # 抜き出す経路の数を指定
        personal_length = int(c1*r1*(route+1))
        local_length = int(c2*r2*(route+1))

        # 部分経路の初期化
        personal_route = []
        local_route = []
        for j in range(personal_length):
            personal_route.append(personal_best[i][j])
        for j in range(local_length):
            local_route.append(local_best[i][j])

        # パーソナルルートからローカルルートの共通部分を削除
        personal_route_dash = [
            j for j in personal_route if j not in local_route]
        # 粒子（経路）からパーソナルルートとローカルルートを削除
        particle_dash_tmp = [j for j in particle[i]
                             if j not in personal_route_dash]
        particle_dash = [j for j in particle_dash_tmp if j not in local_route]

        # print("particle_dash_tmp", len(particle_dash_tmp), particle_dash_tmp)
        # print("local_route", len(local_route), local_route)
        # print("particle_dash", particle_dash)

        # 挿入するリストを逆順にする必要がある
        personal_route_dash_reverse = copy.deepcopy(personal_route_dash)
        personal_route_dash_reverse.reverse()
        # print(personal_route_dash_reverse)
        local_route_reverse = copy.deepcopy(local_route)
        local_route_reverse.reverse()

        min_route = 1000000
        min_route_list = []  # 粒子に最も総経路が短くなるようにパーソナルベストを追加したやつ

        for j in range(len(particle_dash)):
            if(j == 0):
                tmp_route = personal_route_dash+particle_dash
                ans = evaluation(tmp_route)
                if(ans < min_route):
                    min_route = ans
                    min_route_list = copy.deepcopy(tmp_route)
            else:
                tmp_route = copy.deepcopy(particle_dash)
                for k in range(len(personal_route_dash)):
                    tmp_route.insert(j, personal_route_dash_reverse[k])
                ans = evaluation(tmp_route)
                if(ans < min_route):
                    min_route = ans
                    min_route_list = copy.deepcopy(tmp_route)

        min_route2 = 1000000
        min_route_list2 = []

        for j in range(len(min_route_list)):
            if(j == 0):
                tmp_route = min_route_list+local_route_reverse
                ans = evaluation(tmp_route)
                if(ans < min_route2):
                    min_route2 = ans
                    min_route_list2 = copy.deepcopy(tmp_route)
            else:
                tmp_route = copy.deepcopy(min_route_list)
                for k in range(len(local_route_reverse)):
                    tmp_route.insert(j, local_route_reverse[k])
                ans = evaluation(tmp_route)
                if(ans < min_route2):
                    min_route2 = ans
                    min_route_list2 = copy.deepcopy(tmp_route)

        if(len(min_route_list) == 0):
            for j in range(route):
                next_particle[i][j] = particle[i][j]
        else:
            for j in range(route):
                next_particle[i][j] = min_route_list2[j]

    particle = copy.deepcopy(next_particle)


def main():
    print("-------------はじまり-------------")
    read_file()

    particle_gene()
    for now in range(cycle):
        find_solution(now)
        find_local()
        insert_method()

    print("最終的な解", gbest_eval)
    print(solution)


if __name__ == '__main__':
    main()
