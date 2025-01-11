---
title: GTM Server-Side Tagging – Bessere Daten & Mehr Kontrolle
author: gunnar
date: 2020-08-21 15:24:15 +0200
categories: [GTM]
tags: [ga4, gtm-server-side]
comments: false
lang: de
permalink: /posts/gtm-server-side/
---

In den letzten Monaten habe ich eine ganze Reihe von Beta-Tests und Projekten für eine ausgewählte Gruppe von Kunden durchgeführt, um sowohl praktische Erfahrungen zu sammeln als auch die kürzlich veröffentlichte Technologie des Google Tag Manager (GTM) Server-Side Taggings zu optimieren.

Mein Ziel mit diesem Post ist es, sowohl Hintergrundinformationen als auch den Kontext zu liefern, warum ich der Meinung bin, dass die allermeisten Unternehmen ernsthaft in Betracht ziehen sollten, GTM Server-Side Tagging zu übernehmen, um ihr Tracking besser zu unterstützen. Darüber hinaus erhältst Du einen Überblick über die Funktionalität und mögliche Anwendungsfälle dieser neuen Technologie, um sich auf ein zukunftssicheres First-Party-Tracking einzustellen, die Kundenerfahrung insgesamt zu verbessern und die volle Kontrolle über deine Daten zu erlangen.

Die wichtigste Erkenntnis ist, dass GTM Server-Side die Flexibilität und Kontrolle über Ihre Daten erhöht und den langfristigen Nutzen der Lösung für das Unternehmen weit über das hinausgeht, was mit einem herkömmlichen, client-seitigem Google Tag Manager-Setup möglich ist.

## Nichts geht über Datenkontrolle und 1st-Party-Daten

Heutzutage stehen Unternehmen vor vielen Herausforderungen, die sie dazu zwingen, die Art und Weise, wie sie Website- und App-Tracking durchführen, neu zu überdenken. Zum Glück eröffnen diese Herausforderungen mit GTM Server-Side auch viele neue Möglichkeiten für Unternehmen, die bereit sind, sich anzupassen und zu verändern. Traditionelles Tracking steht jedoch vor vielen Problemen, die es technisch unmöglich machen, "Tracking wie gewohnt" fortzusetzen.

Eine dieser Herausforderungen ist das neue "Privacy first"-Paradigma, das uns durch Vorschriften wie die DSGVO (EU) und den CCPA (Kalifornien) auferlegt wird. Auch Browser-Anbieter sind in den letzten Jahren deutlich datenschutzbewusster geworden und möchten die Daten ihrer Nutzer besser vor allzu datenhungrigen Adtech-Tools schützen.

Ähnlich schränken Initiativen wie Safaris "Intelligent Tracking Prevention" (ITP) und Firefox' "Enhanced Tracking Prevention" (ETP) den Zugriff auf häufig verwendete Browser-Speicheroptionen (insbesondere Cookies und lokalen Speicher) stark ein. Google hat kürzlich ebenfalls angekündigt, dass sie Drittanbieter-Cookies in ihrem Chrome-Browser innerhalb der nächsten zwei Jahre vollständig abschaffen werden (ein sogenannter "Privacy Sandbox" wird Drittanbieter-Cookies ersetzen).

Oft haben Werbetreibende auch JavaScript-Snippets auf ihren Websites implementiert, ohne sich über deren volle Funktionalität im Klaren zu sein, was dazu führt, dass sie die Kontrolle über die Daten ihrer Nutzer an unbekannte Dritte abgeben und damit massive Datenschutzverletzungen überhaupt erst ermöglichen.

Daher sollten wir die allgemeine Richtung dieser Maßnahmen begrüßen, da sie dazu beitragen, unsere persönlichen Daten zu sichern, die Branche zu erwachsen werden zu lassen und verlorenes Vertrauen zurückzugewinnen – mit dem Ziel, fragwürdige "Wild-West-Tracking"-Praktiken zu beenden.

