(define (problem ncrm_bw_5_1-problem)
 (:domain ncrm_bw_5_1-domain)
 (:objects
   l1 l2 l3 l4 l5 - location
   b1 b2 b3 b4 b5 - block
 )
 (:init (adjacent l0 l1) (adjacent l1 l10) (clear b2) (clear b5) (emptyhand) (on b1 b3) (on b2 b1) (on b5 b4) (on_table b3) (on_table b4))
 (:goal (and (emptyhand) (on_table b1) (on_table b2) (on_table b3) (on_table b4) (on_table b5) (clear b4) (clear b1) (clear b2) (clear b3) (clear b5)))
)
