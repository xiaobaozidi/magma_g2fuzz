<?php

interface A {}
interface B {}

class Test implements A, B {}

class Foo {
    public function foo(): A&B {
        return new Test();
    }
}

/* This fails because just A larger than A&B */
class FooChild extends Foo {
    public function foo(): A {
        return new Test();
    }
}

?>