# Formula change

### client.scb.fmrp.ExtSettleRouter

Type:XSL

Data Source:mxpayml.dtd

```xml
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:template match="/">
        <xsl:variable name="action" select="/MxPayML/action"></xsl:variable>
        <xsl:choose>
            <xsl:when test="$action='RI2C' or $action='MCXI' or $action='MIXC'">mls</xsl:when>
            <xsl:when test="$action='FAIS' or $action='FMIS' or $action='FMSI' or $action='I2SR'">fmrp</xsl:when>
        </xsl:choose>
    </xsl:template>
</xsl:stylesheet>
```

### client.scb.fmrp.SyncStatus

Type:XSL

Data Source:mxpayml.dtd

```xml
<xsl:stylesheet version="1.0" extension-element-prefixes="mx" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:mx="http://murex.com/xslt/common">
    <xsl:template match="/">
 
        <!--***variable declare starts-->
        <xsl:variable name="flowID" select="/MxPayML/flowID"></xsl:variable>
    <!-- <xsl:message><xsl:value-of select="$flowID"></xsl:value-of></xsl:message>-->
    <!--<xsl:value-of select="$flowID"></xsl:value-of><xsl:text>-flowID|</xsl:text>-->
        <xsl:variable name="cparty" select="/MxPayML/counterparty"></xsl:variable>
    <!--<xsl:value-of select="$cparty"></xsl:value-of><xsl:text>-cparty|</xsl:text>-->
        <xsl:variable name="action" select="/MxPayML/action"></xsl:variable>
    <!--<xsl:value-of select="$action"></xsl:value-of><xsl:text>-action|</xsl:text>-->
        <xsl:variable name="destinationStatus" select="/MxPayML/destinationStatus"></xsl:variable>
    <!--<xsl:value-of select="$destinationStatus"></xsl:value-of><xsl:text>-destinationStatus|</xsl:text>-->
        <xsl:variable name="flowStatus" select="/MxPayML/flowStatus"></xsl:variable>
    <!--<xsl:value-of select="$flowStatus"></xsl:value-of><xsl:text>-flowStatus|</xsl:text>-->
        <xsl:variable name="initCheck">
            <xsl:value-of select="mx:execute-formula('client.scb.fmrp.initCheck',concat( 'FLOW_ID:', $flowID,',STATUS:', 'INIT') )"></xsl:value-of>
        </xsl:variable>
    <!--<xsl:value-of select="$initCheck"></xsl:value-of><xsl:text>-initCheck|</xsl:text>-->
        <xsl:variable name="sentCheck">
            <xsl:value-of select="mx:execute-formula('client.scb.fmrp.initCheck',concat( 'FLOW_ID:', $flowID,',STATUS:', 'SENT') )"></xsl:value-of>
        </xsl:variable>
    <!--<xsl:value-of select="$sentCheck"></xsl:value-of><xsl:text>-sentCheck|</xsl:text>-->
        <xsl:variable name="cancelCheck">
            <xsl:value-of select="mx:execute-formula('client.scb.fmrp.initCheck',concat( 'FLOW_ID:', $flowID,',STATUS:', 'CANC') )"></xsl:value-of>
        </xsl:variable>
    <!--<xsl:value-of select="$cancelCheck"></xsl:value-of><xsl:text>-cancelCheck|</xsl:text>-->
        <xsl:variable name="countCheck">
            <xsl:value-of select="mx:execute-formula('client.scb.fmrp.countCheck',concat( 'FLOW_ID:', $flowID) )"></xsl:value-of>
        </xsl:variable>
    <!--<xsl:value-of select="$countCheck"></xsl:value-of><xsl:text>-countCheck|</xsl:text> -->
        <xsl:choose>
 
            <!--***variable declare ends-->
            <!--FAIS:regular job auto cashflow queue into FRMP  I2SR: When realtime and regular work concurrently and regular job inserted data in staging table-->
            <xsl:when test="($action='FAIS' or $action='I2SR') and $initCheck=1">
                <xsl:value-of select="mx:execute-formula('client.scb.fmrp.updateFmrpPay',concat( 'FLOW_ID:',  $flowID,',STATUS:', 'INIT') )"></xsl:value-of>
            </xsl:when>
 
            <!--Manual move back cashflow status to INIT, this is for replaying cashflow to Ratan, user/pss could perfrom FMIS to replay msg to Ratan, Note FMSI message dont flow to Ratan-->
            <xsl:when test="$action='FMSI' and $sentCheck=1">
                <xsl:value-of select="mx:execute-formula('client.scb.fmrp.sendCancel',concat( 'FLOW_ID:', $flowID) )"></xsl:value-of>
            </xsl:when>
 
            <!--Manual push into MLS for CANC flow -->
            <xsl:when test="$action='FMIS'and $cancelCheck=1">
                <xsl:value-of select="mx:execute-formula('client.scb.fmrp.updateFmrpPay',concat( 'FLOW_ID:',  $flowID,',STATUS:', 'CANC') )"></xsl:value-of>
            </xsl:when>
 
            <!--FMIS: Manual push a new flow I2SR:Realtime push a new flow-->
            <xsl:when test="($action='FMIS' or $action='I2SR') and $countCheck=0">
                <xsl:value-of select="mx:execute-formula('client.scb.fmrp.insertPay',concat( 'FLOW_ID:', $flowID) )"></xsl:value-of>
            </xsl:when>
 
            <!--Manual push, and the record hava already been in table.-->
            <xsl:when test="$action='FMIS'and $initCheck=1">
                <xsl:value-of select="mx:execute-formula('client.scb.fmrp.updateFmrpPay',concat( 'FLOW_ID:',  $flowID,',STATUS:', 'INIT') )"></xsl:value-of>
            </xsl:when>
      <!--TODO: Real Time Status update -->
 
            <!--Supress MLS cashflow
            <xsl:when test="$action='MA2S'">
                <xsl:value-of select="mx:execute-formula('client.scb.mls.ack.sendCheck',concat( 'FLOW_ID:', $flowID) )"></xsl:value-of>
            </xsl:when>
       -->
            <xsl:otherwise>discard</xsl:otherwise>
        </xsl:choose>
    </xsl:template>
</xsl:stylesheet>
```

