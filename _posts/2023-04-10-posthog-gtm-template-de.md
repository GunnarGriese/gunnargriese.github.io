---
title: Entfesseln Sie das Potenzial der PostHog Analytics-Plattform mit Google Tag Manager
author: gunnar
date: 2023-04-10 08:24:15 +0200
categories: [GTM]
tags: [gtm, custom-templates, posthog]
comments: false
lang: de
permalink: /posts/posthog-gtm-template/
---

In der heutigen datengetriebenen Welt ist das Verständnis des Nutzerverhaltens für jedes Unternehmen entscheidend. Product Analytics-Plattformen wie PostHog haben sich als essentielle Tools erwiesen, um Einblicke darüber zu gewinnen, wie Nutzer mit Ihrer Website oder App interagieren. In diesem Blogbeitrag werden wir die PostHog Analytics-Plattform, ihre SDKs, insbesondere das JavaScript-SDK, Google Tag Manager Tag-Vorlagen und wie Du PostHog mit Google Tag Manager mithilfe einer benutzerdefinierten Tag-Vorlage integrieren kannst, näher betrachten.

## Einführung in die PostHog Analytics-Plattform

[PostHog](https://posthog.com/) ist eine Open-Source-Produktanalyseplattform, die Dir hilft, das Nutzerverhalten auf Ihrer Website oder App zu analysieren. Sie bietet ereignisbasiertes Tracking, Trichteranalyse, Nutzersegmentierung und andere wesentliche Funktionen, um zu verstehen, wie Nutzer mit dem Produkt interagieren, für das Du verantwortlich sind. Posthog hat einen ähnlichen Fokus wie Tools wie Mixpanel, Heap und Amplitude, die sich alle darauf spezialisiert haben, Produktmanagern und -analysten die erforderlichen Erkenntnisse zu liefern, um ihre Plattform auf die Bedürfnisse ihrer Nutzer zu optimieren.

Wenn Du nach einer tiefgreifenden Analyse suchen, wie sich Produktanalyse von Marketing-Analyse unterscheidet, empfehle ich Dir, [Adam Grecos Blogserie](https://amplitude.com/blog/marketing-analytics-vs-product-analytics-part-1) zu diesem Thema zu lesen.

## PostHog SDKs für die Datenerfassung

PostHog selbst bietet eine Vielzahl von SDKs (Software Development Kits), um Dir die Datenerfassung von verschiedenen Plattformen zu erleichtern:

- JavaScript: Zum Tracking von Nutzerinteraktionen auf Websites.
- Python: Für Backend-Anwendungen oder Datenpipelines.
- Ruby: Für Ruby on Rails-Anwendungen.
- PHP: Für PHP-basierte Anwendungen.
- Go: Für Anwendungen, die in Go geschrieben sind.
- Node.js: Für serverseitige JavaScript-Anwendungen.
- Android: Für Android-Apps.
- iOS: Für iOS-Apps.

Diese SDKs ermöglichen es Dir, PostHog-Tracking in Ihrer Anwendung oder Website zu implementieren, unabhängig von dem verwendeten Technologie-Stack.

## Details zum JavaScript-SDK

Das [PostHog JavaScript-SDK](https://posthog.com/docs/libraries/js) ist das am häufigsten verwendete SDK zum Tracking von Nutzerinteraktionen auf Websites. Es bietet eine einfache API zum Senden von Ereignissen, Identifizieren von Nutzern und Verwalten von Nutzereigenschaften. Du kannst damit benutzerdefinierte Ereignisse, Seitenaufrufe, Klicks, Formularübermittlungen und mehr mit minimalem Code erfassen.

Das SDK unterstützt auch fortgeschrittene Funktionen wie Autocapture, das automatisch Nutzerinteraktionen mit Deiner Website verfolgt, ohne dass zusätzlicher Code erforderlich ist. Du kannst  das SDK nach Deinen Bedürfnissen konfigurieren, wie zum Beispiel das Deaktivieren bestimmter Funktionen oder das Anpassen der Datenerfassung.

## Google Tag Manager Benutzerdefinierte Vorlagen

Da ich persönlich die meiste Zeit mit Google Tag Manager (GTM) und Google Analytics (GA) arbeite, ist GTM tatsächlich mein bevorzugtes Tool, wenn es darum geht, JS-Tracking-Code auf Websites oder Web-Apps zu implementieren, und es wird weit verbreitet eingesetzt. Wenn Deine Organisation nicht nur Produktanalyse betreibt, sondern auch aktiv digitale Marketingkampagnen durchführt, besteht eine hohe Wahrscheinlichkeit, dass dein Produkt bereits GTM eingebettet hat.

Google Tag Manager (GTM) ist ein leistungsstarkes Tool, mit dem Du Marketing-Tags, Analytics-Tracking und andere Code-Snippets auf Deiner Website verwalten und bereitstellen kannst, ohne dass manuelle Code-Aktualisierungen erforderlich sind. GTM verwendet Tag-Vorlagen, die vorgefertigte Code-Snippets sind, die an Ihre spezifischen Tracking-Anforderungen angepasst werden können.

Tag-Vorlagen helfen dabei, den Prozess der Implementierung von Tracking-Skripten von Drittanbietern, wie PostHog, auf Deiner Website zu optimieren. Sie ermöglichen es Dir, Tracking-Einstellungen zu konfigurieren, ohne direkt Code zu bearbeiten, was die Verwaltung und Pflege Deiner Tracking-Implementierungen erleichtert. Diese Vorlagen können in die GTM-Vorlagengalerie eingereicht werden und stehen dann allen zur Verfügung, die sie nutzen möchten.

Der Haken ist, dass PostHog noch keine offizielle Vorlage veröffentlicht hat, um ihr JS-SDK über GTM auszuführen. Deshalb habe ich mich daran gemacht, (die meisten) Funktionalitäten des PostHog JS-SDK in GTM zu bringen, ohne dass [(potenziell schädliche)](https://web.dev/tag-best-practices/#be-careful-with-custom-html-tags:~:text=Be%20careful%20with%20Custom%20HTML%20tags%20%23) benutzerdefinierte HTML-Tags bereitgestellt werden müssen.

## Integration von PostHog mit Google Tag Manager mithilfe der bereitgestellten Vorlage

Die bereitgestellte PostHog GTM-Tag-Vorlage macht es einfach, PostHog-Tracking in Ihren GTM-Container zu integrieren.

![posthog-event-template](/assets/img/posthog/posthog-custom-event.png)
_Implementierung eines benutzerdefinierten Ereignisses mit Ereignisparametern mithilfe der GTM-Vorlage_

Mit dieser Vorlage kannst Du Ereignisse, Nutzereigenschaften und Konfigurationseinstellungen direkt von Deinem GTM-Arbeitsbereich aus verwalten. Hier ist, was Du mit der Vorlage tun kannst:

- Initialisiere PostHog mit verschiedenen Konfigurationsoptionen.
- Erfasse Ereignisse und virtuelle Seitenaufrufe mit benutzerdefinierten Eigenschaften.
- Identifiziere Nutzer mit Nutzereigenschaften.

Weiter unten habe ich einige Beispiele für die Funktionalitäten der GTM-Vorlage gelistet.

### Initialisierung — Grundkonfiguration

![posthog-config-tag](/assets/img/posthog/posthog-config.png)
_Beispielhafte Konfiguration des Initialisierungs-Tags_

Siehe detaillierte Dokumentation für jede der Konfigurationsoptionen hier. Die in der Tag-Vorlage repräsentierten Konfigurationsoptionen sind:

- `apiHost`: Die Domain Ihrer PostHog-Instanz (z.B. `https://app.posthog.com`). Das Tag wird `/static/array.js` an diesen Wert anhängen, um die tatsächliche Anfrage-URL zu erstellen.
- `apiKey`: PostHog-Projekt-API-Schlüssel
- `autocapture_tuning`: Benutzerdefinierte Allowlist-Einstellungen für Autocapture.
- `autocapture_off`: Deaktiviere Autocapture vollständig.
- `capture_pageview`: Aktiviere/Deaktiviere die Erfassung von Seitenaufrufen.
- `capture_pageleave`: Aktiviere/Deaktiviere die Erfassung von Seitenverlassensereignissen.
- `cross_subdomain_cookie`: Aktiviere/Deaktiviere Subdomain-übergreifendes Cookie-Tracking.
- `disable_persistence`: Aktiviere/Deaktiviere die Cookie/LocalStorage-Persistenz.
- `disable_session_recording`: Aktiviere/Deaktiviere  die Sitzungsaufzeichnung.
- `enable_recording_console_log`: Aktiviere/Deaktiviere die Aufzeichnung von Konsolenprotokollen.
- `mask_all_text`: Aktiviere/Deaktiviere die Maskierung allen Textes.

### Initialisierung — Erweiterte Tracker-Konfiguration

![posthog-callback](/assets/img/posthog/posthog-callback.png)
_Beispielhafte Callback-Funktion_

Die PostHog-Bibliothek kann mit einem _Callback_ initiiert werden (z.B. Aufruf von `identify`), der ausgeführt wird, sobald die Bibliothek geladen wurde.

Damit die Callback-Funktion in der GTM-Vorlagenversion funktioniert, musst Du eine benutzerdefinierte JS-Variable im Feld `loaded` referenzieren (s. Screenshot im Abschnitt Grundkonfiguration), die eine Funktion zurückgibt.

Sobald die PostHog-Skripte verarbeitet und der Tracker initiiert ist, wird diese Funktion ausgeführt.

### Benutzerdefinierte Ereignisse, Nutzereigenschaften und Ereignisparameter

![posthog-event-params](/assets/img/posthog/posthog-event-params.png)
_Beispielhafte Implementierung eines benutzerdefinierten Ereignis-Tags_

Mit der GTM-Vorlage kannst Du mühelos benutzerdefinierte Ereignisse (sowie virtuelle Seitenaufrufe) verfolgen und sie mit fein abgestimmten Ereignisparametern anreichern, was ein umfassendes Verständnis der Nutzerengagement-Muster ermöglicht. Darüber hinaus hat die Vorlage die Funktionalität des JavaScript-SDK übernommen, die es Dir ermöglicht, Nutzereigenschaften sowohl mit den Methoden `$set` als auch `$set_once` festzulegen, was Dir die Flexibilität gibt, zwischen dem Aktualisieren von Werten oder dem Bewahren der ursprünglichen Nutzerattribute zu wählen.

## Wie fange ich an?

Bitte zögere nicht, [die Vorlage herunterzuladen](https://github.com/GunnarGriese/gtm-template-posthog) von meinem GitHub und sie auszuprobieren. Ich freue mich über jedes Feedback, um die Vorlage zu verbessern, mehr Funktionalitäten aus dem Original-SDK einzubeziehen und potenzielle Fehler zu beheben, wenn sie auftreten.

Um die Vorlage zu verwenden, importiere sie einfach in deinen GTM-Arbeitsbereich, erstelle ein neues Tag mit der Vorlage und konfiguriere die Einstellungen basierend auf deinen Bedürfnissen. Diese Integration stellt sicher, dass Du sowohl PostHog als auch Google Tag Manager voll ausnutzen kannst, um Einblicke in das Nutzerverhalten auf deiner Website oder App zu gewinnen.

Während dieser Artikel einen Ansatz skizziert, wie man PostHog über GTM implementiert, möchtest Du vielleicht auf PostHog's großartige und leicht zu befolgende [Dokumentation](https://posthog.com/docs/getting-started/start-here) zurückgreifen, um deine Arbeit mit der Plattform zu beginnen.

## Zusammenfassung

Zusammenfassend lässt sich sagen, dass PostHog eine leistungsstarke Analyseplattform ist, die Dir helfen kann, deine Nutzer besser zu verstehen. Durch die Integration mit Google Tag Manager mithilfe der bereitgestellten Tag-Vorlage kannst Du den Implementierungsprozess optimieren und dein Tracking-Setup effizient verwalten. Diese Kombination von PostHog und Google Tag Manager wird hoffentlich dazu beitragen, Implementierungsprojekte zu beschleunigen und dich in die Lage versetzen, noch schneller datengesteuerte Entscheidungen treffen zu können. Also los, erforsche das Potenzial der PostHog-Analyseplattform und der Google Tag Manager-Integration und erschließe neue Erkenntnisse über das Verhalten deiner Nutzer. Happy tracking!