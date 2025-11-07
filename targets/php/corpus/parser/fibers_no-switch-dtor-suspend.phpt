<?php

$fiber = new Fiber(function () {
    $a = new class () {
        public function __destruct() {
            Fiber::suspend();
        }
    };
});

$fiber->start();

?>