# Illustrative least-privilege execution role for an agent (adapt before use; pin versions).
# Sources:
# - Bedrock IAM identity-based policy examples: https://docs.aws.amazon.com/bedrock/latest/userguide/security_iam_id-based-policy-examples.html
# - AgentCore IAM: https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/security-iam.html
# - Well-Architected GenAI Lens (least privilege to FM endpoints): https://docs.aws.amazon.com/wellarchitected/latest/generative-ai-lens/gensec01-bp01.html
#
# Scope Resource ARNs to the specific models/tools the agent uses. Avoid Resource = "*".

terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0" # pin to a validated version
    }
  }
}

variable "trusted_service_principal" {
  type        = string
  description = "Service principal allowed to assume this role (confirm the correct AgentCore principal in the AgentCore IAM docs)."
}

variable "allowed_model_arns" {
  type        = list(string)
  description = "Specific foundation model ARNs the agent may invoke. Do not use '*'."
}

data "aws_iam_policy_document" "assume" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = [var.trusted_service_principal]
    }
  }
}

resource "aws_iam_role" "agent_exec" {
  name               = "sample-agent-exec-role"
  assume_role_policy = data.aws_iam_policy_document.assume.json
}

# Least-privilege model invocation, scoped to named model ARNs.
data "aws_iam_policy_document" "invoke_models" {
  statement {
    sid     = "InvokeScopedModels"
    actions = [
      "bedrock:InvokeModel",
      "bedrock:InvokeModelWithResponseStream",
    ]
    resources = var.allowed_model_arns
  }
}

resource "aws_iam_role_policy" "invoke_models" {
  name   = "invoke-scoped-models"
  role   = aws_iam_role.agent_exec.id
  policy = data.aws_iam_policy_document.invoke_models.json
}

output "role_arn" {
  value = aws_iam_role.agent_exec.arn
}
