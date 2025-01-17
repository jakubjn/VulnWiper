<?php
declare(strict_types=1);

namespace SampleWebsite;

use Laminas\Diactoros\Response;
use Psr\Http\Message\ResponseInterface;

use mysqli;
use SampleWebsite\Dbconnection;

class Login
{
    private $response;
    private $dbconnection;

    public function __construct(Dbconnection $dbconnection) {
        $this->response = new Response();
        $this->dbconnection = $dbconnection;
    }

    public function __invoke(): ResponseInterface
    {
        if($_SERVER['REQUEST_METHOD'] == "POST") {
            $connection = $this->dbconnection->get_Connection();

            $username = $_POST['username'];
            $password = $_POST['password'];

            $result = mysqli_query($connection, "SELECT username, password FROM users WHERE username='$username' AND password='$password'");

            if (mysqli_num_rows($result) > 0) {
                $response = new Response('php://memory', 301, ['Location' => '/account']);
                return $response;
            } else {
                $response = new Response('php://memory', 403);
                $response->getBody()->write('<h3>Invalid Username/Password</h3>');
                return $response;
            }
        } 

        $response = $this->response->withHeader('Content-Type', 'text/html');
        $response->getBody()
            ->write('
            <html>
                <body>
                    <h1>Login</h1>
                    <br>
                    <form method="POST">
                        Username: <input type="text" name="username">
                        <br>
                        <br>
                        Password: <input type="text" name="password">
                        <br>
                        <br>
                        <input type="submit">
                    </form>
                </body>
            </html>');
 
        return $response;
    }
}