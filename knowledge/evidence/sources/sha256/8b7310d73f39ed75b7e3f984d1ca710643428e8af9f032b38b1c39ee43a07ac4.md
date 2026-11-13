# DB without data

For DB without data case , we can use Flyway script to init DB

![image2024-1-12_11-3-24.png](attachments/image2024-1-12_11-3-24.png)

# DB with Data

For DB with data case, we can use API to re-init  DB

## Step one- get data set file from RDM

![image2024-1-12_11-40-1.png](attachments/image2024-1-12_11-40-1.png)

download file

![image2024-1-12_11-43-3.png](attachments/image2024-1-12_11-43-3.png)

![image2024-1-12_11-44-44.png](attachments/image2024-1-12_11-44-44.png)

remove the line from 1 ~11 in the file and then save as cvs file.

![image2024-1-12_11-46-49.png](attachments/image2024-1-12_11-46-49.png)

![image2024-1-12_11-46-16.png](attachments/image2024-1-12_11-46-16.png)

## Step two - Call delete data API to remove data

| API Name | HTTP Method | [URL ](http://localhost:8989/v1/cashflow/country/cleanDB) | Note |
| --- | --- | --- | --- |
| [clean DB](http://localhost:8989/v1/cashflow/country/cleanDB) | DELETE | [http://{static service domain name}/v1/cashflow/country/cleanDB](http://localhost:8989/v1/cashflow/country/cleanDB) | this api will remove all data from table ratan_static_cashflow_country_mapping |

PostMan

![image2024-1-12_11-31-29.png](attachments/image2024-1-12_11-31-29.png)

Curl：

curl --location --request DELETE '[http://localhost:8989/v1/cashflow/country/cleanDB](http://localhost:8989/v1/cashflow/country/cleanDB)'  --data-raw ''

## Step three - Call upload file API to upload data

| API Name | HTTP Method | [URL ](http://localhost:8989/v1/cashflow/country/cleanDB) | Note |
| --- | --- | --- | --- |
| [upload ](http://localhost:8989/v1/cashflow/country/cleanDB)flie | POST | [http://{static service domain name}/v1/cashflow/country/upload](http://localhost:8989/v1/cashflow/country/cleanDB) | this api will upload file and then will read all data from the file to save to DB table ratan_static_cashflow_country_mapping |

![image2024-1-12_11-48-16.png](attachments/image2024-1-12_11-48-16.png)

curl --location --request POST '[http://localhost:8989/v1/cashflow/country/upload](http://localhost:8989/v1/cashflow/country/upload)' --form 'file=@"/C:/Users/1662744/Downloads/Country-20240111.csv"'