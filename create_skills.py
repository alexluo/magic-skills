#!/usr/bin/env python3
"""Batch create all skills for Magic Skills."""

import os
import yaml

# Define all skills for 6 domains
skills_config = {
    "java-backend": [
        ("spring-boot-controller-gen", "Generate Spring Boot REST Controller code", "code-generation"),
        ("spring-boot-service-gen", "Generate Spring Boot Service layer code", "code-generation"),
        ("spring-boot-dao-gen", "Generate DAO/Repository layer code", "code-generation"),
        ("jpa-entity-gen", "Generate JPA Entity classes", "code-generation"),
        ("rest-api-doc-gen", "Generate REST API documentation", "code-generation"),
        ("swagger-model-gen", "Generate Swagger models", "code-generation"),
        ("dto-gen", "Generate DTO/VO classes", "code-generation"),
        ("code-review-java", "Review Java code for quality issues", "code-analysis"),
        ("performance-analyzer", "Analyze code performance", "code-analysis"),
        ("security-checker", "Check for security vulnerabilities", "code-analysis"),
        ("code-complexity", "Analyze code complexity metrics", "code-analysis"),
        ("dependency-analyzer", "Analyze project dependencies", "code-analysis"),
        ("spring-best-practices", "Check Spring best practices", "code-analysis"),
        ("spring-config-gen", "Generate Spring configuration", "config-generation"),
        ("docker-compose-gen", "Generate Docker Compose files", "config-generation"),
        ("k8s-deployment-gen", "Generate Kubernetes deployment files", "config-generation"),
        ("application-yml-gen", "Generate application.yml", "config-generation"),
        ("logback-config-gen", "Generate Logback configuration", "config-generation"),
        ("junit-test-gen", "Generate JUnit tests", "testing"),
        ("mockito-test-gen", "Generate Mockito tests", "testing"),
        ("integration-test-gen", "Generate integration tests", "testing"),
        ("api-test-gen", "Generate API tests", "testing"),
        ("performance-test-plan", "Generate performance test plans", "testing"),
        ("code-comment-gen", "Generate code comments", "documentation"),
        ("api-documentation", "Generate API documentation", "documentation"),
        ("architecture-doc", "Generate architecture documentation", "documentation"),
        ("deployment-guide", "Generate deployment guide", "documentation"),
        ("legacy-code-refactor", "Refactor legacy code", "refactoring"),
        ("design-pattern-apply", "Apply design patterns", "refactoring"),
        ("code-split-extract", "Split and extract code", "refactoring"),
    ],
    "android-os": [
        ("hal-interface-gen", "Generate HAL interface definitions", "code-generation"),
        ("binder-stub-gen", "Generate Binder stub code", "code-generation"),
        ("aidl-interface-gen", "Generate AIDL interfaces", "code-generation"),
        ("native-lib-gen", "Generate native library code", "code-generation"),
        ("android-service-gen", "Generate Android system service", "code-generation"),
        ("android-architecture-analyze", "Analyze Android architecture", "code-analysis"),
        ("Android.bp-gen", "Generate Android.bp build files", "build-system"),
        ("Android.mk-gen", "Generate Android.mk build files", "build-system"),
        ("driver-template-gen", "Generate driver templates", "driver-development"),
        ("kernel-module-gen", "Generate kernel module code", "driver-development"),
        ("device-tree-gen", "Generate device tree configurations", "driver-development"),
        ("selinux-policy-gen", "Generate SELinux policies", "security"),
        ("init-rc-gen", "Generate init.rc scripts", "system-configuration"),
        ("property-config-gen", "Generate property configurations", "system-configuration"),
        ("log-analysis-android", "Analyze Android logs", "debugging"),
        ("crash-analysis-native", "Analyze native crashes", "debugging"),
        ("anr-analysis", "Analyze ANR issues", "debugging"),
        ("memory-leak-detector", "Detect memory leaks", "debugging"),
        ("power-consumption-analyze", "Analyze power consumption", "performance"),
        ("boot-time-optimize", "Optimize boot time", "performance"),
        ("sysprop-config-gen", "Generate system properties", "system-configuration"),
        ("vintf-manifest-gen", "Generate VINTF manifests", "system-configuration"),
        ("sepolicy-analysis", "Analyze SELinux policies", "security"),
        ("treble-compliance-check", "Check Treble compliance", "compliance"),
        ("gms-compliance-check", "Check GMS compliance", "compliance"),
    ],
    "digital-analytics": [
        ("sql-query-gen", "Generate SQL queries", "query-generation"),
        ("data-cleaning-pipeline", "Generate data cleaning pipelines", "data-processing"),
        ("user-behavior-analysis", "Analyze user behavior patterns", "analytics"),
        ("dashboard-design", "Design analytics dashboards", "visualization"),
        ("etl-pipeline-gen", "Generate ETL pipelines", "data-processing"),
        ("data-model-design", "Design data models", "data-modeling"),
        ("metrics-definition", "Define business metrics", "analytics"),
        ("funnel-analysis", "Perform funnel analysis", "analytics"),
        ("cohort-analysis", "Perform cohort analysis", "analytics"),
        ("retention-analysis", "Analyze user retention", "analytics"),
        ("a-b-test-design", "Design A/B tests", "experimentation"),
        ("statistical-analysis", "Perform statistical analysis", "statistics"),
        ("predictive-model-gen", "Generate predictive models", "machine-learning"),
        ("anomaly-detection", "Detect data anomalies", "machine-learning"),
        ("segmentation-analysis", "Perform user segmentation", "analytics"),
        ("ltv-calculation", "Calculate lifetime value", "analytics"),
        ("roi-analysis", "Analyze ROI metrics", "analytics"),
        ("kpi-dashboard-gen", "Generate KPI dashboards", "visualization"),
        ("report-automation", "Automate report generation", "automation"),
        ("data-quality-check", "Check data quality", "data-quality"),
        ("schema-design", "Design database schemas", "data-modeling"),
        ("data-governance-policy", "Create data governance policies", "governance"),
        ("privacy-compliance-check", "Check privacy compliance", "compliance"),
        ("gdpr-data-export", "Generate GDPR data exports", "compliance"),
        ("real-time-analytics", "Design real-time analytics", "streaming"),
        ("data-warehouse-design", "Design data warehouses", "data-architecture"),
        ("bi-tool-integration", "Integrate BI tools", "integration"),
        ("custom-metric-gen", "Generate custom metrics", "analytics"),
        ("trend-forecasting", "Forecast trends", "predictive"),
        ("competitive-analysis", "Perform competitive analysis", "analytics"),
    ],
    "mobile-app": [
        ("compose-ui-gen", "Generate Jetpack Compose UI", "ui-generation"),
        ("swiftui-view-gen", "Generate SwiftUI views", "ui-generation"),
        ("login-feature-gen", "Generate login feature code", "feature-generation"),
        ("ui-test-gen-android", "Generate Android UI tests", "testing"),
        ("app-permission-analyze", "Analyze app permissions", "security"),
        ("navigation-setup-gen", "Generate navigation setup", "architecture"),
        ("state-management-gen", "Generate state management code", "architecture"),
        ("api-integration-gen", "Generate API integration code", "networking"),
        ("local-storage-gen", "Generate local storage code", "persistence"),
        ("push-notification-setup", "Setup push notifications", "messaging"),
        ("deep-link-config", "Configure deep links", "navigation"),
        ("app-icon-gen", "Generate app icons", "assets"),
        ("splash-screen-gen", "Generate splash screens", "ui"),
        ("onboarding-flow-gen", "Generate onboarding flows", "ux"),
        ("in-app-purchase-setup", "Setup in-app purchases", "monetization"),
        ("analytics-integration", "Integrate analytics", "tracking"),
        ("crash-reporting-setup", "Setup crash reporting", "monitoring"),
        ("performance-monitoring", "Setup performance monitoring", "monitoring"),
        ("ui-test-gen-ios", "Generate iOS UI tests", "testing"),
        ("unit-test-gen-mobile", "Generate mobile unit tests", "testing"),
        ("e2e-test-gen", "Generate E2E tests", "testing"),
        ("accessibility-check", "Check accessibility", "quality"),
        ("localization-setup", "Setup localization", "internationalization"),
        ("dark-mode-support", "Add dark mode support", "ui"),
        ("offline-mode-gen", "Generate offline mode code", "architecture"),
    ],
    "multi-language": [
        ("ui-string-translate", "Translate UI strings", "translation"),
        ("i18n-code-refactor", "Refactor code for i18n", "refactoring"),
        ("resource-file-gen", "Generate resource files", "resource-management"),
        ("translation-quality-check", "Check translation quality", "quality-assurance"),
        ("multi-language-gen", "Generate multi-language support", "internationalization"),
        ("locale-detection-gen", "Generate locale detection", "localization"),
        ("rtl-layout-support", "Add RTL layout support", "localization"),
        ("translation-memory-setup", "Setup translation memory", "translation"),
        ("glossary-management", "Manage translation glossaries", "terminology"),
        ("context-extraction", "Extract translation context", "translation"),
        ("pluralization-rules", "Handle pluralization rules", "localization"),
        ("date-time-localization", "Localize dates and times", "localization"),
        ("number-format-localization", "Localize number formats", "localization"),
        ("currency-localization", "Localize currency", "localization"),
        ("cultural-adaptation", "Adapt content culturally", "localization"),
        ("translation-workflow", "Setup translation workflows", "workflow"),
        ("machine-translation-review", "Review machine translations", "quality-assurance"),
        ("translation-consistency-check", "Check translation consistency", "quality-assurance"),
        ("pseudo-localization", "Generate pseudo-localization", "testing"),
        ("translation-coverage-report", "Generate coverage reports", "reporting"),
    ],
    "software-testing": [
        ("unit-test-gen", "Generate unit tests", "test-generation"),
        ("bug-root-cause", "Analyze bug root causes", "debugging"),
        ("crash-log-analyze", "Analyze crash logs", "debugging"),
        ("e2e-test-gen", "Generate E2E tests", "test-generation"),
        ("performance-bottleneck", "Identify performance bottlenecks", "performance"),
        ("test-case-design", "Design test cases", "test-design"),
        ("test-data-gen", "Generate test data", "test-data"),
        ("mock-server-gen", "Generate mock servers", "mocking"),
        ("api-contract-test", "Generate API contract tests", "contract-testing"),
        ("load-test-scenario", "Generate load test scenarios", "performance-testing"),
        ("stress-test-plan", "Create stress test plans", "performance-testing"),
        ("chaos-engineering", "Design chaos engineering tests", "reliability"),
        ("security-penetration-test", "Generate penetration tests", "security-testing"),
        ("vulnerability-scan", "Scan for vulnerabilities", "security-testing"),
        ("code-coverage-analysis", "Analyze code coverage", "coverage"),
        ("mutation-testing", "Perform mutation testing", "test-quality"),
        ("flaky-test-detection", "Detect flaky tests", "test-maintenance"),
        ("test-suite-optimization", "Optimize test suites", "test-maintenance"),
        ("ci-cd-test-integration", "Integrate tests in CI/CD", "automation"),
        ("regression-test-selection", "Select regression tests", "test-selection"),
        ("visual-regression-test", "Generate visual regression tests", "ui-testing"),
        ("accessibility-test-gen", "Generate accessibility tests", "a11y-testing"),
        ("compatibility-test-plan", "Create compatibility test plans", "compatibility"),
        ("exploratory-test-guide", "Guide exploratory testing", "manual-testing"),
        ("test-report-analysis", "Analyze test reports", "reporting"),
        ("defect-prediction", "Predict potential defects", "predictive"),
        ("test-automation-framework", "Setup test automation frameworks", "automation"),
        ("bdd-scenario-gen", "Generate BDD scenarios", "bdd"),
        ("test-execution-optimize", "Optimize test execution", "optimization"),
        ("quality-gate-config", "Configure quality gates", "quality"),
    ],
}

