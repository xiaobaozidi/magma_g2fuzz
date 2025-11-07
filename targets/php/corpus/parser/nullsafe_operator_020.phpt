<?php

class Foo {
    public $bar;
}

function bar() {
    var_dump('called');
}

$foo = null;
$foo?->bar->baz = bar();

?>