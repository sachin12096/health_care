import pymongo.errors
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from health_service.utils import DbConnection
from medication_scheduler.settings import USERS_COLLECTION
import uuid
db_conn = DbConnection()
db_conn.connect()


@api_view(['POST'])
def save_user_details(request):
    """
    it will insert details about a user into SB
    :param request: request object
    :return: Dictionary consisting user details saved into DB
    """
    # creating default response data
    data = {"data": [],
            "errors": ""}
    users_collection = db_conn.get_collection(USERS_COLLECTION)
    try:
        print("INFO | Reading user details from request")
        user_details = request.data


        user_id = str(uuid.uuid4())
        user_details['user_id'] = user_id
        db_response = users_collection.insert_one(user_details)
        id = str(db_response.inserted_id)
        user_details['_id'] = id
        data["data"] = user_details
        print("INFO | User details successfully inserted into DB")
        return Response(data=data, status=status.HTTP_200_OK)
    except pymongo.errors.DuplicateKeyError:
        error = "User already exist in the DB, Please provide a unique user values"
        print(f"ERROR | {error}")
        data["errors"] = error
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(f"ERROR | Unable to insert user details into DB due to error: {str(e)}")
        data["errors"] = str(e)
        return Response(data=data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_user_details(request, user_id):
    """
    it will fetch user details
    :param request: request object
    : user_id: unique user id
    :return: Dictionary consisting user details
    """
    # creating default response data
    data = {"data": [],
            "errors": ""}
    users_collection = db_conn.get_collection(USERS_COLLECTION)
    try:
        print("INFO | Reading user details from request")
        filter_query = {
            'user_id': user_id
        }
        db_response = users_collection.find_one(filter_query)
        if not db_response:
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)
        id = str(db_response['_id'])
        db_response['_id'] = id
        data["data"] = db_response
        print("INFO | User details successfully retrieved from DB")
        return Response(data=data, status=status.HTTP_200_OK)
    except Exception as e:
        print(f"ERROR | Unable to fetch user details from DB due to error: {str(e)}")
        data["errors"] = str(e)
        return Response(data=data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
def update_user_details(request, user_id):
    """
    it will update user details
    :param request: request object
    :user_id: unique user id
    :return: Dictionary consisting user details
    """
    # creating default response data
    data = {"data": [],
            "errors": ""}
    users_collection = db_conn.get_collection(USERS_COLLECTION)
    try:
        print("INFO | Reading user details from request")
        user_details = request.data
        filter_query = {
            'user_id': user_id
        }
        update_query = {"$set": user_details}
        db_response = users_collection.update_one(filter_query, update_query)
        if db_response.matched_count <= 0:
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)
        print("INFO | User details updated successfully")
        return Response(data=user_details, status=status.HTTP_200_OK)
    except Exception as e:
        print(f"ERROR | Unable to update user details into DB due to error: {str(e)}")
        data["errors"] = str(e)
        return Response(data=data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
def delete_user_details(request, user_id):
    """
    it will delete user
    :param request: request object
    :user_id: unique user id
    :return: Dictionary consisting user details
    """
    # creating default response data
    data = {"data": [],
            "errors": ""}
    users_collection = db_conn.get_collection(USERS_COLLECTION)
    try:
        print("INFO | Reading user details from request")
        user_details = request.data
        filter_query = {
            'user_id': user_id
        }
        db_response = users_collection.delete_one(filter_query)
        if db_response.deleted_count <= 0:
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)
        print("INFO | User deleted successfully")
        return Response(data=user_details, status=status.HTTP_200_OK)
    except Exception as e:
        print(f"ERROR | Unable to delete user due to error: {str(e)}")
        data["errors"] = str(e)
        return Response(data=data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
