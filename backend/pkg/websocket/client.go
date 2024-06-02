package websocket

import (
	"fmt"
	"log"
	"sync"

	"github.com/gorilla/websocket"
)

type Client struct {
	ID   string
	Conn *websocket.Conn
	Pool *Pool
	mu   sync.Mutex
}

type Message struct {
	Type int    `json:"type"`
	Body string `json:"body"`
}

func (c *Client) Read() {
	for {
		messageType, p, err := c.Conn.ReadMessage()
		if err != nil {
			log.Println("Error in client, closing connection")
			log.Println(err)
			c.Pool.Unregister <- c
			c.Conn.Close()
			return
		}

		message := Message{Type: messageType, Body: string(p)}
		c.Pool.Broadcast <- message
		fmt.Printf("Message Received: %+v\n", message)

	}
}
