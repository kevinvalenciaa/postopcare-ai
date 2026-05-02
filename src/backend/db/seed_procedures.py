"""POC-011: Seed the procedures table.

Mirrors src/data/procedures.ts so the frontend dropdown and backend
generation share identical slugs. Adds extra procedures expected by
Sprint 2 to broaden coverage.
"""

from __future__ import annotations

from db.models import Procedure, get_session, init_db

PROCEDURES: list[dict] = [
    # Orthopedic
    {"slug": "total-knee-replacement", "name": "Total Knee Replacement", "specialty": "Orthopedic",
     "description": "Total knee arthroplasty (TKA)", "common_aliases": ["TKA", "TKR", "knee replacement"]},
    {"slug": "total-hip-replacement", "name": "Total Hip Replacement", "specialty": "Orthopedic",
     "description": "Total hip arthroplasty (THA)", "common_aliases": ["THA", "THR", "hip replacement"]},
    {"slug": "acl-reconstruction", "name": "ACL Reconstruction", "specialty": "Orthopedic",
     "description": "Anterior cruciate ligament reconstruction", "common_aliases": ["ACL repair"]},
    {"slug": "rotator-cuff-repair", "name": "Rotator Cuff Repair", "specialty": "Orthopedic",
     "description": "Surgical repair of torn rotator cuff", "common_aliases": ["RCR"]},
    # General Surgery
    {"slug": "laparoscopic-cholecystectomy", "name": "Laparoscopic Cholecystectomy",
     "specialty": "General Surgery", "description": "Gallbladder removal surgery",
     "common_aliases": ["lap chole", "gallbladder removal"]},
    {"slug": "laparoscopic-appendectomy", "name": "Laparoscopic Appendectomy",
     "specialty": "General Surgery", "description": "Appendix removal surgery",
     "common_aliases": ["lap appy"]},
    {"slug": "inguinal-hernia-repair", "name": "Inguinal Hernia Repair",
     "specialty": "General Surgery", "description": "Hernia repair surgery",
     "common_aliases": ["hernia repair"]},
    # OB/GYN
    {"slug": "cesarean-section", "name": "Cesarean Section (C-Section)", "specialty": "OB/GYN",
     "description": "Surgical delivery of baby", "common_aliases": ["C-section", "cesarean"]},
    {"slug": "laparoscopic-hysterectomy", "name": "Laparoscopic Hysterectomy", "specialty": "OB/GYN",
     "description": "Uterus removal surgery", "common_aliases": ["hysterectomy"]},
    # Emergency
    {"slug": "ankle-fracture", "name": "Ankle Fracture (Cast Care)", "specialty": "Emergency",
     "description": "Ankle fracture management", "common_aliases": ["ankle fx"]},
    {"slug": "concussion", "name": "Concussion", "specialty": "Emergency",
     "description": "Mild traumatic brain injury care", "common_aliases": ["mTBI", "head injury"]},
    {"slug": "kidney-stones", "name": "Kidney Stone Passage", "specialty": "Emergency",
     "description": "Renal calculi passage protocol", "common_aliases": ["renal calculi"]},
    {"slug": "wrist-fracture", "name": "Wrist Fracture (Cast Care)", "specialty": "Emergency",
     "description": "Distal radius fracture management", "common_aliases": ["Colles fracture"]},
    # ENT / additional
    {"slug": "tonsillectomy", "name": "Tonsillectomy", "specialty": "ENT",
     "description": "Removal of tonsils", "common_aliases": []},
    {"slug": "thyroidectomy", "name": "Thyroidectomy", "specialty": "ENT",
     "description": "Removal of thyroid gland", "common_aliases": []},
]


def seed() -> int:
    init_db()
    session = get_session()
    inserted = 0
    try:
        for spec in PROCEDURES:
            exists = session.query(Procedure).filter_by(slug=spec["slug"]).first()
            if exists:
                continue
            session.add(Procedure(**spec))
            inserted += 1
        session.commit()
    finally:
        session.close()
    return inserted


if __name__ == "__main__":
    n = seed()
    print(f"Seeded {n} new procedures (skipped existing).")