Der Hauptnachteil dieser Bewegung ist jedoch, dass sie auch Auswirkungen auf geschäftskritische Datenerhebungen basierend auf Nutzerzustimmungen hat: Das technische und regulatorische Umfeld, in dem traditionelles Website- und App-Tracking eingebettet ist, macht es uns schwer, das Verhalten spezifischer Nutzer nachzuverfolgen – was unsere Fähigkeit, die Bedürfnisse der Nutzer zu verstehen, einschränkt.

## GTM Server-Side Tagging als Lösung

Der Google Tag Manager (GTM) kommt jetzt mit einer neuen Funktion (derzeit im Beta-Status), die es Unternehmen ermöglicht, ein First-Party-Analytics-Setup zu erstellen. GTM Server-Side Tagging ist da, um die Art und Weise zu verändern, wie Website- und App-Tracking implementiert wird und wie Daten mit Dritten geteilt werden. In den nachfolgenden Abschnitten erläutere ich, wie diese Funktion hilft, die Benutzererfahrung auf der Website zu verbessern, die Sicherheit der Nutzerdaten zu erhöhen und die Kontrolle über die Datenerfassung zu stärken.

### Wie funktioniert es?

Während der GTM Server-Side Container neue Tools und Funktionen zur Messung der Nutzeraktivität bereitstellt, bleibt das allgemeine Modell von Tags, Triggern und Variablen unverändert.

![gtm-server-side-architecture](/assets/img/gtm-server-side/server-side-tagging.png)
_Quelle: https://developers.google.com/tag-platform/tag-manager/server-side/intro_

GTM Server-Side Tagging bedeutet, dass ein neuer „Server“-Container auf einer App Engine-Instanz läuft – idealerweise der Namespace deiner Domain – in deiner eigenen Google Cloud Platform (GCP)-Projekt. Es ist dann möglich, HTTP-Anfragen vom Gerät des Nutzers oder einem anderen internetfähigen Gerät an den Server zu senden. Der GTM-Server wandelt diese Anfragen in Ereignisse um, die von den Tags, Triggern und Variablen des Containers verarbeitet werden.

Während das bekannte Konzept von Tags, Triggern und Variablen wie gewohnt in clientseitigen GTM-Containern funktioniert, ist der neu eingeführte „Client“ die Brücke zwischen den Geräten, die Anfragen senden, und der Logik des Containers. Der Client kann Anfragen empfangen und beanspruchen (sowie die damit gesendeten Daten), sie in ein oder mehrere Ereignisse parsen, Daten zur Verarbeitung an den Container (Tags, Trigger und Variablen) weiterleiten und eine HTTP-Antwort an das anfragende Gerät zurücksenden.

### Kontrolle und Flexibilität über Daten gewinnen

Der Unterschied zu einem Tracking, das auf clientseitigem JavaScript und Pixeln basiert, besteht darin, dass Sie die volle Kontrolle und Flexibilität darüber haben, wie die Daten verarbeitet werden, bevor Sie sie an Drittanbieter-Tools senden (ermöglicht Hit-Validierung, PII-Kontrollen usw.). Da der GTM-Server (`https://gtm.example.com`) mit der gleichen Domain wie Ihre Website (`https://example.com`) verbunden ist, wird jede Interaktion zwischen ihnen vom Browser des Nutzers als First-Party-Datenaustausch betrachtet.

### Einschränkungen durch Browser-Tracking-Prävention und Adblocker mindern

Durch diesen Kontextwechsel werden erhebliche Einschränkungen durch die Browser-Tracking-Prävention umgangen, da Du die Möglichkeit erhältst, First-Party-HTTP-Cookies zu setzen (z. B. führt GTM Server-Side ein neues FPID-Cookie ein). Beispielsweise wird Safaris ITP nun nicht mehr die Lebensdauer von Cookies einschränken, die mit Google Analytics verbunden sind, wenn diese serverseitig gesetzt werden, was zu einer besseren Datenqualität für Berichte und Analysen führt (insbesondere relevant für Unternehmen mit einer jungen und technikaffinen Zielgruppe). Du solltest jedoch bedenken, dass diese neue "Macht" große Verantwortung mit sich bringt, und Du solltest sich stets der rechtlichen und ethischen Implikationen des Setzens von Cookies und der Datenerhebung bewusst sein.

