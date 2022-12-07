#!/usr/bin/env awk -f

# part of ls
$1 != "$" {
	size = $1 == "dir" ? 0 : $1
	dir = cwd
	do fs[dir] += size
	while (dir = parent(dir))
}

# cd into child dir
$2 == "cd" && $3 != ".." && $3 != "/" {
	cwd = (cwd == "/" ? "" : cwd) "/" $3
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
	path = "/"
	for (i = 1; i < n; i++) if (dirs[i]) path = path "/" dirs[i]
	return path
}
