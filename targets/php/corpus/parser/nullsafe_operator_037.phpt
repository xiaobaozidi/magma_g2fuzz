<?php

$foo = new stdClass();
$foo->bar = 'bar';

$array = ['foo' => ['bar' => 'baz']];

var_dump($array['foo'][$foo?->bar]);

?>