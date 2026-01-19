## Architektura  
- P2P (každý node = jedna banka)  
- **Port:** konfigurovatelný v rozsahu 65525–65535  
- **Identifikace banky:** IP adresa stroje  
- **Přístup:** telnet / PuTTY (ruční posílání příkazů)

## Funkcionalita (BASIC)
- Správa bankovních účtů (create, deposit, withdraw, balance, remove)
- Globální bankovní statistiky (BA, BN)
- Validace vstupů (formát účtu, IP, částky)
- Jednoznačné odpovědi (`<KÓD>` nebo `ER <zpráva>`)
- **Persistence dat:** účty a zůstatky uloženy na disk
- **Logování:** příkazy, odpovědi, chyby, připojení klientů
- **Timeouty:**  
  - odpověď na příkaz (default 5 s)  
  - obsluha klienta

## Funkcionalita (ESSENTIALS – navíc)
- **Proxy režim:**  
  - Příkazy `AD`, `AW`, `AB` s cizí IP adresou se přepošlou na vzdálený node
  - Node funguje jako klient i server zároveň
  - Odpověď vzdálené banky je vrácena původnímu volajícímu
