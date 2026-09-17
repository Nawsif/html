from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler


HOST = "127.0.0.1"
PORT = 8081


class LoveHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        # Required for SharedArrayBuffer / WebAssembly threads
        self.send_header(
            "Cross-Origin-Opener-Policy",
            "same-origin"
        )
        self.send_header(
            "Cross-Origin-Embedder-Policy",
            "require-corp"
        )

        # Helpful for resources loaded by the game
        self.send_header(
            "Cross-Origin-Resource-Policy",
            "same-origin"
        )

        # Prevent caching while we're testing/rebuilding
        self.send_header(
            "Cache-Control",
            "no-store, no-cache, must-revalidate"
        )

        super().end_headers()


if __name__ == "__main__":
    server = ThreadingHTTPServer(
        (HOST, PORT),
        LoveHandler
    )

    print("=" * 50)
    print("LÖVE Web Server")
    print("=" * 50)
    print()
    print(f"Running at: http://{HOST}:{PORT}/")
    print()
    print("Press Ctrl+C to stop.")
    print()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server...")
        server.server_close()