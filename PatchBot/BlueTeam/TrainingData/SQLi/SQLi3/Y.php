<?php

$user_id = $_GET['user_id']; 

$stmt = $db->prepare("DELETE FROM users WHERE id = ?");
$stmt->bind_param("i", $user_id);
$stmt->execute();

echo "User deleted successfully!";