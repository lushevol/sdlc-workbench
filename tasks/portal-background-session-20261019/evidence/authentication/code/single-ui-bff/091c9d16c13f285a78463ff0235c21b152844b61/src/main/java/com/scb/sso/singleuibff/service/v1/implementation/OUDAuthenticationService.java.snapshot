package com.scb.sso.singleuibff.service.v1.implementation;

import com.google.common.collect.Maps;
import com.scb.sso.singleuibff.config.OUDProperties;
import com.scb.sso.singleuibff.config.WhitelistedProperties;
import com.scb.sso.singleuibff.dto.request.RequestOfAuthenticate;
import com.scb.sso.singleuibff.exceptions.AuthenticationException;
import com.scb.sso.singleuibff.service.v1.AuthenticationService;
import com.scb.sso.singleuibff.util.OudUtil;
import lombok.AllArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.ldap.core.LdapTemplate;

import javax.naming.NamingException;
import javax.naming.directory.DirContext;
import java.util.List;
import java.util.Map;
import java.util.Objects;

import static com.scb.sso.singleuibff.util.Constant.OUD_RELATED_CODE;

@Slf4j
@AllArgsConstructor
public class OUDAuthenticationService implements AuthenticationService {

    private final LdapTemplate ldapTemplate;
    private WhitelistedProperties whitelistedProperties;
    private OUDProperties oudProperties;
    private OudUtil oudUtil;

    @Override
    public Map<String, String> authenticate(RequestOfAuthenticate requestOfAuthenticate) throws AuthenticationException {
        DirContext dirContext = null;
        Map<String, String> userInfo;
        try {
            List<String> ids = whitelistedProperties.getIdList();
            List<String> envs = whitelistedProperties.getEnvList();
            log.info("requestOfAuthenticate.getHostName(): {}", requestOfAuthenticate.getHostName());
            if (Objects.nonNull(envs) && !envs.isEmpty() &&
                Objects.nonNull(ids) && !ids.isEmpty() &&
                Objects.nonNull(requestOfAuthenticate.getHostName())
                && envs.contains(requestOfAuthenticate.getHostName())
                && ids.contains(requestOfAuthenticate.getUsername())) {
                userInfo = getUserInfo(requestOfAuthenticate.getUsername());
            } else {
                String USER_PREFIX = "cn=";
                String USER_SUFFIX = ",ou=users,o=standardchartered";
                String userDn = USER_PREFIX.concat(requestOfAuthenticate.getUsername()).concat(USER_SUFFIX);
                dirContext = ldapTemplate.getContextSource().getContext(userDn, requestOfAuthenticate.getPassword());
                userInfo = oudUtil.getOudData(dirContext.getAttributes(userDn));
            }
        } catch (Exception e) {
            log.error("OUD authenticate failed, user: {}, e", requestOfAuthenticate.getUsername(), e.getMessage());
            throw AuthenticationException.builder().code(OUD_RELATED_CODE)
                .message("Invalid username and password combination.")
                .build();
        } finally {
            closeContext(dirContext);
        }
        return userInfo;
    }

    private void closeContext(DirContext dirContext) {
        if (dirContext != null) {
            try {
                dirContext.close();
            } catch (NamingException e) {
                log.info("Exception occurred while closing context, e:", e);
            }
        }
    }

    public Map<String, String> getUserInfo(String bankId) {
        Map<String, String> userInfo = Maps.newHashMap();
        DirContext dirContext = null;
        try {
            String USER_PREFIX = "cn=";
            String USER_SUFFIX = ",ou=users,o=standardchartered";
            String userDn = USER_PREFIX.concat(oudProperties.getUn()).concat(USER_SUFFIX);
            String userText = oudUtil.getEncode(oudProperties.getPw(), oudProperties.getId());
            dirContext = ldapTemplate.getContextSource().getContext(userDn, userText);
            userDn = USER_PREFIX.concat(bankId).concat(USER_SUFFIX);
            userInfo = oudUtil.getOudData(dirContext.getAttributes(userDn));
        } catch (Exception e) {
            log.info("Exception getUserInfo, user: {}, e:", bankId, e);
        } finally {
            closeContext(dirContext);
        }
        return userInfo;
    }

}
