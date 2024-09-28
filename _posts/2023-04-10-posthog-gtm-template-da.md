---
title: Udnyt potentialet i PostHog Analytics-platformen med Google Tag Manager
author: gunnar
date: 2023-04-10 08:24:15 +0200
categories: [GTM]
tags: [gtm, custom-templates, posthog]
comments: false
lang: da
permalink: /posts/posthog-gtm-template/
---

I dagens datadrevne verden er forståelse af brugeradfærd afgørende for enhver virksomhed. Produktanalyseplat forme som PostHog er blevet essentielle værktøjer til at få indsigt i, hvordan brugere interagerer med dit websted eller app. I dette blogindlæg vil vi udforske PostHog analytics-platformen, dens SDK'er, særligt JavaScript SDK'et, Google Tag Manager tag-skabeloner, og hvordan du kan integrere PostHog med Google Tag Manager ved hjælp af en brugerdefineret tag-skabelon.

## Introduktion til PostHog Analytics Platform

[PostHog](https://posthog.com/) er en open-source produktanalyseplat form, der hjælper dig med at analysere brugeradfærd på dit websted eller app. Den tilbyder begivenhedsbaseret sporing, tragtanalyse, brugersegmentering og andre essentielle funktioner til at forstå, hvordan brugere engagerer sig med det produkt, du er ansvarlig for. Den befinder sig i samme rum som værktøjer som Mixpanel, Heap og Amplitude, som alle specialiserer sig i at give produktchefer og analytikere de nødvendige indsigter til at optimere deres platform mod brugernes behov.

Hvis du leder efter en dybtgående gennemgang af, hvordan produktanalyse adskiller sig fra marketing-analyse, anbefaler jeg at tjekke [Adam Grecos blogserie](https://amplitude.com/blog/marketing-analytics-vs-product-analytics-part-1) om emnet.

## PostHog SDK'er til dataindsamling

PostHog tilbyder selv en række SDK'er (Software Development Kits) for at gøre det let for dig at indsamle data fra forskellige platforme:

- JavaScript: Til sporing af brugerinteraktioner på websteder.
- Python: Til backend-applikationer eller datalinjer.
- Ruby: Til Ruby on Rails-applikationer.
- PHP: Til PHP-baserede applikationer.
- Go: Til applikationer skrevet i Go.
- Node.js: Til server-side JavaScript-applikationer.
- Android: Til Android-apps.
- iOS: Til iOS-apps.

Disse SDK'er gør det muligt for dig at implementere PostHog-sporing i din applikation eller på dit websted, uanset hvilken teknologistak du bruger.

## Detaljer om JavaScript SDK'et

[PostHog JavaScript SDK'et](https://posthog.com/docs/libraries/js) er det mest anvendte SDK til sporing af brugerinteraktioner på websteder. Det giver en simpel API til at sende begivenheder, identificere brugere og administrere brugereg enskaber. Du kan spore brugerdefinerede begivenheder, sidevisninger, klik, formularindsendelser og mere med minimal kode.

SDK'et understøtter også avancerede funktioner som autocapture, der automatisk sporer brugerinteraktioner med dit websted uden at kræve yderligere kode. Du kan konfigurere SDK'et til at passe til dine behov, såsom at deaktivere visse funktioner eller tilpasse, hvordan data indfanges.

## Google Tag Manager Brugerdefinerede Skabeloner

Da jeg personligt bruger det meste af min tid på at arbejde med Google Tag Manager (GTM) og Google Analytics (GA), er GTM faktisk mit foretrukne værktøj, når det kommer til at implementere JS-sporingskode på websteder eller web-apps, og det bruges bredt. Hvis din organisation ikke kun beskæftiger sig med produktanalyse, men også aktivt kører digitale marketingkampagner, er der en stor chance for, at dit produkt allerede har GTM indlejret.

Google Tag Manager (GTM) er et kraftfuldt værktøj, der giver dig mulighed for at administrere og implementere marketing-tags, analyticssporing og andre kodestykker på dit websted uden behov for manuelle kodeopdateringer. GTM bruger tag-skabeloner, som er forudbyggede kodestykker, der kan tilpasses til at passe til dine specifikke sporingskrav.

Tag-skabeloner hjælper med at strømline processen med at implementere tredjeparts sporingsskripter, som PostHog, på dit websted. De giver dig mulighed for at konfigurere sporingsindstillinger uden at redigere kode direkte, hvilket gør det lettere at administrere og vedligeholde dine sporingsimplementeringer. Disse skabeloner kan indsendes til GTM Template Gallery og er derefter tilgængelige for alle, der ønsker at bruge dem.

Udfordringen er, at PostHog endnu ikke har udgivet en officiel skabelon til at køre deres JS SDK gennem GTM. Det er derfor, jeg satte mig for at bringe (de fleste af) funktionaliteterne fra PostHog's JS SDK til GTM uden behov for at implementere nogen [(potentielt skadelige)](https://web.dev/tag-best-practices/#be-careful-with-custom-html-tags:~:text=Be%20careful%20with%20Custom%20HTML%20tags%20%23) brugerdefinerede HTML-tags.

## Integration af PostHog med Google Tag Manager ved hjælp af den medfølgende skabelon

Den medfølgende PostHog GTM tag-skabelon gør det enkelt at integrere PostHog-sporing i din GTM-container.

![posthog-event-template](/assets/img/posthog/posthog-custom-event.png)
_Implementering af brugerdefineret begivenhed med begivenhedsparametre ved hjælp af GTM-skabelonen_

Med denne skabelon kan du administrere begivenheder, brugereg enskaber og konfigurationsindstillinger direkte fra dit GTM-arbejdsområde. Her er, hvad du kan gøre med skabelonen:

- Initialisere PostHog med forskellige konfigurationsmuligheder.
- Indfange begivenheder og virtuelle sidevisninger med brugerdefinerede egenskaber.
- Identificere brugere med brugereg enskaber.

Se nedenfor for nogle eksempler på GTM-skabelonens funktionaliteter.

### Initialisering — Grundlæggende konfiguration

![posthog-config-tag](/assets/img/posthog/posthog-config.png)
_Eksemplarisk konfiguration af initialiseringstagget_

Se detaljeret dokumentation for hver af konfigurationsmulighederne her. Konfigurationsmulighederne repræsenteret i tag-skabelonen er:

- `apiHost`: Domænet for din PostHog-instans (f.eks. `https://app.posthog.com`). Tagget vil tilføje `/static/array.js` til denne værdi for at opbygge den faktiske anmodnings-URL.
- `apiKey`: Din PostHog-projekt API-nøgle
- `autocapture_tuning`: Brugerdefinerede allowlist-indstillinger for autocapture.
- `autocapture_off`: Deaktiver autocapture fuldstændigt.
- `capture_pageview`: Aktivér/deaktiver indfangning af sidevisninger.
- `capture_pageleave`: Aktivér/deaktiver indfangning af side-forladelsesbegivenheder.
- `cross_subdomain_cookie`: Aktivér/deaktiver cookie-sporing på tværs af subdomæner.
- `disable_persistence`: Aktivér/deaktiver cookie/localStorage persistens.
- `disable_session_recording`: Aktivér/deaktiver sessionsoptagelse.
- `enable_recording_console_log`: Aktivér/deaktiver optagelse af konsollog.
- `mask_all_text`: Aktivér/deaktiver maskering af al tekst.

### Initialisering — Avanceret tracker-konfiguration

![posthog-callback](/assets/img/posthog/posthog-callback.png)
_Eksemplarisk callback-funktion_

PostHog-biblioteket kan initialiseres med en _callback_ (f.eks. kald `identify`), der udføres, når biblioteket er indlæst.

For at callback-funktionen kan fungere i GTM-skabelonversionen, skal du henvise til en brugerdefineret JS-variabel i feltet `loaded` (se screenshot i afsnittet Grundlæggende konfiguration), der returnerer en funktion.

Så snart PostHog-scriptsene er håndteret, og trackeren er initialiseret, vil denne funktion blive udført.

### Brugerdefinerede begivenheder, brugereg enskaber og begivenhedsparametre

![posthog-event-params](/assets/img/posthog/posthog-event-params.png)
_Eksemplarisk implementering af brugerdefineret begivenhedstag_

Ved hjælp af GTM-skabelonen kan du uden besvær spore brugerdefinerede begivenheder (såvel som virtuelle sidevisninger) og berige dem med finkornede begivenhedsparametre, hvilket giver en omfattende forståelse af brugeren gagement mønstre. Desuden har skabelonen adopteret JavaScript SDK-funktionaliteten, som giver dig mulighed for at indstille brugereg enskaber ved hjælp af både `$set` og `$set_once` metoder, hvilket giver dig fleksibiliteten til at vælge mellem at opdatere værdier eller bevare de oprindelige brugerattributter.

## Hvordan kommer jeg i gang?

Du er velkommen til at [downloade skabelonen](https://github.com/GunnarGriese/gtm-template-posthog) fra min GitHub og give den et forsøg. Jeg er glad for enhver feedback til at forbedre skabelonen, inkludere flere funktionaliteter fra det originale SDK og rette potentielle fejl, efterhånden som de opstår.

For at bruge skabelonen skal du blot importere den til dit GTM-arbejdsområde, oprette et nyt tag ved hjælp af skabelonen og konfigurere indstillingerne baseret på dine behov. Denne integration sikrer, at du kan udnytte både PostHog og Google Tag Manager fuldt ud for at få indsigt i brugeradfærd på dit websted eller app.

Mens denne artikel skitserer en tilgang til, hvordan man implementerer PostHog gennem GTM, vil du måske henvise til PostHogs fremragende og letforståelige [dokumentation](https://posthog.com/docs/getting-started/start-here) om, hvordan du kommer i gang med deres platform.

## Sammenfatning

Afslutningsvis er PostHog en kraftfuld analyseplat form, der kan hjælpe dig med at forstå dine brugere bedre. Ved at integrere den med Google Tag Manager ved hjælp af den medfølgende tag-skabelon kan du strømline implementeringsprocessen og effektivt administrere din sporingsopsætning. Denne kombination af PostHog og Google Tag Manager vil forhåbentlig hjælpe med at accelerere implementeringsprojekter og give dig mulighed for at træffe datadrevne beslutninger endnu hurtigere. Så kom i gang, udforsk potentialet i PostHog analytics-platformen og Google Tag Manager-integrationen, og lås op for nye indsigter i dine brugeres adfærd.