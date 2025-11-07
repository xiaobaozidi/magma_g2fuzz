<?php

enum Foo {
    case Bar;
    const Baz = Foo::Bar;
}

var_dump(unserialize('E:7:"Foo:Baz";'));

?>