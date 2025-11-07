<?php

$b = 'test';
$fn = function () use (
    $b,
    &$a,
) {
    $a = $b;
};
$fn();
echo "$a\n";
?>