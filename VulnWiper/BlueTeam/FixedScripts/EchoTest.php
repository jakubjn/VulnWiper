<?php
declare(strict_types=1);

namespace SampleWebsite;

use Psr\Http\Message\ResponseInterface;
use Laminas\Diactoros\Response;

class EchoTest
{
    private $response;

    public function __construct() {
        $this->response = new Response();
    }

    public function __invoke(): ResponseInterface
    {
        $response = $this->response->withHeader('Content-Type', 'text/html');
        $response->getBody()
            ->write('
            <html>
                <body>
                    <h1>Echo Test!</h1>
                    <br>
                    <form method="POST">
                        <input type="text" name="input">
                        <input type="submit">
                        <br>
                    </form>
                </body>
            </html>');

        if($_SERVER['REQUEST_METHOD'] == "POST") {
            $input = $_POST['input'];
            echo $input;
        }
 
        return $response;
    }
}