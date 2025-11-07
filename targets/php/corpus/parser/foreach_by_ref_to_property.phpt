<?php
$obj = new stdClass;
foreach ([0] as &$obj->prop) {
    var_dump($obj->prop);
}
?>