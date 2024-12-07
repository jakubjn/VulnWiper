<?php

$search = $_GET['search']; 

$stmt = $db->prepare("SELECT * FROM products WHERE name LIKE ?");
$search = "%$search%";
$stmt->bind_param("s", $search);
$stmt->execute();

$result = $stmt->get_result();

while ($row = $result->fetch_assoc()) {
    echo "Product: " . htmlspecialchars($row['name']) . "<br>";
}