(define (problem fr_4_2)
    (:domain first-response)
    (:objects
        l1 l2 l3 l4 - location
        v1 v2 - victim
        m1 m2 m3 m4 - medical_unit
    )
    (:init
        (hospital l1)
        (hospital l2)
        (victim-at v1 l3)
        (victim-status v1 hurt)
        (victim-at v2 l3)
        (victim-status v2 hurt)
        (adjacent l1 l1)
        (adjacent l2 l2)
        (adjacent l3 l3)
        (adjacent l4 l4)
        (adjacent l1 l2)
        (adjacent l2 l1)
        (adjacent l1 l3)
        (adjacent l3 l1)
        (adjacent l4 l1)
        (adjacent l1 l4)
        (adjacent l4 l2)
        (adjacent l2 l4)
        (medical-unit-at m1 l3)
        (medical-unit-at m2 l3)
        (medical-unit-at m3 l4)
        (medical-unit-at m4 l4)
    )
    (:goal
        (and
            (victim-status v1 healthy)
            (victim-status v2 healthy)
        )
    )
)