### client.scb.fmrp.initCheck

Type:SQL

Data Source:sql1.xml

```sql
select count(1) 
from SCB_FMRP_DBF
WHERE M_STATUS='MxCTX#STATUS#Mx'
and   M_FLOW_ID=MxCTX#FLOW_ID#Mx
```

### client.scb.fmrp.countCheck

Type:SQL

Data Source:sql1.xml

```sql
select count(1) 
from SCB_FMRP_DBF
WHERE M_FLOW_ID=MxCTX#FLOW_ID#Mx
```

### client.scb.fmrp.updateFmrpPay

Type:SQL

Data Source:sql1.xml

```sql
declare @publish   CHAR(20)
begin
UPDATE SCB_FMRP_DBF
SET M_STATUS='SENT'
WHERE M_STATUS='MxCTX#STATUS#Mx'
and   M_FLOW_ID=MxCTX#FLOW_ID#Mx
select 'out[STPDOC_DATA_TYPE2=publish]'
end
```

### client.scb.fmrp.sendCancel

Type:SQL

Data Source:sql1.xml

```sql
declare @publish   CHAR(20)
begin
UPDATE SCB_FMRP_DBF
SET M_STATUS='CANC'
WHERE M_STATUS='SENT'
and   M_FLOW_ID=MxCTX#FLOW_ID#Mx
select 'discard[STPDOC_DATA_TYPE2=cancel]'
end
```

### client.scb.fmrp.insertPay

Type:SQL

Data Source:sql1.xml

```sql
begin    
insert into  MUREXDB.SCB_FMRP_DBF(M_FLOW_ID,M_STATUS,M_RATAN_ID,M_INS_DATETIME)
values (MxCTX#FLOW_ID#Mx ,'SENT',0,  GETDATE())
select 'out[STPDOC_DATA_TYPE2=publish]'
end
```

### client.scb.fmrp.fmrpEnrich

Type:XSLTREE

Data Source:mxpayml.dtd

XSL Parameter:

counterparty FORMULA mx.pay.flow.counterparty

trnNum FORMULA mx.pay.trade.iD

```xml
<xsl:stylesheet version="1.0" extension-element-prefixes="mx" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:mx="http://murex.com/xslt/common">

	<!--Variable declare starts-->
	<xsl:variable name="trnNum">Mx#client.scb.pay.trade.tradeid#Mx</xsl:variable>
	<xsl:variable name="counterparty">Mx#mx.pay.flow.counterparty#Mx</xsl:variable>
	<xsl:variable name="LEID">Mx#client.scb.fmrp.LEIDandSCIIDMatrix(0,0)#Mx</xsl:variable>
	<xsl:variable name="SCIID">Mx#client.scb.fmrp.LEIDandSCIIDMatrix(0,1)#Mx</xsl:variable>
	<xsl:variable name="TraderPSID">Mx#client.scb.fmrp.traderPSID#Mx</xsl:variable>
	<xsl:variable name="timeStamp">Mx#client.scb.fmrp.timeStamp#Mx</xsl:variable>
	<xsl:variable name="amendFlag">Mx#client.scb.fmrp.amendFlag#Mx</xsl:variable>
	<xsl:variable name="portBizUnit">Mx#client.scb.fmrp.portBizUnit#Mx</xsl:variable>

	<!--Variable declare ends-->
	<xsl:template match="@*|node()">
		<xsl:copy>
			<xsl:apply-templates select="@*|node()"></xsl:apply-templates>
		</xsl:copy>
	</xsl:template>
	<xsl:template match="/MxPayML">
		<xsl:copy>
			<xsl:apply-templates></xsl:apply-templates>
			<xsl:element name="scbExtraInfoBlock">
				<xsl:element name="publicationDateTime">
					<xsl:value-of select="$timeStamp"></xsl:value-of>
				</xsl:element>
				<xsl:element name="validationLevel">
					<xsl:value-of select="mx:execute-formula( 'client.scb.tds.getValStatus', concat( 'NB:', $trnNum ) )"></xsl:value-of>
				</xsl:element>
				<xsl:element name="entityFMID">
					<xsl:value-of select="$LEID"></xsl:value-of>
				</xsl:element>
				<xsl:element name="entityLEID">
					<xsl:value-of select="$SCIID"></xsl:value-of>
				</xsl:element>
				<xsl:element name="counterpartyFMID">
					<xsl:value-of select="mx:execute-formula( 'client.scb.tds.common.getLEID', concat( 'NAME:', $counterparty ) )"></xsl:value-of>
				</xsl:element>
				<xsl:element name="traderID">
					<xsl:value-of select="$TraderPSID"></xsl:value-of>
				</xsl:element>
				<xsl:element name="portBizUnit">
					<xsl:value-of select="$portBizUnit"></xsl:value-of>
				</xsl:element>
				<xsl:element name="amendmentFlag">
					<xsl:value-of select="$amendFlag"></xsl:value-of>
				</xsl:element>
			</xsl:element>
		</xsl:copy>
	</xsl:template>
</xsl:stylesheet>
```

