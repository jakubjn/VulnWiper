<?php
declare(strict_types=1);

use DI\ContainerBuilder;
use Relay\Relay;
use FastRoute\RouteCollector;
use Middlewares\FastRoute;
use Middlewares\RequestHandler;
use Narrowspark\HttpEmitter\SapiEmitter;
use Laminas\Diactoros\Response;
use Laminas\Diactoros\ServerRequestFactory;
use function DI\create;
use function DI\get;
use function FastRoute\simpleDispatcher;

use SampleWebsite\Dbconnection;

use SampleWebsite\Main;
use SampleWebsite\EchoTest;
use SampleWebsite\Login;
use SampleWebsite\Account;
use SampleWebsite\HiddenPage;

require_once dirname(__DIR__) . '/vendor/autoload.php';

$connection = new Dbconnection("localhost", "webserver", "12345", "userdb");

$containerBuilder = new ContainerBuilder();
$containerBuilder->useAutowiring(false);
$containerBuilder->useAttributes(false);
$containerBuilder->addDefinitions([
    Main::class => create(Main::class),

    EchoTest::class => create(EchoTest::class),

    Login::class => create(Login::class)
        ->constructor(get('Dbconnection')),
            'Dbconnection' => function() {
                global $connection;
                return $connection;
            },

    Account::class => create(Account::class),

    HiddenPage::class => create(HiddenPage::class)
]);

$container = $containerBuilder->build();

$routes = simpleDispatcher(function (RouteCollector $r) {
    $r->get('/', Main::class);
    $r->get('/echo', EchoTest::class);
    $r->get('/login', Login::class);
    $r->get('/account', Account::class);
    $r->get('/xpl', HiddenPage::class);

    $r->post('/echo', EchoTest::class);
    $r->post('/login', Login::class);
});
 
$middlewareQueue[] = new FastRoute($routes);
$middlewareQueue[] = new RequestHandler($container);

$requestHandler = new Relay($middlewareQueue);
$response = $requestHandler->handle(ServerRequestFactory::fromGlobals());

$emitter = new SapiEmitter();
return $emitter->emit($response);




