<?php
    $response = "What's the story";

    echo $_COOKIE;
    echo $response;

    echo "Search results for: " . htmlspecialchars($_GET['query']);
?>