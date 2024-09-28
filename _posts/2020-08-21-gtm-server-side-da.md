---
title: GTM Server-Side Tagging – Bedre Data & Mere Kontrol
author: gunnar
date: 2020-08-21 15:24:15 +0200
categories: [GTM]
tags: [ga4, gtm-server-side]
comments: false
lang: da
permalink: /posts/gtm-server-side/
---

I de seneste måneder har jeg gennemført en række beta-tests og projekter for en udvalgt gruppe af kunder for at få både praktisk erfaring og for at hjælpe med at optimere den nyligt lancerede Google Tag Manager (GTM) server-side tagging opsætning.

Mit mål er at levere både baggrundsinformation og kontekst for, hvorfor jeg mener, at de fleste virksomheder seriøst bør overveje at implementere dette for bedre at støtte markedsføring. Derudover vil du få et overblik over funktionaliteten og mulige brugsscenarier for denne funktion, der vil hjælpe dig med at bevæge dig hen imod en fremtidssikret, first-party tracking opsætning, forbedre den overordnede kundeoplevelse og få fuld kontrol over dine data.

Den vigtigste pointe er, at GTM server-side øger fleksibiliteten og kontrollen over dine data og forbedrer løsningens holdbarhed og direkte forretningsværdi langt ud over, hvad der er muligt med en traditionel Google Tag Manager opsætning.

## Privacy First og 1st Party Analytics

Virksomheder står i dag over for mange udfordringer, der kræver, at de gentænker den måde, de udfører website- og app-tracking på. Heldigvis åbner disse udfordringer med GTM server-side også op for mange agile muligheder for virksomheder, der er villige til at tilpasse sig og ændre sig. Traditionel tracking står imidlertid over for mange udfordringer, der vil gøre det teknisk umuligt at fortsætte med at "tracke som vanligt".

En af disse udfordringer er det nye "Privacy first"-paradigme, der pålægges os af regulativer som GDPR (EU) og CCPA (Californien). Browserudbydere er også blevet langt mere opmærksomme på privatlivets fred inden for de seneste par år og søger at beskytte deres brugeres data mod alt for datahungrende adtech-værktøjer.

Ligeledes begrænser initiativer som Safaris "Intelligent Tracking Prevention" (ITP) og Firefox' "Enhanced Tracking Prevention" (ETP) kraftigt adgangen til ofte brugte browserlagringsmuligheder (især cookies og lokal lagring). Google annoncerede også for nylig, at de vil udfase tredjepartscookies fuldstændigt inden for de næste to år for deres Chrome-browser (en såkaldt "privacy sandbox" vil erstatte tredjepartscookies).

Alt for ofte har annoncører også implementeret JavaScript-snippets på deres websites uden at være klar over deres fulde funktionalitet, hvilket resulterer i, at de overdrager kontrollen over deres brugeres data til ukendte tredjeparter, hvilket har gjort massive databrud mulige.

Derfor bør vi hilse denne generelle retning velkommen, da det hjælper med at sikre vores personlige data, modne branchen og genvinde den længe tabte troværdighed – med det mål at stoppe tvivlsomme "wild west"-tracking praksisser.

Den største ulempe ved denne bevægelse er dog, at den også påvirker og skaber bias i forretningskritisk datainsamling baseret på brugerens samtykke: Det tekniske og lovgivningsmæssige miljø, som traditionel website- og app-tracking er indlejret i, gør det svært for os at holde styr på specifik brugeradfærd – hvilket øger vores blinde vinkel i forståelsen af brugernes behov.

## GTM Server-Side Tagging til undsætning

Google Tag Manager (GTM) har nu en ny funktion (i beta-status i øjeblikket), der vil give virksomheder mulighed for at skabe en first-party analytics opsætning. GTM server-side tagging er her for at ændre måden, hvorpå website- og app-tracking implementeres, og hvordan data deles med tredjeparter. Læs videre for at forstå, hvordan denne funktion vil hjælpe dig med at forbedre brugeroplevelsen på websitet, øge sikkerheden for dine brugeres data og styrke kontrollen over din datainsamling.

### Hvordan fungerer det?

Mens GTM server-side containeren giver nye værktøjer og funktioner til at måle brugeraktivitet, forbliver den generelle model af tags, triggere og variabler uændret.

![gtm-server-side-architecture](/assets/img/gtm-server-side/server-side-tagging.png)
_Kilde: https://developers.google.com/tag-platform/tag-manager/server-side/intro_

GTM Server-Side Tagging betyder, at en ny "Server" container kører på en App Engine instans – (ideelt set) mappet til dit domænes namespace – i dit eget Google Cloud Platform (GCP) projekt. Det er derefter muligt at sende HTTP-anmodninger til serveren fra brugerens enhed eller en hvilken som helst anden internetforbundet enhed. GTM-serveren omdanner disse anmodninger til hændelser, som behandles af containerens tags, triggere og variabler.

