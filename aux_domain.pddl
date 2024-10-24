(define (domain ncrm_example-domain)
 (:requirements :strips :typing)
 (:types
    tile - object
    ice pit wall - tile
 )
 (:predicates (at_ ?tile - tile) (down_of ?down - tile ?up - tile) (left_of ?left - tile ?right - tile))
 (:action down_to_pit_detdup_1
  :parameters ( ?src - ice ?dst1 - ice ?p - pit)
  :precondition (and (at_ ?src) (down_of ?dst1 ?src) (down_of ?p ?dst1))
  :effect (and (not (at_ ?src)) (at_ ?dst1)))
 (:action down_to_pit_detdup_2
  :parameters ( ?src - ice ?dst1 - ice ?p - pit)
  :precondition (and (at_ ?src) (down_of ?dst1 ?src) (down_of ?p ?dst1))
  :effect (and (not (at_ ?src)) (at_ ?p)))
 (:action down_to_wall
  :parameters ( ?src - ice ?dst1 - ice ?w - wall)
  :precondition (and (at_ ?src) (down_of ?dst1 ?src) (down_of ?w ?dst1))
  :effect (and (not (at_ ?src)) (at_ ?dst1)))
 (:action down_detdup_1
  :parameters ( ?src - ice ?dst1 - ice ?dst2 - ice)
  :precondition (and (at_ ?src) (down_of ?dst1 ?src) (down_of ?dst2 ?dst1))
  :effect (and (not (at_ ?src)) (at_ ?dst1)))
 (:action down_detdup_2
  :parameters ( ?src - ice ?dst1 - ice ?dst2 - ice)
  :precondition (and (at_ ?src) (down_of ?dst1 ?src) (down_of ?dst2 ?dst1))
  :effect (and (not (at_ ?src)) (at_ ?dst2)))
 (:action left_to_pit_detdup_1
  :parameters ( ?src - ice ?dst1 - ice ?p - pit)
  :precondition (and (at_ ?src) (left_of ?dst1 ?src) (left_of ?p ?dst1))
  :effect (and (not (at_ ?src)) (at_ ?dst1)))
 (:action left_to_pit_detdup_2
  :parameters ( ?src - ice ?dst1 - ice ?p - pit)
  :precondition (and (at_ ?src) (left_of ?dst1 ?src) (left_of ?p ?dst1))
  :effect (and (not (at_ ?src)) (at_ ?p)))
 (:action left_to_wall
  :parameters ( ?src - ice ?dst1 - ice ?w - wall)
  :precondition (and (at_ ?src) (left_of ?dst1 ?src) (left_of ?w ?dst1))
  :effect (and (not (at_ ?src)) (at_ ?dst1)))
 (:action left_detdup_1
  :parameters ( ?src - ice ?dst1 - ice ?dst2 - ice)
  :precondition (and (at_ ?src) (left_of ?dst1 ?src) (left_of ?dst2 ?dst1))
  :effect (and (not (at_ ?src)) (at_ ?dst1)))
 (:action left_detdup_2
  :parameters ( ?src - ice ?dst1 - ice ?dst2 - ice)
  :precondition (and (at_ ?src) (left_of ?dst1 ?src) (left_of ?dst2 ?dst1))
  :effect (and (not (at_ ?src)) (at_ ?dst2)))
 (:action right_to_pit_detdup_1
  :parameters ( ?src - ice ?dst1 - ice ?p - pit)
  :precondition (and (at_ ?src) (left_of ?src ?dst1) (left_of ?dst1 ?p))
  :effect (and (not (at_ ?src)) (at_ ?dst1)))
 (:action right_to_pit_detdup_2
  :parameters ( ?src - ice ?dst1 - ice ?p - pit)
  :precondition (and (at_ ?src) (left_of ?src ?dst1) (left_of ?dst1 ?p))
  :effect (and (not (at_ ?src)) (at_ ?p)))
 (:action right_to_wall
  :parameters ( ?src - ice ?dst1 - ice ?w - wall)
  :precondition (and (at_ ?src) (left_of ?src ?dst1) (left_of ?dst1 ?w))
  :effect (and (not (at_ ?src)) (at_ ?dst1)))
 (:action right_detdup_1
  :parameters ( ?src - ice ?dst1 - ice ?dst2 - ice)
  :precondition (and (at_ ?src) (left_of ?src ?dst1) (left_of ?dst1 ?dst2))
  :effect (and (not (at_ ?src)) (at_ ?dst1)))
 (:action right_detdup_2
  :parameters ( ?src - ice ?dst1 - ice ?dst2 - ice)
  :precondition (and (at_ ?src) (left_of ?src ?dst1) (left_of ?dst1 ?dst2))
  :effect (and (not (at_ ?src)) (at_ ?dst2)))
 (:action up_to_pit_detdup_1
  :parameters ( ?src - ice ?dst1 - ice ?p - pit)
  :precondition (and (at_ ?src) (down_of ?src ?dst1) (down_of ?dst1 ?p))
  :effect (and (not (at_ ?src)) (at_ ?dst1)))
 (:action up_to_pit_detdup_2
  :parameters ( ?src - ice ?dst1 - ice ?p - pit)
  :precondition (and (at_ ?src) (down_of ?src ?dst1) (down_of ?dst1 ?p))
  :effect (and (not (at_ ?src)) (at_ ?p)))
 (:action up_to_wall
  :parameters ( ?src - ice ?dst1 - ice ?w - wall)
  :precondition (and (at_ ?src) (down_of ?src ?dst1) (down_of ?dst1 ?w))
  :effect (and (not (at_ ?src)) (at_ ?dst1)))
 (:action up_detdup_1
  :parameters ( ?src - ice ?dst1 - ice ?dst2 - ice)
  :precondition (and (at_ ?src) (down_of ?src ?dst1) (down_of ?dst1 ?dst2))
  :effect (and (not (at_ ?src)) (at_ ?dst1)))
 (:action up_detdup_2
  :parameters ( ?src - ice ?dst1 - ice ?dst2 - ice)
  :precondition (and (at_ ?src) (down_of ?src ?dst1) (down_of ?dst1 ?dst2))
  :effect (and (not (at_ ?src)) (at_ ?dst2)))
)
