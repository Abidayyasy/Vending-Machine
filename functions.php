<?php

function solve_bounded($x, $coins, $stock, &$memo, &$used) {
    $key = $x . '-' . implode(',', $stock);
    if (isset($memo[$key])) {
        return $memo[$key];
    }

    if ($x === 0) {
        return 0;
    }

    $best = INF;
    $best_choice = null;

    for ($i = 0; $i < count($coins); $i++) {
        $coin = $coins[$i];
        if ($coin <= $x && $stock[$i] > 0) {
            $stock[$i]--; // pakai koin
            $candidate = solve_bounded($x - $coin, $coins, $stock, $memo, $used);
            $stock[$i]++; // backtrack

            if ($candidate !== INF && $candidate + 1 < $best) {
                $best = $candidate + 1;
                $best_choice = $i;
            }
        }
    }

    $memo[$key] = $best;
    $used[$key] = $best_choice;
    return $best;
}

function get_combination_bounded($x, $coins, $stock, $used) {
    $result = array_fill(0, count($coins), 0);
    $current_x = $x;
    $current_stock = $stock;

    while ($current_x > 0) {
        $key = $current_x . '-' . implode(',', $current_stock);
        if (!isset($used[$key])) {
            return null; // tidak ada solusi
        }

        $coin_index = $used[$key];
        $result[$coin_index]++;
        $current_x -= $coins[$coin_index];
        $current_stock[$coin_index]--;
    }

    return $result;
}

// ======= CONTOH PENGGUNAAN =======

$coins = [1, 3, 4];
$stock = [20, 10, 11]; // jumlah tiap koin
$target = 6;

$memo = [];
$used = [];

$min_koin = solve_bounded($target, $coins, $stock, $memo, $used);
$kombinasi = get_combination_bounded($target, $coins, $stock, $used);

if ($kombinasi !== null && $min_koin !== INF) {
    echo "Jumlah koin minimum: $min_koin<br>";
    echo "Kombinasi koin terbaik:<br>";
    for ($i = 0; $i < count($coins); $i++) {
        echo "  Koin {$coins[$i]}: {$kombinasi[$i]} buah<br>";
    }
} else {
    echo "Tidak ada kombinasi yang memungkinkan.<br>";
}
?>
