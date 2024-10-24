(define (problem fr_6_9)
    (:domain first-response)
    (:objects
        l1 l2 l3 l4 l5 l6 - location
        v1 v2 v3 v4 v5 v6 v7 v8 v9 - victim
        m1 m2 - medical_unit
    )
    (:init
        (hospital l5)
        (hospital l2)
        (victim-at v1 l5)
        (victim-status v1 dying)
        (victim-at v2 l4)
        (victim-status v2 dying)
        (victim-at v3 l6)
        (victim-status v3 hurt)
        (victim-at v4 l5)
        (victim-status v4 hurt)
        (victim-at v5 l5)
        (victim-status v5 dying)
        (victim-at v6 l6)
        (victim-status v6 dying)
        (victim-at v7 l6)
        (victim-status v7 hurt)
        (victim-at v8 l1)
        (victim-status v8 hurt)
        (victim-at v9 l1)
        (victim-status v9 hurt)
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
        (adjacent l1 l4)
        (adjacent l4 l1)
        (adjacent l1 l5)
        (adjacent l5 l1)
        (adjacent l2 l3)
        (adjacent l3 l2)
        (adjacent l2 l4)
        (adjacent l4 l2)
        (adjacent l2 l5)
        (adjacent l5 l2)
        (adjacent l5 l3)
        (adjacent l3 l5)
        (adjacent l5 l4)
        (adjacent l4 l5)
        (adjacent l6 l1)
        (adjacent l1 l6)
        (adjacent l6 l2)
        (adjacent l2 l6)
        (adjacent l6 l3)
        (adjacent l3 l6)
        (adjacent l6 l4)
        (adjacent l4 l6)
        (medical-unit-at m1 l3)
        (medical-unit-at m2 l6)
    )
    (:goal
        (and
            (victim-status v1 healthy)
            (victim-status v2 healthy)
            (victim-status v3 healthy)
            (victim-status v4 healthy)
            (victim-status v5 healthy)
            (victim-status v6 healthy)
            (victim-status v7 healthy)
            (victim-status v8 healthy)
            (victim-status v9 healthy)
        )
    )
)
