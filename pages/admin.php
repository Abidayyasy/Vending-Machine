<?php
session_start();

// Simulasi login (jika belum login, redirect)
if (!isset($_SESSION['admin_logged_in'])) {
    $_SESSION['admin_logged_in'] = true; // Simulasi login tetap aktif
}

// Inisialisasi koin
if (!isset($_SESSION['stock'])) {
    $_SESSION['coins'] = [30, 3000, 4000];
    $_SESSION['stock'] = [20, 10, 11];
}
// print_r($_SESSION['coins']);
// Tangani form submit
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    for ($i = 0; $i < count($_SESSION['coins']); $i++) {
        $added = intval($_POST['add_' . $i] ?? 0);
        $_SESSION['stock'][$i] += $added;
    }
    $message = "Saldo koin berhasil diperbarui!";
}
?>

<!DOCTYPE html>
<html>
<head>
    <title>Admin Vending Machine</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
<nav class="navbar navbar-expand-lg navbar-dark bg-dark mb-4">
    <div class="container-fluid">
        <a class="navbar-brand" href="#">Vending Admin</a>
        <div class="d-flex">
            <a href="reset.php" class="btn btn-outline-light">Logout</a>
        </div>
    </div>
</nav>

<div class="container">
    <div class="card shadow-sm">
        <div class="card-body">
            <h3 class="card-title mb-3">Tambah Saldo Koin</h3>

            <?php if (isset($message)) : ?>
                <div class="alert alert-success"><?= $message ?></div>
            <?php endif; ?>

            <form method="POST">
                <table class="table table-bordered">
                    <thead class="table-light">
                        <tr>
                            <th>Jenis Koin</th>
                            <th>Stok Saat Ini</th>
                            <th>Tambah Saldo</th>
                        </tr>
                    </thead>
                    <tbody>
                        <?php foreach ($_SESSION['coins'] as $i => $coin): ?>
                            <tr>
                                <td>Koin <?= $coin ?></td>
                                <td><?= $_SESSION['stock'][$i] ?></td>
                                <td>
                                    <input type="number" class="form-control" name="add_<?= $i ?>" min="0" value="0">
                                </td>
                            </tr>
                        <?php endforeach; ?>
                    </tbody>
                </table>
                <button type="submit" class="btn btn-primary">Simpan Perubahan</button>
            </form>
        </div>
    </div>
</div>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
