## last updated by CH

rm(list=ls())
setwd("/n/data1/hsph/biostat/celehs/ch263/Relation_Pairs/disease_drug/")

library(data.table)
library(dplyr)

############# 1. generic names
## generic names: downloaded from drugs.com
## need to clean them
## change to lower case
## remove the duplicated one

df = fread("data/drug_disease.csv", data.table=F, header=T)
dim(df)
##15121

df = df[df$"generic name"!= "[]",] 
dim(df)
#14384

generic=df[,"generic name"]
generic=gsub("'","",generic)
generic=gsub("\\[|\\]","",generic)
#examples of noises 
generic[which(grepl("  ", generic)==1)[2]]

generic=gsub("  ", " ", generic)
generic=gsub(" )", "", generic)
generic=gsub(")", "", generic)
generic=tolower(unique(generic[generic!=""]))
#TODO: Ning, please expend the above cleaning procedures to futher clean the data

##############2. attach rxnorm to generic names (approach 1)
## str_rxnorm mapping
str_rxnorm = fread("data/RXNORM-ingredient-base.csv", data.table=F, header=T)
str_rxnorm=str_rxnorm[,c("ingredient_str", "ingredient")]
str_rxnorm=str_rxnorm[duplicated(str_rxnorm)!=1,]
colnames(str_rxnorm)=c("str","rxnorm")
str_rxnorm$str=tolower(str_rxnorm$str)
generic_rxnorm1=left_join(data.frame(str=generic), str_rxnorm, by="str")
sum(is.na(generic_rxnorm1$rxnorm))/dim(generic_rxnorm1)[1]
#[1] 0.455386
#missing rate is 0.45. 
#Ning, this is different from what you reported (~30%), because you didnt remove the duplicated generic names

##############3. attach rxnorm to generic names (approach 2)
generic_notmap=generic_rxnorm1[which(is.na(generic_rxnorm1$rxnorm)),"str"]
head(generic_notmap)

### 3.1 str_cui mapping 
## we have two str_cui mappings, which were difference versions of the broad dictionary.
str_cui1=fread("data/cui_term_mapping.txt", data.table=F, quote="", header=F) 
str_cui2=read.csv("data/cui_term_mapping_CH.csv")
## TODO: Vidul, please replace the above dictionary with a version without "ispref=y", but with english filter. 

str_cui1=str_cui1[duplicated(str_cui1)!=1,]
str_cui2=str_cui2[duplicated(str_cui2)!=1,]
colnames(str_cui1)=colnames(str_cui2)=c("CUI", "str")
str_cui=rbind(str_cui1, str_cui2)
rm(str_cui1)
rm(str_cui2)
gc()

str_cui[,"str"]=tolower(str_cui[,"str"])
str_cui=str_cui[duplicated(str_cui)!=1,]

### 3.2. attach cui to generic names
## one thing tricky is in the CUI dictionary, sometimes "/" were used for "and", but sometimes not.
## some with xx,xx and xx pattern can be xx/xx/xx
generic_notmap2=gsub("and", "/", generic_notmap)
str_cui.tmp1=str_cui[str_cui$str%in%generic_notmap,]
str_cui.tmp2=str_cui[str_cui$str%in%generic_notmap2,]

generic_cui1=left_join(data.frame(str=generic_notmap), str_cui.tmp1, by="str")
colnames(generic_cui1)=c("generic_str","CUI")

generic_cui2=left_join(data.frame(str=generic_notmap2), str_cui.tmp2, by="str")
colnames(generic_cui2)=c("generic_str","CUI")

generic_cui=generic_cui1
generic_cui[which(is.na(generic_cui[,"CUI"])),"CUI"]=generic_cui2[which(is.na(generic_cui[,"CUI"])),"CUI"]
generic_cui[complete.cases(generic_cui)!=1,]
#TODO: need to check why some generic name cannot be assigned CUI. Need manual check from UMLS
generic_cui=generic_cui[complete.cases(generic_cui),]

### 3.3. attach cui to rxnorm
str_cui.tmp=str_cui[str_cui$str%in%str_rxnorm[,"str"],]
rxnorm_cui=left_join(str_rxnorm, str_cui.tmp, by="str")
colnames(rxnorm_cui)=c("rxnorm_str","rxnorm", "CUI")
rxnorm_cui[complete.cases(rxnorm_cui)!=1,]
#TODO: need to check why the above rxnorm cannot be assigned CUI. Need manual check from rxnav
rxnorm_cui=rxnorm_cui[complete.cases(rxnorm_cui),]

### 3.4. attach rxnorm to generic name via cui
generic_rxnorm2=left_join(data.frame(generic_cui), data.frame(rxnorm_cui), by="CUI")
generic_rxnorm2=generic_rxnorm2[,setdiff(colnames(generic_rxnorm2), c("CUI", "rxnorm_str"))]
generic_rxnorm2=generic_rxnorm2[complete.cases(generic_rxnorm2),]

####### 4. final dictionary, comparing approach 1 and approach 1+2
set1=str_rxnorm[,c("str","rxnorm")]
set2=generic_rxnorm2
colnames(set2)=c("str", "rxnorm")
tmp=rbind(set1,set2)

dict_drug_rxnorm1=left_join(data.frame(str=generic), set1, by="str")
dict_drug_rxnorm1=left_join(dict_drug_rxnorm1, str_rxnorm, by="rxnorm")
colnames(dict_drug_rxnorm1)=c("generic_names", "rxnorm1", "rxnorm_str1")

dict_drug_rxnorm2=left_join(data.frame(str=generic), tmp, by="str")
dict_drug_rxnorm2=left_join(dict_drug_rxnorm2, str_rxnorm, by="rxnorm")
colnames(dict_drug_rxnorm2)=c("generic_names", "rxnorm2", "rxnorm_str2")
dict_drug_rxnorm=left_join(dict_drug_rxnorm1, dict_drug_rxnorm2, by="generic_names")
dict_drug_rxnorm=dict_drug_rxnorm[duplicated(dict_drug_rxnorm)!=1,]
sum(is.na(dict_drug_rxnorm[,"rxnorm1"]))
sum(is.na(dict_drug_rxnorm[,"rxnorm2"]))

## TODO: need to manual check the reason for those missing: 
## summarize how to further clean the generic names

write.csv(dict_drug_rxnorm, file="output/dict_drug_rxnorm.csv", row.names=F)
