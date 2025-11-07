<?php

class Foo {
    public $bar;
}

class Bar {
    public $baz;
}

$foo = new Foo();
$foo->bar = new Bar();

[$foo?->bar->baz] = ['bar'];
var_dump($foo);

?>