#!/usr/bin/env awk -f

BEGIN {
	FS = "-|,"
}

contains($1, $2, $3, $4) || contains($3, $4, $1, $2) {
	pt1++
}

overlaps($1, $2, $3, $4) || overlaps($3, $4, $1, $2) {
	pt2++
}

END {
	print pt1
	print pt2
}

function contains(a, b, c, d) {
	return a <= c && d <= b
}

function overlaps(a, b, c, d) {
	return (a <= c && c <= b) \
		|| (a <= d && d <= b)
}
