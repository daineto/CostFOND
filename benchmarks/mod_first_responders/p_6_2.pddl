(define (problem fr_6_2)
    (:domain first-response)
    (:objects
        l1 l2 l3 l4 l5 l6 - location
        v1 v2 - victim
        m1 m2 m3 - medical_unit
    )
    (:init
        (hospital l4)
        (hospital l6)
        (hospital l3)
        (victim-at v1 l5)
        (victim-status v1 hurt)
        (victim-at v2 l5)
        (victim-status v2 hurt)
        (adjacent l1 l1)
        (adjacent l2 l2)
        (adjacent l3 l3)
        (adjacent l4 l4)
        (adjacent l5 l5)
        (adjacent l6 l6)
        (adjacent l1 l2)
        (adjacent l2 l1)
        (adjacent l1 l3)
        (adjacent l3 l1)
        (adjacent l2 l3)
        (adjacent l3 l2)
        (adjacent l3 l4)
        (adjacent l4 l3)
        (adjacent l3 l5)
        (adjacent l5 l3)
        (adjacent l5 l1)
        (adjacent l1 l5)
        (adjacent l5 l2)
        (adjacent l2 l5)
        (adjacent l6 l1)
        (adjacent l1 l6)
        (adjacent l6 l2)
        (adjacent l2 l6)
        (medical-unit-at m1 l6)
        (medical-unit-at m2 l3)
        (medical-unit-at m3 l5)
    )
    (:goal
        (and
            (victim-status v1 healthy)
            (victim-status v2 healthy)
        )
    )
)
