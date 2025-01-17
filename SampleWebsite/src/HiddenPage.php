<?php
declare(strict_types=1);

namespace SampleWebsite;

use Psr\Http\Message\ResponseInterface;
use Laminas\Diactoros\Response;

class HiddenPage
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
                    <h1>This is a hidden directory!</h1>
                </body>
            </html>');
 
        return $response;
    }
}