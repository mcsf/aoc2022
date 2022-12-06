#!/usr/bin/env awk -f

{
	print markIndex(4)
	print markIndex(14)
}

function markIndex(n) {
	for (i = 1; i <= length() - n + 1; i++) {
		s = substr($0, i, n)
		delete set
		for (j = 1; j <= length(s); j++) {
			set[substr(s, j, 1)] = 1
		}
		if (length(set) == n) {
			return i + n - 1
		}
	}
}
