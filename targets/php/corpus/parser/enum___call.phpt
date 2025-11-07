<?php

enum Foo {
    case Bar;

    public function __call(string $name, array $args)
    {
        return [$name, $args];
    }
}

var_dump(Foo::Bar->baz('qux', 'quux'));

?>