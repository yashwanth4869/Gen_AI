from src.models.qa_records import QARecords

def map_query(user_id, user_query,session_id, service_type):
    return QARecords(
        UserId = user_id,
        Question = user_query,
        SessionId = session_id,
        ServiceType = service_type
    )