<?php

class TestClass
{
    function __toString()
    {
        return "Foo";
    }
}

define("Bar", new TestClass);
var_dump(Bar);

try {
    define("Baz", new stdClass);
} catch (TypeError $exception) {
    echo $exception->getMessage() . "\n";
}

try {
    var_dump(Baz);
} catch (Error $exception) {
    echo $exception->getMessage() . "\n";
}

?>