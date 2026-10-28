import os
import click
from datetime import datetime, timezone, timedelta
from app import create_app
from app.extensions import db
from app.models import (
    User, Department, DepartmentMembership, DepartmentApplication,
    Complaint, ComplaintImage, ComplaintStatusHistory, AIAnalysisResult,
    Escalation, Notification, AuditLog, utc_now
)
from app.services.escalation_service import EscalationService
from app.services.ai_analyzer import AIComplaintAnalyzer

app = create_app(os.environ.get('FLASK_ENV', 'development'))

@app.cli.command('init-db')
def init_db():
    """Create all database tables."""
    db.create_all()
    click.echo(click.style("Database tables initialized successfully.", fg="green"))

@app.cli.command('create-admin')
@click.option('--email', default=None, help='Admin email')
@click.option('--password', default=None, help='Admin password')
@click.option('--name', default=None, help='Admin full name')
def create_admin(email, password, name):
    """Create default system administrator account."""
    admin_email = email or os.environ.get('ADMIN_EMAIL', 'admin@civicpulse.gov.in')
    admin_pass = password or os.environ.get('ADMIN_PASSWORD', 'Admin@CivicPulse2026')
    admin_name = name or os.environ.get('ADMIN_NAME', 'National System Administrator')

    existing = User.query.filter_by(email=admin_email).first()
    if existing:
        click.echo(click.style(f"Administrator with email '{admin_email}' already exists.", fg="yellow"))
        return

    admin = User(
        email=admin_email,
        full_name=admin_name,
        mobile='9820000001',
        role='admin',
        state='Delhi',
        district='New Delhi',
        city_village='Central Secretariat',
        preferred_language='en'
    )
    admin.set_password(admin_pass)
    db.session.add(admin)
    db.session.commit()
    click.echo(click.style(f"Administrator created successfully! Email: {admin_email}", fg="green"))

@app.cli.command('check-escalations')
def check_escalations():
    """Run Day 2 & Day 4 Escalation Engine."""
    result = EscalationService.process_all_escalations()
    click.echo(click.style(
        f"Escalation Check Completed: Day 2 triggered: {result['day2_escalations_triggered']}, "
        f"Day 4 triggered: {result['day4_escalations_triggered']}", fg="cyan"
    ))

