<?php
$error = $_GET['error'] ?? '';
if ($error) {
    echo "<div class='error'>Error: " . htmlspecialchars($error) . "</div>";
}