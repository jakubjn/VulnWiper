<?php
declare(strict_types=1);

namespace SampleWebsite;

use Psr\Http\Message\ResponseInterface;

class Account
{
    private $response;

    public function __construct(ResponseInterface $response) {
        $this->response = $response;
    }

    public function __invoke(): ResponseInterface
    {
        $response = $this->response->withHeader('Content-Type', 'text/html');
        $response->getBody()
            ->write('
            <html>
                <body>
                    <h1>Welcome to the account page!</h1>
                    <br>
                    <a href=/>Logout</a>
                </body>
            </html>');
 
        return $response;
    }
}