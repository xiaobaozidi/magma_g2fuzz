<?php

interface X {}
interface Y {}

class TestOne implements X, Y {}

interface A
{
    public function foo(): X&Y;
}

interface B extends A
{
    public function foo(): TestOne|int;
}

?>