<?php

enum Suit {
    case Hearts;
    case Diamonds;
    case Clubs;
    case Spades;
    /** @deprecated Typo, use Suit::Hearts */
    const Hearst = self::Hearts;
}

var_dump(Suit::cases());

?>