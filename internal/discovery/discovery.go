// Package discovery exposes non-sensitive local node capabilities.
// Пакет discovery предоставляет нечувствительные возможности локального узла.
package discovery

import (
	"crypto/sha256"
	"encoding/hex"
	"os"
	"runtime"
	"sort"
	"strings"
)

// Capabilities is safe for local diagnostics and public test fixtures.
// Capabilities безопасна для локальной диагностики и публичных test fixtures.
type Capabilities struct {
	NodeID       string   `json:"node_id"`
	OS           string   `json:"os"`
	Architecture string   `json:"architecture"`
	CPUThreads   int      `json:"cpu_threads"`
	Capabilities []string `json:"capabilities"`
}

// Discover returns a privacy-minimised capability record.
// Discover возвращает минимизированную с точки зрения приватности запись возможностей.
func Discover() (Capabilities, error) {
	hostname, err := os.Hostname()
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
		NodeID:       nodeID(hostname),
		OS:           runtime.GOOS,
		Architecture: runtime.GOARCH,
		CPUThreads:   runtime.NumCPU(),
		Capabilities: capabilities,
	}, nil
}

// nodeID produces a stable pseudonymous identifier without exposing the hostname.
// nodeID создаёт стабильный псевдонимный идентификатор без раскрытия hostname.
func nodeID(hostname string) string {
	material := strings.ToLower(strings.TrimSpace(hostname)) + ":" + runtime.GOOS + ":" + runtime.GOARCH
	sum := sha256.Sum256([]byte(material))
	return "node-" + hex.EncodeToString(sum[:8])
}
