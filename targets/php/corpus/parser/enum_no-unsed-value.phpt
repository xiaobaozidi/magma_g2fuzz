<?php

enum Foo: int {
    case Bar = 0;
}

unset(Foo::Bar->value);

?>