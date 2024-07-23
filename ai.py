# 记录每局游戏智能体胜负情况的列表
# 0表示失败, 1表示胜利或平局
games = []

# 计算智能体近50局的成功率
# 参数res的值可能为'胜利','平局','失败'
def cal_rate(res):

# ===智能体胜利或平局,在games末尾添加元素1===
    if res != '失败':
        games.append(1)
# ===智能体失败,在games末尾添加元素0===
    else:
        games.append(0)

    # 切片截取后50局游戏记录
    game_50 = games[-50:]
    # 计算并返回成功率
    rate = game_50.count(1) / 50
    return rate
