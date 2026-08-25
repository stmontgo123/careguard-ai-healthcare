import argparse
import json
import os
try:
    from dotenv import load_dotenv
except ImportError:
    def load_dotenv(*args, **kwargs):
        return False

from src.authz import AccessContext
from src.agent import run_case

def main():
    load_dotenv("config/.env")
    p = argparse.ArgumentParser(description="CareGuard AI synthetic healthcare RAG demo")
    p.add_argument("--role", default=os.getenv("CAREGUARD_ROLE", "CARE_COORDINATOR"))
    p.add_argument("--purpose", default=os.getenv("CAREGUARD_PURPOSE", "CARE_COORDINATION"))
    p.add_argument("--patient", default=os.getenv("CAREGUARD_PATIENT_ID", "PAT-1001"))
    p.add_argument("--encounter", default=os.getenv("CAREGUARD_ENCOUNTER_ID", "ENC-240817"))
    p.add_argument("--question", default="What is preventing discharge readiness right now?")
    p.add_argument("--no-ollama", action="store_true")
    args = p.parse_args()

    ctx = AccessContext(
        user_id="demo-user",
        role=args.role,
        purpose=args.purpose,
        patient_id=args.patient,
        encounter_id=args.encounter,
    )

    result = run_case(ctx, args.question, use_ollama=not args.no_ollama)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
