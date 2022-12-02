#!/usr/bin/awk -f

{
	gsub("A|X", 0)
	gsub("B|Y", 1)
	gsub("C|Z", 2)
	sum1 += score1($1, $2)
	sum2 += score2($1, $2)
}

END {
	print sum1
	print sum2
}

function score1(a, b, outcome, diff) {
	outcome = 0
	diff = b - a
	if (diff == 1 || diff == -2)
		outcome = 2
	else if (! diff)
		outcome = 1
	return b + 1 + outcome * 3
}

function score2(a, outcome, b, diff) {
	b = a
	if (outcome == 2)
		b = (a + 1) % 3
	else if (! outcome)
		b = (a + 2) % 3
	return b + 1 + outcome * 3
}