### client.scb.fmrp.LEIDandSCIIDMatrix

Type:XSL

Data Source:mxpayml.dtd

Local Parameter:

entity Mx#mx.pay.flow.entity#Mx

```xml
<Operand Code="Matrix">Mx#client.scb.fmrp.getLEIDandSCIID{NAME:Contexts.entity}#Mx</Operand>
```

### client.scb.fmrp.getLEIDandSCIID

Type:SQL

Data Source:sql1.xml

```sql
select        rtrim(M_ATLAS_LEID ) 'LEID', rtrim(M_SCI_ID) 'SCIID'
from    TABLE#DATA#COUNTERP_DBF c,
            TABLE#DATA#ENTITY_DBF e 
where  c.M_LABEL = e.M_CTP_COD
and e.M_LABEL = 'MxCTX#NAME#Mx'
```

### client.scb.fmrp.traderPSID

Type:SQL

Data Source:sql1.xml

```sql
select top 1 rtrim(M_L_CODE)  from TRN_USRD_DBF WHERE M_LABEL ='Mx#client.scb.fmrp.trader#Mx'
```

### client.scb.fmrp.trader

Type:SQL

Data Source:sql1.xml

```sql
select CASE WHEN M_COMMENT_BS = 'B' THEN rtrim(M_BTRADER) ELSE rtrim(M_STRADER) END from TRN_HDR_DBF WHERE M_NB=Mx#client.scb.pay.trade.tradeid#Mx
```

### client.scb.fmrp.timeStamp

Type:SQL

Data Source:sql1.xml

```sql
select rtrim(convert(CHAR,getdate(),105)) + ' ' + rtrim(convert(CHAR,getdate(),20))
```

### client.scb.fmrp.amendFlag

Type:XSL

Data Source:mxpayml.dtd

```xml
<xsl:stylesheet version="1.0" extension-element-prefixes="mx"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:mx="http://murex.com/xslt/common">
    <xsl:template match="/">

    <xsl:variable name="tradeRef">Mx#client.scb.pay.trade.tradeRef#Mx</xsl:variable>
        <xsl:variable name="sysDate" select="/MxPayML/systemDate"></xsl:variable>

    <xsl:variable name="tradeAmendRecordCount">
      <xsl:value-of select="mx:execute-formula('client.scb.fmrp.tradeMktOpRecord', concat( 'tradeRef:', $tradeRef,',sysDate:', $sysDate) )"></xsl:value-of>
    </xsl:variable>

        <xsl:choose>
            <xsl:when test="$tradeAmendRecordCount = 0">N</xsl:when>
            <xsl:when test="$tradeAmendRecordCount > 0">Y</xsl:when>
        </xsl:choose>

    </xsl:template>
</xsl:stylesheet>
```

### client.scb.fmrp.tradeMktOpRecord

Type:SQL

Data Source:sql1.xml

```sql
select count(1) 
 from MKT_OP_DBF 
where M_DEST_NB=MxCTX#tradeRef#Mx and (M_TYPE='RPL' or M_TYPE='RPL_M') and M_SYS_DATE = 'MxCTX#sysDate#Mx'
```

### client.scb.fmrp.portBizUnit

Type:SQL

Data Source:sql1.xml

```sql
select top 1 rtrim(M_BIZ_UNIT) from TABLE#DATA#PORTFOLI_DBF WHERE M_LABEL ='Mx#client.scb.pay.flow.portfolio#Mx'
```

### client.scb.fmrp.retryCheck

Type:XMLF

Data Source:

```xml
<Operator Code="If">
    <Operator Code="Or">
        <Operator Code="Equal">
            <Operand Code="ScalarField">STPDOC_DATA_TYPE3</Operand>
            <Operand Code="ScalarString"></Operand>
        </Operator>
        <Operator Code="LessThan">
            <Operator Code="StringToDouble">
                <Operand Code="ScalarField">STPDOC_DATA_TYPE3</Operand>
            </Operator>
            <Operand Code="ScalarDouble">3.0</Operand>
        </Operator>
    </Operator>
    <Operand Code="ScalarString">retry[STPDOC_DATA_TYPE3=Mx#client.scb.fmrp.retryCnt#Mx]</Operand>
    <Operand Code="ScalarString">stop</Operand>
</Operator>
```

