def solve(x, coins, memo, computed, last_used):
    if x < 0:
        return float('inf')
    if x == 0:
        return 0
    if computed.get(x, False):
        return memo[x]

    best = float('inf')
    for coin in coins:
        res = solve(x - coin, coins, memo, computed, last_used)
        if res + 1 < best:
            best = res + 1
            last_used[x] = coin

    memo[x] = best
    computed[x] = True
    return best


def get_coin_combination(x, last_used):
    result = []
    while x > 0 and last_used[x] is not None:
        coin = last_used[x]
        result.append(coin)
        x -= coin
    return result