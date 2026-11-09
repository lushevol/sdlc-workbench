import com.scb.auth.login.configuration.EntitlementMappingProperties;
import com.scb.auth.login.dto.Ems3DataEntitlementDto;
import com.scb.auth.login.entitlement.mapper.DefaultEms3EntitlementMapper;
import java.util.List;
import java.util.Map;

/**
 * Scenario AUTH-PROBE-001: Inspect mapping revision propagation.
 * Given a valid CES functional assignment and mapping revision ems3-v2
 * When the actual candidate mapper projects that assignment
 * Then capture the emitted revision and its role/action projection
 * And assert whether the configured revision reaches the projection.
 */
public class AuthMappingProbe {
    public static void main(String[] args) {
        var properties = new EntitlementMappingProperties();
        properties.setVersion("ems3-v2");
        properties.setRoleMappings(Map.of("COMMON", "ROLE_AFTER_CHANGE"));
        var dto = new Ems3DataEntitlementDto();
        var user = new Ems3DataEntitlementDto.UserData();
        user.setUserId("synthetic-review-user");
        dto.setUserData(user);
        var source = new Ems3DataEntitlementDto.Entitlements();
        source.setEntitlementName(List.of("COMMON"));
        var action = new Ems3DataEntitlementDto.RoleEntitlement();
        action.setFeature("TRADE");
        action.setAction("READ");
        source.setRoleEntitlements(List.of(action));
        dto.setEntitlements(source);
        var result = new DefaultEms3EntitlementMapper(properties).toUnified(dto, false);
        if (!"ROLE_AFTER_CHANGE".equals(result.role()) || !List.of("TRADE:READ").equals(result.actions())) {
            throw new AssertionError("Fixture failed to produce the changed mapping");
        }
        if (!"ems3-v1".equals(result.version())) {
            throw new AssertionError("Candidate behavior changed: recheck the version finding");
        }
        System.out.println("{\"case\":\"AUTH-PROBE-001\",\"configuredVersion\":\""
            + properties.getVersion() + "\",\"actualVersion\":\"" + result.version()
            + "\",\"role\":\"" + result.role() + "\",\"action\":\"TRADE:READ\","
            + "\"configuredVersionPropagated\":false,\"observedCandidateBehaviorAsserted\":true}");
    }
}
