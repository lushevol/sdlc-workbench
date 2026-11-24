#

# Formula change

### client.scb.fmrp.inbound.duplicator

Type:XSL

Data Source: mlspayml.dtd

```sql
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
	<xsl:template match="/">
		<xsl:for-each select="/MxPayMLResponse/MXG2000/flowID">
			<Line>
				<Col1 Ftype="C">out[STPDOC_DATA_TYPE2=<xsl:value-of select="@id"></xsl:value-of>]</Col1>
			</Line>
		</xsl:for-each>
	</xsl:template>
</xsl:stylesheet>
```

### client.scb.fmrp.inbound.inboundRouter

Type:XSL

Data Source: mlspayml.dtd

```sql
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

Data Source: mlspayml.dtd

```sql
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

Data Source:

```sql
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

### client.scb.fmrp.inbound.payInsertionFilter

Type:XMLF

Data Source: mxpayml.dtd

```sql
<Operator Code="If">
<!-- static data check -->
	<Operator Code="Or">
		<!-- Entity -->
		<Operator Code="Equal">
			<Operand Code="ScalarString">Mx#client.scb.fmrp.isFmrpEntity#Mx</Operand>
			<Operand Code="ScalarString">N</Operand>
		</Operator>
		<!-- Non Deliverable Currency -->
		<Operator Code="Equal">
			<Operand Code="ScalarString">Mx#client.scb.fmrp.isNDCurrency#Mx</Operand>
			<Operand Code="ScalarString">Y</Operand>
		</Operator>
		<!-- zero Amount -->
		<Operator Code="Equal">
			<Operand Code="ScalarString">Mx#client.scb.fmrp.Amount#Mx</Operand>
			<Operand Code="ScalarString">Y</Operand>
		</Operator>
	</Operator>
	<!-- static data check failed-->
	<Operand Code="ScalarString">discard</Operand>
	<!-- static data check pass-->
	<Operator Code="If">
		<Operator Code="Equal">
			<Operand Code="ScalarString">Mx#client.scb.fmrp.tradePaymentCheck#Mx</Operand>
			<Operand Code="ScalarString">Y</Operand>
		</Operator>
		<Operator Code="If">
			<!-- trade related info -->
			<Operator Code="Or">
				<!-- PreciousMetal-->
				<Operator Code="Equal">
					<Operand Code="ScalarString">Mx#client.scb.fmrp.isPreciousMetalDealFlow#Mx</Operand>
					<Operand Code="ScalarString">Y</Operand>
				</Operator>
				<!-- FXD Supprission -->
				<Operator Code="Equal">
					<Operand Code="ScalarString">Mx#client.scb.fmrp.fxdSupprission#Mx</Operand>
					<Operand Code="ScalarString">Y</Operand>
				</Operator>
				<!-- CPT Eligible logic -->
				<Operator Code="Equal">
					<Operand Code="ScalarString">Mx#client.scb.fmrp.isCPT#Mx</Operand>
					<Operand Code="ScalarString">Y</Operand>
				</Operator>
				<!-- CPT Eligible logic -->				
			</Operator>
			<Operand Code="ScalarString">discard</Operand>
			<Operand Code="ScalarString">process</Operand>			
		</Operator>
		<Operator Code="If">
			<Operator Code="Or">
				<Operator Code="Equal">
					<Operand Code="ScalarField">STPDOC_DATA_TYPE2</Operand>
					<Operand Code="ScalarString"></Operand>
				</Operator>
				<Operator Code="LessThan">
					<Operator Code="StringToDouble">
						<Operand Code="ScalarField">STPDOC_DATA_TYPE2</Operand>
					</Operator>
					<Operand Code="ScalarDouble">3.0</Operand>
				</Operator>
			</Operator>
			<Operand Code="ScalarString">retry[STPDOC_DATA_TYPE2=Mx#client.scb.fmrp.retryCnt#Mx]</Operand>
			<Operand Code="ScalarString">discard</Operand>
		</Operator>
	</Operator>
</Operator>
```

### client.scb.fmrp.inbound.processAck

Type:XSL

Data Source:  mlspayml.dtd

```sql
<xsl:stylesheet version="1.0" extension-element-prefixes="mx" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:mx="http://murex.com/xslt/common">
	<xsl:template match="/">
		<xsl:variable name="murexID" select="normalize-space(/MxPayMLResponse/MXG2000/flowID)"></xsl:variable>
		<xsl:variable name="ratanEvent" select="normalize-space(/MxPayMLResponse/event)"></xsl:variable>
		<xsl:variable name="ratanMsgType" select="normalize-space(/MxPayMLResponse/message)"></xsl:variable>
		<xsl:variable name="ratanID" select="normalize-space(/MxPayMLResponse/sourceID)"></xsl:variable>
		<xsl:variable name="ratanTimestamp" select="normalize-space(/MxPayMLResponse/timestamp)"></xsl:variable>
		<xsl:value-of select="mx:execute-formula('client.scb.fmrp.inbound.syncAck',concat( 'murexID:',$murexID,',ratanMsgType:',$ratanMsgType,',ratanID:',$ratanID,',ratanTimestamp:',$ratanTimestamp,',ratanEvent:',$ratanEvent) )"></xsl:value-of>
</xsl:template>
</xsl:stylesheet>
```

### client.scb.fmrp.inbound.processRelease

Type:XSL

Data Source:  mlspayml.dtd

```sql
<xsl:stylesheet version="1.0" extension-element-prefixes="mx" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:mx="http://murex.com/xslt/common">
	<xsl:template match="/">
		<xsl:variable name="murexID" select="normalize-space(/MxPayMLResponse/MXG2000/flowID)"></xsl:variable>
		<xsl:variable name="sourceID" select="normalize-space(/MxPayMLResponse/sourceID)"></xsl:variable>
		<xsl:variable name="ratanNetId">
			<xsl:choose>
				<xsl:when test="starts-with($sourceID,'N')">
					<xsl:value-of select="$sourceID"></xsl:value-of>
				</xsl:when>
				<xsl:otherwise>0</xsl:otherwise>
			</xsl:choose>
		</xsl:variable>
		<xsl:value-of select="mx:execute-formula('client.scb.fmrp.inbound.syncRelease',concat( 'murexID:',$murexID,',ratanNetId:',$ratanNetId) )"></xsl:value-of>
	</xsl:template>
</xsl:stylesheet>
```

### client.scb.fmrp.inbound.ratanEvent

Type:XSL

Data Source:  mlspayml.dtd

```sql
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:template match="/">
        <xsl:choose>
            <xsl:when test="normalize-space(/MxPayMLResponse/event) !=''">
                <xsl:value-of select="normalize-space(/MxPayMLResponse/event)"></xsl:value-of>
            </xsl:when>
            <xsl:otherwise></xsl:otherwise>
        </xsl:choose>
    </xsl:template>
</xsl:stylesheet>
```

### client.scb.fmrp.inbound.ratanID

Type:XSL

Data Source:  mlspayml.dtd

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

### client.scb.fmrp.inbound.ratanMessageType

Type:XSL

Data Source:  mlspayml.dtd

```sql
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:template match="/">
        <xsl:choose>
            <xsl:when test="normalize-space(/MxPayMLResponse/message) !=''">
                <xsl:value-of select="normalize-space(/MxPayMLResponse/message)"></xsl:value-of>
            </xsl:when>
            <xsl:otherwise></xsl:otherwise>
        </xsl:choose>
    </xsl:template>
</xsl:stylesheet>
```

### client.scb.fmrp.inbound.releasedEnrich

Type:XSL

Data Source:  mlspayml.dtd

```sql
<xsl:stylesheet version="1.0" extension-element-prefixes="mx" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:mx="http://murex.com/xslt/common">
	<xsl:template match="@*|node()">
		<xsl:copy>
			<xsl:apply-templates select="@*|node()"/>
		</xsl:copy>
	</xsl:template>
  <xsl:template match="/MxPayMLResponse/sourceSystem">
				<sourceSystem>MX2.11</sourceSystem>
    </xsl:template>
  <xsl:template match="/MxPayMLResponse/message">
				<message>MX2.11 Acknowledged</message>
    </xsl:template>
  <xsl:template match="/MxPayMLResponse/event">
				<event>Released</event>
    </xsl:template>

</xsl:stylesheet>
```

### client.scb.fmrp.inbound.syncAck

Type:SQL

Data Source:  sql1.xml

```sql
begin
    update SCB_FMRP_DBF
    set M_RATAN_ID='MxCTX#ratanID#Mx', M_ACK_DATETIME=GETDATE()
    where M_FLOW_ID = MxCTX#murexID#Mx
    update TABLE#DATA#PAYFLOW_DBF
    set M_REASONS='MxCTX#ratanMsgType#Mx'+' ['+'MxCTX#ratanID#Mx'+'] ['+'MxCTX#ratanEvent#Mx'+']'
    where M_FLOW_ID = MxCTX#murexID#Mx
    select 'success'
end 
```

### client.scb.fmrp.inbound.syncRelease

Type:SQL

Data Source:  sql1.xml

```sql
begin
update SCB_FMRP_DBF
set M_STATUS='MATH',M_RATAN_NET_ID='MxCTX#ratanNetId#Mx',M_RLS_DATETIME= GETDATE()
where M_FLOW_ID = MxCTX#murexID#Mx
select 'success'
end    
```

### client.scb.fmrp.inbound.transformation

Type:XSLTREE

Data Source:  mlspayml.dtd

```sql
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
	<xsl:variable name="flow.id" select="normalize-space('Mx#client.scb.fmrp.datatype2#Mx')"></xsl:variable>
	<xsl:template match="MxPayMLResponse">
		<xsl:copy>
			<xsl:copy-of select="@*"></xsl:copy-of>
			<xsl:copy-of select="sourceSystem"></xsl:copy-of>
			<xsl:copy-of select="objectNature"></xsl:copy-of>
			<xsl:copy-of select="timestamp"></xsl:copy-of>
			<xsl:copy-of select="sourceID"></xsl:copy-of>
			<xsl:copy-of select="event"></xsl:copy-of>
			<xsl:copy-of select="result"></xsl:copy-of>
			<xsl:copy-of select="message"></xsl:copy-of>
			<MXG2000>
				<xsl:copy-of select="MXG2000/flowID[@id=$flow.id]"></xsl:copy-of>
			</MXG2000>
		</xsl:copy>
	</xsl:template>
</xsl:stylesheet>    
```

### client.scb.fmrp.action

Type:SQL

Data Source:  sql1.xml

```sql
select rtrim (M_ACTION) from MUREXDB.PAY_FLOW_DBF where M_FLOW_ID=MxCTX#FLOWID#Mx
```

### client.scb.fmrp.amendFlag

Type:XSL

Data Source:  MXPAYML.DTD

```sql
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

### client.scb.fmrp.Amount

Type:XSL

Data Source:  MXPAYML.DTD

```sql
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:mx="http://murex.com/xslt/common">
	<xsl:template match="/">
		<xsl:variable name="Amount">Mx#mx.pay.flow.amount#Mx</xsl:variable>

	
		<xsl:choose>
			<xsl:when test="$Amount = 0">Y</xsl:when>
			<xsl:otherwise>N</xsl:otherwise>
		</xsl:choose>

	</xsl:template>
</xsl:stylesheet>
```

### client.scb.fmrp.countCheck

Type:SQL

Data Source:  sql1.xml

```sql
select count(1) 
from SCB_FMRP_DBF
WHERE M_FLOW_ID=MxCTX#FLOW_ID#Mx
```

### client.scb.fmrp.cptCheck

Type:SQL

Data Source:  sql1.xml

```sql
select count(*) from MUREXDB.TRN_HDR_DBF T1,
MUREXDB.TABLE#DATA#DEALCURR_DBF U1,
MUREXDB.TABLE#DATA#DEALCRD_DBF U2,
MUREXDB.TABLE#DATA#DEALCOM_DBF U3,
MUREXDB.TABLE#DATA#DEALIRD_DBF U4,
MUREXDB.TABLE#DATA#DEALSCF_DBF U5
where 
T1.M_NB*=U1.M_NB
AND T1.M_NB*=U2.M_NB
AND T1.M_NB*=U3.M_NB
AND T1.M_NB*=U4.M_NB
AND T1.M_NB*=U5.M_NB
AND 'fmrp_test'= case T1.M_TRN_FMLY
when 'CURR' then U1.M_ADD_COMM
when 'CRD'  then U2.M_ADD_COMM
when 'COM'  then U3.M_ADD_COMM
when 'IRD'  then U4.M_ADD_COMM
when 'SCF'  then U5.M_ADD_COMM
end 
AND T1.M_NB = MxCTX#tradeid#Mx
```

### client.scb.fmrp.currency

Type:XSL

Data Source:  MxPayML.dtd

```sql
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
	<xsl:template match="/">
		<xsl:value-of select="MxPayML/currency" />
	</xsl:template>
</xsl:stylesheet>
```

### client.scb.fmrp.datatype2

Type:XMLF

Data Source:  MxPayML.dtd

```sql
<Operand Code="ScalarField">STPDOC_DATA_TYPE2</Operand>
```

### client.scb.fmrp.ExtSettleRouter

Type:XSL

Data Source:  MxPayML.dtd

```sql
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

### client.scb.fmrp.fmrpEnrich

Type:XSLTREE

Data Source:  MxPayML.dtd

XSL Parameter:

counterparty FORMULA mx.pay.flow.counterparty

trnNum FORMULA mx.pay.trade.iD

```sql
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
		<xsl:variable name="flowID">Mx#mx.pay.flow.iD#Mx</xsl:variable>
	  <xsl:variable name="lastMKT" select="mx:execute-formula( 'client.scb.fmrp.lastMKT', concat( 'NB:', $trnNum ) )"></xsl:variable>
		<xsl:variable name="parentID">Mx#client.scb.fmrp.PIDandOIDMatrix(0,0)#Mx</xsl:variable>
		<xsl:variable name="orginalID">Mx#client.scb.fmrp.PIDandOIDMatrix(0,1)#Mx</xsl:variable>
 		<xsl:variable name="sysDate">Mx#client.scb.fmrp.sysDate#Mx</xsl:variable>
 		<xsl:variable name="refList" select="mx:execute-formula( 'client.scb.fmrp.getPayRefList' , concat( 'tradeRef:', $trnNum ))"></xsl:variable> 
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
								<!-- -->
                <xsl:element name="mxSystemDate">
                    <xsl:value-of select="$sysDate"></xsl:value-of>
                </xsl:element>
								<xsl:element name="action">
                    <xsl:value-of select="mx:execute-formula( 'client.scb.fmrp.action', concat( 'FLOWID:', $flowID ) )"></xsl:value-of>
                </xsl:element>
								<xsl:element name="tradeLastMKT">
										<xsl:choose>
											<xsl:when test="$lastMKT =1">
											<xsl:text>EXR</xsl:text>
											</xsl:when>
											<xsl:when test="$lastMKT =2">
											<xsl:text>EXP</xsl:text>
											</xsl:when>
											<xsl:when test="$lastMKT =3">
											<xsl:text>XIT</xsl:text>
											</xsl:when>
											<xsl:when test="$lastMKT =4">
											<xsl:text>NET</xsl:text>
											</xsl:when>
											<xsl:when test="$lastMKT =5">
											<xsl:text>RPL</xsl:text>
											</xsl:when>
											<xsl:when test="$lastMKT =6">
											<xsl:text>RPL_M</xsl:text>
											</xsl:when>
											<xsl:when test="$lastMKT =7">
											<xsl:text>RPL_D</xsl:text>
											</xsl:when>
											<xsl:otherwise></xsl:otherwise>
										</xsl:choose>
                </xsl:element>
 								<xsl:element name="TrnParentID">
                    <xsl:value-of select="$parentID"></xsl:value-of>
                </xsl:element>
                <xsl:element name="TrnOrginalID">
                    <xsl:value-of select="$orginalID"></xsl:value-of>
                </xsl:element>
            		 <xsl:element name="Flows">
                      <xsl:for-each select="$refList/row/cell[1]">
                        <xsl:element name="flow">
                            <xsl:value-of select="."></xsl:value-of>
                        </xsl:element>
                      </xsl:for-each>
                </xsl:element>
            </xsl:element>
        </xsl:copy>
    </xsl:template>
</xsl:stylesheet>
```

### client.scb.fmrp.fmrpEntityCheck

Type:SQL

Data Source:  sql1.xml

```sql
select count(1) 
from FMRP_ENTITY_DBF
where M_ENTITY = 'MxCTX#entity#Mx'
```

### client.scb.fmrp.fmrpPrecioiusMetalCheck

Type:SQL

Data Source:  sql1.xml

```sql
SELECT COUNT(*) FROM MUREXDB.TRN_HDR_DBF HDR,MUREXDB.TABLE#DATA#CURRENCY_DBF CCY1,MUREXDB.TABLE#DATA#CURRENCY_DBF CCY2,MUREXDB.TABLE#DATA#CURRENCY_DBF CCY3,MUREXDB.TABLE#DATA#CURRENCY_DBF CCY4,MUREXDB.TABLE#DATA#CURRENCY_DBF CCY5
WHERE HDR.M_BRW_NOMU1*=CCY1.M_LABEL
AND   HDR.M_BRW_NOMU2*=CCY2.M_LABEL
AND   HDR.M_BRW_ODNC0*=CCY3.M_LABEL
AND   HDR.M_BRW_ODNC1*=CCY4.M_LABEL
AND   substring(HDR.M_INSTRUMENT,1,3) *=CCY5.M_LABEL
AND   (CCY1.M_BUL_CUR_FL='Y' OR CCY2.M_BUL_CUR_FL='Y' OR CCY3.M_BUL_CUR_FL='Y' OR CCY4.M_BUL_CUR_FL='Y' OR CCY5.M_BUL_CUR_FL='Y')
AND   HDR.M_NB = MxCTX#trnID#Mx
```

### client.scb.fmrp.fxdSuppriseCheck

Type:SQL

Data Source:  sql1.xml

```sql
			select count(*) from MUREXDB.PAY_FLOW_DBF T1, MUREXDB.TABLE#DATA#COUNTERP_DBF T2
			where T2.M_LABEL = T1.M_CNTRP
			and (T1.M_TRN_GRP<>'FXD'
			or (
				T1.M_TRN_GRP='FXD' and(
					T1.M_STRATEGY='FEDSVALIDATOR' or (T1.M_STRATEGY='FX_DCD' and T2.M_CLASSIFY<>'INTERNAL') or T1.M_TYPOLOGY IN('NDF','NDS Fixing') or T1.M_CNTRP LIKE 'INTL/%'
					)
				)
			)
			AND T1.M_FLOW_ID=MxCTX#FLOWID#Mx
```

### client.scb.fmrp.fxdSupprission

Type:XSL

Data Source:  mxpayml.dtd

```sql
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:mx="http://murex.com/xslt/common">
	<xsl:template match="/">
		<xsl:variable name="flowID">Mx#mx.pay.flow.iD#Mx</xsl:variable>
		<xsl:variable name="isFXDSupp">
			<xsl:value-of select="mx:execute-formula( 'client.scb.fmrp.fxdSuppriseCheck', concat( 'FLOWID:', $flowID ) )"></xsl:value-of>
		</xsl:variable>
	
		<xsl:choose>
			<xsl:when test="$isFXDSupp = 0">Y</xsl:when>
			<xsl:otherwise>N</xsl:otherwise>
		</xsl:choose>

	</xsl:template>
</xsl:stylesheet>
```

### client.scb.fmrp.getLEIDandSCIID

Type:SQL

Data Source:  sql1.xml

```sql
select rtrim(M_ATLAS_LEID ) 'LEID', rtrim(M_SCI_ID) 'SCIID'
from    TABLE#DATA#COUNTERP_DBF c,
            TABLE#DATA#ENTITY_DBF e 
where  c.M_LABEL = e.M_CTP_COD
and e.M_LABEL = 'MxCTX#NAME#Mx'
```

### client.scb.fmrp.getPayRefList

Type:SQL

Data Source:  sql1.xml

```sql
SELECT  'Flowid:'+convert(varchar(10), M_FLOW_ID)+', status:'+M_STATUS+', value_date:'+convert(varchar(10), M_VALUE_DATE,112) , '1'
FROM MUREXDB.PAY_FLOW_DBF
WHERE M_TRN_REF=MxCTX#tradeRef#Mx
```

### client.scb.fmrp.getPIDandOID

Type:SQL

Data Source:  sql1.xml

```sql
select convert(varchar(10), M_CREATOR) ,convert(varchar(10), CASE WHEN M_MRPL_ONB<1 THEN M_NB ELSE M_MRPL_ONB END) 
from MUREXDB.TRN_HDR_DBF
where M_NB=MxCTX#NB#Mx
```

### client.scb.fmrp.initCheck

Type:SQL

Data Source:  sql1.xml

```sql
select count(1) 
from SCB_FMRP_DBF
WHERE M_STATUS='MxCTX#STATUS#Mx'
and   M_FLOW_ID=MxCTX#FLOW_ID#Mx
```

### client.scb.fmrp.insertPay

Type:SQL

Data Source:  sql1.xml

```sql
begin   
insert into  MUREXDB.SCB_FMRP_DBF(M_FLOW_ID,M_STATUS,M_RATAN_ID,M_RATAN_NET_ID,M_INS_DATETIME)
values (MxCTX#FLOW_ID#Mx ,'SENT','0','0', GETDATE())
select 'out[STPDOC_DATA_TYPE2=publish]'
end
```

### client.scb.fmrp.insertTimer

Type:XMLF

Data Source:

```sql
<!-- 10 sec -->
<Operand Code="ScalarDouble">10000</Operand>
```

### client.scb.fmrp.isCompleteFlowCheck

Type:SQL

Data Source:  sql1.xml

```sql
select count(*) from MUREXDB.PAY_FLOW_DBF PAY,  MUREXDB.TRN_HDR_DBF HDR
where HDR.M_NB=PAY.M_TRN_ID
AND PAY.M_FLOW_ID= MxCTX#flowID#Mx
```

### client.scb.fmrp.isCPT

Type:XSL

Data Source:  mxpayml.dtd

```sql
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:mx="http://murex.com/xslt/common">
	<xsl:template match="/">
		<xsl:variable name="tradeid">Mx#client.scb.fmrp.tradeid#Mx</xsl:variable>
		<xsl:variable name="isCPTeligible">
			<xsl:value-of select="mx:execute-formula( 'client.scb.fmrp.cptCheck', concat( 'tradeid:', $tradeid ) )"></xsl:value-of>
		</xsl:variable>
		<xsl:choose>
			<xsl:when test="$isCPTeligible = 0">Y</xsl:when>
			<xsl:otherwise>N</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
</xsl:stylesheet>
```

### client.scb.fmrp.isFmrpEntity

Type:XSL

Data Source:  mxpayml.dtd

```sql
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

### client.scb.fmrp.isNDCurrency

Type:XSL

Data Source:  mxpayml.dtd

```sql
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:mx="http://murex.com/xslt/common">
	<xsl:template match="/">
		<xsl:variable name="ccy">Mx#client.scb.fmrp.currency#Mx</xsl:variable>
		<xsl:variable name="isNonDeliverableCurr">
			<xsl:value-of select="mx:execute-formula( 'client.scb.fmrp.ndCurrencyCheck', concat( 'ccy:', $ccy ) )"></xsl:value-of>
		</xsl:variable>
	
		<xsl:choose>
			<xsl:when test="$isNonDeliverableCurr > 0">Y</xsl:when>
			<xsl:otherwise>N</xsl:otherwise>
		</xsl:choose>

	</xsl:template>
</xsl:stylesheet>
```

### client.scb.fmrp.isPreciousMetalDealFlow

Type:XSL

Data Source:  mxpayml.dtd

```sql
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:mx="http://murex.com/xslt/common">
	<xsl:template match="/">
		<xsl:variable name="trnID" select="/MxPayML/transactionID"></xsl:variable>
		<xsl:variable name="isPreciousMetalDealFlow">
			<xsl:value-of select="mx:execute-formula( 'client.scb.fmrp.fmrpPrecioiusMetalCheck', concat( 'trnID:', $trnID ) )"></xsl:value-of>
		</xsl:variable>
	
		<xsl:choose>
			<xsl:when test="$isPreciousMetalDealFlow > 0">Y</xsl:when>
			<xsl:otherwise>N</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
</xsl:stylesheet>


```

### client.scb.fmrp.lastMKT

Type:SQL

Data Source:  sql1.ml

```sql
SELECT CASE WHEN M_MOP_LAST > 0 THEN M_MOP_LAST ELSE  M_MOP_CREAT END AS 'M_MOP'
FROM MUREXDB.TRN_HDR_DBF
WHERE M_NB=MxCTX#NB#Mx
```

### client.scb.fmrp.LEIDandSCIIDMatrix

Type:XMLF

Data Source:  MXPAYML.DTD

```sql
<Operand Code="Matrix">Mx#client.scb.fmrp.getLEIDandSCIID{NAME:Contexts.entity}#Mx</Operand>
```

### client.scb.fmrp.ndCurrencyCheck

Type:SQL

Data Source:  [sql1.ml](http://sql1.ml)

```sql
select count(1) 
from MUREXDB.TABLE#DATA#CURRENCY_DBF
where M_LABEL = 'MxCTX#ccy#Mx'
AND M_NDF_CCY='Y'
```

### client.scb.fmrp.PIDandOIDMatrix

Type:XMLF

Data Source:  MXPAYML.DTD

```sql
<Operand Code="Matrix">Mx#client.scb.fmrp.getPIDandOID{NB:Contexts.nb}#Mx</Operand>
```

### client.scb.fmrp.portBizUnit

Type:SQL

Data Source:  [sql1.ml](http://sql1.ml)

```sql
select top 1 rtrim(M_BIZ_UNIT) from TABLE#DATA#PORTFOLI_DBF WHERE M_LABEL ='Mx#client.scb.pay.flow.portfolio#Mx'
```

### client.scb.fmrp.retryCheck

Type:XMLF

Data Source:  MXPAYML.DTD

```sql
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
			<Operand Code="ScalarDouble">5.0</Operand>
		</Operator>
	</Operator>
	<Operator Code="If">
		<Operator Code="Equal">
			<Operand Code="ScalarField">STPDOC_ACTION</Operand>
			<Operand Code="ScalarString">ACK_ALLEGE</Operand>
		</Operator>
		<Operand Code="ScalarString">retry2[STPDOC_DATA_TYPE3=Mx#client.scb.fmrp.retryCnt#Mx]</Operand>
		<Operand Code="ScalarString">retry1[STPDOC_DATA_TYPE3=Mx#client.scb.fmrp.retryCnt#Mx]</Operand>
	</Operator>
	<Operand Code="ScalarString">stop</Operand>
</Operator>
```

### client.scb.fmrp.retryTimer

Type:XMLF

Data Source:

```sql
<!-- 2 min -->
<Operand Code="ScalarDouble">120000</Operand>
```

### client.scb.fmrp.sendCancel

Type:SQL

Data Source: sql1.xml

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

### client.scb.fmrp.SyncPub

Type:XSL

Data Source: mxpayml.dtd

```sql
<xsl:stylesheet version="1.0" extension-element-prefixes="mx" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:mx="http://murex.com/xslt/common">
			<xsl:template match="/">
      	<!--***variable declare starts-->
      	<xsl:variable name="flowID" select="/MxPayML/flowID">	</xsl:variable>		 
        <xsl:value-of select="mx:execute-formula('client.scb.fmrp.updatePubDate',concat( 'FLOW_ID:', $flowID) )"></xsl:value-of>
    </xsl:template>
</xsl:stylesheet>
```

### client.scb.fmrp.SyncStatus

Type:XSL

Data Source: mxpayml.dtd

```sql
<xsl:stylesheet version="1.0" extension-element-prefixes="mx" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:mx="http://murex.com/xslt/common">
    <xsl:template match="/">
 
        <!--***variable declare starts-->
        <xsl:variable name="flowID" select="/MxPayML/flowID"></xsl:variable>
        <xsl:variable name="cparty" select="/MxPayML/counterparty"></xsl:variable>
        <xsl:variable name="action" select="/MxPayML/action"></xsl:variable>
        <xsl:variable name="destinationStatus" select="/MxPayML/destinationStatus"></xsl:variable>
        <xsl:variable name="flowStatus" select="/MxPayML/flowStatus"></xsl:variable>

        <xsl:variable name="initCheck">
            <xsl:value-of select="mx:execute-formula('client.scb.fmrp.initCheck',concat( 'FLOW_ID:', $flowID,',STATUS:', 'INIT') )"></xsl:value-of>
        </xsl:variable>

        <xsl:variable name="sentCheck">
            <xsl:value-of select="mx:execute-formula('client.scb.fmrp.initCheck',concat( 'FLOW_ID:', $flowID,',STATUS:', 'SENT') )"></xsl:value-of>
        </xsl:variable>

        <xsl:variable name="cancelCheck">
            <xsl:value-of select="mx:execute-formula('client.scb.fmrp.initCheck',concat( 'FLOW_ID:', $flowID,',STATUS:', 'CANC') )"></xsl:value-of>
        </xsl:variable>

        <xsl:variable name="countCheck">
            <xsl:value-of select="mx:execute-formula('client.scb.fmrp.countCheck',concat( 'FLOW_ID:', $flowID) )"></xsl:value-of>
        </xsl:variable>

        <xsl:choose>

            <!--FAIS:controlm job auto INIT-SNTR  
                I2SR: Data publisher realtime INIT-SNTR, below works when realtime and regular run concurrently and regular job inserted data in staging table
                FMIS: Manual queue move status INIT-SNTR       -->
            <xsl:when test="($action='FAIS' or $action='I2SR' or $action='FMIS') and $initCheck=1">
                <xsl:value-of select="mx:execute-formula('client.scb.fmrp.updateFmrpPay',concat( 'FLOW_ID:',  $flowID,',STATUS:', 'INIT') )"></xsl:value-of>
            </xsl:when>
 
            <!--FMSI: Manual queue move back status SNTR-INIT, this is for user/pss replaying cashflow to Ratan, Note FMSI message dont flow to Ratan, just change status-->
            <xsl:when test="$action='FMSI' and $sentCheck=1">
                <xsl:value-of select="mx:execute-formula('client.scb.fmrp.sendCancel',concat( 'FLOW_ID:', $flowID) )"></xsl:value-of>
            </xsl:when>
 
            <!--FMIS: Manual queue move status INIT-SNTR, this specially for replay process, FMIS produce replayed message and flow to Ratan -->
            <xsl:when test="$action='FMIS'and $cancelCheck=1">
                <xsl:value-of select="mx:execute-formula('client.scb.fmrp.updateFmrpPay',concat( 'FLOW_ID:',  $flowID,',STATUS:', 'CANC') )"></xsl:value-of>
            </xsl:when>
 
            <!--FMIS: Manual queue move status INIT-SNTR, this is for normal manual send to ratan. I2SR: Data publisher realtime INIT-SNTR-->
            <xsl:when test="($action='FMIS' or $action='I2SR') and $countCheck=0">
                <xsl:value-of select="mx:execute-formula('client.scb.fmrp.insertPay',concat( 'FLOW_ID:', $flowID) )"></xsl:value-of>
            </xsl:when>
 
            <xsl:otherwise>discard</xsl:otherwise>
        </xsl:choose>
    </xsl:template>
</xsl:stylesheet>
```

### client.scb.fmrp.sysDate

Type:SQL

Data Source: sql1.xml

```sql
SELECT M_DATE FROM MUREXDB.TRN_PC_DBF
```

### client.scb.fmrp.timeStamp

Type:SQL

Data Source: sql1.xml

```sql
select rtrim(convert(CHAR,getdate(),105)) + ' ' + rtrim(convert(CHAR,getdate(),20))
```

### client.scb.fmrp.tradeid

Type:XSL

Data Source: mxpayml.dtd

```sql
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
	<xsl:template match="/">
		<xsl:value-of select="MxPayML/transactionID" />
	</xsl:template>
</xsl:stylesheet>
```

### client.scb.fmrp.tradeMktOpRecord

Type:SQL

Data Source: sql1.xml

```sql
select count(1) 
 from MKT_OP_DBF 
where M_DEST_NB=MxCTX#tradeRef#Mx and (M_TYPE='RPL' or M_TYPE='RPL_M') and M_SYS_DATE = 'MxCTX#sysDate#Mx'
```

### client.scb.fmrp.tradePaymentCheck

Type:XSL

Data Source: mxpayml.dtd

```sql
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:mx="http://murex.com/xslt/common">
	<xsl:template match="/">
		<xsl:variable name="flowID" select="/MxPayML/flowID"></xsl:variable>
		<xsl:variable name="isCompleteFlow">
			<xsl:value-of select="mx:execute-formula( 'client.scb.fmrp.isCompleteFlowCheck', concat( 'flowID:', $flowID ) )"></xsl:value-of>
		</xsl:variable>
	
		<xsl:choose>
			<xsl:when test="$isCompleteFlow > 0">Y</xsl:when>
			<xsl:otherwise>N</xsl:otherwise>
		</xsl:choose>

	</xsl:template>
</xsl:stylesheet>
```

### client.scb.fmrp.trader

Type:SQL

Data Source: sql1.xml

```sql
select CASE WHEN M_COMMENT_BS = 'B' THEN rtrim(M_BTRADER) ELSE rtrim(M_STRADER) END from TRN_HDR_DBF WHERE M_NB=Mx#client.scb.pay.trade.tradeid#Mx
```

### client.scb.fmrp.traderPSID

Type:SQL

Data Source: sql1.xml

```sql
select top 1 rtrim(M_L_CODE)  from TRN_USRD_DBF WHERE M_LABEL ='Mx#client.scb.fmrp.trader#Mx'
```

### client.scb.fmrp.updateFmrpPay

Type:SQL

Data Source: sql1.xml

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

### client.scb.fmrp.updatePubDate

Type:SQL

Data Source: sql1.xml

```sql
begin
UPDATE  MUREXDB.SCB_FMRP_DBF
SET M_PUB_DATETIME=getdate()
WHERE M_FLOW_ID=MxCTX#FLOW_ID#Mx
select 'out'
end
```

### client.scb.mxmlexchange.pay.test.countXmlErrors - Modify

Modify

```xml
<!--MLS CPN netting starts-->
<Operator Code="If">
  <Operator Code="Equal">
    <Operand Code="ScalarString">Mx#client.scb.mls.cpnEligible#Mx</Operand>
    <Operand Code="ScalarString">Y</Operand>
  </Operator>
  <Operand Code="ScalarString">extSettle</Operand>
  <Operator Code="If">
    <Operator Code="Equal">
      <Operand Code="ScalarString">Mx#client.scb.pay.insertPay#Mx</Operand>
      <Operand Code="ScalarString">Y</Operand>
    </Operator>
    <Operand Code="ScalarString">insert</Operand>
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

### client.scb.pay.insertPay

Type:XSL

Data Source:mxpayml.dtd

```xml
<xsl:stylesheet version="1.0" extension-element-prefixes="mx"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:mx="http://murex.com/xslt/common">
  <xsl:template match="/">

    <xsl:variable name="event">Mx#client.scb.pay.event#Mx</xsl:variable>
    <xsl:variable name="portfolio">Mx#client.scb.pay.flow.portfolio#Mx</xsl:variable>
    <xsl:variable name="fmrpEntity">
      <xsl:value-of select="mx:execute-formula( 'client.scb.fmrp.fmrpPortfolioCheck', concat( 'portfolio:', $portfolio ) )"></xsl:value-of>
    </xsl:variable>


    <xsl:choose>
      <xsl:when test=" $event='Insert' and $fmrpEntity > 0">Y</xsl:when>
      <xsl:otherwise>N</xsl:otherwise>
    </xsl:choose>
  </xsl:template>
</xsl:stylesheet>
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

### client.scb.pay.trade.tradeRef

Type:XSL

Data Source:MXPAYML.DTD

```sql
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:template match="/">
        <xsl:value-of select="format-number( MxPayML/transactionID, '0' )" />
    </xsl:template>
</xsl:stylesheet>
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

![image2023-1-16_0-30-4.png](attachments/image2023-1-16_0-30-4.png)

![image2023-9-15_14-58-54.png](attachments/image2023-9-15_14-58-54.png)

### FmrpPub

payment push time marker task

Router task

Task code:FmrpPub

Task Description: Sync the Message Publish time

Routing Fomula: client.scb.fmrp.SyncPub

![image2023-9-15_16-36-13.png](attachments/image2023-9-15_16-36-13.png)

### PayInsertionFilter

payment insertion filter task

Router task

Task code:PayInsertionFilte

Task Description: filter for payment insertion

Routing Fomula: client.scb.fmrp.inbound.payInsertionFilter

Node :

process

discard

retry

![image2023-1-16_0-38-15.png](attachments/image2023-1-16_0-38-15.png)

### INIT2SNTR

pay action task

Task code:INIT2SNTR

Task Description:INIT2SNTR

Workflow Type:Payment

Action:I2S

Filter Formula:[client.scb.pay.flow.id](http://client.scb.pay.flow.id)

![image2023-1-16_0-36-30.png](attachments/image2023-1-16_0-36-30.png)

two node:

Triggered

Error

![image2023-9-15_16-43-40.png](attachments/image2023-9-15_16-43-40.png)

### FmrpTimerTask

Timer Task

Task code:FmrpTimerTask

Task Description: Timer task for FMRP realtime insert payment.

Routing Fomula: client.scb.fmrp.insertTimer

![image2023-1-16_0-56-25.png](attachments/image2023-1-16_0-56-25.png)

### FmrpPurge

Purge task

Task Code:FmrpPurge

Task Description:FmrpPurge

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

![image2023-9-15_16-51-45.png](attachments/image2023-9-15_16-51-45.png)

### FmrpRetryTimer

Timer Task

Task code:FmrpTimerTask

Task Description: Timer setup for retry process

Routing Fomula: client.scb.fmrp.retryTimer

![image2023-1-16_0-42-30.png](attachments/image2023-1-16_0-42-30.png)

### FmrpRetryCheck

Router task

Task code:FmrpRetryCheck

Task Description:max retry times 3

Routing Fomula:client.scb.fmrp.retryCheck

Two node:

stop

retry

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

![image2023-9-15_16-55-39.png](attachments/image2023-9-15_16-55-39.png)

### FmrpInboundRouter

Router task

Task code:FmrpInboundRouter

Task Description:FmrpInboundRouter

Routing Fomula: [client.scb.fmrp.inbound.inboundRouter](https://confluence.global.standardchartered.com/display/DSP/CN+Settlement+-+Murex+2.11+workflow+change#CNSettlementMurex2.11workflowchange-client.scb.fmrp.inbound.inboundRouter)

Three node:

acked

released

discard

![image2023-9-15_16-59-55.png](attachments/image2023-9-15_16-59-55.png)

### FmrpAckProcessor

Router task

Task code:FmrpAckProcessor

Task Description:FmrpAckProcessor

Routing Fomula: client.scb.fmrp.inbound.processAck

![image2023-9-15_17-2-17.png](attachments/image2023-9-15_17-2-17.png)

### FlowEntrySpliter

spliter task

Task code:FlowEntrySpliter

Task Description:Splite the components to individual

Routing Formula: client.scb.fmrp.inbound.duplicator

Transformation Formula: client.scb.fmrp.inbound.transformation

![image2023-9-15_17-5-32.png](attachments/image2023-9-15_17-5-32.png)

![image2023-9-15_17-12-24.png](attachments/image2023-9-15_17-12-24.png)

### SNTR2RLSR

pay action task

Task code:SNTR2RLSR

Task Description:SNTR2RLSR

Workflow Type:Payment

Action:S2RR

Filter Formula:[client.](http://client.scb.pay.flow.id)scb.fmrp.inbound.payFlowID

![image2023-9-15_17-14-59.png](attachments/image2023-9-15_17-14-59.png)

two node:

Error

Triggered

![image2023-9-15_17-18-24.png](attachments/image2023-9-15_17-18-24.png)

### FmrpReleaseProcessor

Router task

Task code:FmrpReleaseProcessor

Task Description:FmrpReleaseProcessor

Routing Fomula: client.scb.fmrp.inbound.processRelease

![image2023-9-15_17-21-5.png](attachments/image2023-9-15_17-21-5.png)

### ReleaseAckEnrichment

Enrichment task

Task code:ReleaseAckEnrichment

Task Description:add extra tags into ReleaseAck Message

Routing Fomula: client.scb.fmrp.inbound.releasedEnrich

![image2023-9-15_17-24-6.png](attachments/image2023-9-15_17-24-6.png)

![image2023-9-15_17-25-58.png](attachments/image2023-9-15_17-25-58.png)

### FmrpOutboundMQ2

MQ Task

duplicate for FmrpOutboundMQ

# Payment workflow

![image2023-9-15_17-28-56.png](attachments/image2023-9-15_17-28-56.png)