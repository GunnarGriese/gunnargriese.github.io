---
title: Wie repliziere ich den GA4 Path Exploration-Bericht mit BigQuery SQL?
author: gunnar
date: 2022-10-23 11:24:15 +0200
categories: [BigQuery]
tags: [ga4, bigquery, sql]
comments: false
lang: de
permalink: /posts/bigquery-path-exploration/
---

Das neue Google Analytics (GA4) bietet eine neue Explorationsfunktion, mit der GA-Nutzer tiefer in ihre Daten eintauchen können — und zwar über die Möglichkeiten der standardmäßig integrierten Berichte hinaus. Während die Standardberichte das Monitoring von wichtigen Geschäftskennzahlen ermöglichen, bietet der Explorationsbereich erweiterte Analysetechniken, um schnell Ad-hoc-Einblicke zu gewinnen.

Die verfügbaren Analysetechniken sind die folgenden:

* Explorative Datenanalyse im freien Format
* Explorative Kohortenanalyse
* Explorative Trichteranalyse
* Segmentüberschneidung*
* Explorative Nutzeranalyse
* Explorative Pfadanalyse
* Nutzer-Lifetime

Schauen Sie sich die [offizielle Google Dokumentation](https://support.google.com/analytics/answer/7579450?hl=de) für eine ausführlichere Einführung in die leistungsstarke Explorationsfunktion von GA4 an.

## Explorative Pfadanalyse in GA4

Der Pfad-Explorationsbericht ermöglicht es, Nutzerinteraktionen ab einem bestimmten Ereignis/einer bestimmten Seite vorwärts (Startpunkt) oder rückwärts (Endpunkt) aggregiert zu visualisieren. Analysten können mit dieser Technik Fragen wie die folgenden beantworten:

* Welche Top-Seiten rufen neue Nutzer nach dem Besuch der Startseite auf?
* Wie wirkt sich ein Ereignis auf nachfolgende Nutzeraktionen aus?
* Welche Seiten enthalten defekte Links zu 404-Seiten?

![path-structure](/assets/img/path-exploration/path-structure.png)
_Elemente der Pfad-Exploration_

Die Visualisierung ist ein Sankey-Diagramm, bei dem jeder Knoten ein Ereignis oder eine Seite darstellt. Analysten können nach Belieben Knoten hinzufügen, um weitere Sequenzelemente offenzulegen, und Segmente, Filter sowie Aufschlüsselungsdimensionen anwenden, um den Bericht an ihre Bedürfnisse anzupassen.

## Verwendung von BigQuery zur Datenextraktion

Obwohl diese Analysetechnik mächtig ist, ist sie nicht immer das ideale Werkzeug, um diese Einblicke mit Stakeholdern zu teilen — insbesondere nicht mit denen, die mit GA nicht vertraut sind. Glücklicherweise haben alle GA4-Nutzer die Möglichkeit, ihre GA4-Daten in BigQuery zu exportieren (Googles cloudbasierte, vollständig verwaltete Datenbank für analytische Workloads).

Um kritische Nutzerflüsse kontinuierlich zu überwachen und sie in Ihre Standard-Berichtswerkzeuge (z. B. Looker Studio, Power BI oder Tableau) einzubetten, sollten Sie die [GA4-Rohdaten in BigQuery](https://support.google.com/analytics/answer/9358801?hl=de) nutzen und die Daten extrahieren. Aber…

## Wie repliziere ich einen einfachen GA4 Path Exploration-Bericht in BigQuery?

Wir können Fensterfunktionen in BigQuery verwenden, um die page_location-Sequenzen über alle Sitzungen hinweg, die mit GA4 gemessen wurden, zu aggregieren. Eine Abfrage könnte so aussehen:

![starting-point](/assets/img/path-exploration/starting-point.png)
_Abfrageergebnis für Pfad-Exploration mit Startpunkt_

Die Kernelemente der Abfrage sind die folgenden:

* `ga4EventParams`-Funktion
* `LEAD()`-Funktion über eine Sitzungs-`WINDOW`
* Temporäre Tabelle, die in einer `WITH`-Klausel definiert ist

### Benutzerdefinierte Funktionen zur Erhöhung der Lesbarkeit

Da wir daran interessiert sind, die `page_location` für jedes zugehörige page_view-Ereignis zu erhalten, ist page_location der Schlüssel, den wir als Eingabe für die Funktion bereitstellen. Die `ga4EventParams`-Funktion gibt den entsprechenden Wert für den eingegebenen Schlüssel aus dem `event_params` RECORD zurück. Weitere Details finden Sie in [Alejandros Beiträgen](https://zielinsky.alejand.ro/) zur Verwendung einer BigQuery-Funktion.

### Fensterfunktionen zur Abfrage von Sequenzen

Die `LEAD()`-Navigationsfunktion ermöglicht es uns, nachfolgende Zeilen aus einem angegebenen Fenster abzufragen. Das Ändern des Offset-Werts bestimmt, welche nachfolgende Zeile zurückgegeben wird; der Standardwert ist `1`, was die nächste Zeile im Fensterrahmen angibt. Der Offset-Wert kann verwendet werden, um je nach Analyse mehr Knoten zu Ihrer Abfrage hinzuzufügen. Im obigen Beispiel wurden 3 zusätzliche Knoten (neben dem Startpunkt) einbezogen.

Die obenstehende `WINDOW`-Klausel bewirkt, dass sich das Fenster über die Sitzung eines Nutzers erstreckt. Um das Fenster nutzerspezifisch zu gestalten, entfernen Sie den Verweis auf `ga_session_id`.

### Temporäre Tabellen zur Speicherung von Zwischenergebnissen

Die temporäre Tabelle ermöglicht es uns, die resultierende Tabelle — eine Zeile pro `page_view`-Ereignis mit den nachfolgenden `page_locations` als Spalten — als Zwischenergebnis im Speicher (Daten) zu speichern und sie in einem späteren Teil der Abfrage verfügbar zu machen. Die Datentabelle wird dann in der abschließenden `FROM`-Klausel verwendet, um die Häufigkeit jeder Sequenz über alle Sitzungen hinweg zu zählen.

## Wie schaut man in der Zeit zurück?

> Das klingt ja gut und schön, aber wie startet man die Sequenz am Ende und arbeitet sich von dort rückwärts?

Gute Frage, insbesondere weil die Festlegung des Endpunkts und die Analyse, wie Nutzer dorthin gelangten, eine wesentliche Funktion der Pfad-Explorationstechnik von GA4 ist.

Glücklicherweise erfordert dies nur wenige Anpassungen in unserer temporären Tabelle, wie hier:

![ending-point](/assets/img/path-exploration/ending-point.png)
_Abfragebeispiel für Pfad-Exploration mit Endpunkt_

Durch einfaches Ersetzen von `LEAD()` durch `LAG()` geben wir den Wert der page_location in der vorherigen Zeile zurück. Also das vorherige `page_view`-Ereignis einer Sitzung.

## Wie startet man die Sequenz mit der tatsächlichen Einstiegsseite?

Um dies zu erreichen, müssen wir erneut auf die uns vertraute `LEAD()`-Funktion zurückgreifen und eine Spalte zu unserer temporären Tabelle hinzufügen — den `entrances`-Ereignisparameter. Dieser zeigt an, ob ein bestimmtes `page_view`-Ereignis das erste innerhalb einer Sitzung war und somit die Einstiegsseite ist.

Das Filtern nach Sequenzen, die auf der Einstiegsseite beginnen, liefert das gewünschte Ergebnis:

![landing-page](/assets/img/path-exploration/landing-page.png)
_Abfragebeispiel für Pfad-Exploration mit der Einstiegsseite als Startpunkt_

## Abschließende Bemerkungen

Ich hoffe, dass dieser Post wDich hilfreich war und Dich ermutigt, tiefer in die BigQuery-Rohdaten von GA4 einzutauchen. Aus meiner Sicht ist der Zugriff auf die Rohdaten einer der größten Vorteile, die man beim Umstieg von Universal Analytics auf GA4 erhält. Ich beabsichtige, weitere Anwendungsfälle zu identifizieren, um die Möglichkeiten und Grenzen von GA4 und BigQuery zu erkunden. Falls Sie Fehler in den Abfragen entdecken, Anmerkungen haben oder etwas unklar finden, kontaktieren Sie mich gerne. Ich spreche immer gerne über Analytics!
