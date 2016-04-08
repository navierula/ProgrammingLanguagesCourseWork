---------------------------------------------------------------------
--
-- CAS CS 320, Fall 2015
-- Assignment 5 (skeleton code)
-- SuperString.hs
-- Navraj Narula

module SuperString where

import Data.List (isPrefixOf)
import Graph
import Algorithm

data SuperString =
    SuperStr String [String]
  deriving (Eq, Show)



-- To merge two strings, take the longest suffix of the first string
-- that overlaps with the second, and replace it with the second string.
merge :: String -> String -> String
merge (x:xs) ys  = if isPrefixOf (x:xs) ys then ys else x:(merge xs ys)
merge []     ys  = ys

instance Ord SuperString where
--   ... Complete for Problem #2, part (a) ...
    SuperStr a _ < SuperStr b _ = length(a) < length(b)
    SuperStr a _ <= SuperStr b _ = length(a) <= length(b)
-- write more comparisons

instance State SuperString where
    outcome (SuperStr x []) = True
    outcome (SuperStr x _) = False
    choices (SuperStr a (x:k)) = (SuperStr (merge a x) k , SuperStr (merge x a) k)



--eof