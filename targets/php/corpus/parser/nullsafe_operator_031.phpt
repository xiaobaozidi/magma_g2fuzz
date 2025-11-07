<?php

$val = null;
$ref =& $val;
var_dump($ref?->foo);

$val = new stdClass;
var_dump($ref?->foo);

?>