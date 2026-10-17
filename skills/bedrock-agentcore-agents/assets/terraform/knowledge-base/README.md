# Knowledge Base (Terraform starter)

Illustrative starting point for provisioning a Bedrock Knowledge Base with Terraform. Adapt and
pin versions before use.

Recommended path: use the AWS-maintained module, which can create a knowledge base via input flags.

- Module: https://github.com/aws-ia/terraform-aws-bedrock
- Knowledge Bases concepts: https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html
- Supported models/Regions: https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base-supported.html

```hcl
# Illustrative — confirm inputs/outputs against the module README for the version you pin.
terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0" # pin to a validated version
    }
  }
}

module "bedrock" {
  source  = "aws-ia/bedrock/aws"
  version = "x.y.z" # pin to a real, validated module version from the registry

  # Disable the default agent if you only want a knowledge base.
  create_agent = false

  # Set the knowledge-base creation flag and its inputs per the module README.
  create_kb = true
  # ... embedding model, data source (e.g. S3), and vector store inputs go here ...
}
```

Do not hard-code model IDs, account IDs, or Regions — pass them as variables. Verify current
supported embedding/generation models for your Region at the supported-models page above.
