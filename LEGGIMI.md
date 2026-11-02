# Calcolatore SO2 corretto e test aggiornati

## Come usarlo su Windows
1. Estrarre lo ZIP in una nuova cartella, distinta dalla versione precedente.
2. In VS Code: File > Apri cartella > so2_pytest_corretto.
3. Aprire Terminale > Nuovo terminale ed eseguire:
   python -m pip install -r requirements-dev.txt
   python -m pytest -q
4. Risultato verificato: 157 passed, 3 skipped.
5. Per usare il calcolatore:
   python main.py

La copia corretta di main.py è già inclusa. Non occorre modificare righe a mano.
Per integrare successivamente nel repository, trasferire main.py, tests/,
pytest.ini e requirements-dev.txt; aggiungere al README la fonte e queste note.
Il repository GitHub non è stato modificato.

## Fonte e correzioni
Jenkins TW, Howe PA, Sacks GL, Waterhouse AL (2020).
Determination of Molecular and “Truly” Free Sulfur Dioxide in Wine:
A Comparison of Headspace and Conventional Methods.
DOI: https://doi.org/10.5344/ajev.2020.19052
Fonte verificata: PDF Papers in Press fornito dall'utente, online 13 marzo 2020;
pagina 6, Eq.1; pagina 7, Eqs.2-5, righe 144-148.
Questa versione anticipata avverte che la versione finale può cambiare:
non è stato verificato il testo editoriale definitivo né eventuali errata.

Config originale -> trascrizione del PDF:
M2: 0.00883782 -> 0.000883782 (Eq.2)
M3: 0.004437522 -> 0.00443752 (Eq.2)
Q3: 0.000479931 -> 0.00479931 (Eq.3)
Gli altri coefficienti e le strutture delle Eqs.1,4,5 sono coerenti.
I=0.056 M è un valore tipico assunto nell'articolo; il testo cita un intervallo
tipico 0.016-0.100 M. Non è una misura della forza ionica del singolo vino.
Temperatura in gradi Celsius e alcol in percentuale volumica (12, non 0.12).

## Verifiche
Python 3.12, pytest 9.2.0: 157 superati, 3 sospesi.
test_article_equations.py confronta i coefficienti con valori trascritti dal
PDF e ricalcola indipendentemente le equazioni con Decimal a 50 cifre.
Decimal è l'aritmetica decimale di Python: riduce gli arrotondamenti durante
la costruzione dei valori attesi. Non legge coefficienti da Config.
La tolleranza 1e-12 è numerica, non sperimentale.

Contro il main.py originale, gli stessi test dell'articolo producono
28 fallimenti e 15 successi: intercettano effettivamente le discrepanze.
Il dettaglio è in test-original-detection.txt.
I precedenti test di regressione numerica basati sui vecchi coefficienti
sono stati sostituiti dai controlli delle equazioni pubblicate.
Rimangono i test di formato, limiti interattivi, Config e coerenza interna.
test-results.txt contiene l'esecuzione sulla versione corretta.

Esempio calcolato (non misura sperimentale): libera 30 mg/L, pH 3.20,
temperatura 20.0 gradi Celsius, alcol 12.00% vol:
prima 1.504445161572305 mg/L; dopo 1.5990314672451933 mg/L.

## Tre verifiche ancora sospese
1. Applicabilità del valore di forza ionica assunto al campione specifico.
2. Accordo con misure indipendenti di SO2 molecolare nel dominio.
3. Dominio scientifico di validità e tolleranze sperimentali.

La fonte delle formule è ora identificata. La conformità alla trascrizione
delle formule NON equivale a validazione sperimentale del modello.
I limiti dell'interfaccia (libera 0-80, pH 2.80-4.00, temperatura 0-40,
alcol 0-20) rimangono scelte del software: non sono certificati da questo PDF.
Le griglie dei test includono estremi come sonde matematiche, non come
affermazioni di validità scientifica.

L'articolo distingue SO2 libera apparente e realmente libera: l'Eq.5 non
elimina eventuali distorsioni del metodo analitico con cui si misura l'input.
I valori di pKm in Tabella 4 sono calcolati, non misure indipendenti;
non sono stati usati per inventare tolleranze sperimentali.

La validazione resta in control_input; le funzioni di calcolo e Config non
validano gli argomenti. La gestione dei caratteri Unicode e degli input
diretti fuori dominio resta quella originale.
SOURCE_README.md è la copia storica del README del repository, non la nuova
documentazione scientifica; queste note descrivono le modifiche del pacchetto.
