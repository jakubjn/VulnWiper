<form action="search.php" method="post">
    <input type="text" name="query" placeholder="Search...">
    <input type="submit" value="Search">
</form>

<?php
    $_test = "Hello";
    echo "Search results for: " . $_POST['query'];
?>