# Create skill directories and files
for domain, skills in skills_config.items():
    for skill_name, description, category in skills:
        skill_dir = f"skills/{domain}/{skill_name}"
        os.makedirs(skill_dir, exist_ok=True)
        
        # Create skill.yaml
        skill_yaml = {
            "name": skill_name,
            "description": description,
            "version": "1.0.0",
            "author": "Magic Skills Team",
            "category": domain,
            "tags": [domain, category],
            "parameters": {
                "type": "object",
                "properties": {
                    "input": {
                        "type": "string",
                        "description": "Input for the skill"
                    }
                },
                "required": ["input"]
            }
        }
        
        with open(f"{skill_dir}/skill.yaml", "w") as f:
            yaml.dump(skill_yaml, f, default_flow_style=False, allow_unicode=True)
        
        # Create prompt.txt
        with open(f"{skill_dir}/prompt.txt", "w") as f:
            f.write(f"You are an expert in {domain}. Help with: {description}\n\nInput: {{input}}")
        
        # Create handler.py
        handler_content = f'''"""{description} Handler."""

from typing import Any, Dict, Optional


def execute(params: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> str:
    """{description}."""
    user_input = params.get("input", "")
    
    if not user_input:
        return "Error: No input provided"
    
    # TODO: Implement {skill_name} logic
    return f"Processed: {{user_input}}"
'''
        with open(f"{skill_dir}/handler.py", "w") as f:
            f.write(handler_content)

total_skills = sum(len(skills) for skills in skills_config.values())
print(f"Created {total_skills} skills across {len(skills_config)} domains")
