#!/usr/bin/env bash
set -euo pipefail

command -v sam >/dev/null || { echo "AWS SAM CLI is required."; exit 1; }
sam delete --stack-name careguard-claim-guard-demo
