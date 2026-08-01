package main

import (
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"
)

func TestHealthEndpointIsReadOnlyAndHardened(t *testing.T) {
	handler := newHandler()

	request := httptest.NewRequest(http.MethodGet, "/health", nil)
	response := httptest.NewRecorder()
	handler.ServeHTTP(response, request)

	if response.Code != http.StatusOK {
		t.Fatalf("expected 200, got %d", response.Code)
	}
	if contentType := response.Header().Get("Content-Type"); !strings.HasPrefix(contentType, "application/json") {
		t.Fatalf("expected JSON content type, got %q", contentType)
	}
	if response.Header().Get("Cache-Control") != "no-store" {
		t.Fatal("expected no-store cache policy")
	}
	if response.Header().Get("X-Content-Type-Options") != "nosniff" {
		t.Fatal("expected nosniff response header")
	}
}

func TestMutationMethodsAreRejected(t *testing.T) {
	handler := newHandler()
	request := httptest.NewRequest(http.MethodPost, "/capabilities", strings.NewReader("{}"))
	response := httptest.NewRecorder()
	handler.ServeHTTP(response, request)

	if response.Code != http.StatusMethodNotAllowed {
		t.Fatalf("expected 405, got %d", response.Code)
	}
	if response.Header().Get("Allow") != "GET, HEAD" {
		t.Fatalf("unexpected Allow header: %q", response.Header().Get("Allow"))
	}
}

func TestHeadReturnsNoBody(t *testing.T) {
	handler := newHandler()
	request := httptest.NewRequest(http.MethodHead, "/capabilities", nil)
	response := httptest.NewRecorder()
	handler.ServeHTTP(response, request)

	if response.Code != http.StatusOK {
		t.Fatalf("expected 200, got %d", response.Code)
	}
	if response.Body.Len() != 0 {
		t.Fatalf("expected empty HEAD body, got %q", response.Body.String())
	}
}
