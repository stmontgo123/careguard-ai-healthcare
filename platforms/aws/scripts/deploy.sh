#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."
command -v sam >/dev/null || { echo "AWS SAM CLI is required."; exit 1; }
sam build --template-file infra/template.yaml
sam deploy --guided --stack-name careguard-claim-guard-demo
