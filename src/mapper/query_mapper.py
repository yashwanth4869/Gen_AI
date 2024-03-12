from src.models.qa_records import QARecords

def map_query(user_id, user_query):
    return QARecords(
        UserId = user_id,
        Question = user_query
    )