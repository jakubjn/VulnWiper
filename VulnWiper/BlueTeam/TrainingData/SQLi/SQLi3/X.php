<?php

$user_id = $_GET['user_id']; 

$query = "DELETE FROM users WHERE id = $user_id";
$db->query($query);

echo "User deleted successfully!";