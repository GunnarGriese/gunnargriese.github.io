---
title: Debugging von Google Analytics Tracking für Mobile Apps - Ein Leitfaden für Anfänger
author: gunnar
date: 2023-05-05 11:24:15 +0200
categories: [Firebase Analytics]
tags: [ga4, firebase-analytics, charles-proxy, gtm, ios-debugger]
comments: true
lang: de
permalink: /posts/firebase-analytics-debugging/
---

Bist du ein digitaler Analyst, der Google Analytics Tracking über Firebase für deine mobilen iOS-Apps implementieren und debuggen möchte und keine Ahnung hat, wo du anfangen sollst? Dieser Blogbeitrag ist für dich! Ich werde dich kurz durch den Prozess der Einrichtung von Google Analytics Tracking mit dem Firebase SDK und Google Tag Manager (GTM) führen. Vor allem werde ich die effektivsten Debugging-Tools vorstellen, einschließlich Charles Proxy und David Vallejos iOS/Android Debugger, um dir zu helfen, eine genaue und zuverlässige Datenerfassung zu erreichen.

## Einführung in Google Analytics Tracking für Apps

Google Analytics 4 (GA4) markiert das Debüt einer einheitlichen Plattform für das Tracking von Web- und Mobile-App-Daten in Googles Analytics-Suite. Diese Änderung erkennt den zunehmenden Trend an, dass Unternehmen ihre Websites und mobilen Apps als miteinander verbunden betrachten, anstatt als separate Verkaufskanäle. GA4 wurde entwickelt, um ein umfassenderes Verständnis der Benutzerinteraktionen über verschiedene Plattformen hinweg zu ermöglichen.

Da GA4 Web- und App-Analysen enger integriert, müssen digitale Analysten ihr Wissen über App-Tracking erweitern, um das volle Potenzial von GA4 auszuschöpfen. Traditionell konzentrierten sich die meisten digitalen Analysten hauptsächlich auf Website-Messungen, die über Google Tag Manager (GTM) oder gtag.js implementiert wurden.

![ga4-data-collection](/assets/img/firebase-debug/ga4-data-collection.png)
_Quelle: https://developers.google.com/analytics/devguides/collection/protocol/ga4_

Die Implementierung und das Debugging von GA4 für Apps unterscheidet sich jedoch erheblich vom webbasierten Ansatz und ist aufwändiger.

Es gibt zwei Hauptmethoden, um GA4-Tracking in deinen mobilen Apps zu aktivieren:

1. Ausschließliche Verwendung des Firebase SDK
2. Verwendung des Firebase SDK in Verbindung mit GTM für Android/iOS

### Firebase SDK

Firebase ist eine umfassende App-Entwicklungsplattform, die verschiedene Tools und Dienste anbietet, um Entwicklern beim Erstellen, Verbessern und Wachsen ihrer Apps zu helfen. Mit einer direkten Integration in GA4 über das Analytics Software Development Kit (SDK) bietet Firebase wertvolle Einblicke in das Benutzerverhalten und die App-Leistung.

{% include embed/youtube.html id='8iZpH7O6zXo' %}

Durch die Integration des Firebase Analytics SDK in deine App kannst du die Leistungsfähigkeit von Google Analytics 4 (GA4) nutzen, um Benutzerinteraktionen, E-Commerce-Aktionen und andere wichtige Metriken zu verfolgen. Entwickler bevorzugen oft diesen Ansatz, da er fortschrittliche Datenerfassungs- und Analysefähigkeiten sowie zusätzliche Firebase-Funktionen wie Cloud Messaging und Crashlytics bietet.

### Google Tag Manager für Apps

GTM bietet zwei Container-Typen für native App-Tagging-Setups: Android und iOS, die speziell für ihre jeweiligen App-Typen entwickelt wurden. Beide Container verfügen über mehrere Tag-Typen (hauptsächlich Google-spezifisch) sowie begrenzte Trigger- und Variablenmöglichkeiten im Vergleich zum GTM-Web-Container.

![gtm-tag-types](/assets/img/firebase-debug/gtm-tag-types.png)
_Tag-Optionen im GTM iOS-Container_

Obwohl GTM für Websites ein leistungsstarkes und praktisches Tool ist, um Messungen ohne notwendige Änderungen am Quellcode zu ermöglichen, ist es für App-Tracking aus zwei Hauptgründen weniger nützlich:

1. Die Möglichkeiten des App-Containers sind begrenzt. Zum Beispiel gibt es keine Möglichkeit, benutzerdefinierten Code über den Container in die App einzufügen, und nur wenige Anzeigen-Pixel werden unterstützt (wie bereits erwähnt).
2. App-Container sind aus Sicht des Debuggings und der Bereitstellung unpraktisch. Zum Beispiel musst du jedes Mal, wenn du Änderungen an deinem Container vornimmst, diesen exportieren, die exportierte JSON in deine App einbetten und eine neue App-Version veröffentlichen, damit deine Benutzer die Änderungen sehen können.

Infolgedessen müssen grundlegende Änderungen im Quellcode der App vorgenommen werden, und die meisten Spezialisten sind sich einig, dass GTM-App-Container nicht die "Standard"-Wahl für dein Tracking-Setup sein sollten - stattdessen sollte es einen triftigen Grund für ihre Verwendung geben. Da du jedoch in realen Situationen auf diese Container-Typen stoßen könntest, wurden sie in dieser Übersicht zu deiner Information aufgenommen.

## Google Analytics Tracking für Apps einrichten

Der folgende Abschnitt bietet einen Überblick über die Implementierung von App-Tracking über das Firebase SDK und GTM für Apps. Da sich dieser Artikel hauptsächlich auf den Debugging-Prozess konzentriert und in der Praxis die SDK-Implementierung normalerweise von App-Entwicklern übernommen wird, werden wir nicht ins Detail gehen.