### client.scb.fmrp.retryCnt

Type:XMLF

Data Source

```xml
<Operator Code="If">
	<Operator Code="Equal">
		<Operand Code="ScalarField">STPDOC_DATA_TYPE3</Operand>
		<Operand Code="ScalarString"/>
	</Operator>
	<Operand Code="ScalarDouble">1</Operand>
	<Operator Code="Plus">
		<Operator Code="StringToDouble">
			<Operand Code="ScalarField">STPDOC_DATA_TYPE3</Operand>
		</Operator>
		<Operand Code="ScalarDouble">1</Operand>
	</Operator>
</Operator>
```

### client.scb.fmrp.inbound.inboundRouter

Type:XSL

```xml
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
	<xsl:template match="/">
		<!--variable declare-->
		<xsl:variable name="sourceSystem" select="normalize-space(/MxPayMLResponse/sourceSystem)"></xsl:variable>
		<xsl:variable name="objectNature" select="normalize-space(/MxPayMLResponse/objectNature)"></xsl:variable>
		<xsl:variable name="murexID" select="normalize-space(/MxPayMLResponse/MXG2000/flowID)"></xsl:variable>
		<xsl:variable name="ratanMsgType" select="normalize-space(/MxPayMLResponse/message)"></xsl:variable>
		<xsl:choose>
			<xsl:when test="$sourceSystem='RATAN' and $objectNature='cashflow' and $murexID>0 and $ratanMsgType='RATAN Acknowledged'">acked</xsl:when>
			<xsl:when test="$sourceSystem='RATAN' and $objectNature='cashflow' and $murexID>0 and $ratanMsgType='RATAN Released'">released</xsl:when>
			<xsl:otherwise>discard</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
</xsl:stylesheet>
```

### client.scb.fmrp.isFmrpEntity

Type:XSL

```xml
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:mx="http://murex.com/xslt/common">
	<xsl:template match="/">
		<xsl:variable name="entity">Mx#client.scb.pay.flow.entity#Mx</xsl:variable>
		<xsl:variable name="isFmrpEntity">
			<xsl:value-of select="mx:execute-formula( 'client.scb.fmrp.fmrpEntityCheck', concat( 'entity:', $entity ) )"></xsl:value-of>
		</xsl:variable>
	
		<xsl:choose>
			<xsl:when test="$isFmrpEntity > 0">Y</xsl:when>
			<xsl:otherwise>N</xsl:otherwise>
		</xsl:choose>

	</xsl:template>
</xsl:stylesheet>
```

### client.scb.fmrp.fmrpEntityCheck

Type:SQL

```xml
select count(1) 
from FMRP_ENTITY_DBF
where M_ENTITY = 'MxCTX#entity#Mx'
```

### client.scb.fmrp.fmrpPrecioiusMetalCheck

```xml
SELECT count(*)
FROM PAY_FLOW_DBF T
WHERE EXISTS( select 1 from PAY_FLOW_DBF A
INNER JOIN TABLE#DATA#CURRENCY_DBF B ON A.M_CURRENCY = B.M_LABEL
WHERE A.M_TRN_REF = T.M_TRN_REF
AND B.M_BUL_CUR_FL='Y')
AND T.M_FLOW_ID  = MxCTX#flowID#Mx
```

### client.scb.fmrp.isPreciousMetalDealFlow

```xml
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:mx="http://murex.com/xslt/common">
	<xsl:template match="/">
		<xsl:variable name="flowID" select="/MxPayML/flowID"></xsl:variable>
		<xsl:variable name="isPreciousMetalDealFlow">
			<xsl:value-of select="mx:execute-formula( 'client.scb.fmrp.fmrpPrecioiusMetalCheck', concat( 'flowID:', $flowID ) )"></xsl:value-of>
		</xsl:variable>
	
		<xsl:choose>
			<xsl:when test="$isPreciousMetalDealFlow > 0">Y</xsl:when>
			<xsl:otherwise>N</xsl:otherwise>
		</xsl:choose>

	</xsl:template>
</xsl:stylesheet>
```

### client.scb.fmrp.inbound.inboundRouter

Type:XSL

```xml
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
	<xsl:template match="/">
		<!--variable declare-->
		<xsl:variable name="sourceSystem" select="normalize-space(/MxPayMLResponse/sourceSystem)"></xsl:variable>
		<xsl:variable name="objectNature" select="normalize-space(/MxPayMLResponse/objectNature)"></xsl:variable>
		<xsl:variable name="murexID" select="normalize-space(/MxPayMLResponse/MXG2000/flowID)"></xsl:variable>
		<xsl:variable name="ratanMsgType" select="normalize-space(/MxPayMLResponse/message)"></xsl:variable>
		<xsl:choose>
			<xsl:when test="$sourceSystem='RATAN' and $objectNature='cashflow' and $murexID>0 and $ratanMsgType='RATAN Acknowledged'">acked</xsl:when>
			<xsl:when test="$sourceSystem='RATAN' and $objectNature='cashflow' and $murexID>0 and $ratanMsgType='RATAN Released'">released</xsl:when>
			<xsl:otherwise>discard</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
</xsl:stylesheet>
```

