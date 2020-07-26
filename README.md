# Warcaby Multiplayer

Zbudowanie gry w dockerze

`docker build -t warcaby .`

Uruchomienie serwera gry

`docker run -it -p 5000:5000 warcaby`

Struktura mikroserwisu

    ├── async_client.py              # skrypt klienta
    ├── async_server.py              # Obiekt servera
    ├── Dockerfile                  
    ├── game.py                      # Obiekty związane z grą
    ├── LICENSE
    ├── README.md
    └── tests.py                     # unit tests