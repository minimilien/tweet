package main

import (
	"bytes"
	"fmt"
	"log"
	"net/http"
	"os/exec"
	"strings"
	"time"
)

//CMDcall sert à envoyer des commandes à la console
func CMDcall(commande string, debug bool) (string, error) {
	commandesplit := strings.Split(commande, " ")
	cmd := exec.Command(commandesplit[0], commandesplit[1:]...)
	out, err := cmd.CombinedOutput()
	fmt.Printf("combined out:\n%s\n", string(out))
	if (err != nil) && (debug == true) {
		log.Fatalf("cmd.Run() failed with %s\n", err)
	}
	return string(out), err
}

type reponse struct {
	statut bool
	data   string
}

func requete(c chan int, adresse string) bool {
	responseBody := []byte("{\"phrase\": \"wall\"}")
	http.Post(adresse, "json", bytes.NewBuffer(responseBody))
	//resp, err := http.Post(adresse, "json", bytes.NewBuffer(responseBody))
	//fmt.Println(resp, err)
	//body, _ := ioutil.ReadAll(resp.Body)
	//fmt.Println(body, err2)
	//sb := string(body)
	//fmt.Printf(sb)
	c <- 1
	return true
}

func test(adresse string) {
	start := time.Now()
	c := make(chan int)
	param := 1000
	for i := 0; i < param; i++ {
		go requete(c, adresse)
	}
	result := 0
	for j := 0; j < param; j++ {
		result += <-c
	}
	fmt.Println(result)
	//regles à ajouter
	elapsed := time.Since(start)
	fmt.Println("Durée d'exécution du programme :", &elapsed, "\n")
}

func main() {
	test("http://127.0.0.1:5000/horloge/")
	test("http://127.0.0.1:5000/RAM/")
	test("http://127.0.0.1:5000/azerty")
	//test("http://127.0.0.1:5000/SIM")

}
