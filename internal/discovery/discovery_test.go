package discovery

import (
	"strings"
	"testing"
)

func TestDiscoverReturnsPrivacyMinimisedShape(t *testing.T) {
	first, err := Discover()
	if err != nil {
		t.Fatal(err)
	}
	second, err := Discover()
	if err != nil {
		t.Fatal(err)
	}

	if !strings.HasPrefix(first.NodeID, "ephemeral-") {
		t.Fatalf("unexpected node identifier format: %q", first.NodeID)
	}
	if first.NodeID != second.NodeID {
		t.Fatalf("identifier changed within one process: %q != %q", first.NodeID, second.NodeID)
	}
	if len(strings.TrimPrefix(first.NodeID, "ephemeral-")) != 16 {
		t.Fatalf("unexpected identifier entropy length: %q", first.NodeID)
	}
	if first.CPUThreads < 1 {
		t.Fatalf("invalid CPU thread count: %d", first.CPUThreads)
	}
	if first.OS == "" || first.Architecture == "" {
		t.Fatalf("missing platform fields: %+v", first)
	}
	if !sortStringsAreStable(first.Capabilities) {
		t.Fatalf("capabilities are not sorted: %v", first.Capabilities)
	}
}

func sortStringsAreStable(values []string) bool {
	for index := 1; index < len(values); index++ {
		if values[index-1] > values[index] {
			return false
		}
	}
	return true
}
