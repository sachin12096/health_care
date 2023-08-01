import pymongo.errors
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from health_service.utils import DbConnection
from medication_scheduler.settings import PATIENTS_COLLECTION, SCHEDULES_COLLECTION
import uuid

db_conn = DbConnection()
db_conn.connect()


@api_view(['POST'])
def save_medicine_details(request):
    """
        it will insert details about a medicines and timming into SB
        :param request: request object
        :return: Dictionary consisting medicine and timing details saved into DB
        """
    data = {"data": [],
            "errors": ""}

    medications_collection = db_conn.get_collection(SCHEDULES_COLLECTION)
    patients_collection = db_conn.get_collection(PATIENTS_COLLECTION)

    try:
        print("INFO | Regarding medication schedule from request")
        medication_details = request.data
        patient_id = medication_details.get('patient_id')
        filter_query = {
            'patient_id': patient_id
        }
        db_response = patients_collection.find_one(filter_query)
        if not db_response:
            data['errors'] = "patient not found enter valid patient id"
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)
        db_response = medications_collection.insert_one(medication_details)
        id = str(db_response.inserted_id)
        medication_details['_id'] = id
        data['data'] = medication_details
        print('medication schedule details inserted into db')
        return Response(data=data, status=status.HTTP_200_OK)
    except pymongo.errors.DuplicateKeyError:
        error = "medication already exist in the DB, Please provide a unique medicine details"
        print(f'error |{error}')
        data['errors'] = error
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(f"ERROR | Unable to insert medication details into DB due to error: {str(e)}")
        data["errors"] = str(e)
        return Response(data=data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_medication_details(request, patient_id):
    """
    it will fetch medicine details
    :param request: request object
    : patient_id: unique patient id
    :return: Dictionary consisting user details
    """
    # creating default response data
    data = {"data": [],
            "errors": ""}
    medication_collection = db_conn.get_collection(SCHEDULES_COLLECTION)
    try:
        print("INFO | Reading user details from request")
        filter_query = {
            'patient_id': patient_id
        }
        db_response = medication_collection.find_one(filter_query)
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
def update_medication_details(request, patient_id):
    """
    it will update medication details
    :param request: request object
    :patient_id: unique patient id
    :return: Dictionary consisting user details
    """
    # creating default response data
    data = {"data": [],
            "errors": ""}
    medication_collection = db_conn.get_collection(SCHEDULES_COLLECTION)
    try:
        print("INFO | Reading user details from request")
        medication_details = request.data
        filter_query = {
            'patient_id': patient_id
        }
        update_query = {"$set": medication_details}
        db_response = medication_collection.update_one(filter_query, update_query)
        if db_response.matched_count <= 0:
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)
        print("INFO | User details updated successfully")
        return Response(data=medication_details, status=status.HTTP_200_OK)
    except Exception as e:
        print(f"ERROR | Unable to update user details into DB due to error: {str(e)}")
        data["errors"] = str(e)
        return Response(data=data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
def delete_medication_details(request, patient_id):
    """
    it will delete medication
    :param request: request object
    :patient_id: unique patient id
    :return: Dictionary consisting user details
    """
    # creating default response data
    data = {"data": [],
            "errors": ""}
    medication_collection = db_conn.get_collection(SCHEDULES_COLLECTION)
    try:
        print("INFO | Reading user details from request")
        medication_details = request.data
        filter_query = {
            'patient_id': patient_id
        }
        db_response = medication_collection.delete_one(filter_query)
        if db_response.deleted_count <= 0:
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)
        print("INFO | User deleted successfully")
        return Response(data=medication_details, status=status.HTTP_200_OK)
    except Exception as e:
        print(f"ERROR | Unable to delete user due to error: {str(e)}")
        data["errors"] = str(e)
        return Response(data=data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)