### client.scb.fmrp.inbound.murexID

Type:XSL

Data Source:mlspayml.dtd

```xml
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:template match="/">
        <xsl:choose>
            <xsl:when test="normalize-space(/MxPayMLResponse/MXG2000/flowID) !=''">
                <xsl:value-of select="normalize-space(/MxPayMLResponse/MXG2000/flowID)"></xsl:value-of>
            </xsl:when>
            <xsl:otherwise>0</xsl:otherwise>
        </xsl:choose>
    </xsl:template>
</xsl:stylesheet>
```

### client.scb.fmrp.inbound.payFlowID

Type:XMLF

```xml
<Operator Code="Plus">
	<Operand Code="ScalarString">FLOW_ID=</Operand>
	<Operand Code="ScalarString">Mx#client.scb.fmrp.inbound.murexID#Mx</Operand>
</Operator>
```

### client.scb.fmrp.inbound.payInsertionFilter

Type:XMLF

```xml
<Operator Code="If">
	<Operator Code="Or">
		<Operator Code="Equal">
			<Operand Code="ScalarString">Mx#client.scb.fmrp.isFmrpEntity#Mx</Operand>
			<Operand Code="ScalarString">N</Operand>
		</Operator>
		<Operator Code="Equal">
			<Operand Code="ScalarString">Mx#client.scb.fmrp.isPreciousMetalDealFlow#Mx</Operand>
			<Operand Code="ScalarString">Y</Operand>
		</Operator>
	</Operator>
	<Operand Code="ScalarString">discard</Operand>
	<Operand Code="ScalarString">process</Operand>
</Operator>
```

### client.scb.fmrp.inbound.processAck

Type:XSL

Data Source:mlspayml.dtd

```xml
<xsl:stylesheet version="1.0" extension-element-prefixes="mx" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:mx="http://murex.com/xslt/common">
	<xsl:template match="/">
		<xsl:variable name="murexID" select="normalize-space(/MxPayMLResponse/MXG2000/flowID)"></xsl:variable>
		<xsl:variable name="ratanMsgType" select="normalize-space(/MxPayMLResponse/message)"></xsl:variable>
		<xsl:variable name="ratanID" select="normalize-space(/MxPayMLResponse/sourceID)"></xsl:variable>
		<xsl:variable name="ratanTimestamp" select="normalize-space(/MxPayMLResponse/timestamp)"></xsl:variable>
		<xsl:value-of select="mx:execute-formula('client.scb.fmrp.inbound.syncAck',concat( 'murexID:',$murexID,',ratanMsgType:',$ratanMsgType,',ratanID:',$ratanID,',ratanTimestamp:',$ratanTimestamp) )"></xsl:value-of>
	</xsl:template>
</xsl:stylesheet>
```

### client.scb.fmrp.inbound.ratanID

Type:XSL

Data Source:mlspayml.dtd

```sql
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:template match="/">
        <xsl:choose>
            <xsl:when test="normalize-space(/MxPayMLResponse/sourceID) !=''">
                <xsl:value-of select="normalize-space(/MxPayMLResponse/sourceID)"></xsl:value-of>
            </xsl:when>
            <xsl:otherwise>0</xsl:otherwise>
        </xsl:choose>
    </xsl:template>
</xsl:stylesheet>
```

### client.scb.fmrp.inbound.syncAck

Type:SQL

Data Source:sql1.xml

```xml
begin
    update SCB_FMRP_DBF
    set M_RATAN_ID='MxCTX#ratanID#Mx', M_REC_DATETIME=convert(datetime,'MxCTX#ratanTimestamp#Mx')
    where M_FLOW_ID = MxCTX#murexID#Mx
    update TABLE#DATA#PAYFLOW_DBF
    set M_REASONS='MxCTX#ratanMsgType#Mx'+' '+'MxCTX#ratanID#Mx'
    where M_FLOW_ID = MxCTX#murexID#Mx
    select 'success'
end 
```

### client.scb.fmrp.inbound.syncRelease

Type:SQL

Data Source:sql1.xml

```sql
begin
update SCB_FMRP_DBF
set M_STATUS='MATH'
where M_FLOW_ID = Mx#client.scb.fmrp.inbound.murexID#Mx
select 'success'
end    
```

### client.scb.mls.cpnEligible - Modify

Type:XSL

Data Source:mxpayml.dtd

