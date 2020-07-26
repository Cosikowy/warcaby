# Warcaby Multiplayer w czystym pyhonie

Zbudowanie gry w dockerze

`docker build -t warcaby .`

Uruchomienie serwera gry

`docker run -it -p 5000:5000 warcaby`

Struktura

    ├── async_client.py              # skrypt klienta
    ├── async_server.py              # Obiekt servera
    ├── Dockerfile                  
    ├── game.py                      # Obiekty związane z grą
    ├── LICENSE
    ├── README.md
    └── tests.py                     # testy jednostkowe


W celu zmiany IP na którym jest serwowany serwer należy zmienić wartość SERVER_IP w klasie serwera w pliku async_server.py oraz SERVER_IP w pliku async_client.py

W celu zmiany portu na którym jest serwowany serwer należy zmienić wartość SERVER_PORT w klasie serwera w pliku async_server.py oraz SERVER_PORT w pliku async_client.py

---

- Poprawny format ruchu: "a3,b4" - a3 pozycja kamienia, którym chcemy wykonać ruch, b4 nowa pozycja
- Aby zaatakować kamieniem kamień przeciwnika należy ruszyć się na pole na którym znajduje się ten kamień (np. twój kamień jest na a4, a kamień przeciwnika jest na b5, za nim jest wolne pole należy wpisać "a4,b5" wtedy atak zostanie poprawnie wykonany)


# Multiplayer Brazilian draughts in pure python

Command for docker build (server)

`docker build -t draughts .`

Docker launch

`docker run -it -p 5000:5000 draughts`

Structure

    ├── async_client.py              # client script
    ├── async_server.py              # Server object
    ├── Dockerfile                  
    ├── game.py                      # Game objects
    ├── LICENSE
    ├── README.md
    └── tests.py                     # Unit tests

In case u want to change IP adress of server u need to change value of SERVER_IP in Server class in file async_server.py and SERVER_IP in async_client.py

In case u want to change port of server u need to change value of SERVER_PORT in Server class in file async_server.py and SERVER_PORT in async_client.py

- Correct move format is "a3,b4" - a3 is position of your stone, b4 is new position
- If u want to attak enemy's stone, you need to point it's location(e.g. your stone is on a4, enemmy's on b5 and behind is free space, your move will look like "a4,b5" for correct attack)