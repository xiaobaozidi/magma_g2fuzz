<?php

#[Attribute(Attribute::TARGET_CLASS_CONSTANT)]
class EnumCaseAttribute {
    public function __construct(
        public string $value,
    ) {}
}

enum Foo {
    #[EnumCaseAttribute('Bar')]
    case Bar;
}

var_dump((new \ReflectionClassConstant(Foo::class, 'Bar'))->getAttributes(EnumCaseAttribute::class)[0]->newInstance());

?>