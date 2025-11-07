<?php

$fiber = new Fiber(function () {
    call_user_func(function () {
        $a = new class () {};

        $b = new class () {
            public function __destruct() {
                Fiber::suspend();
            }
        };

        $a->next = $b;
        $b->next = $a;
    });

    gc_collect_cycles();
});

$fiber->start();

?>