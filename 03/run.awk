#!/usr/bin/env awk -f

BEGIN {
	FS = ""

	# Compute ord table for char operations
	for (n=0; n<256; n++) ord[sprintf("%c",n)] = n
}

# Part 1
{
	delete set
	for (i = 1; i <= NF / 2; i++) set[$i] = 1
	for (; i <= NF; i++) {
		if ($i in set) {
			sum1 += priority($i)
			break
		}
	}
}

# Part 2
(NR % 3) == 1 { delete set1; for (i = 1; i <= NF; i++) set1[$i] = 1 }
(NR % 3) == 2 { delete set2; for (i = 1; i <= NF; i++) set2[$i] = 1 }
(NR % 3) == 0 {
	for (i = 1; i <= NF; i++) {
		if ($i in set1 && $i in set2) {
			sum2 += priority($i)
			break
		}
	}
}

END {
	print sum1
	print sum2
}

function priority(c) {
	return ord[c] + 1 - (c < "a" ? ord["A"] - 26 : ord["a"])
}
