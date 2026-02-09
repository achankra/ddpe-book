# guardrails.rego (Open Policy Agent) 
package platform.guardrails 

# Security guardrails 

deny[msg] { 

  input.kind == "Service" 
  input.spec.exposure == "public" 
  not input.spec.waf_enabled 
  msg := "Public services must have WAF enabled" 

} 

deny[msg] { 

  input.kind == "Database" 
  input.spec.encryption.enabled == false 
  msg := "Database encryption must be enabled" 

} 

# Compliance guardrails 

deny[msg] { 

  input.kind == "Database" 
  input.metadata.domain == "payments" 
  input.spec.backup_retention_days < 90 
  msg := "PCI-DSS requires 90-day backup retention" 

} 

# Operational guardrails 

deny[msg] { 

  input.kind == "Deployment" 
  not input.spec.health_check 
  msg := "All deployments must define health checks" 

} 