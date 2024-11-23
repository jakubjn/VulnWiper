<?php
if (isset($_GET['username'])) {
    $username = $_GET['username'];
    echo "Hello, " . $username;
}
