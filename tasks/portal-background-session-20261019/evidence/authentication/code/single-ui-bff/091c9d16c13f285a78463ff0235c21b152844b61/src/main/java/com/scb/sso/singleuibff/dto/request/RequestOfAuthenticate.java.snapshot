package com.scb.sso.singleuibff.dto.request;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;

import java.util.List;

@Data
public class RequestOfAuthenticate {

    private String username;
    private String password;
    private String code;
    private String iss;
    @JsonProperty("client_id")
    private String clientId;
    private String hostName;
    private List<String> entities;

}
