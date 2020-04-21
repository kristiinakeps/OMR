\version "2.20.0"
\score {
    \new Staff {
        \time 4/4
        \cadenzaOn
            c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8 \bar"|"
            d''8 e''8 f''8 g''8 b8 a8 g8 f8 \bar"|"
        \cadenzaOff
            c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8 \bar"|"
            d''8 e''8 f''8 g''8 b8 a8 g8 f8 \bar"|"
            c'8 c'8 c'8 c'8 c''8 c''8 c''8 c''8 \bar"|"
          \cadenzaOn
            c'16 d'16 e'16 f'16 g'16 a'16 b'16 c''16 \bar"|"
            d''16 e''16 f''16 g''16 b16 a16 g16 f16 \bar"|"
        \cadenzaOff
            c'16 d'16 e'16 f'16 g'16 a'16 b'16 c''16 \bar"|"
            d''16 e''16 f''16 g''16 b16 a16 g16 f16 \bar"|"
            c'16 c'16 c'16 c'16 c''16 c''16 c''16 c''16 \bar"|"
    }
}