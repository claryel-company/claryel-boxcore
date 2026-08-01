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
	listen := flags.String("listen", "127.0.0.1:8091", "loopback listen address")
	_ = flags.Parse(arguments)

	mux := http.NewServeMux()
	mux.HandleFunc("/health", func(writer http.ResponseWriter, request *http.Request) {
		writer.Header().Set("Content-Type", "application/json")
		writer.Header().Set("Cache-Control", "no-store")
		response := map[string]any{
			"status":  "ok",
			"version": version,
			"time":    time.Now().UTC().Format(time.RFC3339),
		}
		_ = json.NewEncoder(writer).Encode(response)
	})
	mux.HandleFunc("/capabilities", func(writer http.ResponseWriter, request *http.Request) {
		capabilities, err := discovery.Discover()
		if err != nil {
			http.Error(writer, "capability discovery failed", http.StatusInternalServerError)
			return
		}
		writer.Header().Set("Content-Type", "application/json")
		writer.Header().Set("Cache-Control", "no-store")
		_ = json.NewEncoder(writer).Encode(capabilities)
	})

	server := &http.Server{
		Addr:              *listen,
		Handler:           mux,
		ReadHeaderTimeout: 5 * time.Second,
	}

	// English: The public baseline listens on loopback by default and performs no privileged mutation.
	// Русский: Публичная основа по умолчанию слушает loopback и не выполняет привилегированные изменения.
	log.Printf("boxcore-node listening on %s", *listen)
	log.Fatal(server.ListenAndServe())
}

func fail(message string) {
	fmt.Fprintln(os.Stderr, message)
	os.Exit(1)
}
