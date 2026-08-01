package discovery

import "testing"

func TestDiscoverReturnsPrivacyMinimisedShape(t *testing.T) {
	capabilities, err := Discover()
	if err != nil {
		t.Fatal(err)
	}
	if capabilities.NodeID == "" {
		t.Fatal("node identifier is empty")
	}
	if capabilities.CPUThreads < 1 {
		t.Fatalf("invalid CPU thread count: %d", capabilities.CPUThreads)
	}
	if capabilities.OS == "" || capabilities.Architecture == "" {
		t.Fatalf("missing platform fields: %+v", capabilities)
	}
}
