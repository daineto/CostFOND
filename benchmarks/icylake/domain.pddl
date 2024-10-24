;Header and description

(define (domain icylake)

;remove requirements that are not needed
(:requirements :strips :typing :non-deterministic)

(:types 
    tile - object
    ice wall pit - tile
)

; un-comment following line if constants are needed
(:constants 
    wall_tile - wall
    pit_tile - pit
)

(:predicates ;todo: define predicates here
    (at ?tile - tile)
    (left-of ?left - tile ?right - tile)
    (down-of ?down - tile ?up - tile)
)

;define actions here

(:action left
    :parameters (?src - ice ?dst1 - ice ?dst2 - ice)
    :precondition (and (at ?src) (left-of ?dst1 ?src) (left-of ?dst2 ?dst1))
    :effect (and
        (not (at ?src))
        (oneof (at ?dst1) (at ?dst2))
     )
)

(:action left-to-wall
    :parameters (?src - ice ?dst1 - ice)
    :precondition (and (at ?src) (left-of ?dst1 ?src) (left-of wall_tile ?dst1))
    :effect (and
        (not (at ?src)) (at ?dst1)
     )
)

(:action left-to-pit
    :parameters (?src - ice ?dst1 - ice)
    :precondition (and (at ?src) (left-of ?dst1 ?src) (left-of pit_tile ?dst1))
    :effect (and
        (not (at ?src))
        (oneof (at ?dst1) (at pit_tile))
     )
)

(:action right
    :parameters (?src - ice ?dst1 - ice ?dst2 - ice)
    :precondition (and (at ?src) (left-of ?src ?dst1) (left-of ?dst1 ?dst2))
    :effect (and
        (not (at ?src))
        (oneof (at ?dst1) (at ?dst2))
     )
)

(:action right-to-wall
    :parameters (?src - ice ?dst1 - ice)
    :precondition (and (at ?src) (left-of ?src ?dst1) (left-of ?dst1 wall_tile))
    :effect (and
        (not (at ?src)) (at ?dst1)
     )
)

(:action right-to-pit
    :parameters (?src - ice ?dst1 - ice)
    :precondition (and (at ?src) (left-of ?src ?dst1) (left-of ?dst1 pit_tile))
    :effect (and
        (not (at ?src))
        (oneof (at ?dst1) (at pit_tile))
     )
)

(:action down
    :parameters (?src - ice ?dst1 - ice ?dst2 - ice)
    :precondition (and (at ?src) (down-of ?dst1 ?src) (down-of ?dst2 ?dst1))
    :effect (and
        (not (at ?src))
        (oneof (at ?dst1) (at ?dst2))
     )
)

(:action down-to-wall
    :parameters (?src - ice ?dst1 - ice)
    :precondition (and (at ?src) (down-of ?dst1 ?src) (down-of wall_tile ?dst1))
    :effect (and
        (not (at ?src)) (at ?dst1)
     )
)

(:action down-to-pit
    :parameters (?src - ice ?dst1 - ice)
    :precondition (and (at ?src) (down-of ?dst1 ?src) (down-of pit_tile ?dst1))
    :effect (and
        (not (at ?src))
        (oneof (at ?dst1) (at pit_tile))
     )
)

(:action up
    :parameters (?src - ice ?dst1 - ice ?dst2 - ice)
    :precondition (and (at ?src) (down-of ?src ?dst1) (down-of ?dst1 ?dst2))
    :effect (and
        (not (at ?src))
        (oneof (at ?dst1) (at ?dst2))
     )
)

(:action up-to-wall
    :parameters (?src - ice ?dst1 - ice)
    :precondition (and (at ?src) (down-of ?src ?dst1) (down-of ?dst1 wall_tile))
    :effect (and
        (not (at ?src)) (at ?dst1)
     )
)

(:action up-to-pit
    :parameters (?src - ice ?dst1 - ice)
    :precondition (and (at ?src) (down-of ?src ?dst1) (down-of ?dst1 pit_tile))
    :effect (and
        (not (at ?src))
        (oneof (at ?dst1) (at pit_tile))
     )
)


)