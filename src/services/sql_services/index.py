from sql_chain import SQLService

query = input("Enter the query :")

sql_service = SQLService()

print(sql_service.get_property_information(user_question=query))