## Welche Anwendungsfälle können sich ergeben?

GTM Server-Side Tracking stellt die Transparenz bei der Nutzung von Drittanbieter-Tools und Websites wieder her, doch darüber hinaus gibt es noch einige andere Vorteile des serverseitigen Trackings, die starke Anwendungsfälle für Unternehmen schaffen können.

### Verbesserte Datengenauigkeit und Kontrolle

Die Datengenauigkeit kann noch weiter verbessert werden, wenn Unternehmen sich entscheiden, die serverseitige Kommunikation für geschäftskritische Ereignisse wie Transaktionen zu nutzen. Wir alle haben schon Diskrepanzen zwischen der Anzahl von Transaktionen in Google Analytics (GA) und CRM-Systemen erlebt, die auf Adblocker und andere Nebeneffekte des clientseitigen Trackings (Seiten-Neuladungen usw.) zurückzuführen sind. Dies kann vermieden werden, indem das clientseitige Tracking von Transaktionen entfernt und die erforderlichen Datenpunkte direkt von deinem CRM-Systemen an den GTM-Server gesendet werden, um sie an GA zur Analyse weiterzuleiten.

### Verbesserte Seitenladegeschwindigkeit und Datensicherheit

Generell kann serverseitiges Tracking die Verarbeitungsbelastung von einem bestimmten Browser in die Cloud verlagern. Da eine HTTP-Anfrage ausreicht, um ein Ereignis im Server-Side-Container auszulösen, kann sie mehrere Tags in der serverseitigen Umgebung auslösen. Beispielsweise könnte der Client bei jedem Seitenaufruf eine HTTP-Anfrage senden, die einen Seitenaufruf für GA und Facebook gleichzeitig auslöst. Da kein von Facebook geschriebenes JavaScript im Browser des Nutzers ausgeführt werden muss, könnte das serverseitige Tracking die Seitenladegeschwindigkeit erhöhen. Da dies die Benutzererfahrung positiv beeinflusst, kann dies deine Conversion Rates steigern.

### Nahtlose Integration in die Google Cloud Platform

Darüber hinaus wird es durch die Ausführung des GTM-Containers in der Google-Cloud-Integration wahrscheinlich bald möglich sein, andere GCP-Ressourcen wie BigQuery, ML Engine und Cloud Functions zu integrieren. Dies wird zahlreiche Möglichkeiten für fortgeschrittene Anwendungsfälle eröffnen, die maschinelles Lernen und [eventbasierte Analysen](https://gunnargriese.com/posts/ga4-the-cdp-you-didnt-know-you-had/) nutzen.

Sobald diese neue GTM-Funktion aus der Beta-Phase herauskommt und basierend auf Funktionsanforderungen und Beiträgen aktiver Community-Mitglieder verbessert wird, werden noch mehr Möglichkeiten verfügbar sein, was die Tracking-Implementierungen auf Basis von GTM erheblich verändern wird.

> **Hinweis**: Mehr über die Möglichkeiten der Integration von GCP-Diensten in GTM Server-Side, um in Zukunft leistungsstarke Anwendungsfälle freizuschalten, erfährst DU in [meiner neuesten Blog-Serie](https://gunnargriese.com/posts/gtm-server-side-firestore-integrations/).

## Abschließende Gedanken

Die Veröffentlichung des GTM Server-Side Containers setzt einen allgemeinen Trend fort, der bei vielen Google Marketing Platform-Tools zu beobachten ist: die Stärkung der Tool-Integration und die Hinwendung zur GCP. Durch diese Strategie stellt Google einen reibungslosen Datenfluss zwischen den Systemen sicher und erhöht gleichzeitig die Funktionalität jedes Tools, um mit dem sich ständig ändernden Adtech-Umfeld Schritt zu halten.
