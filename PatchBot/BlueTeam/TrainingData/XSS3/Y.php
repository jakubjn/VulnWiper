<?php
if (isset($_GET['username'])) {
    $username = htmlspecialchars($_GET['username']);
    echo "Hello, " . $username;
}