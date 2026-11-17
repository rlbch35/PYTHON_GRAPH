# Rapport d'analyse réseau (TP1, TP2 & TP3)

*Généré automatiquement le 17/11/2026 à 08:47:50 depuis `Projet_main.py`*

---



### Recherche du chemin numéro 1

- **`Prédécesseurs`** : {'S*': None, 'DC-A': 'S*', 'DC-B': 'S*', 'R1': 'DC-A', 'R2': 'DC-B', 'R3': 'R1', 'LIVE': 'R1', 'BACKUP': 'R2', 'T*': 'LIVE'}
- **`Chemin trouvé`** : [('S*', 'DC-A'), ('DC-A', 'R1'), ('R1', 'LIVE'), ('LIVE', 'T*')]
- **`Quantité supplémentaire possible`** : 100
- **`Arc S* -> DC-A`** : débit = 100, capacité restante = 100
- **`Arc DC-A -> R1`** : débit = 100, capacité restante = 100
- **`Arc R1 -> LIVE`** : débit = 100, capacité restante = 0
- **`Arc LIVE -> T*`** : débit = 100, capacité restante = 120


### Recherche du chemin numéro 2

- **`Prédécesseurs`** : {'S*': None, 'DC-A': 'S*', 'DC-B': 'S*', 'R1': 'DC-A', 'R2': 'DC-B', 'R3': 'R1', 'BACKUP': 'R2', 'LIVE': 'R3', 'T*': 'BACKUP'}
- **`Chemin trouvé`** : [('S*', 'DC-B'), ('DC-B', 'R2'), ('R2', 'BACKUP'), ('BACKUP', 'T*')]
- **`Quantité supplémentaire possible`** : 100
- **`Arc S* -> DC-B`** : débit = 100, capacité restante = 150
- **`Arc DC-B -> R2`** : débit = 100, capacité restante = 150
- **`Arc R2 -> BACKUP`** : débit = 100, capacité restante = 0
- **`Arc BACKUP -> T*`** : débit = 100, capacité restante = 100


### Recherche du chemin numéro 3

- **`Prédécesseurs`** : {'S*': None, 'DC-A': 'S*', 'DC-B': 'S*', 'R1': 'DC-A', 'R2': 'DC-B', 'R3': 'R1', 'LIVE': 'R3', 'BACKUP': 'R3', 'T*': 'LIVE'}
- **`Chemin trouvé`** : [('S*', 'DC-A'), ('DC-A', 'R1'), ('R1', 'R3'), ('R3', 'LIVE'), ('LIVE', 'T*')]
- **`Quantité supplémentaire possible`** : 100
- **`Arc S* -> DC-A`** : débit = 200, capacité restante = 0
- **`Arc DC-A -> R1`** : débit = 200, capacité restante = 0
- **`Arc R1 -> R3`** : débit = 100, capacité restante = 60
- **`Arc R3 -> LIVE`** : débit = 100, capacité restante = 120
- **`Arc LIVE -> T*`** : débit = 200, capacité restante = 20


### Recherche du chemin numéro 4

- **`Prédécesseurs`** : {'S*': None, 'DC-B': 'S*', 'R2': 'DC-B', 'R3': 'R2', 'LIVE': 'R3', 'BACKUP': 'R3', 'R1': 'R3', 'T*': 'LIVE'}
- **`Chemin trouvé`** : [('S*', 'DC-B'), ('DC-B', 'R2'), ('R2', 'R3'), ('R3', 'LIVE'), ('LIVE', 'T*')]
- **`Quantité supplémentaire possible`** : 20
- **`Arc S* -> DC-B`** : débit = 120, capacité restante = 130
- **`Arc DC-B -> R2`** : débit = 120, capacité restante = 130
- **`Arc R2 -> R3`** : débit = 20, capacité restante = 200
- **`Arc R3 -> LIVE`** : débit = 120, capacité restante = 100
- **`Arc LIVE -> T*`** : débit = 220, capacité restante = 0


### Recherche du chemin numéro 5

- **`Prédécesseurs`** : {'S*': None, 'DC-B': 'S*', 'R2': 'DC-B', 'R3': 'R2', 'LIVE': 'R3', 'BACKUP': 'R3', 'R1': 'R3', 'T*': 'BACKUP'}
- **`Chemin trouvé`** : [('S*', 'DC-B'), ('DC-B', 'R2'), ('R2', 'R3'), ('R3', 'BACKUP'), ('BACKUP', 'T*')]
- **`Quantité supplémentaire possible`** : 100
- **`Arc S* -> DC-B`** : débit = 220, capacité restante = 30
- **`Arc DC-B -> R2`** : débit = 220, capacité restante = 30
- **`Arc R2 -> R3`** : débit = 120, capacité restante = 100
- **`Arc R3 -> BACKUP`** : débit = 100, capacité restante = 150
- **`Arc BACKUP -> T*`** : débit = 200, capacité restante = 0


