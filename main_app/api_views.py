import numpy as np
import face_recognition
from rest_framework.decorators import api_view
from django.http import JsonResponse
from .models import *
import datetime
import os
from django.db import transaction
from django.shortcuts import redirect, render, get_object_or_404

known_face_encodings = np.load("/home/cuong/Project2.1/known_face_encodings.npy")
known_face_ids = np.load("/home/cuong/Project2.1/known_face_names.npy")

# Create your views here.
@api_view(["POST"])
@transaction.atomic
def recognize_faces(request):
    if request.method == 'POST':
        frame = request.FILES.get('image')  # Retrieve the uploaded image
        pk = request.POST.get('clazz_id')  # Retrieve the selected class ID from the request
        clazz = get_object_or_404(Clazz, pk=pk)
        class_id = clazz.clazz_id
        all_students = clazz.students.all()
        date = datetime.date.today()  # Get the current date

        # Create new attendance instance or retrieve it.
        attendance, created = Attendance.objects.get_or_create(clazz=clazz, date=date)

        if created:
            attendance_records = [
                AttendanceRecord(student=std, attendance=attendance, status=False)
                for std in all_students
            ]
            AttendanceRecord.objects.bulk_create(attendance_records)

        if frame is not None:
            image = face_recognition.load_image_file(frame)

            # Find all the faces and face encodings in the image
            face_locations = face_recognition.face_locations(image)
            face_encodings = face_recognition.face_encodings(image, face_locations)

            student_results = []
            status_results = []


            # Get the label
            face_encode_load_path = os.path.join('class_encoded', class_id, 'known_face_encodings.npy')
            face_id_load_path = os.path.join('class_encoded', class_id, 'known_face_ids.npy')

            known_face_encodings = np.load(face_encode_load_path)
            known_face_ids = np.load(face_id_load_path)

            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                std_id = 'Unknown'

                # Find the best match
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    std_id = known_face_ids[best_match_index]

                # Mark attendance for the recognized student
                if std_id != 'Unknown':
                    student = Student.objects.get(student_id=std_id)
                    attendance_records = AttendanceRecord.objects.filter(student=student, attendance=attendance)
                    attendance_records.update(status=True)

            for student_attend in all_students:
                attend_result = AttendanceRecord.objects.get(student=student_attend, attendance=attendance)
                name = student_attend.__str__()
                status = attend_result.status
                student_results.append(name)
                status_results.append(status)

            # Prepare the response data
            response_data = {
                'face_locations': face_locations,
                'student_results': student_results,
                'status_results': status_results
            }

            # Return the response
            return JsonResponse(response_data)

        else:
            return JsonResponse({'error': 'No image provided'}, status=400)

    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

