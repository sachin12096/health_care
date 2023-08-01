import pymongo.errors
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from health_service.utils import DbConnection
from medication_scheduler.settings import PATIENTS_COLLECTION, USERS_COLLECTION
import uuid
db_conn = DbConnection()
db_conn.connect()

@api_view(['POST'])
def save_patient_details(request):
    """
        it will insert details about a patient into SB
        :param request: request object
        :return: Dictionary consisting patient details saved into DB
        """

    data={'data':[],
          "errors":""}

    patient_collection =db_conn.get_collection(PATIENTS_COLLECTION)
    users_collection = db_conn.get_collection(USERS_COLLECTION)
    try:
        print("INFO | Regarding deatils of patients from request")
        patient_details = request.data
        user_id = patient_details.get('user_id')
        filter_query = {
            'user_id': user_id
        }
        db_response = users_collection.find_one(filter_query)
        if not db_response:
            data['errors'] = "user not found enter valid user id"
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)



        patient_id = str(uuid.uuid4())
        patient_details['patient_id'] = patient_id
        db_response= patient_collection.insert_one(patient_details)
        id = str(db_response.inserted_id)
        patient_details['_id'] = id
        data['data'] = patient_details
        print('patient details inserted into db')
        return Response(data=data, status=status.HTTP_200_OK)
    except pymongo.errors.DuplicateKeyError:
        error= "Patient already exist in the DB, Please provide a unique patient details"
        print(f'error |{error}')
        data['errors']= error
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(f"ERROR | Unable to insert user details into DB due to error: {str(e)}")
        data["errors"] = str(e)
        return Response(data=data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_patient_details(request, patient_id):
    """
    it will fetch patient details
    :param request: request object
    : patient_id: unique patient id
    :return: Dictionary consisting user details
    """
    # creating default response data
    data = {"data": [],
            "errors": ""}
    patients_collection = db_conn.get_collection(PATIENTS_COLLECTION)
    users_collection = db_conn.get_collection(USERS_COLLECTION)
    try:
        print("INFO | Reading patient details from request")
        filter_query = {
            'patient_id': patient_id
        }
        db_response = patients_collection.find_one(filter_query)
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
def update_patient_details(request, patient_id):
    """
    it will update patient details
    :param request: request object
    :patient_id: unique patient id
    :return: Dictionary consisting user details
    """
    # creating default response data
    data = {"data": [],
            "errors": ""}
    patients_collection = db_conn.get_collection(PATIENTS_COLLECTION)
    try:
        print("INFO | Reading user details from request")
        patient_details = request.data
        filter_query = {
            'patient_id': patient_id
        }
        update_query = {"$set": patient_details}
        db_response = patients_collection.update_one(filter_query, update_query)
        if db_response.matched_count <= 0:
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)
        print("INFO | User details updated successfully")
        return Response(data=patient_details, status=status.HTTP_200_OK)
    except Exception as e:
        print(f"ERROR | Unable to update user details into DB due to error: {str(e)}")
        data["errors"] = str(e)
        return Response(data=data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
def delete_patient_details(request, patient_id):
    """
    it will delete patient
    :param request: request object
    :patient_id: unique patient id
    :return: Dictionary consisting user details
    """
    # creating default response data
    data = {"data": [],
            "errors": ""}
    patients_collection = db_conn.get_collection(PATIENTS_COLLECTION)
    try:
        print("INFO | Reading user details from request")
        patient_details = request.data
        filter_query = {
            'patient_id': patient_id
        }
        db_response = patients_collection.delete_one(filter_query)
        if db_response.deleted_count <= 0:
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)
        print("INFO | User deleted successfully")
        return Response(data=patient_details, status=status.HTTP_200_OK)
    except Exception as e:
        print(f"ERROR | Unable to delete user due to error: {str(e)}")
        data["errors"] = str(e)
        return Response(data=data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)