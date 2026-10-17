# Illustrative Bedrock Guardrail skeleton (adapt before use; pin provider versions).
# Source (resource schema): https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/bedrockagent_guardrail
# Source (Guardrails concepts): https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html
# Confirm the exact resource arguments in the registry docs for your pinned provider version.

terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0" # illustrative; pin to a version you have validated
    }
  }
}

variable "region" {
  type        = string
  description = "AWS Region to deploy into."
}

variable "guardrail_name" {
  type    = string
  default = "sample-guardrail"
}

provider "aws" {
  region = var.region
}

# NOTE: argument names/blocks can change between provider versions — verify against the registry
# resource page above before applying.
resource "aws_bedrockagent_guardrail" "this" {
  name                      = var.guardrail_name
  blocked_input_messaging   = "This request was blocked by the guardrail."
  blocked_outputs_messaging = "This response was blocked by the guardrail."

  # Example content policy: enable filters and set strengths per your risk model.
  content_policy_config {
    filters_config {
      type            = "SEXUAL"
      input_strength  = "HIGH"
      output_strength = "HIGH"
    }
    filters_config {
      type            = "VIOLENCE"
      input_strength  = "HIGH"
      output_strength = "HIGH"
    }
  }
}

output "guardrail_id" {
  value = aws_bedrockagent_guardrail.this.guardrail_id
}
