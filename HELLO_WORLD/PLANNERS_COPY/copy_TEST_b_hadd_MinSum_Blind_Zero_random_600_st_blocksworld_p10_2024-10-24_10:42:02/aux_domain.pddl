(define (domain ncrm_bw_5_10-domain)
 (:requirements :strips :typing)
 (:types location block)
 (:constants
   l0 l10 - location
 )
 (:predicates (adjacent ?l1 - location ?l2 - location) (at_ ?b - block ?l - location) (clear ?x - block) (emptyhand) (faulty ?b - block ?l - location) (holding ?b - block) (on ?bm - block ?bf - block) (on_table ?x - block))
 (:action fix
  :parameters ( ?b - block ?l1 - location)
  :precondition (and (faulty ?b ?l1))
  :effect (and (at_ ?b ?l1) (not (faulty ?b ?l1))))
 (:action init_pick_up
  :parameters ( ?b1 - block ?b2 - block)
  :precondition (and (emptyhand) (clear ?b1) (on ?b1 ?b2))
  :effect (and (at_ ?b1 l0) (not (clear ?b1)) (clear ?b2) (not (emptyhand)) (not (on ?b1 ?b2))))
 (:action move_detdup_1
  :parameters ( ?b1 - block ?l1 - location ?l2 - location)
  :precondition (and (at_ ?b1 ?l1) (adjacent ?l1 ?l2))
  :effect (and (at_ ?b1 ?l2) (not (at_ ?b1 ?l1))))
 (:action move_detdup_2
  :parameters ( ?b1 - block ?l1 - location ?l2 - location)
  :precondition (and (at_ ?b1 ?l1) (adjacent ?l1 ?l2))
  :effect (and (faulty ?b1 ?l2) (not (at_ ?b1 ?l1))))
 (:action pick_tower_detdup_1
  :parameters ( ?b1 - block ?b2 - block ?b3 - block)
  :precondition (and (emptyhand) (on ?b1 ?b2) (on ?b2 ?b3))
  :effect (and (holding ?b2) (clear ?b3) (not (emptyhand)) (not (on ?b2 ?b3))))
 (:action pick_tower_detdup_2
  :parameters ( ?b1 - block ?b2 - block ?b3 - block)
  :precondition (and (emptyhand) (on ?b1 ?b2) (on ?b2 ?b3))
  :effect (and (emptyhand) (on ?b1 ?b2) (on ?b2 ?b3)))
 (:action pick_up_from_table_detdup_1
  :parameters ( ?b - block)
  :precondition (and (emptyhand) (clear ?b) (on_table ?b))
  :effect (and (emptyhand) (clear ?b) (on_table ?b)))
 (:action pick_up_from_table_detdup_2
  :parameters ( ?b - block)
  :precondition (and (emptyhand) (clear ?b) (on_table ?b))
  :effect (and (holding ?b) (not (emptyhand)) (not (on_table ?b))))
 (:action pick_up_detdup_1
  :parameters ( ?b1 - block)
  :precondition (and (at_ ?b1 l10))
  :effect (and (not (at_ ?b1 l10)) (holding ?b1)))
 (:action pick_up_detdup_2
  :parameters ( ?b1 - block)
  :precondition (and (at_ ?b1 l10))
  :effect (and (not (at_ ?b1 l10)) (clear ?b1) (on_table ?b1) (emptyhand) (not (holding ?b1))))
 (:action put_down
  :parameters ( ?b - block)
  :precondition (and (holding ?b))
  :effect (and (on_table ?b) (emptyhand) (clear ?b) (not (holding ?b))))
 (:action put_on_block_detdup_1
  :parameters ( ?b1 - block ?b2 - block)
  :precondition (and (holding ?b1) (clear ?b2))
  :effect (and (on ?b1 ?b2) (emptyhand) (clear ?b1) (not (holding ?b1)) (not (clear ?b2))))
 (:action put_on_block_detdup_2
  :parameters ( ?b1 - block ?b2 - block)
  :precondition (and (holding ?b1) (clear ?b2))
  :effect (and (on_table ?b1) (emptyhand) (clear ?b1) (not (holding ?b1))))
 (:action put_tower_down
  :parameters ( ?b1 - block ?b2 - block)
  :precondition (and (holding ?b2) (on ?b1 ?b2))
  :effect (and (on_table ?b2) (emptyhand) (not (holding ?b2))))
 (:action put_tower_on_block_detdup_1
  :parameters ( ?b1 - block ?b2 - block ?b3 - block)
  :precondition (and (holding ?b2) (on ?b1 ?b2) (clear ?b3))
  :effect (and (on ?b2 ?b3) (emptyhand) (not (holding ?b2)) (not (clear ?b3))))
 (:action put_tower_on_block_detdup_2
  :parameters ( ?b1 - block ?b2 - block ?b3 - block)
  :precondition (and (holding ?b2) (on ?b1 ?b2) (clear ?b3))
  :effect (and (on_table ?b2) (emptyhand) (not (holding ?b2))))
)
