<?php
    if($_SERVER['REQUEST_METHOD'] == "POST") {
        echo "Search results for: " . $_POST['query'];
    }
?>