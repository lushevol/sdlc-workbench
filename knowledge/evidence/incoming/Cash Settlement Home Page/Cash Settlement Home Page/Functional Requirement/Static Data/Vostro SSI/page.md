Per JIRA [RATAN-10123](https://jira.global.standardchartered.com/browse/RATAN-10123), Summary for the SSI+ and Murex2.11 analysis result

**For the redundancy check:**

There’re duplicate Vostro SSI defined on different Murex products like IRD/CCS, IRD/IRS.

1. SSI+ China entity and CURR security. Only 2 records are same. Please refer to below. Sample volume is 147. | **Parent Trading Account** | **Currency** | **Branch Id** | **Security** | **Country** | **Method** | **BIC** | **AccountRef** | **SwiftType** | | --- | --- | --- | --- | --- | --- | --- | --- | --- | | 00000000-0000-0000-0000-000000052cae | USD - US DOLLAR | SHANGHAI | MXG CURR FXD FXD | United States | CASH | SCBLUS33XXX | | MT202 | | 00000000-0000-0000-0000-000000052cae | USD - US DOLLAR | SHANGHAI | MXG CURR FXD XSW | United States | CASH | SCBLUS33XXX | | MT202 |
2. SSI+ China entity and IRD security. 4 groups have same values except one field. And 3 groups have the same value. Sample volume is 410. | | Parent Trading Account | Currency | Branch | Security | Country | Method | BIC | AccountRef | SwiftType | | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | | One field diff | 00000000-0000-0000-0000-000000041113 | CNO - CHINESE YUAN ONSHORE | SHANGHAI | MXG IRD IRS | China | CASH | CIBKCNBJXXX | 34111 | MT202 | | 00000000-0000-0000-0000-000000041113 | CNO - CHINESE YUAN ONSHORE | SHANGHAI | MXG SCF | China | CASH | CIBKCNBJXXX | 34111 | Default | | 00000000-0000-0000-0000-000000041113 | CNO - CHINESE YUAN ONSHORE | SHANGHAI | MXG IRD | China | CASH | CIBKCNBJXXX | 34111 | Default | | | | 00000000-0000-0000-0000-000000041fb0 | CNO - CHINESE YUAN ONSHORE | SHANGHAI | MXG IRD CS | China | CASH | BOSHCNSHXXX | 31600702320120800 | MT202 | | 00000000-0000-0000-0000-000000041fb0 | CNO - CHINESE YUAN ONSHORE | SHANGHAI | MXG IRD IRS | China | CASH | BOSHCNSHXXX | 115500730 | MT202 | | | | 00000000-0000-0000-0000-000000046b6f | CNO - CHINESE YUAN ONSHORE | SHANGHAI | MXG IRD CS | China | CASH | HSBCCNSHXXX | 115500794 | MT202 | | 00000000-0000-0000-0000-000000046b6f | CNO - CHINESE YUAN ONSHORE | SHANGHAI | MXG IRD IRS | China | CASH | HSBCCNSHXXX | 115500794 | Default | | | | 00000000-0000-0000-0000-000000047736 | CNO - CHINESE YUAN ONSHORE | SHANGHAI | MXG IRD CS | China | CASH | DBSSCNSHXXX | 115500805 | Default | | 00000000-0000-0000-0000-000000047736 | CNO - CHINESE YUAN ONSHORE | SHANGHAI | MXG IRD IRS | China | CASH | DBSSCNSHXXX | 115500805 | MT202 | | | | | Totally same | 00000000-0000-0000-0000-000000049bce | CNO - CHINESE YUAN ONSHORE | SHANGHAI | MXG SCF | China | CASH | PCBCCNBJXXX | 44201518300052500000 | MT103 | | 00000000-0000-0000-0000-000000049bce | CNO - CHINESE YUAN ONSHORE | SHANGHAI | MXG IRD | China | CASH | PCBCCNBJXXX | 44201518300052500000 | MT103 | | | | 00000000-0000-0000-0000-00000004e70b | USD - US DOLLAR | HHANGZHOU | MXG IRD IRS | United States | CASH | SCBLCNSXHZH | 501510242360 | Default | | 00000000-0000-0000-0000-00000004e70b | USD - US DOLLAR | HHANGZHOU | MXG IRD | United States | CASH | SCBLCNSXHZH | 501510242360 | Default | | | | 00000000-0000-0000-0000-0000000ebc74 | USD - US DOLLAR | NANJING | MXG IRD IRS | United States | CASH | SCBLCNSXNJG | 501510564843 | MT103 | | 00000000-0000-0000-0000-0000000ebc74 | USD - US DOLLAR | NANJING | MXG IRD | United States | CASH | SCBLCNSXNJG | 501510564843 | MT103 | **For the Murex2.11 and SSI+ product catalogue:** Product catalogue for Murex 2.11 BAU SSI: Murex family/group/type

![1.png](attachments/1.png)

SSI+ CHINA Security is CURR catalogue

![2.png](attachments/2.png)

SSI+ China Security is IRD catalogue

![3.png](attachments/3.png)

SSI+ Global Security is IRD  catalogue

![4.png](attachments/4.png)

SSI+ Global Security is CURR

![5.png](attachments/5.png)

The catalogue betwee the Murex2.11 and the SSI+ is same based on the above analysis.

Used data for Vostro from Murex2.11 and SSI+ are attached below page:

[Murex 2.11 CN Vostro SSI]