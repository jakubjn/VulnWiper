<?php

$search = $_GET['search']; 

$query = "SELECT * FROM products WHERE name LIKE '%$search%'";

$result = $db->query($query);

while ($row = $result->fetch_assoc()) {
    echo "Product: " . $row['name'] . "<br>";
}