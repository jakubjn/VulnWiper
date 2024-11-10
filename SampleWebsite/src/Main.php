<?php
declare(strict_types=1);

namespace SampleWebsite;

use Psr\Http\Message\ResponseInterface;

class Main
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
                    <h1>Welcome to my simple website!</h1>
                    <br>
                    <a href=/echo>Echo Test</a>
                    <br>
                    <a href=/login>Login Test</a>
                </body>
            </html>');
 
        return $response;
    }
}