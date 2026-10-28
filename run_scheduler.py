import os
import time
import logging
from app import create_app
from app.services.escalation_service import EscalationService

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] [SLA-SCHEDULER] %(message)s'
)

def run_periodic_escalation_checks(interval_seconds=60):
    """
    Continuous background worker checking for Day 2 and Day 4 statutory escalation conditions.
    Idempotent: Running repeatedly will never create duplicate escalation records.
    """
    app = create_app(os.environ.get('FLASK_ENV', 'development'))
    logging.info(f"Starting CivicPulse AI Statutory Escalation Engine (Polling every {interval_seconds}s)...")
    
    with app.app_context():
        while True:
            try:
                result = EscalationService.process_all_escalations()
                if result['day2_escalations_triggered'] > 0 or result['day4_escalations_triggered'] > 0:
                    logging.info(
                        f"Escalation event triggered: "
                        f"Day 2 (Supervisor): {result['day2_escalations_triggered']}, "
                        f"Day 4 (Dept Head): {result['day4_escalations_triggered']}"
                    )
                else:
                    logging.info("Periodic SLA audit check completed. All active tickets in compliance.")
            except Exception as e:
                logging.error(f"Error executing escalation check: {e}")

            time.sleep(interval_seconds)

if __name__ == '__main__':
    run_periodic_escalation_checks(interval_seconds=60)
