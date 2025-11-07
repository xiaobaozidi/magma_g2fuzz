<?php

enum Foo {
    case Bar;
    case Baz;
}

enum IntFoo: int {
    case Bar = 0;
    case Baz = 1;
}

var_dump((new ReflectionClass(Foo::class))->getProperties());
var_dump(Foo::Bar->name);

var_dump((new ReflectionClass(IntFoo::class))->getProperties());
var_dump(IntFoo::Bar->name);

?>