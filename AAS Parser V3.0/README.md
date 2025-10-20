# Introduction  
This program is used to convert the AAS files into a suitable format for AAS-based cloud data acquisition & storage system and was developed to be used in Windows 10 (and 11) environment to provide the user convenience. 

### [Note] Create nodeset.xml
Value tags may not be created if you are using the latest module version. Check the module version to create the nodeset.xml file.
- $ pip3 list

If you don't have the modules below, Install them.

|modul_name|version|Uninstall commands|Install commands|
|----------|-------|------------------|----------------|
|asyncua|0.9.14|$pip3 uninstall asyncua|$pip3 install asyncua==0.9.14|
|xmlschema|1.1.1|$pip3 uninstall xmlschema|$pip3 install xmlschema==1.1.1|
|xmltodict|0.12.0|$pip3 uninstall xmltodict|$pip3 install xmltodict==0.12.0|
|asyncio|3.4.3|$pip3 uninstall asyncio|$pip3 install asyncio==3.4.3|

Check the installed versions again with the command below.
- $ pip3 list


# Running on Windows

 ### Run script
 * python3 main3.py --aas [AAS].xml
 * python3 syscfg3.py --aas [AAS].xml

# How to edit an AAS Model for utilizing this program.
 ### Step 0
 * Using the [AASX Package Explorer](https://github.com/admin-shell-io/aasx-package-explorer/releases) provided by [IDTA(Industrial Digital Twine Association)](https://industrialdigitaltwin.org/en/), you can easily create AAS models on Windows operating systems.
 * Create your own AAS model like below or Download the already created AAS template model.
 
 ### Step 1
 * Create CloudDataSolution AAS in the AASX Package Explorer. 
 * Then create CloudSolution Submodel and EdgeSolution Submodel. The submodels are composed of the following submodel elements.
 * [Note 1] Value and valueType of all submodel elements (especially properties) must be filled in.
 * [Note 2] If you have multiple field devices to communicate with the edge gateway, model it as follows.

![ed0](https://user-images.githubusercontent.com/114371609/214991995-f6a65e31-7716-44cf-a552-1046d9712686.png)

 ### Step 2
 * Now you can convert your AAS model using the AAS Parser Web Server. 
 * Follow the **3. Running on Windows** guide to convert your AAS model.
 * Example of template conversion result:
 
![eg1](https://user-images.githubusercontent.com/114371609/214994448-75b7d748-723c-4dc2-a194-72723cfc58e2.png)

![eg2](https://user-images.githubusercontent.com/114371609/214994455-f1fad61c-2be3-4cc7-9abd-1315c040b958.png)

# 5. How to edit configuration files  
### Step 1 : syscfg.json  
* This file is for applying basic communication information.  
* If you create CloudDataSolution AAS and fill contents successfully, Basic Configuration will be created as below :  
![image](https://github.com/auto-mos/AAS-Parser-for-Windows/assets/114371609/75470303-e9f9-4102-b125-74324c4beaa9)  
* But if you get empty syscfg.json file, you just can fill contents manually.  
* (Recommendation : editing AAS file and try again.)  

### Step 2 : engineering.csv  
* This file is for mapping field data tags with AAS tags.  
![image](https://github.com/auto-mos/AAS-Parser-for-Windows/assets/114371609/ba5c0053-0474-4ede-a46d-f6eda3afa4ab)   
* A, E, F Columns are created automatically and B, C, D Columns are needed to be filled manually.  
* Details are as follows :  
  A : AAS Tag name from AAS file. This doesn't need to be modified.  
  B : Gateway name. This column should be filled with the gateway name (defined in AAS) from which the data will be collected.  
  C : Device name. This column should be filled with the field device name (defined in AAS) from which the data will be collected.  
  D : Field Tag name. This column should be filled with the field data tag name(OPCUA). It contains namespace and tag identifier.  
  E : Sampling rate. Basic value is 50 and engineer can change this column with appropriate value.  
  F : Array index. If field data tag is an array, engineer should fill this column with array index. But field data tag is not an array, it should be filled with the value : -1(default value).
  
### Step 3 : nodeset.xml  
* This file is the OPCUA information model.  
* It is recommended not to modify it arbitrarily.  
  
  
