# wildlife-observations

## Background

This application provides the user interface and database (SQLite) for entering observations and identifications of wildlife. Whilst its basis is fairly generic, it has been somewhat tailored to a project that I am doing recording Orthoptera (commonly known as grasshopper, crickets, katydids, etc.) and therefore there are some aspects which mean it is not fully applicable to other projects. It would, however, with a little extra effort, provide a base for a similar project that could be used for records of any species.

My primary reason for building this application is that I have several normalised spreadsheets which contain the data of a large number of observations of Orthoptera. This is becoming unwieldy and I am worried about a) losing information at some point, and b) making typos or entering incorrect information. On top of that, it is very hard to see how much progress I am making with data entry and some of the work I am doing, therefore I want to get it into a database as soon as possible. I should have done this to begin with, but because of other priorities, I had been putting it off. 

## Basic structure 

The basic structure of an observation is as follows: 
* a **survey** was undertaken on a **visit** to a particular **site**;
* the **survey** used a particular **method** and may have been **repeat**ed;
* an **observation** of an individual was made during the **survey**, which was undertaken in certain **meteorological conditions**;
* each **observation** is assigned a **specimen label** and was then **identified**, in some cases more than once;
* the **vegetation structure** was recorded at certain points during a **survey**.

## Current development

I do not currently have plans to develop the application a lot further and due to time constraints, I will not build forms for data entry. As there is only myself using it locally, currently, I will use a combination of commands to import data from existing spreadsheets and the admin for entering any further data. This is not the ideal way to go, but as a compromise I will use database constraints, normalisation and other aspects to their full to help avoid data entry mistakes wherever possible.

## Future plans

Once the models have been finalised and checked, I will concentrate on producing some basic reports so I can see my progress with data entry. Following that, or possibly beforehand, I will begin writing importers for the data that I currently have in spreadsheets. 

I will most likely be using R for data analysis, therefore once I have the other priorities sorted, I will start working on some simple data exports and possibly investigate ways in which I can interrogate the database directly with R.

# Acknowledgements

A huge thanks to [@cpina](https://github.com/cpina) for sanity-checking models, answering questions about Django and generally improving the code and functionality.  