### Recherche du chemin numéro 6

- Aucun chemin résiduel de S* vers T*.
- Coupe minimale: A=['S*', 'DC-B', 'R2', 'R3', 'LIVE', 'BACKUP', 'R1', 'DC-A'] | B={'T*'}


### Débit final sur chaque arc

- (S*, DC-A) = 200 / capacité restante = 0
- (S*, DC-B) = 220 / capacité restante = 30
- (DC-A, R1) = 200 / capacité restante = 0
- (DC-B, R2) = 220 / capacité restante = 30
- (R1, R3) = 100 / capacité restante = 60
- (R1, LIVE) = 100 / capacité restante = 0
- (R2, R3) = 120 / capacité restante = 100
- (R2, BACKUP) = 100 / capacité restante = 0
- (R3, LIVE) = 120 / capacité restante = 100
- (R3, BACKUP) = 100 / capacité restante = 150
- (LIVE, T*) = 220 / capacité restante = 0
- (BACKUP, T*) = 200 / capacité restante = 0


### Bilan final du flot

- **`Valeur totale du flot`** : 420
- **`Capacité de la coupe`** : 420 == capacité du flot : 420


### Débit f / capacité c sur chaque arc

- **`S* -> DC-A`** : f = 200, c = 200, f/c = 1.00, latence = 0.00
- **`S* -> DC-B`** : f = 220, c = 250, f/c = 0.88, latence = 0.00
- **`DC-A -> R1`** : f = 200, c = 200, f/c = 1.00, latence = 5.75
- **`DC-B -> R2`** : f = 220, c = 250, f/c = 0.88, latence = 7.63
- **`R1 -> R3`** : f = 100, c = 160, f/c = 0.62, latence = 6.14
- **`R1 -> LIVE`** : f = 100, c = 100, f/c = 1.00, latence = 20.70
- **`R2 -> R3`** : f = 120, c = 220, f/c = 0.55, latence = 12.16
- **`R2 -> BACKUP`** : f = 100, c = 100, f/c = 1.00, latence = 28.75
- **`R3 -> LIVE`** : f = 120, c = 220, f/c = 0.55, latence = 8.11
- **`R3 -> BACKUP`** : f = 100, c = 250, f/c = 0.40, latence = 10.04
- **`LIVE -> T*`** : f = 220, c = 220, f/c = 1.00, latence = 0.00
- **`BACKUP -> T*`** : f = 200, c = 200, f/c = 1.00, latence = 0.00


- **`Le chemin le plus court a pour distance`** : 19 et est (('S*', 'DC-A'), ('DC-A', 'R1'), ('R1', 'R3'), ('R3', 'LIVE'), ('LIVE', 'T*'))


### Classement des impacts

- **`R3 -> Clients`** : flot sans l'arc = 160, impact = 160
- **`R4 -> Clients`** : flot sans l'arc = 160, impact = 160
- **`DC -> R1`** : flot sans l'arc = 180, impact = 140
- **`DC -> R2`** : flot sans l'arc = 180, impact = 140
- **`R1 -> R3`** : flot sans l'arc = 240, impact = 80
- **`R2 -> R4`** : flot sans l'arc = 240, impact = 80
- **`R1 -> R4`** : flot sans l'arc = 300, impact = 20
- **`R2 -> R3`** : flot sans l'arc = 300, impact = 20


### TP3 - Scénario initial (DC -> Clients)



### Débit final sur chaque arc

- (DC, R1) = 180 / capacité restante = 0
- (DC, R2) = 140 / capacité restante = 40
- (R1, R3) = 140 / capacité restante = 0
- (R1, R4) = 40 / capacité restante = 40
- (R2, R3) = 20 / capacité restante = 60
- (R2, R4) = 120 / capacité restante = 20
- (R3, Clients) = 160 / capacité restante = 0
- (R4, Clients) = 160 / capacité restante = 0


### Bilan final du flot

- **`Valeur totale du flot`** : 320
- **`Capacité de la coupe`** : 320 == capacité du flot : 320
- **`Arcs de la coupe minimale`** : [('R3', 'Clients', 160), ('R4', 'Clients', 160)] (capacité = 320)


### TP3 - Arc R1 -> R3 désactivé (DC -> Clients)



### Débit final sur chaque arc

- (DC, R1) = 80 / capacité restante = 100
- (DC, R2) = 160 / capacité restante = 20
- (R1, R4) = 80 / capacité restante = 0
- (R2, R3) = 80 / capacité restante = 0
- (R2, R4) = 80 / capacité restante = 60
- (R3, Clients) = 80 / capacité restante = 80
- (R4, Clients) = 160 / capacité restante = 0


### Bilan final du flot

