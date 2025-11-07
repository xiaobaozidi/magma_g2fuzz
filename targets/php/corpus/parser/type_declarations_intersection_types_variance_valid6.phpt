<?php

interface X {}
interface Y {}
interface Z {}

class A {
    public function test(): X|Z {}
}
class B extends A {
    public function test(): X&Y {}
}

?>
===DONE===