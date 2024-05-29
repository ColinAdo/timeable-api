import pandas as pd
from rest_framework import status, permissions
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView

from units.models import Unit
from timetables.generate import generate_timetable

class UnitUploadView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [FileUploadParser]

    def post(self, request):
        file_obj = request.data['file']

        try:
            df = pd.read_excel(file_obj, engine='openpyxl')

            unit_code_list = df['unit_code'].tolist()
            unit_name_list = df['unit_name'].tolist()

            for unit_code, unit_name in zip(unit_code_list, unit_name_list):
                unit = Unit.objects.create(
                    code=unit_code,
                    name=unit_name
                )

                generate_timetable(unit, request.user)

        except pd.errors.EmptyDataError:
            return Response({"message": "Empty file"})
        except pd.errors.ParserError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": "Empty file, please upload a .xlsx file"})

        return Response(status=status.HTTP_201_CREATED)
