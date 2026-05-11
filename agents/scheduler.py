def get_availability():
    return ["10:00 AM", "1:00 PM", "3:00 PM"]

def create_draft_appointment(patient_id, slot):
    return {
        "patient_id": patient_id,
        "slot": slot,
        "status": "draft"
    }


def handle_scheduler(query: str, patient_id: str = None):

    q = query.lower()
    slots = get_availability()

    if "book" in q or "schedule" in q or "appointment" in q:

        for slot in slots:

            if slot.lower() in q:

                draft = create_draft_appointment(
                    patient_id,
                    slot
                )

                return {
                    "intent": "scheduler",
                    "action": "draft_appointment",
                    "data": draft,
                    "sources": []
                }

        return {
            "intent": "scheduler",
            "action": "show_slots",
            "data": slots,
            "sources": []
        }

    return {
        "intent": "scheduler",
        "action": "availability",
        "data": slots,
        "sources": []
    }