package main

import (
	"flag"
	"fmt"
	"log"
	"net"
	"os"
	"os/exec"
	"strings"
)

func main() {
	task := flag.String("task", "", "task name if alloc contains multiple")
	socatPath := flag.String("socat-path", "/usr/bin/socat", "path to socat binary in task")
	portMap := flag.String("p", "", "port mapping local_port:remote_port")
	flag.Parse()

	args := flag.Args()
	if len(args) != 1 {
		log.Fatalf("expected 1 alloc argument given %d", len(args))
	}

	portMapParts := strings.Split(*portMap, ":")
	if len(portMapParts) != 2 {
		log.Fatalf("expected 2 parts (local_port:remote_port) for -p flag, given %d", len(portMapParts))
	}

	ln, err := net.Listen("tcp", fmt.Sprintf("localhost:%s", portMapParts[0]))
	if err != nil {
		log.Fatalf("failed to create local listener: %v", err)
	}
	defer ln.Close()

	log.Printf("started local server: %v", ln.Addr())
	for {
		conn, err := ln.Accept()
		if err != nil {
			log.Fatalf("failed to accept new connection: %v", err)
		}
		log.Printf("accepted new connection: %v", conn.RemoteAddr())
		go func(conn net.Conn) {
			defer conn.Close()
			defer log.Printf("closed connection: %v", conn.RemoteAddr())

			argsStr := fmt.Sprintf("alloc exec -i -t=false -task=%s %s %s - TCP4:localhost:%s", *task, args[0], *socatPath, portMapParts[1])

			log.Printf("running command: nomad %s", argsStr)
			cmd := exec.Command("nomad", strings.Split(argsStr, " ")...)

			cmd.Stdin = conn
			cmd.Stdout = conn
			cmd.Stderr = os.Stderr

			err = cmd.Run()
			if err != nil {
				log.Printf("nomad exec command error: %v", err)
				return
			}
		}(conn)
	}
}

