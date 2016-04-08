---------------------------------------------------------------------
--
-- CAS CS 320, Fall 2015
-- Assignment 5 (skeleton code)
-- BinPacking.hs
-- Navraj Narula

module BinPacking where


import Graph
import Algorithm

type Item = Integer
type Bin = Integer

data BinPacking =
    BinPack Bin Bin [Item]
  deriving (Eq, Show)


-- instance Ord BinPacking where
--   ... Complete for Problem #1, part (a) ...
instance Ord BinPacking where
    BinPack x y _ < BinPack a b _ = abs(x-y) < abs(a-b) 
    BinPack x y _ <= BinPack a b _ = abs(x-y) <= abs(a-b)

-- instance State BinPacking where
--   ... Complete for Problem #1, part (b) ...  
instance State BinPacking where
    outcome (BinPack x y []) = True
    outcome (BinPack x y _) = False
    choices (BinPack a b (x:k)) = ((BinPack (a + x) b k), (BinPack a (b + x) k))




--eof