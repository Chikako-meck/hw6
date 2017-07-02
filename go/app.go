package app

import (
	"fmt"
	"net/http"
)

func init() {
	http.HandleFunc("/", handlePata)
}

func handlePata(w http.ResponseWriter, r *http.Request) {
	values := url.Values{}
  	values.Add(a, r[0])
  	values.Add(b, r[1])

  	resp, err := http.Get([アクセス先URL] + "?" + values.Encode())
  	if err != nil {
    	fmt.Println(err)
    	return
  	}
	w.Header().Set("Content-Type", "text/html; charset=utf-8")
	fmt.Fprintf(w, "Hello world!\n")
}
