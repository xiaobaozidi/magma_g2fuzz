<?php

function create_fiber(): Fiber
{
    $fiber = new Fiber('create_fiber');
    $fiber->start();
    return $fiber;
}

$fiber = new Fiber('create_fiber');
$fiber->start();

?>