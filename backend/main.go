package main

import (
	"fmt"
	"net/http"
	"github.com/algorithm-ssau/golang-chat/pkg/websocket"
)

func main() {
	fmt.Println("Go chat project")
	setupRoutes()
	http.ListenAndServe(":9000", nil)

}

func setupRoutes() {
	pool := websocket.NewPool();
	go pool.Start()

	http.HandleFunc("/ws", func(w http.ResponseWriter, r *http.Request)){
		serveWS(pool, w, r)
	}

}

func serveWS(pool *websocket.Pool, w http.ResponseWriter, r http.Request){
	fmt.Println("websocket endpoint reached")

	conn, err := websocket.Upgrade(w, r)

	if(err != nil){
		fmt.Println(w, "%+V\n", err)
	}
	client := &websocket.Client{
		Conn: conn,
		Pool: pool,
	} 
	pool.Register <- client
	client.Read()
}