@app.cli.command('seed-data')
def seed_data():
    """Populate database with realistic Indian civic demo data across all 5 roles."""
    db.create_all()
    now = utc_now()

    # 1. System Administrator
    admin = User.query.filter_by(email='admin@civicpulse.gov.in').first()
    if not admin:
        admin = User(
            email='admin@civicpulse.gov.in',
            full_name='Dr. Rajesh Sharma, IAS',
            mobile='9820000001',
            role='admin',
            state='Maharashtra',
            district='Mumbai City',
            city_village='Mantralaya',
            preferred_language='en'
        )
        admin.set_password('Admin@CivicPulse2026')
        db.session.add(admin)

    # 2. Key Departments
    departments_data = [
        {
            'code': 'PWD-MUM-01',
            'name': 'Public Works Department (PWD) - Mumbai Metro',
            'category': 'Roads and Public Infrastructure',
            'state': 'Maharashtra',
            'district': 'Mumbai Suburban',
            'jurisdiction_type': 'Municipal Corporation',
            'description': 'Maintains arterial roadways, flyovers, footpaths and pedestrian bridges in Mumbai Suburban.'
        },
        {
            'code': 'ELEC-MUM-02',
            'name': 'Brihanmumbai Electric Supply & Transport (BEST) Lighting',
            'category': 'Electricity and Streetlights',
            'state': 'Maharashtra',
            'district': 'Mumbai Suburban',
            'jurisdiction_type': 'Municipal Corporation',
            'description': 'Municipal streetlighting network, high-tension lines, and distribution transformers.'
        },
        {
            'code': 'SWM-MUM-03',
            'name': 'Solid Waste Management & Sanitation Division (BMC)',
            'category': 'Garbage and Sanitation',
            'state': 'Maharashtra',
            'district': 'Mumbai Suburban',
            'jurisdiction_type': 'Municipal Corporation',
            'description': 'Daily municipal solid waste collection, community dustbins, and sanitation drives.'
        },
        {
            'code': 'WSSB-MUM-04',
            'name': 'Hydraulic Engineer & Water Supply Department',
            'category': 'Water Supply',
            'state': 'Maharashtra',
            'district': 'Mumbai Suburban',
            'jurisdiction_type': 'Municipal Corporation',
            'description': 'Potable drinking water supply pipelines, reservoirs, and pipeline leak remediation.'
        },
        {
            'code': 'DRAIN-MUM-05',
            'name': 'Storm Water Drains & Sewerage Operations (SWD)',
            'category': 'Drainage and Sewage',
            'state': 'Maharashtra',
            'district': 'Mumbai Suburban',
            'jurisdiction_type': 'Municipal Corporation',
            'description': 'Monsoon drainage desilting, manhole maintenance, and underground sewage networks.'
        }
    ]

    dept_map = {}
    for d in departments_data:
        existing_dept = Department.query.filter_by(code=d['code']).first()
        if not existing_dept:
            new_dept = Department(**d)
            db.session.add(new_dept)
            db.session.flush()
            dept_map[d['code']] = new_dept
        else:
            dept_map[d['code']] = existing_dept

    # 3. Department Officials, Supervisors, and Department Heads
    pwd_dept = dept_map['PWD-MUM-01']

    # Official (Field Engineer)
    official = User.query.filter_by(email='engineer.pwd@civicpulse.gov.in').first()
    if not official:
        official = User(
            email='engineer.pwd@civicpulse.gov.in',
            full_name='Vikram Shinde',
            mobile='9820011111',
            role='department_official',
            state='Maharashtra',
            district='Mumbai Suburban',
            city_village='Bandra East',
            preferred_language='en'
        )
        official.set_password('Official@2026')
        db.session.add(official)
        db.session.flush()

        mem_official = DepartmentMembership(
            user_id=official.id,
            department_id=pwd_dept.id,
            designation='Assistant Engineer (Roads)',
            office_address='PWD Sub-Divisional Office, Bandra East, Mumbai',
            employee_ref_no='MH-PWD-4091',
            is_supervisor=False,
            is_head=False
        )
        db.session.add(mem_official)

    # Supervisor (Zonal Supervisor for Day 2 Escalations)
    supervisor = User.query.filter_by(email='supervisor.pwd@civicpulse.gov.in').first()
    if not supervisor:
        supervisor = User(
            email='supervisor.pwd@civicpulse.gov.in',
            full_name='Anil Kulkarni',
            mobile='9820022222',
            role='supervisor',
            state='Maharashtra',
            district='Mumbai Suburban',
            city_village='Bandra East',
            preferred_language='en'
        )
        supervisor.set_password('Supervisor@2026')
        db.session.add(supervisor)
        db.session.flush()

        mem_sup = DepartmentMembership(
            user_id=supervisor.id,
            department_id=pwd_dept.id,
            designation='Executive Engineer & Zonal Supervisor',
            office_address='PWD Divisional Headquarters, Mumbai',
            employee_ref_no='MH-PWD-EXEC-104',
            is_supervisor=True,
            is_head=False
        )
        db.session.add(mem_sup)

    # Department Head (Day 4 Escalations & Executive Orders)
    head = User.query.filter_by(email='head.pwd@civicpulse.gov.in').first()
    if not head:
        head = User(
            email='head.pwd@civicpulse.gov.in',
            full_name='Er. Sunil Deshmukh',
            mobile='9820033333',
            role='department_head',
            state='Maharashtra',
            district='Mumbai Suburban',
            city_village='Mantralaya',
            preferred_language='en'
        )
        head.set_password('DeptHead@2026')
        db.session.add(head)
        db.session.flush()

        mem_head = DepartmentMembership(
            user_id=head.id,
            department_id=pwd_dept.id,
            designation='Chief Engineer & Department Head',
            office_address='Chief Engineering Directorate, Mumbai',
            employee_ref_no='MH-PWD-CHIEF-01',
            is_supervisor=False,
            is_head=True
        )
        db.session.add(mem_head)

    # 4. Verified Citizen Account
    citizen = User.query.filter_by(email='citizen@civicpulse.in').first()
    if not citizen:
        citizen = User(
            email='citizen@civicpulse.in',
            full_name='Pooja Mehta',
            mobile='9820044444',
            role='citizen',
            state='Maharashtra',
            district='Mumbai Suburban',
            city_village='Andheri West',
            preferred_language='en'
        )
        citizen.set_password('Citizen@2026')
        db.session.add(citizen)
        db.session.flush()

    # 5. Pending Verification Department Applicant (For Admin approval testing)
    applicant = User.query.filter_by(email='applicant.sanitation@civicpulse.in').first()
    if not applicant:
        applicant = User(
            email='applicant.sanitation@civicpulse.in',
            full_name='Ramesh Salunke',
            mobile='9820055555',
            role='department_applicant',
            state='Maharashtra',
            district='Mumbai Suburban',
            city_village='Kurla West',
            preferred_language='en'
        )
        applicant.set_password('Applicant@2026')
        db.session.add(applicant)
        db.session.flush()

        app_record = DepartmentApplication(
            user_id=applicant.id,
            department_name='BMC Solid Waste Division Ward L',
            department_category='Garbage and Sanitation',
            designation='Junior Sanitation Overseer',
            employee_ref_no='BMC-SWM-9921',
            supervising_office='Assistant Municipal Commissioner Ward L',
            state='Maharashtra',
            district='Mumbai Suburban',
            jurisdiction='Ward L - Kurla & Sakinaka',
            office_address='Ward L Municipal Building, S.G. Barve Marg, Kurla',
            reason='Required to access daily sanitation complaints and coordinate compactor truck routing.',
            status='pending'
        )
        db.session.add(app_record)

    # 6. Realistic Complaints across various operational states
    complaints_seed = [
        {
            'cid': 'CP-2026-X8K92',
            'title': 'Severe pothole crater near Andheri West Metro Station exit',
            'desc': 'Extremely dangerous 2-foot wide pothole crater directly at the bus stop exit near Andheri West Metro station. Multiple two-wheelers have skidded in the dark. Requires urgent asphalt resurfacing.',
            'cat': 'Roads and Public Infrastructure',
            'priority': 'Urgent',
            'status': 'In Progress',
            'dept': pwd_dept,
            'lat': 19.1197,
            'lon': 72.8464,
            'landmark': 'Near Pillar 112, SV Road, Andheri West',
            'days_ago': 1,
            'assigned': official
        },
        {
            'cid': 'CP-2026-B3N71',
            'title': 'Open live electrical wires hanging from damaged feeder box',
            'desc': 'Pedestrian shock hazard: A roadside feeder junction box door is broken and exposed live sparking electrical wires are touching the wet pavement.',
            'cat': 'Electricity and Streetlights',
            'priority': 'Urgent',
            'status': 'Assigned',
            'dept': dept_map['ELEC-MUM-02'],
            'lat': 19.0600,
            'lon': 72.8335,
            'landmark': 'Opposite National College, Linking Road, Bandra West',
            'days_ago': 3, # Past 48h -> Day 2 Escalation candidate!
            'is_esc_day2': True
        },
        {
            'cid': 'CP-2026-M4P19',
            'title': 'Main water supply pipeline burst flooding residential lane',
            'desc': 'High pressure potable drinking water pipeline ruptured beneath the pavement. Massive clean water loss flooding the road for 5 days without repair.',
            'cat': 'Water Supply',
            'priority': 'High',
            'status': 'Assigned',
            'dept': dept_map['WSSB-MUM-04'],
            'lat': 19.1351,
            'lon': 72.8146,
            'landmark': 'Lane 4, Versova Village, Andheri West',
            'days_ago': 5, # Past 96h -> Day 4 Escalation candidate!
            'is_esc_day2': True,
            'is_esc_day4': True
        },
        {
            'cid': 'CP-2026-K7W55',
            'title': 'Overflowing municipal garbage dumpster blocking pedestrian walkway',
            'desc': 'Community waste container has not been cleared for four days. Foul odor and stray animals scattering litter onto the main road.',
            'cat': 'Garbage and Sanitation',
            'priority': 'Medium',
            'status': 'Resolved — Awaiting Citizen Verification',
            'dept': dept_map['SWM-MUM-03'],
            'lat': 19.0728,
            'lon': 72.8826,
            'landmark': 'Near Kurla Railway Station West Market',
            'days_ago': 2,
            'resolved_ago': 0.2
        },
        {
            'cid': 'CP-2026-T9Q44',
            'title': 'Damaged stormwater drain slab collapsed on footpath',
            'desc': 'Concrete cover over the stormwater nullah collapsed, leaving a 4-foot deep hazard hole on the public pedestrian pathway.',
            'cat': 'Drainage and Sewage',
            'priority': 'High',
            'status': 'Closed',
            'dept': dept_map['DRAIN-MUM-05'],
            'lat': 19.0178,
            'lon': 72.8478,
            'landmark': 'Dadar TT Circle, near Flower Market',
            'days_ago': 7,
            'resolved_ago': 3
        }
    ]

    for comp in complaints_seed:
        existing_c = Complaint.query.filter_by(complaint_id=comp['cid']).first()
        if not existing_c:
            created_time = now - timedelta(days=comp['days_ago'])
            d2_deadline = created_time + timedelta(hours=48)
            d4_deadline = created_time + timedelta(hours=96)
            resolved_time = (now - timedelta(days=comp['resolved_ago'])) if 'resolved_ago' in comp else None

            c = Complaint(
                complaint_id=comp['cid'],
                citizen_id=citizen.id,
                title=comp['title'],
                description=comp['desc'],
                category=comp['cat'],
                state='Maharashtra',
                district='Mumbai Suburban',
                city_village='Mumbai',
                address_landmark=comp['landmark'],
                latitude=comp['lat'],
                longitude=comp['lon'],
                status=comp['status'],
                priority=comp['priority'],
                department_id=comp['dept'].id if comp.get('dept') else None,
                assigned_staff_id=comp.get('assigned').id if comp.get('assigned') else None,
                deadline_day2=d2_deadline,
                deadline_day4=d4_deadline,
                is_escalated_day2=comp.get('is_esc_day2', False),
                is_escalated_day4=comp.get('is_esc_day4', False),
                created_at=created_time,
                resolved_at=resolved_time
            )
            db.session.add(c)
            db.session.flush()

            # Add AI Analysis record
            ai = AIAnalysisResult(
                complaint_id=c.id,
                is_real_ai=False,
                model_name='Deterministic Rule Engine (CivicNLP v2.6)',
                analysis_type='Rule-based analysis (External AI key not configured)',
                recommended_category=c.category,
                recommended_department_code=comp['dept'].code if comp.get('dept') else 'PWD',
                suggested_priority=c.priority,
                confidence_score=0.91,
                explanation=f"Evaluated grievance title and description. Matched keywords for '{c.category}'. Urgency determined as '{c.priority}'.",
                safety_risks="Identified public mobility and safety risk factor." if c.priority in ['Urgent', 'High'] else "Routine civic maintenance.",
                recommended_next_action="Immediate site inspection and barrier deployment." if c.priority == 'Urgent' else "Queue for standard departmental dispatch."
            )
            db.session.add(ai)

            # Add History
            hist = ComplaintStatusHistory(
                complaint_id=c.id,
                previous_status=None,
                new_status='Submitted',
                changed_by_id=citizen.id,
                notes="Grievance filed by citizen.",
                created_at=created_time
            )
            db.session.add(hist)

            if comp.get('is_esc_day2'):
                esc2 = Escalation(
                    complaint_id=c.id,
                    escalation_level=2,
                    reason="Automated Day 2 SLA breach: No departmental action recorded in 48h.",
                    recipient_role='supervisor',
                    recipient_user_id=supervisor.id,
                    status='triggered',
                    triggered_at=d2_deadline
                )
                db.session.add(esc2)
                hist2 = ComplaintStatusHistory(
                    complaint_id=c.id,
                    previous_status=c.status,
                    new_status=c.status,
                    notes="SYSTEM ALERT: Automated Day 2 escalation to Zonal Supervisor.",
                    created_at=d2_deadline
                )
                db.session.add(hist2)

            if comp.get('is_esc_day4'):
                esc4 = Escalation(
                    complaint_id=c.id,
                    escalation_level=4,
                    reason="Automated Day 4 SLA breach: Unresolved after 96h.",
                    recipient_role='department_head',
                    recipient_user_id=head.id,
                    status='triggered',
                    triggered_at=d4_deadline
                )
                db.session.add(esc4)
                hist4 = ComplaintStatusHistory(
                    complaint_id=c.id,
                    previous_status=c.status,
                    new_status=c.status,
                    notes="EXECUTIVE ESCALATION: Day 4 escalation to Department Head.",
                    created_at=d4_deadline
                )
                db.session.add(hist4)

    db.session.commit()
    click.echo(click.style("Seed data successfully created! All 5 roles ready for demo.", fg="green"))
    click.echo(click.style("""
Demo Credentials:
1. Administrator:   admin@civicpulse.gov.in       | Admin@CivicPulse2026
2. Dept Head:       head.pwd@civicpulse.gov.in     | DeptHead@2026
3. Supervisor:      supervisor.pwd@civicpulse.gov.in| Supervisor@2026
4. Dept Official:   engineer.pwd@civicpulse.gov.in | Official@2026
5. Citizen:         citizen@civicpulse.in          | Citizen@2026
6. Pending Dept:    applicant.sanitation@civicpulse.in | Applicant@2026
""", fg="yellow"))

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        # CLI command invoked e.g. python run.py seed-data or python run.py check-escalations
        app.cli()
    else:
        # Standalone development server run
        with app.app_context():
            db.create_all()
        app.run(host='0.0.0.0', port=5000, debug=True)
