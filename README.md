# Medical Relation
I stopped updating because I don't have time. 
If you have any question about UMLS (I think I have a fairly good understanding of it now) or if you are working on training models for medical relations (struggling on this) please [contact me](yining_hua@college.harvard.edu)

-- Ning

### Crosswalks of data scraped from everywhere. Work for the [CELEHS](https://celehs.hms.harvard.edu/) group at HMS
A doc on all links I have: [click here](https://docs.google.com/document/d/1bUWSk_qSs-gtChQsYYjqabRDIDAZKYCUQwg0QiDXU6I/edit?usp=sharing)

## Currently this project has:
### 1. Drug-RxNorms Mapping of data from drugs.com
For documentation and evaluations [click here](https://docs.google.com/document/d/1_Z5ddvA3-F_kr7k873oCFksNscmLST6nmONuf3WSbTI/edit?usp=sharing)

### 2. Disease-PheCodes Mapping of data from drugs.com
For documentation and evaluations [click here](https://docs.google.com/document/d/1KUbgcE6ODoSuk-Nxhq9kiDf0zVGkKbUeqqnBXA8bDD4/edit?usp=sharing)

### 3. MedScape Drug-Disease Conditions articles 
(See documentation of how it's scraped [here](https://docs.google.com/document/d/1braCaXNtjnTiuPc64KEnI0rDJGbmDJfgS_MYgKwARGk/edit?usp=sharing))

### 4. Running NER on titles
See documentation at [README.md in the ner/ folder](https://github.com/ningkko/UMLS-Mapping/blob/master/ner/README.md)

### 5. Running NLP on titles and contents
Not much stored here but you can find how to load data to a database using python [here](https://github.com/ningkko/UMLS-Mapping/tree/master/nlp).

### 6. PPMISVD
Not (directly) part of the mapping project, but the tool calculates the PPMI and the SVD of a given input source.

If you read Chinese, here is a good [introduction](https://www.zhongxiaoping.cn/2019/03/09/GLOVE,PPMI,SVD/) to GLOVE, PPMI, and SVD.\
If you don't, read the paper [Clinical Concept Embeddings Learned from Massive Sources of Multimodal
Medical Data](https://arxiv.org/pdf/1804.01486.pdf)

TODO: Add PPMISVD documentation 

### 7. Loinc Roll-Up
Logical Observation Identifiers Names and Codes (LOINC) is a database and universal standard for identifying medical laboratory observations. 

See documentation [here](https://docs.google.com/document/d/1fMmjrmlKOHVhPnxR3My1TnL4azSzdA_7BSg7912uz2c/edit?usp=sharing
)

For a clearer understanding of what each Loinc TTY means in the UMLS database, what MTHU#, LA#, LG# are, and how can these codes be mapped to Loinc codes, see [LOINC TTY and Mapping](https://docs.google.com/document/d/1_OTmCOjJtNM2A-W7OpLRBlxHBJYsB5BlmhFaDLGsEnQ/edit?usp=sharing)

### 8. PheCode to CPT code Mapping
In progress. See [documentation](https://docs.google.com/document/d/1Hh0aPIVisUUo2T2cMcYDL8b4ya-qyDvR4FOqTtPh_a8/edit?usp=sharing)
