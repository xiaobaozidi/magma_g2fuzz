<?php

$fiber = new Fiber(function () {
    Fiber::suspend();
});
$fiber->start();

return new class ($fiber) {
    private $fiber;

    public function __construct(Fiber $fiber) {
        $this->fiber = $fiber;
    }

    public function __destruct() {
        $this->fiber->resume(1);
    }
};

?>