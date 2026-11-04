package com.example.migration;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;
import org.springframework.mock.env.MockEnvironment;
import java.nio.file.Files;
import java.nio.file.Path;
import static org.junit.jupiter.api.Assertions.*;

class VerificationRunnerTest {
    @TempDir Path directory;

    @Test void incompletePopulationNeverGetsParityPercentage() {
        assertEquals("INCOMPLETE", VerificationRunner.verdict(3, 3, 3, false));
        assertNull(VerificationRunner.accountMetrics(3, 3, 3, false).get("sdkParityPercent"));
    }
    @Test void failedAcquisitionCannotPassTwoEmptyMaps() {
        assertEquals("INCOMPLETE", VerificationRunner.verdict(3, 2, 2, true));
        assertNull(VerificationRunner.accountMetrics(3, 2, 2, true).get("sdkParityPercent"));
    }
    @Test void differencesPreventPassAndFullScopedMatchCanPass() {
        assertEquals("DIFFERENCES", VerificationRunner.verdict(3, 3, 2, true));
        assertEquals("SCOPED_SDK_PARITY_PASS", VerificationRunner.verdict(3, 3, 3, true));
        assertEquals(100.0, VerificationRunner.accountMetrics(3, 3, 3, true).get("sdkParityPercent"));
    }
    @Test void emptyPopulationHasNoCoverageDenominator() {
        assertEquals("INCOMPLETE", VerificationRunner.verdict(0, 0, 0, true));
        assertNull(VerificationRunner.accountMetrics(0, 0, 0, true).get("sdkParityPercent"));
    }
    @Test void liveModeRequiresExplicitCompletenessAndSource() {
        MockEnvironment environment = new MockEnvironment();
        assertTrue(VerificationRunner.populationComplete(environment, "replay"));
        assertFalse(VerificationRunner.populationComplete(environment, "live"));
        environment.setProperty("verification.population-complete", "true");
        assertFalse(VerificationRunner.populationComplete(environment, "live"));
        environment.setProperty("verification.population-source", "retained-authoritative-inventory-revision");
        assertTrue(VerificationRunner.populationComplete(environment, "live"));
        environment.setProperty("verification.population-complete", "false");
        assertFalse(VerificationRunner.populationComplete(environment, "replay"));
    }
    @Test void rejectsDuplicateAndUnsafeAccountsInsteadOfChangingThePopulation() throws Exception {
        Path users = directory.resolve("users.csv");
        Files.writeString(users, "userId\nalice\nalice\n");
        assertThrows(IllegalArgumentException.class, () -> VerificationRunner.readUsers(users));
        Files.writeString(users, "userId\nalice/other\n");
        assertThrows(IllegalArgumentException.class, () -> VerificationRunner.readUsers(users));
        Files.writeString(users, "userId\n");
        assertThrows(IllegalArgumentException.class, () -> VerificationRunner.readUsers(users));
    }
}
