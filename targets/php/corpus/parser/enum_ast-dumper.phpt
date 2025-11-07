<?php

try {
    assert((function () {
        enum Foo {
            case Bar;
        }

        #[EnumAttr]
        enum IntFoo: int {
            #[CaseAttr]
            case Bar = 1 << 0;
            case Baz = 1 << 1;

            public function self() {
                return $this;
            }
        }

        return false;
    })());
} catch (Error $e) {
    echo $e->getMessage();
}

?>