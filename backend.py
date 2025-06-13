def solve_bounded(x, coins, stock, memo, used):
    key = (x, tuple(stock))
    if key in memo:
        return memo[key]

    if x == 0:
        return 0

    best = float('inf')
    best_choice = None

    for i, coin in enumerate(coins):
        if coin <= x and stock[i] > 0:
            stock[i] -= 1
            candidate = solve_bounded(x - coin, coins, stock, memo, used)
            stock[i] += 1

            if candidate != float('inf') and candidate + 1 < best:
                best = candidate + 1
                best_choice = i

    # ❗ Buat ulang key di akhir karena stock sudah berubah-ubah
    key = (x, tuple(stock))
    memo[key] = best
    used[key] = best_choice
    return best



def get_combination_bounded(x, coins, stock, used):
    result = [0] * len(coins)
    current_x = x
    current_stock = stock.copy()

    while current_x > 0:
        key = (current_x, tuple(current_stock))
        coin_index = used.get(key)

        if coin_index is None:
            return None  # tidak ada solusi

        result[coin_index] += 1
        current_x -= coins[coin_index]
        current_stock[coin_index] -= 1

    return result
