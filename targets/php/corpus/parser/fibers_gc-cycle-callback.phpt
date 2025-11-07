<?php

$ref = new class () {
    public $fiber;
    
    public function __destruct() {
        var_dump('DTOR');
    }
};

$fiber = new Fiber(function () use ($ref) {
    die('UNREACHABLE');
});

$ref->fiber = $fiber;

$fiber = null;
$ref = null;

var_dump('COLLECT CYCLES');
gc_collect_cycles();
var_dump('DONE');

?>