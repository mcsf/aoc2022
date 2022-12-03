#!/bin/sh

test_day() {
	(
		day=$1
		cd "$day" || exit 2
		echo "$day"
		for runner in run*; do
			if [ -x "$runner" ]; then
				printf "  %s\t%s\n" "$runner" "$(pass_or_fail "$runner")"
			else
				printf "  %s\tnot executable\n" "$runner"
			fi
		done
	)
}

pass_or_fail() {
	runner="$1"
	if "./$runner" < input | diff - expected; then
		echo PASS
	else
		echo FAIL
	fi
}

cd "$(dirname "$0")" || exit 2
for day in */; do
	if [ -f "$day"/expected ]; then
		test_day "$day"
	else
		printf "%s\n  (skipped)\n" "$day"
	fi
done
