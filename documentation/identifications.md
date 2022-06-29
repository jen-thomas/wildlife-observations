# Background to identification confirmation

In this project, specimens were identified to the lowest taxonomic level possible. In some cases, this was the suborder but in others it was species, or somewhere inbetween. Generally, this depended on whether the specimen was an adult or nymph, but in some cases, the taxonomy could not be determined further because a particular feature was missing or hard to see. 

During the process of identifying the specimens, each identification was classified into categories, to note whether it was certain, needed redoing or checking against other similar specimens. This documentation describes how these categories were used. 

## Identification confirmation categories and reasons

Specimens with a *confirmed* identification always arrived at one conclusion, but this could be at any taxonomic level.

- **Confirmed, ID certain**: a specimen was identified to a particular species and this identification was certain.
- **Confirmed, cannot determine further**: a specimen was identified to a particular taxonomic level that was higher than species. This identification was certain, but it could not be identified to a lower taxonomic level for one of the reasons described above.
- **Confirmed, small nymph**: a specimen was identified to a particular taxonomic level, normally suborder. This identification was certain, but it could not be identified to a lower taxonomic level because it was a very small nymph. Generally, these specimens were < 7 mm in length and did not have features which were well-developed enough to determine the identification to a lower taxonomic level. This category is equivalent to confirmed, cannot determine further, but it was useful at the time of identification to distinguish these specimens further for practical reasons.

Specimens with a *finalised* identification always arrived at multiple conclusions, which could be at any taxonomic level.

- **Finalised, cannot split further**: these specimens were identified to one of multiple taxa within a certain taxonomic level. At some points in the identification keys, it was not possible to determine the identification further due to the reasons described above, but at that point, the key determined it to one of two or more taxa. 

## Checking the identification data

Given the complex situation with the identifications described above, great care was taken with checks of the data. These can be run using the command, `data_checks_identifications.py`. 

The following checks were undertaken: 
- all specimens have either a confirmed or finalised identification, but not both
- if a specimen has multiple confirmed identifications, the final identification (to whichever taxonomic level), should be the same
- if a specimen has multiple confirmed identifications, the sex and stage should be the same
- specimens should have two or more finalised identifications (if they have any finalised identifications)
- if a specimen has finalised identifications, the sex and stage should be the same

## Exporting the identification data

Following the checks described above, the confirmed and finalised identifications were exported to be used in analysis. One confirmed identification per specimen and all finalised identifications for those specimens, were exported. Logic for the use of these identifications is done separately as part of the analysis, because their use depends on the questions being asked.