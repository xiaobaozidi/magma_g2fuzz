<?php

interface X {}
interface Y {}
interface Z {}

class A implements X {}

class Collection {
    public X&Y $intersect;
}

function foo(): X&Y {
    return new A();
}

function bar(X&Y $o): void {
    var_dump($o);
}

try {
    $o = foo();
    var_dump($o);
} catch (\TypeError $e) {
    echo $e->getMessage(), "\n";
}

$c = new Collection();
$a = new A();

try {
    $c->intersect = $a;
} catch (\TypeError $e) {
    echo $e->getMessage(), "\n";
}

try {
    bar($a);
} catch (\TypeError $e) {
    echo $e->getMessage(), "\n";
}

?>