<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

  <xsl:output method="html" indent="yes" />

  <xsl:template match="/">
    <html>
      <head>
        <meta charset="utf-8"/>
        <title>CANdela CDD Overview</title>
        <style>
          body{font:14px system-ui;padding:16px;max-width:1200px;margin:0 auto}
          h1{color:#005CA2;border-bottom:2px solid #005CA2}
          h2{color:#0074CC;margin-top:24px}
          table{border-collapse:collapse;width:100%;margin:16px 0;box-shadow:0 2px 4px rgba(0,0,0,0.1)}
          th,td{border:1px solid #ddd;padding:8px;text-align:left;vertical-align:top}
          th{background:#f8f9fa;font-weight:600;color:#333}
          tr:nth-child(even){background:#f8f9fa}
          tr:hover{background:#e3f2fd}
          code{background:#f0f0f0;padding:2px 6px;border-radius:4px;font-family:monospace;font-size:13px}
          .sid{background:#e8f5e8;color:#2e7d32;font-weight:bold}
          .did{background:#fff3e0;color:#f57c00;font-weight:bold}
          .desc{max-width:300px;word-wrap:break-word}
          .center{text-align:center}
        </style>
      </head>
      <body>
        <h1>CANdela CDD Overview</h1>
        
        <p><strong>Document:</strong> <xsl:value-of select="//ECUDOC/@manufacturer"/> | 
           <strong>Version:</strong> <xsl:value-of select="//CANDELA/@dtdvers"/></p>

        <h2>UDS Diagnostic Services</h2>
        <p>Total Services: <strong><xsl:value-of select="count(//PROTOCOLSERVICE)"/></strong></p>
        <table>
          <tr>
            <th>SID</th>
            <th>Service Name</th>
            <th>Qualifier</th>
            <th>Func</th>
            <th>Phys</th>
            <th>Request</th>
            <th>Response</th>
          </tr>
          <xsl:for-each select="//PROTOCOLSERVICE">
            <tr>
              <td class="center">
                <!-- Extract SID from service name (e.g., "($10) DiagnosticSessionControl") -->
                <code class="sid">
                  <xsl:choose>
                    <xsl:when test="contains(NAME/TUV, '($')">
                      <xsl:value-of select="substring-before(substring-after(NAME/TUV, '($'), ')')"/>
                    </xsl:when>
                    <xsl:when test="REQ//CONSTCOMP[@spec='sid']">
                      <xsl:variable name="sidValue" select="REQ//CONSTCOMP[@spec='sid']/@v"/>
                      <xsl:choose>
                        <xsl:when test="$sidValue">0x<xsl:value-of select="format-number($sidValue, '00')"/></xsl:when>
                        <xsl:otherwise>N/A</xsl:otherwise>
                      </xsl:choose>
                    </xsl:when>
                    <xsl:otherwise>N/A</xsl:otherwise>
                  </xsl:choose>
                </code>
              </td>
              <td>
                <xsl:choose>
                  <xsl:when test="contains(NAME/TUV, ') ')">
                    <xsl:value-of select="substring-after(NAME/TUV, ') ')"/>
                  </xsl:when>
                  <xsl:otherwise>
                    <xsl:value-of select="NAME/TUV"/>
                  </xsl:otherwise>
                </xsl:choose>
              </td>
              <td><code><xsl:value-of select="QUAL"/></code></td>
              <td class="center">
                <xsl:choose>
                  <xsl:when test="@func='1'">✓</xsl:when>
                  <xsl:otherwise>✗</xsl:otherwise>
                </xsl:choose>
              </td>
              <td class="center">
                <xsl:choose>
                  <xsl:when test="@phys='1'">✓</xsl:when>
                  <xsl:otherwise>✗</xsl:otherwise>
                </xsl:choose>
              </td>
              <td><xsl:value-of select="REQ/QUAL"/></td>
              <td><xsl:value-of select="POS/QUAL"/></td>
            </tr>
          </xsl:for-each>
        </table>

        <h2>Data Identifiers (DIDs)</h2>
        <p>Total DIDs: <strong><xsl:value-of select="count(//DID)"/></strong></p>
        <table>
          <tr>
            <th>DID</th>
            <th>Name</th>
            <th>Qualifier</th>
            <th>Description</th>
          </tr>
          <xsl:for-each select="//DID">
            <xsl:sort select="@n" data-type="number"/>
            <tr>
              <td class="center">
                <code class="did">
                  <xsl:choose>
                    <xsl:when test="@n">
                      0x<xsl:value-of select="format-number(@n, 'X')"/>
                    </xsl:when>
                    <xsl:otherwise>N/A</xsl:otherwise>
                  </xsl:choose>
                </code>
              </td>
              <td><xsl:value-of select="NAME/TUV"/></td>
              <td><code><xsl:value-of select="QUAL"/></code></td>
              <td class="desc">
                <xsl:choose>
                  <xsl:when test="DESC/TUV">
                    <xsl:value-of select="substring(DESC/TUV, 1, 150)"/>
                    <xsl:if test="string-length(DESC/TUV) > 150">...</xsl:if>
                  </xsl:when>
                  <xsl:otherwise>-</xsl:otherwise>
                </xsl:choose>
              </td>
            </tr>
          </xsl:for-each>
        </table>

        <h2>Service Details</h2>
        <xsl:for-each select="//PROTOCOLSERVICE[position() &lt;= 10]">
          <h3>
            <xsl:choose>
              <xsl:when test="contains(NAME/TUV, ') ')">
                <xsl:value-of select="substring-after(NAME/TUV, ') ')"/>
              </xsl:when>
              <xsl:otherwise>
                <xsl:value-of select="NAME/TUV"/>
              </xsl:otherwise>
            </xsl:choose>
          </h3>
          <table style="width:60%">
            <tr><th>Property</th><th>Value</th></tr>
            <tr><td>Service ID</td><td>
              <code class="sid">
                <xsl:choose>
                  <xsl:when test="contains(NAME/TUV, '($')">
                    0x<xsl:value-of select="substring-before(substring-after(NAME/TUV, '($'), ')')"/>
                  </xsl:when>
                  <xsl:when test="REQ//CONSTCOMP[@spec='sid']">
                    0x<xsl:value-of select="format-number(REQ//CONSTCOMP[@spec='sid']/@v, '00')"/>
                  </xsl:when>
                  <xsl:otherwise>N/A</xsl:otherwise>
                </xsl:choose>
              </code>
            </td></tr>
            <tr><td>Functional Addressing</td><td>
              <xsl:choose>
                <xsl:when test="@func='1'">✓ Supported</xsl:when>
                <xsl:otherwise>✗ Not supported</xsl:otherwise>
              </xsl:choose>
            </td></tr>
            <tr><td>Physical Addressing</td><td>
              <xsl:choose>
                <xsl:when test="@phys='1'">✓ Supported</xsl:when>
                <xsl:otherwise>✗ Not supported</xsl:otherwise>
              </xsl:choose>
            </td></tr>
            <tr><td>Multiple Responses</td><td>
              <xsl:choose>
                <xsl:when test="@mresp='1'">✓ Supported</xsl:when>
                <xsl:otherwise>✗ Not supported</xsl:otherwise>
              </xsl:choose>
            </td></tr>
            <tr><td>Request Structure</td><td><code><xsl:value-of select="REQ/QUAL"/></code></td></tr>
            <tr><td>Response Structure</td><td><code><xsl:value-of select="POS/QUAL"/></code></td></tr>
          </table>
        </xsl:for-each>

        <hr style="margin-top:40px"/>
        <p style="text-align:center;color:#666;font-size:12px">
          Generated from CANdela CDD file | <xsl:value-of select="count(//PROTOCOLSERVICE)"/> Services | 
          <xsl:value-of select="count(//DID)"/> DIDs
        </p>

      </body>
    </html>
  </xsl:template>
</xsl:stylesheet>