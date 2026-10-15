package com.scb.sso.singleuibff.util;

import com.google.common.collect.Maps;
import com.scb.sso.singleuibff.config.WhitelistedProperties;
import jakarta.servlet.http.HttpServletRequest;
import lombok.AllArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.jasypt.properties.PropertyValueEncryptionUtils;
import org.jasypt.util.text.BasicTextEncryptor;

import javax.naming.NamingEnumeration;
import javax.naming.directory.Attribute;
import javax.naming.directory.Attributes;
import java.util.List;
import java.util.Map;
import java.util.Objects;

import static com.scb.sso.singleuibff.util.Constant.*;

@Slf4j
@AllArgsConstructor
public class OudUtil {

    private WhitelistedProperties whitelistedProperties;
    private BasicTextEncryptor encryptor;

    public Map<String, String> getOudData(Attributes attributes) {
        Map<String, String> userInfo = Maps.newHashMap();
        List<String> attrList = whitelistedProperties.getAttrList();
        try {
            for (NamingEnumeration<? extends Attribute> ae = attributes.getAll(); ae != null & ae.hasMoreElements();) {
                Attribute attribute = (Attribute) ae.next();
                NamingEnumeration e = attribute.getAll();
                while (e.hasMore()) {
                    String attributeValue = e.next().toString();
                    if (Objects.nonNull(attrList) && !attrList.isEmpty() && attrList.contains(attribute.getID())) {
                        String key = attribute.getID();
                        if (attribute.getID().equalsIgnoreCase("co")) {
                            key = "country";
                        } else if (attribute.getID().equalsIgnoreCase("givenName")) {
                            key = "firstName";
                        } else if (attribute.getID().equalsIgnoreCase("sn")) {
                            key = "lastName";
                        } else if (attribute.getID().equalsIgnoreCase("uid")) {
                            key = "userId";
                        } else if (attribute.getID().equalsIgnoreCase("mail")) {
                            key = "emailId";
                        } else if (attribute.getID().equalsIgnoreCase("preferredLocale")) {
                            key = "locale";
                        }
                        userInfo.put(key, attributeValue);
                    }
                }
            }
        } catch (Exception e) {
            log.error("Exception getOudDate, e:", e);
        }
        return userInfo;
    }

    public String getIp(HttpServletRequest request) {
        String ip = request.getHeader(X_REAL_IP);
        if (Objects.isNull(ip)) {
            ip = request.getHeader(X_FORWARD_IP);
        }
        if (Objects.isNull(ip)) {
            ip = request.getRemoteAddr();
        }
        return ip;
    }

    public String getEncode(String text, String id) {
        try {
            return PropertyValueEncryptionUtils.decrypt(text, encryptor);
        } catch (Exception e) {
            encryptor.setPassword(id);
            return PropertyValueEncryptionUtils.decrypt(text, encryptor);
        }
    }

}
