#!/usr/bin/env runhaskell

import Data.Char (isDigit)

main = do
    pairs <- fmap parsePair getContents
    print $ length $ filter (bothWays contains) pairs
    print $ length $ filter (bothWays overlaps) pairs

contains :: [Int] -> Bool
contains (a:b:c:d:_) = a <= c && d <= b

overlaps :: [Int] -> Bool
overlaps (a:b:c:d:_) = (a <= c && c <= b) || (a <= d && d <= b)

bothWays :: ([a] -> Bool) -> [a] -> Bool
bothWays f xs@(a:b:c:d:_) = (f xs) || (f [c, d, a, b])

parsePair :: String -> [[Int]]
parsePair = map (map read . words . replacePuntuation) . lines
    where replacePuntuation s = [if isDigit c then c else ' ' | c <- s]
