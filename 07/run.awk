#!/usr/bin/env awk -f

# part of ls
$1 != "$" {
	size = $1 == "dir" ? 0 : $1
	dir = cwd "/" $2
	while ((dir = parent(dir))) fs[dir] += size
}

# cd into child dir
$2 == "cd" && $3 != ".." && $3 != "/" {
	if (cwd == "/") cwd = cwd $3
	cwd = cwd "/" $3
}

# cd ..
$2 == "cd" && $3 == ".." {
	cwd = parent(cwd)
}

END {
	need = 30000000 - (70000000 - fs["/"])
	for (k in fs) {
		if (fs[k] <= 100000) part1 += fs[k]
		if (fs[k] >= need && (! part2 || fs[k] < part2)) part2 = fs[k]
	}
	print part1
	print part2
}

# "/a/b/c" -> "/a/b"
function parent(path,   dirs, n) {
	if (path == "/") return
	n = split(path, dirs, "/")
	if (n == 2) return "/"
	path = ""
	for (i = 2; i < n; i++) path = path "/" dirs[i]
	return path
}
