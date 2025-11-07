<?php

register_shutdown_function(static function (): void {
    global $fiber;
    var_dump($fiber->getReturn());
});

$fiber = new Fiber(static function (): void {
    str_repeat('X', PHP_INT_MAX);
});
$fiber->start();

?>