Mens det velkendte koncept med tags, triggere og variabler fungerer som de plejer i client-side GTM containere, er den nyligt introducerede "klient" forbindelsen mellem de enheder, der sender anmodninger, og containerens logik. Klienten kan modtage og kræve anmodninger (og data sendt med den), analysere dem til en eller flere hændelser, dirigere data til at blive behandlet i containeren (tags, triggere og variabler) og returnere et HTTP-svar til den anmodende enhed.

### Få datakontrol og fleksibilitet

Det, der adskiller denne tilgang fra tracking baseret på client-side JavaScript og pixels, er, at du har fuld kontrol og opnår fleksibilitet over, hvordan dataene behandles, indtil du sender dem til tredjepartsværktøjer (hvilket muliggør hitvalidering, PII-kontroller osv.). Faktisk, da GTM-serveren (https://gtm.example.com) er forbundet med det samme domæne som dit website (https://example.com), betragtes enhver interaktion mellem dem som en first-party dataudveksling af brugerens browser.

### Reducer virkningen af browser-tracking forhindringer og adblockere

Med denne ændring af konteksten vil betydelige restriktioner pålagt os af browser-tracking-forhindringer blive omgået, fordi du får mulighed for at sætte first-party HTTP-cookies (f.eks. introducerer GTM server-side en ny FPID-cookie). For eksempel vil Safaris ITP ikke længere begrænse levetiden for cookies forbundet med Google Analytics, når de placeres fra server-siden, hvilket resulterer i bedre datakvalitet til rapportering og analyse (især relevant for virksomheder med en ung og teknologikyndig brugerbase). Husk, at denne magt kommer med et stort ansvar, og du bør altid være opmærksom på de juridiske og etiske konsekvenser af at sætte cookies og de data, du indsamler.

## Hvilke brugsscenarier kan afsløres?

GTM Server-Side tracking genopretter gennemsigtighed i brugen af tredjepartsværktøjer og websites, men ud over det er der et par andre fordele ved at tracke hændelser på server-siden, der kan føre til stærke brugsscenarier for virksomheden.

### Forbedret datanøjagtighed og kontrol

Datanøjagtigheden kan forbedres yderligere, når virksomheder beslutter at udnytte server-til-server kommunikation til forretningskritiske hændelser som transaktioner. Vi har alle oplevet uoverensstemmelser mellem antallet af transaktioner i Google Analytics (GA) og CRM-systemer på grund af adblockere og andre sideeffekter, når vi er afhængige af client-side tracking (sidegenindlæsninger osv.). Dette kan afhjælpes ved at fjerne client-side tracking af transaktioner og sende de nødvendige datapunkter direkte fra dine CRM-systemer til GTM-serveren og sende dem videre til GA til analyse.

### Forbedret sideindlæsningstid og datasikkerhed

Generelt kan server-side tracking fjerne behandlingsbyrden fra en given browser og flytte den til skyen. Da én HTTP-anmodning er nok til at udløse en hændelse i server-side containeren, kan den udløse flere tags i server-side miljøet. For eksempel kunne klienten sende én HTTP-anmodning ved hver sideindlæsning, der udløser en sidevisningshændelse for GA og Facebook på samme tid. Da der ikke ville være behov for at udføre JavaScript skrevet af Facebook i brugerens browser, kunne server-side tracking øge sideindlæsningstiden. Da dette vil påvirke den overordnede brugeroplevelse positivt, har det potentialet til at øge dine konverteringsrater.

### Glat integration i Google Cloud Platform

Derudover, fordi GTM-containeren udføres i Googles cloud-integrationer, vil andre GCP-ressourcer som BigQuery, ML Engine og Cloud Functions sandsynligvis blive integreret snart. Dette vil åbne op for mange muligheder for avancerede brugsscenarier, der involverer maskinlæring og [hændelsesbaseret analyse](https://gunnargriese.com/posts/ga4-the-cdp-you-didnt-know-you-had/).

Når denne nye GTM-funktion bevæger sig ud af betafasen og bliver forbedret baseret på funktionsanmodninger og bidrag fra aktive community-medlemmer, vil endnu flere muligheder være tilgængelige, hvilket betydeligt vil ændre tracking-implementeringer baseret på GTM.

> **Bemærk**: Du kan læse mere om mulighederne for at integrere GCP-tjenester i GTM Server-Side for at låse op for kraftfulde brugsscenarier i fremtiden i [min nyeste blogserie](https://gunnargriese.com/posts/gtm-server-side-firestore-integrations/).

## Afsluttende tanker

Udgivelsen af GTM Server-Side containeren fortsætter en generel trend, der kan observeres i mange Google Marketing Platform-værktøjer: Styrkelse af værktøjsintegration og skub mod GCP. Ved at følge denne strategi sikrer Google en glat dataflow mellem systemer og øger samtidig hvert værktøjs funktionalitet for at kunne følge med det konstant skiftende adtech-miljø.
