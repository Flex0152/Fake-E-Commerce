## Über das Projekt
Es soll das Erstellen von Dashboards mit plotly erlernt werden. 
Um Daten zum analysieren zu haben, wurde ein eigener Datengenerator geschrieben. 
Die Analyse wird mit DuckDB im Datawarehouse Stil durchgeführt. Die Analyse deckt nicht alle Fragen ab, 
der Schwerpunkt liegt auf die Erstellung des Dashboards. 

## Datensatz
Es handelt sich um synthetische Daten die mit dem Generator create_data.py erstellt wurden. Sie sollen 
ein fiktiven Online Shop abbilden. 
Der Generator ist verbesserungswürdig. Zum Beispiel ist die Verteilung viel zu linear. Alle 100 Kunden haben 1000 Bestellungen abgegeben. Die bestellten Services sind ebenfalls viel zu gleichmäßig verteilt.  

## Datenbank
Die Datenbank wird immer neu erstellt. Das ermöglicht die Analyse der im Moment
aktuellen Werte. 
Wenn alle Werte wichtig sind, sollte die Datenbank losgelöst von den Daten erstellt werden. 
Die Daten würden dann in eigenen Routinen importiert werden (Stichwort MERGE). 