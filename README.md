# WWW_project_174714
## StageHub - System do zarządzania koncertami oraz rezerwacji scen
### System pozwala na dodawanie eventów (koncertów), tworzenie harmonogramu występu artystów konkretnego eventu oraz określanie pul biletów, ich rodzaje i ceny.
### Projekt składa się z 5 modeli:
### * **Stage:** Przechowuje informacje o dostępnych scenach do rezerwacji: nazwę, lokalizację, pojemność oraz cenę wynajmu.
### * **Artist:** Przechowuje informacje o artystach lub zespołach uczestniczących w konkretnym evencie/koncercie, gatunek muzyczny, gatunek muzyczny oraz kraj pochodzenia.
### * **Concert:** Przechowuje informacje o organizatorze eventu, zarezerwowanej scenie, line=upie artystów, ramy czasowe rezerwacji oraz status eventu/koncertu.
### * **LineupSlot:** Przechowuje informacje o dokładnym czasie występu konkretnego artysty oraz jego wynagrodzeniu.
### * **TicketTier:** Przechowuje informacje o kategorii biletów dla koncertu, ich cenę oraz dostępną pulę miejsc.