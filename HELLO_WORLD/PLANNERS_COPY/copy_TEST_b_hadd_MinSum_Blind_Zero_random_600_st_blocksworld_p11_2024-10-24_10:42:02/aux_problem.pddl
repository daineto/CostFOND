(define (problem ncrm_bw_10_11-problem)
 (:domain ncrm_bw_10_11-domain)
 (:objects
   l1 l2 l3 l4 l5 - location
   b1 b10 b2 b3 b4 b5 b6 b7 b8 b9 - block
 )
 (:init (adjacent l0 l10) (clear b1) (clear b3) (clear b6) (clear b7) (clear b8) (emptyhand) (on b1 b9) (on b2 b4) (on b5 b2) (on b7 b5) (on b8 b10) (on_table b10) (on_table b3) (on_table b4) (on_table b6) (on_table b9))
 (:goal (and (emptyhand) (on_table b1) (on_table b2) (on_table b3) (on_table b4) (on_table b5) (on_table b6) (on_table b7) (on_table b8) (on_table b9) (on_table b10) (clear b4) (clear b1) (clear b2) (clear b3) (clear b5) (clear b6) (clear b7) (clear b8) (clear b9) (clear b10)))
)