```xml
<xsl:stylesheet version="1.0" extension-element-prefixes="mx" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:mx="http://murex.com/xslt/common">
	<xsl:template match="/">
		<xsl:variable name="action" select="MxPayML/action"></xsl:variable>
		<xsl:variable name="destinationStatus">
			<xsl:value-of select="MxPayML/destinationStatus"></xsl:value-of>
		</xsl:variable>
		<xsl:variable name="sourceStatus">
			<xsl:value-of select="MxPayML/flowStatus"></xsl:value-of>
		</xsl:variable>

		<!--###Cash-flow are coming from CPN queue will be sent MLS CPN for netting
RI2C: INIT to CNET -STP QUEUE
MIXC: INIT to CNET -Manual QUEUE
MCXI: CNET to INIT -Manual MLS UNDO
	    <xsl:when test="$action='RI2C' or $action='MIXC'or $action='MCXI'">Y</xsl:when>
			<xsl:when test="$action='RI2C' or $action='MIXC'or $action='MCXI'">Y</xsl:when>
comments ends-->
		<xsl:choose>
			<xsl:when test=" $sourceStatus='INIT'and  $destinationStatus='CNET' ">Y</xsl:when>
			<xsl:when test=" $sourceStatus='CNET'and  $destinationStatus='INIT' ">Y</xsl:when>
      <!--FMRP-->
			<xsl:when test=" $sourceStatus='INIT'and  $destinationStatus='SNTR' ">Y</xsl:when>
			<xsl:when test=" $sourceStatus='SNTR'and  $destinationStatus='INIT' ">Y</xsl:when>
      <!--FMRP END-->
			<xsl:otherwise>N</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
</xsl:stylesheet>
```

### client.scb.mxmlexchange.pay.test.countXmlErrors - Modify

Modify

```xml
<Operator Code="If">
	<Operator Code="Equal">
		<Operand Code="ScalarString">Mx#client.scb.pay.insertPay#Mx</Operand>
		<Operand Code="ScalarString">Y</Operand>
	</Operator>
	<Operand Code="ScalarString">insert</Operand>
	<!--MLS CPN netting starts-->
	<Operator Code="If">
		<Operator Code="Equal">
			<Operand Code="ScalarString">Mx#client.scb.mls.cpnEligible#Mx</Operand>
			<Operand Code="ScalarString">Y</Operand>
		</Operator>
		<Operand Code="ScalarString">extSettle</Operand>
		<!--MLS CPN netting ends-->
		<Operator Code="If">
			<Operand Code="ScalarBoolean">Mx#client.scb.mxmlexchange.pay.test.check#Mx</Operand>
			<Operator Code="If">
				<Operator Code="Equal">
					<Operand Code="ScalarString">Mx#client.scb.mls.optimise.CLSorCCIL#Mx</Operand>
					<Operand Code="ScalarString">others</Operand>
				</Operator>
				<Operator Code="If">
					<Operator Code="Equal">
						<Operand Code="ScalarString">Mx#client.scb.mxmlexchange.pay.test.stpchk#Mx</Operand>
						<Operand Code="ScalarString">Y</Operand>
					</Operator>
					<Operator Code="If">
						<Operator Code="Equal">
							<Operator Code="StrLength">
								<Operand Code="ScalarString">Mx#client.scb.mxmlexchange.pay.test.testXmlValues#Mx</Operand>
							</Operator>
							<Operand Code="ScalarDouble">0</Operand>
						</Operator>
						<Operator Code="If">

							<!-- Purge net payments without initial trade id and email settlement team to settle them outside Murex-->
							<Operator Code="Equal">
								<Operand Code="ScalarString">Mx#client.scb.mxmlexchange.pay.undoNet.initialTradePurgecheck#Mx</Operand>
								<Operand Code="ScalarString">Email</Operand>
							</Operator>
							<Operand Code="ScalarString">Email</Operand>
							<Operator Code="If">
								<Operator Code="Equal">
									<Operand Code="ScalarString">Mx#client.scb.mxmlexchange.legalId.pay.legalId#Mx</Operand>
									<Operand Code="ScalarString"></Operand>
								</Operator>
								<Operand Code="ScalarString">ALERT_SD[STPDOC_TEMPLATE_NAME=client.scb.alert.legalIdpay]</Operand>
								<Operator Code="If">
									<Operator Code="Equal">
										<Operand Code="ScalarString">Mx#mx.pay.flow.entity#Mx</Operand>
										<Operand Code="ScalarString"></Operand>
									</Operator>
									<Operand Code="ScalarString">ALERT_SD[STPDOC_TEMPLATE_NAME=client.scb.alert.entitypayment]</Operand>
									<Operator Code="If">
										<Operator Code="And">
											<Operator Code="Equal">
												<Operand Code="ScalarString">Mx#mx.pay.flow.entity#Mx</Operand>
												<Operand Code="ScalarString">SCFB_SEOUL</Operand>
											</Operator>
											<Operator Code="In">
												<Operand Code="ScalarString">Mx#mx.pay.flow.currency#Mx</Operand>
												<Operand Code="Vector">
													<Operand Code="ScalarString">KRW</Operand>
													<Operand Code="ScalarString">KRO</Operand>
												</Operand>
											</Operator>
										</Operator>
										<Operand Code="ScalarString">KFB</Operand>
										<Operator Code="If">
											<Operand Code="ScalarBoolean">Mx#client.scb.mxmlexchange.pay.com.isUnderScope#Mx</Operand>
											<Operand Code="ScalarString">Mx#client.scb.mxmlexchange.pay.com.swiftC6TemplateName#Mx</Operand>
											<Operand Code="ScalarString">OUT</Operand>
										</Operator>
									</Operator>
								</Operator>
							</Operator>
						</Operator>
						<Operand Code="ScalarString">ALERT_SI[STPDOC_TEMPLATE_NAME=client.scb.alert.si]</Operand>
					</Operator>
					<Operand Code="ScalarString">DISCARD</Operand>
				</Operator>
				<Operand Code="ScalarString">Mx#client.scb.mls.optimise.CLSorCCIL#Mx</Operand>
			</Operator>
			<Operand Code="ScalarString">DISCARD</Operand>
		</Operator>
	</Operator>
</Operator>
```

