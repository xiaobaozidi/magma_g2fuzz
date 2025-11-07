<?php

set_error_handler(function($_, $m) {
    throw new Exception($m);
});

try {
    $foo?->foo;
} catch (Exception $e) {
    echo $e->getMessage(), "\n";
}

?>