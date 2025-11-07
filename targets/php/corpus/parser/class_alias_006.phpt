<?php

try {
    class_alias('stdclass', 'foo');
} catch (ValueError $exception) {
    echo $exception->getMessage() . "\n";
}

?>