### client.scb.pay.flow.portfolio

Type:XSL

Data Source:mxpayml.dtd

```xml
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:template match="/">
        <xsl:value-of select="MxPayML/portfolio" />
    </xsl:template>
</xsl:stylesheet>
```

### client.scb.pay.insertPay

Type:XSL

Data Source:mxpayml.dtd

```xml
<xsl:stylesheet version="1.0" extension-element-prefixes="mx" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:mx="http://murex.com/xslt/common">
    <xsl:template match="/">
        <xsl:variable name="event">Mx#client.scb.pay.event#Mx</xsl:variable>
        <xsl:choose>
            <xsl:when test=" $event='Insert'">Y</xsl:when>
            <xsl:otherwise>N</xsl:otherwise>
        </xsl:choose>
    </xsl:template>
</xsl:stylesheet>
```

### client.scb.pay.trade.tradeRef

Type:XSL

Data Source:mxpayml.dtd

```sql
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:template match="/">
        <xsl:value-of select="format-number( MxPayML/transactionID, '0' )" />
    </xsl:template>
</xsl:stylesheet>
```

```xml

```

```xml

```

# Task change

### docPayment

add two node:

- insert
- extSettle

Remove node:

- mls

### extSettleRouter

![image2023-1-16_0-13-21.png](attachments/image2023-1-16_0-13-21.png)

Router task

Task code:extSettleRouter

Task Description:extSettleRouter

Routing Fomula:client.scb.fmrp.ExtSettleRouter

node:

fmrp

mls

![image2023-1-16_0-15-43.png](attachments/image2023-1-16_0-15-43.png)

### FmrpFilter

Router task

Task code:FmrpFilter

Task Description:sync cf status & suppression

Routing Fomula:client.scb.fmrp.SyncStatus

node:

out

discard

![image2023-1-16_0-28-3.png](attachments/image2023-1-16_0-28-3.png)

### FmrpSettleEnrichment

Xml transform task

Task code:FmrpSettleEnrichment

Task Description:add extra tags into payment mxml

Transformation Fomula:client.scb.fmrp.fmrpEnrich

Add XML header  √

STPDOC_TEMPLATE_GRAMMAR mxpayml.dtd

STPDOC_TEMPLATE_GRAMMAR mxpayml.dtd

![image2023-1-16_0-18-55.png](attachments/image2023-1-16_0-18-55.png)

![image2023-1-16_0-25-52.png](attachments/image2023-1-16_0-25-52.png)

### FmrpSettleFilter

Body filter task

Task code:FmrpSettleFilter

Task Description:Exclude the payment context

Choice:Exclude

STPDOC_TEMPLATE_GRAMMAR mxcontext.dtd

![image2023-1-16_0-24-40.png](attachments/image2023-1-16_0-24-40.png)

![image2023-1-16_0-26-33.png](attachments/image2023-1-16_0-26-33.png)

### FmrpOutboundMQ

Outbound MQ task

Task code:FmrpOutboundMQ

Task Description:MQ

| Host | 10.198.198.93 |
| --- | --- |
| Port | 8212 |
| Channel | UKMXGCLNTS2 |
| Queue manager | UKFM02S1 |
| Queue | GM.MXG.MLS.FEDS.UAT |
| User | ukmxgmq |

![image2023-2-7_10-56-18.png](attachments/image2023-2-7_10-56-18.png)

![image2023-1-16_0-38-15.png](attachments/image2023-1-16_0-38-15.png)

### INIT2SNTR

pay action task

Task code:INIT2SNTR

Task Description:INIT2SNTR

Workflow Type:Payment

Action:I2SR