Trotzdem ist es sehr empfehlenswert, dass du eine eigene Test-App einrichtest. Dadurch kannst du den SDK-Implementierungsprozess aus erster Hand erleben, die Tracking-Möglichkeiten von Firebase erkunden und letztendlich dein Verständnis von GA4 App-Tracking verbessern.

Es gibt zahlreiche Tutorials, aber dieses sticht durch sein gut strukturiertes und leicht zu befolgendes Format hervor:

{% include embed/youtube.html id='X2W9MPjrIbk' %}

### Firebase SDK installieren

Um Google Analytics Tracking mit dem Firebase SDK einzurichten, befolge bitte diese Schritte (weitere Details in der [offiziellen Dokumentation](https://firebase.google.com/docs/analytics/get-started?platform=ios)):

1. Erstelle ein Firebase-Projekt in der Firebase-Konsole.
2. Füge deine iOS-App zum Projekt hinzu, indem du die Bundle-ID der App angibst.
3. Lade das Firebase SDK herunter und integriere es in deine App, indem du der offiziellen Dokumentation folgst.
4. Aktiviere GA4 in deinen Firebase-Projekteinstellungen.
5. Füge [Consent Mode v2](/posts/consent-mode-v2/) zu deiner App hinzu, um die volle Verfügbarkeit von Googles Audience-Funktionen zu haben.
6. Implementiere Event-Tracking im Code deiner App, um bestimmte Benutzeraktionen und App-Leistung zu verfolgen.

### Google Tag Manager hinzufügen

Da GTM für Apps im Wesentlichen eine Firebase-Erweiterung ist, funktioniert es nur, wenn du auch das Firebase SDK korrekt implementiert hast. Ansonsten sieht der Setup-Ablauf wie folgt aus (weitere Details in der [offiziellen Dokumentation](https://developers.google.com/tag-platform/tag-manager/ios/v5)):

1. Füge das Google Tag Manager Paket hinzu
2. Erstelle einen iOS- oder Android-GTM-Container (falls zutreffend)
3. Nimm Änderungen in deinem GTM-Workspace vor und veröffentliche sie
4. Exportiere deine Container-Version (`.json`-Datei)
5. Füge die heruntergeladene Datei zu deinem App-Projekt hinzu

### GA4 Event-Tracking aktivieren

Um Events für GA4 zu loggen, verwende die logEvent-Methode, die vom Firebase Analytics SDK bereitgestellt wird. Diese Methode erfordert einen Event-Namen und optional ein Bündel von Parametern, um zusätzliche Informationen über das Event bereitzustellen. Zum Beispiel könntest du ein benutzerdefiniertes "purchase"-Event [mit den erforderlichen Parametern](https://developers.google.com/analytics/devguides/collection/protocol/ga4/reference/events#purchase) wie transaction_id, Artikelname, Preis und Währung loggen.

```swift
// Ein Paar Jeggings
var jeggings: [String: Any] = [
  AnalyticsParameterItemID: "SKU_123",
  AnalyticsParameterItemName: "jeggings",
  AnalyticsParameterItemCategory: "pants",
  AnalyticsParameterItemVariant: "black",
  AnalyticsParameterItemBrand: "Google",
  AnalyticsParameterPrice: 9.99,
  AnalyticsParameterQuantity = 2
]

// Kaufparameter vorbereiten
var purchaseParams: [String: Any] = [
  AnalyticsParameterTransactionID: "T12345",
  AnalyticsParameterAffiliation: "Google Store",
  AnalyticsParameterCurrency: "USD",
  AnalyticsParameterValue: 14.98,
  AnalyticsParameterTax: 2.58,
  AnalyticsParameterShipping: 5.34,
  AnalyticsParameterCoupon: "SUMMER_FUN"
]

// Artikel hinzufügen
purchaseParams[AnalyticsParameterItems] = [jeggings]

// Kauf-Event loggen
Analytics.logEvent(AnalyticsEventPurchase, parameters: purchaseParams)
```

Dieser Code-Snippet führt dazu, dass ein Kauf-Event von deiner App gesendet wird. Dieses Event wird von deinem GTM-Container erfasst, und du kannst das "purchase"-Event verwenden, um einen anderen Tag in deinem GTM-Container auszulösen (s. unten) und auf die Event-Parameter über eingebaute Variablen zugreifen.

![floodlight-tag](/assets/img/firebase-debug/floodlight-tag.png)

Für eine detailliertere Beschreibung des Setup-Prozesses kann ich empfehlen, Simo Ahavas Schnellstartanleitungen für Android und iOS durchzuarbeiten.

## Debugging von Google Analytics Tracking für Apps

Die Bedeutung des Debuggings von Google Analytics Tracking kann nicht genug betont werden, da es eine genaue und zuverlässige Datenerfassung sicherstellt, die entscheidend für den Aufbau von Vertrauen und das Treffen fundierter Entscheidungen über App-Entwicklung und Marketingstrategien ist. Durch das Identifizieren und Lösen von Problemen wie fehlenden oder ungenauen Daten, Konfigurationsfehlern und SDK-Kompatibilität können du und deine Stakeholder ein umfassendes Verständnis des Benutzerverhaltens, der App-Leistung und der Verbesserungsmöglichkeiten gewinnen.
In den folgenden Abschnitten werde ich dich durch die verfügbaren Optionen führen. Je nach deinen Ressourcen und deinem Setup empfehle ich dir, die für dich effizienteste Option zum Debuggen deiner Tagging-Implementierung zu wählen.