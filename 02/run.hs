#!/usr/bin/env runhaskell

-- Use of Enum
-- ===========
--
-- By making declaring these types as instances of Enum, we can easily extract
-- a numeric value from an abstract type, which is helpful in computing scores.
-- See `shapeScore`. Also, the numeric value acts as a bridge, allowing us to
-- "recast" a Variable as a Shape or a Outcome. See `recast`.

-- Use of Bounded
-- ==============
--
-- By making Shape an instance of Bounded, we can then treat the shape space as
-- a ring and define `succ'` to get the next shape, which conveniently tells us
-- who wins in a round. For example, `succ' Scissors` is `Rock`, which beats
-- Scissors.

data Shape = Rock | Paper | Scissors
    deriving (Read, Show, Eq, Enum, Bounded)

data Outcome = Lose | Draw | Win
    deriving (Show, Eq, Enum)

data Variable = X | Y | Z
    deriving (Read, Show, Enum)

-- Like `succ`, but treat the enum space as a ring
succ' :: (Eq a, Enum a, Bounded a) => a -> a
succ' x | x == maxBound = minBound
        | otherwise = succ x

-- Like `pred`, but treat the enum space as a ring
pred' :: (Eq a, Enum a, Bounded a) => a -> a
pred' x | x == minBound = maxBound
        | otherwise = pred x

-- "Recasts" a value, e.g. `recast Y :: Shape` is `Paper`
recast :: (Enum a, Enum b) => a -> b
recast = toEnum . fromEnum


--
-- Part 1
--

score :: Shape -> Shape -> Int
score s1 s2 = shapeScore + outcomeScore
    where shapeScore = fromEnum s2 + 1
          outcomeScore = fromEnum (outcome s1 s2) * 3

outcome :: Shape -> Shape -> Outcome
outcome s1 s2 | s2 == succ' s1 = Win
              | s2 == s1       = Draw
              | otherwise      = Lose

--
-- Part 2
--

score' :: Shape -> Outcome -> Int
score' s1 o = score s1 s2
    where s2 = case o of Win  -> succ' s1
                         Draw -> s1
                         Lose -> pred' s1

--
-- Parsing and IO
--

readLine :: String -> (Shape, Variable)
readLine (c1:_:c2:_) = (s1, s2)
    where s1 = toEnum $ fromEnum c1 - fromEnum 'A'
          s2 = read [c2]

main = do
    rounds <- fmap (map readLine . lines) getContents
    print $ sum $ map (\(a, b) -> score  a (recast b)) rounds
    print $ sum $ map (\(a, b) -> score' a (recast b)) rounds
