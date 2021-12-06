# Dataverse Dataset Exporter

### Step 0 use python 3.7+ and pyDataverse 0.2.1
Please be noted that latest version of pyDataverse 0.3.x is not backwards compatible. We stick to `0.2.1`. 

Install all the required packets
```shell
pip install -r requirements.txt
```

### Step 1 copy and rename sample-dvconfig.py to dvconfig.py
```shell
cp sample-dvconfig.py dvconfig.py
```
Adjust the content of the newly created dvconfig.py
```python
base_url = 'https://dataverse-url-without-trailing-back-slash.com'
api_token = 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx'

output_folder = 'output'
```
* `base_url` is the link of your Dataverse installation. 
* `api_token` is the _super user_ token of your Dataverse user. 
* `output_folder` is the local folder on your computer within the working directory

### Step 2 adjust the main.py file and run
Adjust the script according to your own need
```python
...

if __name__ == '__main__':
    '''export all the datasets from specific dataverse to default format json_ld'''
    # export_datasets_dataverse('liss_dc')
    '''export single dataset to default format json_ld'''
    # export_dataset('oai:11.32332/aabb-ccdd-eff')
    '''export list of datasets to default format json_ld'''
    # export_datasets(['oai:11.32332/aabb-ccdd-eff1', 'oai:11.32333/aabb-ccdd-eff2', 'oai:11.32334/aabb-ccdd-eff3'...])
```
uncomment ONE of the statements below according to your needs

- `export_datasets_dataverse('dataverse_name')` - this statement get all the datasets from the given dataverse. 
- `export_dataset('oai:11.32332/aabb-ccdd-eff')` - export only one dataset, given the PID
- `export_datasets(['oai:11.32332/aabb-ccdd-eff1', 'oai:11.32333/aabb-ccdd-eff2', 'oai:11.32334/aabb-ccdd-eff3'...])` - 
export datasets by list of PIDs

### You can as well indicate the export format, while the default one is json-ld

Available formats listed below
```python
ExportFormats.json_ld
ExportFormats.ddi
ExportFormats.oai_dc
ExportFormats.Datacite
ExportFormats.dataverse_json
ExportFormats.dcterms
ExportFormats.oai_datacite
ExportFormats.oai_ddi
ExportFormats.OAI_ORE
```

Format can be given as the second parameter with any of the 3 statement

For example, 
```python
export_datasets_dataverse('dataverse_name', ExportFormat.ddi)
```
```python
export_dataset('oai:11.32332/aabb-ccdd-eff', ExportFormat.oai_dc)
```
```python
export_datasets(['oai:11.32332/aabb-ccdd-eff1', 'oai:11.32333/aabb-ccdd-eff2', 'oai:11.32334/aabb-ccdd-eff3'], ExportFormat.OAI_ORE)
```
