#!/usr/bin/awk -f

# GAWK extensions might have made this slightly smoother, but this is fine too.

{
	for (i=1; i<=$2; i++) {
		step(knots02,  2, $1, visited02)
		step(knots10, 10, $1, visited10)
	}
}

END {
	print length(visited02)
	print length(visited10)
}

function step(knots, n, motion, visited) {
	move_head(knots, motion)
	follow(knots, n)
	visited[knots[n, 1], knots[n, 2]] = 1
}

function move_head(knots, motion,   coord) {
	coord = motion ~ /R|L/ ? 1 : 2
	knots[1, coord] += motion ~ /R|U/ ? 1 : -1
}

function follow(knots, n,   j) {
	for (j=1; j<n; j++) {
		if (is_touching(knots, j, j+1))
			continue
		if (knots[j, 1] != knots[j+1, 1])
			knots[j+1, 1] += (knots[j, 1] > knots[j+1, 1]) ? 1 : -1
		if (knots[j, 2] != knots[j+1, 2])
			knots[j+1, 2] += (knots[j, 2] > knots[j+1, 2]) ? 1 : -1
	}
}

function is_touching(knots, a, b) {
	return abs(knots[a, 1] - knots[b, 1]) <= 1 && abs(knots[a, 2] - knots[b, 2]) <= 1
}

function abs(n) {
	return n >= 0 ? n : -n
}
