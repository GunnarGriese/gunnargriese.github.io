---
title: Hvordan replikerer man GA4 Path Exploration-rapporten med BigQuery SQL?
author: gunnar
date: 2022-10-23 11:24:15 +0200
categories: [BigQuery]
tags: [ga4, bigquery, sql]
comments: false
lang: da
permalink: /posts/bigquery-path-exploration/
---

Det nye Google Analytics (GA4) kommer med en ny Exploration-funktion (eller Udforskninger), som giver GA-brugere mulighed for at dykke dybt ned i deres data - ud over mulighederne i de indbyggede standardrapporter. Mens standardrapporterne tillader overvågning af nøgleforretningsmetrikker, gør Exploration-sektionen avancerede analytiske teknikker tilgængelige for hurtigt at generere ad hoc-indsigter.

De tilgængelige analytiske teknikker er følgende:

- Udforskning i frit format
- Kohorte-udforskning
- Tragt-udforskning
- Segmentoverlap
- Brugerudforskning
- Brugerlevetid
- Sti-udforskning

Tjek den officielle Google [dokumentation](https://support.google.com/analytics/answer/7579450?hl=da) for en mere detaljeret introduktion til GA4's kraftfulde Explorations-funktion.

## Sti-udforskning i GA4

Sti-udforskningsrapporten lader dig visualisere brugerinteraktioner fra en specifik begivenhed/side fremad (startpunkt) eller bagud (slutpunkt) på en samlet måde. Analytikere, der bruger denne teknik, kan besvare spørgsmål som:

- Hvilke topsider åbner nye brugere efter at have besøgt hjemmesiden?
- Hvad er effekten af en begivenhed på efterfølgende brugerhandlinger?
- Hvilke sider har ødelagte links til 404-sider?

![sti-struktur](/assets/img/path-exploration/path-structure.png)
_Elementer i Sti-udforskning (https://support.google.com/analytics/answer/9317498?hl=en&ref_topic=9266525)_

Visualiseringen er et Sankey-diagram, hvor hver node repræsenterer en begivenhed eller side. Analytikere kan vilkårligt tilføje noder for at afsløre flere sekvenselementerer og anvende segmenter, filtre og nedbrydningsdimensioner for at skræddersy rapporten til deres behov.

## Vende sig mod BigQuery for at udtrække data

Mens denne analyseteknik er kraftfuld, er den ikke altid det ideelle værktøj til at dele disse indsigter med interessenter - især ikke til dem, der ikke er fortrolige med GA. Heldigvis har alle brugere med GA4 mulighed for at eksportere deres GA4-data til BigQuery (Googles cloud-baserede, fuldt administrerede database designet til analytiske arbejdsbelastninger).

For konstant at overvåge kritiske brugerflows og indlejre dem i dine standard rapporteringsværktøjer (f.eks. Looker Studio, Power BI eller Tableau), er det at vende sig mod [GA4 rådata i BigQuery](https://support.google.com/analytics/answer/9358801?hl=en) og udtrække dataene vejen frem. Men...

## Hvordan replikerer man en grundlæggende GA4 Sti-udforskningsrapport i BigQuery?

Vi kan udnytte vinduesfunktioner i BigQuery til at aggregere `page_location`-sekvenser på tværs af alle sessioner målt med GA4 med en forespørgsel som denne:

![startpunkt](/assets/img/path-exploration/starting-point.png)
_Forespørgselseksempel for sti-udforskning med et startpunkt_

Ovenstående forespørgsel vil returnere én række for hver sti og antallet af forekomster inden for den forespurgte tabel:

![startpunkt-resultat](/assets/img/path-exploration/starting-point-result.png)
_Forespørgselsresultat for sti-udforskning med startpunkt_

Forespørgslens kernekomponenter er følgende:

- `ga4EventParams` funktion
- `LEAD()` funktion over en sessions `WINDOW`
- Midlertidig tabel specificeret i en `WITH` klausul

### Brugerdefinerede funktioner for at øge læsbarheden

Da vi er interesserede i at opnå `page_location` for hver tilknyttet `page_view` begivenhed, er `page_location` den nøgle, vi giver som input til funktionen. Funktionen `ga4EventParams` returnerer den respektive værdi for input-nøglen fra `event_params RECORD`. For flere detaljer, tjek [Alejandros indlæg](https://zielinsky.alejand.ro/) om, hvordan man bruger en BigQuery-funktion.

### Vinduesfunktioner til forespørgsel af sekvenser

Navigationsfunktionen `LEAD()` giver os mulighed for at forespørge efterfølgende rækker fra et specificeret vindue. Ændring af forskydningsværdien ændrer, hvilken efterfølgende række der returneres; standardværdien er `1`, hvilket indikerer den næste række i vinduesrammen. Du kan bruge forskydningsværdien til at tilføje flere noder til din forespørgsel, afhængigt af din analyse. I ovenstående eksempel er der inkluderet 3 yderligere noder (ud over startpunktet).

`WINDOW`-klausulen ovenfor vil resultere i, at vinduet spænder over en brugers session. For at gøre vinduet bruger-omfangsbestemt, fjern `ga_session_id` referencen.

### Midlertidige tabeller til at gemme mellemresultater

Den midlertidige tabel giver os mulighed for at gemme den resulterende tabel - 1 række pr. `page_view` begivenhed med de efterfølgende page_locations som kolonner - som et mellemliggende forespørgselsresultat i hukommelsen (data) og gøre det tilgængeligt for en senere del af forespørgslen. Datatabellen bruges derefter i den endelige `FROM`-klausul til at tælle forekomsterne af hver sekvens på tværs af alle sessioner.

## Hvordan ser man tilbage i tiden?

> Alt fint og godt, men hvordan starter man sekvensen med dens afslutning og arbejder sig tilbage derfra?

Et fair spørgsmål, især fordi det at specificere slutpunktet og analysere, hvordan brugere endte der, er en afgørende funktion i GA4's Sti-udforskingsteknik.

Heldigvis ville dette kun kræve et par mindre justeringer inden for vores midlertidige tabel, som så:

![slutpunkt](/assets/img/path-exploration/ending-point.png)
_Forespørgselseksempel for sti-udforskning med et slutpunkt_

Ved simpelthen at erstatte `LEAD()` med `LAG()`, returnerer vi værdien af `page_location` på en foregående række. Altså den forrige `page_view` begivenhed i en session.

## Hvordan starter man sekvensen med den faktiske landingsside?

For at opnå dette skal vi endnu engang vende os mod vores velkendte `LEAD()` funktion og tilføje en kolonne til vores midlertidige tabel - parameteren for `entrances` begivenheden. Det vil indikere, hvorvidt en bestemt `page_view` begivenhed var den første inden for en session og derfor er landingssiden.

Filtrering af sekvenser, der starter på landingssiden, vil returnere det ønskede resultat:

![landingsside](/assets/img/path-exploration/landing-page.png)
_Forespørgselseksempel for sti-udforskning med landingssiden som startpunkt_

## Afsluttende bemærkninger

Jeg håber, at dette stykke kontekst var nyttigt for dig og opmuntrer dig til at dykke dybere ned i GA4's BigQuery rådata. Fra mit perspektiv er det at have adgang til rådataene en af de væsentlige gevinster, du får ved at migrere fra Universal Analytics til GA4.

Jeg har til hensigt at identificere andre use cases for at udforske mulighederne og begrænsningerne ved GA4 og BigQuery.

Så hvis du opdager fejl i forespørgslerne, har bemærkninger eller finder noget uklart, så kontakt mig venligst. Jeg er altid glad for at tale om analyse!