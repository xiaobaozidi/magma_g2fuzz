<?php

enum Foo: string {
    case Bar = 'bar';
    case Baz = 'baz';
}

echo Foo::Bar->value . "\n";
echo Foo::Baz->value . "\n";

?>