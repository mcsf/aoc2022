#!/usr/bin/env awk -f

BEGIN {
	# Split records at paragraphs
	RS = "\n\n"; FS = "\n"

	# For part 2
	pipe = "sort -gr | head -n3 | awk '{sum+=$0} END{print sum}'"
}

{
	# Part 1
	sum = 0
	for (i = 1; i <= NF; i++) sum += $i
	if (sum > max) max = sum

	# Part 2
	print sum | pipe
}

END {
	print max
	close(pipe)
}
