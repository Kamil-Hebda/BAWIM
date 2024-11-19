
# Instrukcja uruchamiania aplikacji Flask i połączenia z bazą danych PostgreSQL

## 1. Klonowanie repozytorium

Aby rozpocząć, musisz sklonować repozytorium na swoje lokalne środowisko. Użyj poniższego polecenia:

```bash
git clone <URL_REPOZYTORIUM>
cd <NAZWA_REPOZYTORIUM>
```

## 2. Uruchomienie aplikacji Flask

Aby uruchomić aplikację Flask, postępuj zgodnie z poniższymi krokami:

### a. Uruchom wirtulane środowisko

Tworzenie i aktywacja wirtualnego środowiska:
Na Windows:

```bash
python -m venv venv
venv\Scripts\activate
```
Na Mac/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### b. Zainstaluj zależności

Aplikacja wymaga kilku zależności, które można zainstalować za pomocą `pip`. Wykonaj poniższe polecenie, aby zainstalować wymagane pakiety:

```bash
pip install -r requirements.txt
```

### c. Uruchom aplikację

Po zainstalowaniu zależności, uruchom aplikację Flask za pomocą poniższego polecenia:

```bash
python app.py
```

Aplikacja będzie dostępna pod adresem `http://127.0.0.1:5000/` w twojej przeglądarce.

## 3. Połączenie z bazą danych PostgreSQL

Aplikacja wymaga połączenia z bazą danych PostgreSQL. W tym celu używamy kontenera Docker.

### a. Pobranie obrazu kontenera

Najpierw musisz pobrać obraz kontenera z Docker Hub. Użyj poniższego polecenia:

```bash
docker pull khebda/oob_sqli1:latest
```

### b. Uruchomienie kontenera

Aby uruchomić kontener PostgreSQL, użyj poniższego polecenia:

```bash
docker run --name oob_sqli1 -p 5432:5432 -v nowy_volume4:/var/lib/postgresql/data khebda/oob_sqli1:latest
```

Po uruchomieniu kontenera, aplikacja będzie dostępna na porcie `5432`. Teraz możesz połączyć się z bazą danych.

### c. Wejście do kontenera

Aby wejść do uruchomionego kontenera i zacząć pracę w środowisku, użyj poniższego polecenia:

```bash
docker exec -it oob_sqli1 bash
```

Będziesz mógł teraz pracować w kontenerze i wykonywać wszelkie niezbędne operacje na bazie danych.


## 4. Testowanie aplikacji

Po skonfigurowaniu wszystkiego, uruchom aplikację i sprawdź, czy połączenie z bazą danych działa poprawnie. Możesz to zrobić, otwierając aplikację w przeglądarce pod adresem `http://127.0.0.1:5000/` i sprawdzając, czy aplikacja działa bez błędów związanych z bazą danych.

## 5. Dodatkowe informacje

- Aplikacja jest uruchomiona w trybie deweloperskim, co oznacza, że wszelkie zmiany w kodzie aplikacji są natychmiastowo widoczne po jej odświeżeniu.
- Aby uzyskać dostęp do bazy danych z aplikacji, upewnij się, że kontener jest uruchomiony i że połączenie z bazą jest poprawnie skonfigurowane.
