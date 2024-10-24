(define (problem example) (:domain icylake)
(:objects 
    tile_0_5 tile_1_5 tile_2_5 tile_3_5 tile_5_5 - ice
    tile_0_4 tile_2_4 tile_3_4 tile_4_4 tile_5_4 - ice
    tile_0_3 tile_1_3 tile_2_3 tile_3_3 tile_5_3 - ice
    tile_0_2 tile_1_2 tile_2_2 tile_3_2 tile_4_2 tile_5_2 - ice
    tile_0_1 tile_3_1 tile_5_1 - ice
    tile_0_0 tile_1_0 tile_2_0 tile_3_0 tile_4_0 tile_5_0 - ice
)

(:init
    (at tile_0_5)

    (left-of wall_tile tile_0_5) (left-of tile_0_5 tile_1_5) (left-of tile_1_5 tile_2_5) (left-of tile_2_5 tile_3_5) (left-of tile_3_5 pit_tile) (left-of pit_tile tile_5_5) (left-of tile_5_5 wall_tile)
    (left-of wall_tile tile_0_4) (left-of tile_0_4 pit_tile) (left-of pit_tile tile_2_4) (left-of tile_2_4 tile_3_4) (left-of tile_3_4 tile_4_4) (left-of tile_4_4 tile_5_4) (left-of tile_5_4 wall_tile)
    (left-of wall_tile tile_0_3) (left-of tile_0_3 tile_1_3) (left-of tile_1_3 tile_2_3) (left-of tile_2_3 tile_3_3) (left-of tile_3_3 pit_tile) (left-of pit_tile tile_5_3) (left-of tile_5_3 wall_tile)
    (left-of wall_tile tile_0_2) (left-of tile_0_2 tile_1_2) (left-of tile_1_2 tile_2_2) (left-of tile_2_2 tile_3_2) (left-of tile_3_2 tile_4_2) (left-of tile_4_2 tile_5_2) (left-of tile_5_2 wall_tile)
    (left-of wall_tile tile_0_1) (left-of tile_0_1 wall_tile) (left-of wall_tile wall_tile) (left-of wall_tile tile_3_1) (left-of tile_3_1 pit_tile) (left-of pit_tile tile_5_1) (left-of tile_5_1 wall_tile)
    (left-of wall_tile tile_0_0) (left-of tile_0_0 tile_1_0) (left-of tile_1_0 tile_2_0) (left-of tile_2_0 tile_3_0) (left-of tile_3_0 tile_4_0) (left-of tile_4_0 tile_5_0) (left-of tile_5_0 wall_tile)

    (down-of tile_0_5 wall_tile) (down-of tile_1_5 wall_tile) (down-of tile_2_5 wall_tile) (down-of tile_3_5 wall_tile) (down-of pit_tile wall_tile) (down-of tile_5_5 wall_tile) 
    (down-of tile_0_4 tile_0_5) (down-of pit_tile tile_1_5) (down-of tile_2_4 tile_2_5) (down-of tile_3_4 tile_3_5) (down-of tile_4_4 pit_tile) (down-of tile_5_4 tile_5_5)
    (down-of tile_0_3 tile_0_4) (down-of tile_1_3 pit_tile) (down-of tile_2_3 tile_2_4) (down-of tile_3_3 tile_3_4) (down-of pit_tile tile_4_4) (down-of tile_5_3 tile_5_4)
    (down-of tile_0_2 tile_0_3) (down-of tile_1_2 tile_1_3) (down-of tile_2_2 tile_2_3) (down-of tile_3_2 tile_3_3) (down-of tile_4_2 pit_tile) (down-of tile_5_2 tile_5_3)
    (down-of tile_0_1 tile_0_2) (down-of wall_tile tile_1_2) (down-of wall_tile tile_2_2) (down-of tile_3_1 tile_3_2) (down-of pit_tile tile_4_2) (down-of tile_5_1 tile_5_2)
    (down-of tile_0_0 tile_0_1) (down-of tile_1_0 wall_tile) (down-of tile_2_0 wall_tile) (down-of tile_3_0 tile_3_1) (down-of tile_4_0 pit_tile) (down-of tile_5_0 tile_5_1)
    (down-of wall_tile tile_0_0) (down-of wall_tile tile_1_0) (down-of wall_tile tile_2_0) (down-of wall_tile tile_3_0) (down-of wall_tile tile_4_0) (down-of wall_tile tile_5_0)
)

(:goal (and
    (at tile_5_5)
))
)
