<?php

try {
    define('foo', new stdClass);
} catch (TypeError $exception) {
    echo $exception->getMessage() . "\n";
}

try {
    var_dump(foo);
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}

define('foo', fopen(__FILE__, 'r'));
var_dump(foo);

?>