- **`Valeur totale du flot`** : 240
- **`Capacité de la coupe`** : 240 == capacité du flot : 240
- **`Arcs de la coupe minimale`** : [('R2', 'R3', 80), ('R4', 'Clients', 160)] (capacité = 240)


### TP3 - Arc R3 -> Clients désactivé (DC -> Clients)



### Débit final sur chaque arc

- (DC, R1) = 80 / capacité restante = 100
- (DC, R2) = 80 / capacité restante = 100
- (R1, R4) = 80 / capacité restante = 0
- (R2, R3) = 0 / capacité restante = 80
- (R2, R4) = 80 / capacité restante = 60
- (R4, Clients) = 160 / capacité restante = 0


### Bilan final du flot

- **`Valeur totale du flot`** : 160
- **`Capacité de la coupe`** : 160 == capacité du flot : 160
- **`Arcs de la coupe minimale`** : [('R4', 'Clients', 160)] (capacité = 160)

- **`Sommets atteignables depuis DC`** : {'R4', 'R2', 'R1', 'R3', 'Clients', 'DC'}


### Étude de connectivité graph_data_TP3_datacenter - Désactivation de DC-LILLE

- **`Performance après désactivation de DC-LILLE`** : 730
- **`Taux maximal d'utilisation`** : 100.0%
- **`Zones non totalement servies`** : ['IDF (130/530)']
- **`Arcs de la coupe minimale`** : [('S*', 'DC-PARIS', 500), ('LYO', 'STR', 230)]
- **`Capacité de la coupe minimale`** : 730


### Étude de connectivité graph_data_TP3_datacenter - Désactivation de DC-PARIS

- **`Performance après désactivation de DC-PARIS`** : 580
- **`Taux maximal d'utilisation`** : 100.0%
- **`Zones non totalement servies`** : ['IDF (100/530)', 'Sud-Est (230/350)']
- **`Arcs de la coupe minimale`** : [('S*', 'DC-LILLE', 350), ('LYO', 'STR', 230)]
- **`Capacité de la coupe minimale`** : 580


### Étude de connectivité graph_data_TP3_datacenter - Désactivation de DC-LYON

- **`Performance après désactivation de DC-LYON`** : 850
- **`Taux maximal d'utilisation`** : 100.0%
- **`Zones non totalement servies`** : ['IDF (310/530)', 'Sud-Est (290/350)']
- **`Arcs de la coupe minimale`** : [('S*', 'DC-LILLE', 350), ('S*', 'DC-PARIS', 500)]
- **`Capacité de la coupe minimale`** : 850


### Étude de connectivité graph_data_TP3_datacenter - Désactivation de LIL

- **`Performance après désactivation de LIL`** : 730
- **`Taux maximal d'utilisation`** : 100.0%
- **`Zones non totalement servies`** : ['IDF (130/530)']
- **`Arcs de la coupe minimale`** : [('S*', 'DC-PARIS', 500), ('LYO', 'STR', 230)]
- **`Capacité de la coupe minimale`** : 730


### Étude de connectivité graph_data_TP3_datacenter - Désactivation de PAR

- **`Performance après désactivation de PAR`** : 470
- **`Taux maximal d'utilisation`** : 100.0%
- **`Zones non totalement servies`** : ['NORD (240/250)', 'IDF (0/530)', 'Sud-Est (230/350)']
- **`Arcs de la coupe minimale`** : [('LIL', 'REI', 240), ('LYO', 'STR', 230)]
- **`Capacité de la coupe minimale`** : 470


### Étude de connectivité graph_data_TP3_datacenter - Désactivation de LYO

- **`Performance après désactivation de LYO`** : 820
- **`Taux maximal d'utilisation`** : 100.0%
- **`Zones non totalement servies`** : ['IDF (310/530)', 'Sud-Est (260/350)']
- **`Arcs de la coupe minimale`** : [('LIL', 'REI', 240), ('PAR', 'REI', 320), ('PAR', 'STR', 260)]
- **`Capacité de la coupe minimale`** : 820


### Étude de connectivité graph_data_TP3_datacenter - Désactivation de REI

- **`Performance après désactivation de REI`** : 490
- **`Taux maximal d'utilisation`** : 100.0%
- **`Zones non totalement servies`** : ['NORD (0/250)', 'IDF (140/530)']
- **`Arcs de la coupe minimale`** : [('PAR', 'STR', 260), ('LYO', 'STR', 230)]
- **`Capacité de la coupe minimale`** : 490


### Étude de connectivité graph_data_TP3_datacenter - Désactivation de STR

- **`Performance après désactivation de STR`** : 560
- **`Taux maximal d'utilisation`** : 100.0%
- **`Zones non totalement servies`** : ['IDF (310/530)', 'Sud-Est (0/350)']
- **`Arcs de la coupe minimale`** : [('LIL', 'REI', 240), ('PAR', 'REI', 320)]
- **`Capacité de la coupe minimale`** : 560