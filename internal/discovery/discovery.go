// Package discovery exposes non-sensitive local node capabilities.
package discovery

import (
	"crypto/rand"
	"encoding/hex"
	"runtime"
	"sort"
	"sync"
)

// Capabilities is safe for local diagnostics and synthetic public evidence.
type Capabilities struct {
	NodeID       string   `json:"node_id"`
	OS           string   `json:"os"`
	Architecture string   `json:"architecture"`
	CPUThreads   int      `json:"cpu_threads"`
	Capabilities []string `json:"capabilities"`
}

var (
	identifierOnce sync.Once
	identifier     string
	identifierErr  error
)

// Discover returns a privacy-minimised capability record.
func Discover() (Capabilities, error) {
	nodeIdentifier, err := processIdentifier()
	if err != nil {
		return Capabilities{}, err
	}

	capabilities := []string{
		"system.health",
		"system.inventory.minimised",
	}
	if runtime.GOOS == "linux" {
		capabilities = append(capabilities, "runtime.nixos-candidate")
	}
	sort.Strings(capabilities)

	return Capabilities{
		NodeID:       nodeIdentifier,
		OS:           runtime.GOOS,
		Architecture: runtime.GOARCH,
		CPUThreads:   runtime.NumCPU(),
		Capabilities: capabilities,
	}, nil
}

// processIdentifier is random for each process. It is stable long enough to
// correlate local health calls without creating a persistent hostname-derived
// fingerprint in logs or public evidence.
func processIdentifier() (string, error) {
	identifierOnce.Do(func() {
		material := make([]byte, 8)
		if _, err := rand.Read(material); err != nil {
			identifierErr = err
			return
		}
		identifier = "ephemeral-" + hex.EncodeToString(material)
	})
	return identifier, identifierErr
}
