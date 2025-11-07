<?php

return new class () {
    public function __destruct() {
        $fiber = new Fiber(fn () => null);
        $fiber->start();
    }
};

?>