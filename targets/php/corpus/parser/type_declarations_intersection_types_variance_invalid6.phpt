<?php

// Let Y and Z be loadable.
interface Y {}
interface Z {}

class Test {
    function method(): X&Y {}
}
class Test2 extends Test {
    function method(): Y&Z {}
}

?>
===DONE===