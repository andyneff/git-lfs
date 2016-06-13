package config

import (
	"fmt"
	"runtime"
	"strings"
)

var (
	GitCommit   string
	Version     = "1.2.0"
	VersionDesc string
)

func init() {
	gitCommit := strings.Split("$Id$", " ")[1][0:7]

	VersionDesc = fmt.Sprintf("git-lfs/%s (GitHub; %s %s; go %s; git %s)",
		Version,
		runtime.GOOS,
		runtime.GOARCH,
		strings.Replace(runtime.Version(), "go", "", 1),
		gitCommit,
	)

}
