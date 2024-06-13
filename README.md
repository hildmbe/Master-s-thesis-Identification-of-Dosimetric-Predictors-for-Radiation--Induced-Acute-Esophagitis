# Oversikt over kode:

## Filer kjørt i python: 

CheckRSfiles:
   - Brukt til å sjekke om strutur DICOM filene er "hele" eller om noen snitt fra spiserøret mangler.
   - Brukt også til å sjekke om snittykkelsen i RS filen og "vokselsnittykkelsen" er lik eller ulik.
     
FindSamplePoints:
   - Brukt til å finne DICOM koordinatene til punktene rundt øsofagus hvor dosen skal samples og inngå i dosekartene.
     
PlotDSMs:
   - Brukt til å plotte dosekartene.
     
Convert_dsm_EQD2:
   - Brukt til å konvertere dosekartene til eqd2 med ab=10.

ScaleDSMs:
   - Brukt til å skalere dosekartene til en standard pixelstørrelse for å lage de gjennomsnittlige dosekartene.
     
RotateDSMs:
   - Brukt til å mappe den høyeste dose regionen til sentrum av kartet.
     
ExtendDSMs:
   - Brukt til å standardisere lengden av dose kartene ved å utvide de til å matche den høyeste observerte lengden i pasientpopulasjonen.
     
CreateAverageDSMs:
   - Brukt til å lage gjennomsnittlige dose kart per grad av øsofagitt. Her er de utvidete (extended) 
     dose kartene brukt. 
   - Også brukt til å lage gjennomsnittlige dose-differanse kart.
      
PerformMCP:
   - Brukt til å utføre MCP test
     
SaveDSMFeatures:
   - Brukt til å hente ut DSM parametrene.
   - Hentet ut på orginiale EQD2 dosekart.

HelperFunctions: 
   - Mange av funksjonene er lagret her.
   - Noen av funksjonene er hentet fra Patrick HM, Kildea J. Technical note: rtdsm-An open-source software for radiotherapy dose-surface map generation and analysis. Med Phys. 2022 Nov;49(11):7327-7335. doi: 10.1002/mp.15900. Epub 2022 Aug 8. PMID: 35912447. 

## Filer kjørt i RayStation: 

ExportDoseData.py
   - Brukt til å eksportere dose- og volum matriser fra RayStation

ExportDoseMatrixAndXYZPositions.py

InterpolateDoseInPoints:
- Brukt til å regne ut dosen i punktene som ble funnet i FindSamplePoints.py. 
