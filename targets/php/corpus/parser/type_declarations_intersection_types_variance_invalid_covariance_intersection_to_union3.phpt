<?php

interface X {}
interface Y {}
interface Z extends Y {}

class TestOne implements X, Z {}
class TestTwo implements X, Y {}

interface A
{
    public function foo(): X&Z;
}

interface B extends A
{
    public function foo(): TestOne|TestTwo;
}

?>