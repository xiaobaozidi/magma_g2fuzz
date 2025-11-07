<?php

class A {}

class_alias('A', 'B');
function foo(): A&B {}

?>
===DONE===