Filter Formula:[client.scb.pay.flow.id](http://client.scb.pay.flow.id)

![image2023-1-16_0-36-30.png](attachments/image2023-1-16_0-36-30.png)

two node:

Triggered

Error

![image2023-1-16_0-37-48.png](attachments/image2023-1-16_0-37-48.png)

### FmrpRemoveError

Body filter task

Task code:FmrpRemoveError

Task Description:FmrpRemoveError

| Choice | Exclude |
| --- | --- |
| STPDOC_TEMPLATE_GRAMMAR | trigger_err.dtd |
| STPDOC_INPUT_OUTPUT | O |
| STPDOC_CONTENT_TYPE | RES.XML |

![image2023-1-16_0-41-36.png](attachments/image2023-1-16_0-41-36.png)

![image2023-1-16_0-42-30.png](attachments/image2023-1-16_0-42-30.png)

### FmrpRetryCheck

Router task

Task code:FmrpRetryCheck

Task Description:max retry times 3

Routing Fomula:client.scb.fmrp.retryCheck

Two node:

stop

retry

![image2023-1-16_0-56-25.png](attachments/image2023-1-16_0-56-25.png)

### FmrpPurge

Purge task

Task Code:FmrpPurge

Task Description:FmrpPurge

![image2023-1-16_1-1-24.png](attachments/image2023-1-16_1-1-24.png)

### FmrpInboundMQ

Inbound MQ task

Task code:FmrpInboundMQ

Task Description:RATAN-MUREX cashflow inbound

| Host | 10.193.106.152 |
| --- | --- |
| Port | 1414 |
| Channel | UKMXGCLNTS1 |
| Queue manager | UKIG01S2 |
| Queue | GMPCI.MLS.MXG.RQSTIN |
| User | ukmxgmq |

![image2023-1-16_1-4-28.png](attachments/image2023-1-16_1-4-28.png)

| STPDOC_ACTION | ACK_ALLEGE |
| --- | --- |
| STPDOC_DATA_TYPE1 | RATAN_CASHFLOW |
| STPDOC_DATA_TYPE2 | client.scb.fmrp.inbound.razorID |
| STPDOC_DATA_TYPE3 | client.scb.fmrp.inbound.murexID |
| STPDOC_REF | client.scb.fmrp.inbound.murexID |
| STPDOC_REF_TYPE | PAYMENT |

![image2023-1-16_1-7-28.png](attachments/image2023-1-16_1-7-28.png)

| STPDOC_CONTENT_TYPE | RES.XML |
| --- | --- |
| STPDOC_TEMPLATE_GRAMMAR | mlspayml.dtd |
| XMLFLOW_TYPE | UserDefined |

![image2023-1-16_1-8-29.png](attachments/image2023-1-16_1-8-29.png)

### PayInsertionFilter

![image2023-1-19_11-39-27.png](attachments/image2023-1-19_11-39-27.png)

Router task

Task code: PayInsertionFilter

Task Description: filter for payment insertion

Routing Fomula: client.scb.fmrp.inbound.payInsertionFilter

Two node:

process

discard

# Link change

### DocPayment

Delete link: mls → PaymentMLSOUTboundRouter

Add Link: extSettle → extSettleRouter

Add Link: insert → INIT2SNTR

### extSettleRouter

Add link: fmrp → FmrpFilter

Add link: mls → PaymentMLSOUTboundRouter

### FmrpFilter

Add link: out → FmrpSettleEnrichment

### FmrpSettleEnrichment

Add link: Output → FmrpSettleFilter

### FmrpSettleFilter

Add link: Output → FmrpOutboundMQ

### INIT2SNTR

Add link: Triggered → FmrpPurge

Add link: Error →  FmrpRemoveError

### FmrpRemoveError

Add link: Output → FmrpRetryCheck

### FmrpRetryCheck

Add link: stop→ FmrpPurge

Add link:  retry → INIT2SNTR

### FmrpInboundMQ

Add link: Output→ FmrpAckRouter

# Payment workflow

![image2023-1-16_1-54-38.png](attachments/image2023-1-16_1-54-38.png)

![image2023-1-16_1-55-29.png](attachments/image2023-1-16_1-55-29.png)

*Update of 2023.01.17 by Lyn:

RATAN-11101

1.Upated formula

client.scb.mxmlexchange.pay.test.countXmlErrors

client.scb.pay.insertPay

2.delete formula

client.scb.fmrp.fmrpPortfolioCheck

3.create new formula

client.scb.fmrp.inbound.payInsertionFilter

client.scb.fmrp.isFmrpEntity

client.scb.fmrp.fmrpEntityCheck

4.delete link between task docpayment and INIT2SNTR

5.Create new task

PayInsertionFilter   input task: docPayment  output node1:process -> task: SNTR   output node2:discard -> task:FmrpPurge

RATAN-10822

1.create new formula

client.scb.fmrp.inbound.inboundRouter

client.scb.fmrp.inbound.payFlowID

client.scb.fmrp.inbound.syncRelease

client.scb.fmrp.inbound.processAck

client.scb.fmrp.inbound.syncAck

2.delete formula

client.scb.fmrp.inbound.msgRouter

client.scb.fmrp.inbound.razorID

client.scb.fmrp.inbound.razorAckVald

client.scb.fmrp.inbound.recordCount

3.updated formula

client.scb.fmrp.inbound.murexID

4.delete task FmrpAckRouter

5.create task

FmrpInboundRouter

SNTR2RLSR

FmrpAckProcessor

FmrpReleaseProcessor

![image2023-1-18_11-34-44.png](attachments/image2023-1-18_11-34-44.png)