package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"log"
	"net/http"
	"os"
	"time"

	"github.com/claryel-company/claryel-boxcore/internal/discovery"
)

var version = "dev"

func main() {
	if len(os.Args) < 2 {
		fail("usage: boxcore-node <discover|serve|version>")
	}

	switch os.Args[1] {
	case "discover":
		capabilities, err := discovery.Discover()
		if err != nil {
			fail(err.Error())
		}
		output, err := json.MarshalIndent(capabilities, "", "  ")
		if err != nil {
			fail(err.Error())
		}
		fmt.Println(string(output))
	case "serve":
		serve(os.Args[2:])
	case "version":
		fmt.Println(version)
	default:
		fail("unknown command")
	}
}

func serve(arguments []string) {
	flags := flag.NewFlagSet("serve", flag.ExitOnError)
	listen := flags.String("listen", "127.0.0.1:8091", "listen address; loopback is the safe default")
	_ = flags.Parse(arguments)

	server := &http.Server{
		Addr:              *listen,
		Handler:           newHandler(),
		ReadHeaderTimeout: 5 * time.Second,
		ReadTimeout:       10 * time.Second,
		WriteTimeout:      10 * time.Second,
		IdleTimeout:       30 * time.Second,
		MaxHeaderBytes:    1 << 20,
	}

	log.Printf("boxcore-node listening on %s", *listen)
	if err := server.ListenAndServe(); err != nil && err != http.ErrServerClosed {
		log.Fatal(err)
	}
}

func newHandler() http.Handler {
	mux := http.NewServeMux()
	mux.HandleFunc("/health", readOnlyJSON(func() (any, error) {
		return map[string]any{
			"status":  "ok",
			"version": version,
			"time":    time.Now().UTC().Format(time.RFC3339),
		}, nil
	}))
	mux.HandleFunc("/capabilities", readOnlyJSON(func() (any, error) {
		return discovery.Discover()
	}))

	return http.HandlerFunc(func(writer http.ResponseWriter, request *http.Request) {
		writer.Header().Set("Cache-Control", "no-store")
		writer.Header().Set("Content-Security-Policy", "default-src 'none'; frame-ancestors 'none'")
		writer.Header().Set("Referrer-Policy", "no-referrer")
		writer.Header().Set("X-Content-Type-Options", "nosniff")
		writer.Header().Set("X-Frame-Options", "DENY")
		mux.ServeHTTP(writer, request)
	})
}

func readOnlyJSON(build func() (any, error)) http.HandlerFunc {
	return func(writer http.ResponseWriter, request *http.Request) {
		if request.Method != http.MethodGet && request.Method != http.MethodHead {
			writer.Header().Set("Allow", "GET, HEAD")
			http.Error(writer, "method not allowed", http.StatusMethodNotAllowed)
			return
		}

		payload, err := build()
		if err != nil {
			http.Error(writer, "capability discovery failed", http.StatusInternalServerError)
			return
		}

		writer.Header().Set("Content-Type", "application/json; charset=utf-8")
		if request.Method == http.MethodHead {
			writer.WriteHeader(http.StatusOK)
			return
		}
		if err := json.NewEncoder(writer).Encode(payload); err != nil {
			log.Printf("response encoding failed: %v", err)
		}
	}
}

func fail(message string) {
	fmt.Fprintln(os.Stderr, message)
	os.Exit(1)
}
