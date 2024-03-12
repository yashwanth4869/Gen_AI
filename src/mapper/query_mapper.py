from src.models.qa_records import QARecords

def query_map(user_id, user_query):
    return QARecords(
        UserId = user_id,
        Question = user_query
    )