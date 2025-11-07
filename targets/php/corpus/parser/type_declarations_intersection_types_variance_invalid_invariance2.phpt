<?php

interface X {}
interface Y {}
class A implements X, Y {}

class Test {
    public X&Y $prop;
}
class Test2 extends Test {
    public A $prop;
}

?>
===DONE===