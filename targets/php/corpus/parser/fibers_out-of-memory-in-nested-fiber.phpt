<?php

$fiber = new Fiber(function (): void {
    $fiber = new Fiber(function (): void {
        $buffer = '';
        while (true) {
            $buffer .= str_repeat('.', 1 << 10);
        }
    });

    $fiber->start();
});

$fiber->start();

?>