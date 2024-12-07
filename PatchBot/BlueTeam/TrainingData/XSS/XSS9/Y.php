<html>
    <body>
        <h1>Echo Test!</h1>
        <br>

        <form method="GET">
            <input type="text" name="username">
            <input type="submit">
            <br>
        </form>
    </body>
</html>

<?php
    $data = [
        "username" => htmlspecialchars($_GET['username'])
    ];

    header('Content-Type: application/json');
    echo json_encode($data);
?>