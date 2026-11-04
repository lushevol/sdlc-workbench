package com.example.migration;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.WebApplicationType;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class MigrationVerifierApplication {
    public static void main(String[] args) {
        SpringApplication application = new SpringApplication(MigrationVerifierApplication.class);
        application.setWebApplicationType(WebApplicationType.NONE);
        int exit;
        try (var context = application.run(args)) {
            exit = new VerificationRunner().run(context.getEnvironment());
        } catch (Exception error) {
            System.err.println("VERIFICATION_INCOMPLETE: startup or configuration failed; no credential values were retained.");
            exit = 2;
        }
        System.exit(exit);
    }
}
