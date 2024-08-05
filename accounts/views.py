from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status
import traceback
from .models import *
from .serializers import *

class ManageExpense(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            data = request.data
            expense_serializer = ExpenseSerializer(data=data)
            if expense_serializer.is_valid():
                expense_serializer.save()
                message = f"Expense created successfully"
                return Response({"message": message}, status=status.HTTP_201_CREATED)
            else:
                return Response({"errors": expense_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            print(traceback.format_exc())
            return Response({"message": "Failed to create expense"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):
        try:
            all_expenses = Expense.objects.order_by('-date')
            paginator = PageNumberPagination()
            paginator.page_size = 10
            result_page = paginator.paginate_queryset(all_expenses, request)
            serializer = ExpenseSerializer(result_page, context={'request': request}, many=True)
            return paginator.get_paginated_response(serializer.data)
        except Exception as err:
            print(traceback.format_exc())
            return Response({"message": "Failed to get expenses list"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request):
        try:
            data = request.data
            expense_id = data.get('id', None)
            expense = Expense.objects.get(id=expense_id)
            serializer = ExpenseSerializer(expense, data=data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                message = f"Expense updated successfully"
                return Response({"message": message}, status=status.HTTP_200_OK)
            else:
                return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            print(traceback.format_exc())
            return Response({"message": "Failed to update expense"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request):
        try:
            expense_id = request.GET.get('id', None)
            expense = Expense.objects.filter(id=expense_id).first()
            if not expense:
                return Response({"message": f"Expense not found with id: {expense_id}"}, status=status.HTTP_404_NOT_FOUND)
            expense.delete()
            return Response({"message": "Successfully deleted the expense"}, status=status.HTTP_200_OK)
        except Exception as err:
            print(traceback.format_exc())
            return Response({"message": "Failed to delete expense"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ManageRevenue(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            data = request.data
            revenue_serializer = RevenueSerializer(data=data)
            if revenue_serializer.is_valid():
                revenue_serializer.save()
                message = f"Revenue created successfully"
                return Response({"message": message}, status=status.HTTP_201_CREATED)
            else:
                return Response({"errors": revenue_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            print(traceback.format_exc())
            return Response({"message": "Failed to create revenue"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):
        try:
            all_revenues = Revenue.objects.order_by('-date')
            paginator = PageNumberPagination()
            paginator.page_size = 10
            result_page = paginator.paginate_queryset(all_revenues, request)
            serializer = RevenueSerializer(result_page, context={'request': request}, many=True)
            return paginator.get_paginated_response(serializer.data)
        except Exception as err:
            print(traceback.format_exc())
            return Response({"message": "Failed to get revenues list"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request):
        try:
            data = request.data
            revenue_id = data.get('id', None)
            revenue = Revenue.objects.get(id=revenue_id)
            serializer = RevenueSerializer(revenue, data=data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                message = f"Revenue updated successfully"
                return Response({"message": message}, status=status.HTTP_200_OK)
            else:
                return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            print(traceback.format_exc())
            return Response({"message": "Failed to update revenue"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request):
        try:
            revenue_id = request.GET.get('id', None)
            revenue = Revenue.objects.filter(id=revenue_id).first()
            if not revenue:
                return Response({"message": f"Revenue not found with id: {revenue_id}"}, status=status.HTTP_404_NOT_FOUND)
            revenue.delete()
            return Response({"message": "Successfully deleted the revenue"}, status=status.HTTP_200_OK)
        except Exception as err:
            print(traceback.format_exc())
            return Response({"message": "Failed to delete revenue"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class ManageHotelFinancialStatement(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            data = request.data
            financial_statement_serializer = HotelFinancialStatementSerializer(data=data)
            if financial_statement_serializer.is_valid():
                financial_statement_serializer.save()
                message = f"Hotel financial statement created successfully"
                return Response({"message": message}, status=status.HTTP_201_CREATED)
            else:
                return Response({"errors": financial_statement_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            print(traceback.format_exc())
            return Response({"message": "Failed to create hotel financial statement"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):
        try:
            all_statements = HotelFinancialStatement.objects.order_by('-period_start')
            paginator = PageNumberPagination()
            paginator.page_size = 10
            result_page = paginator.paginate_queryset(all_statements, request)
            serializer = HotelFinancialStatementSerializer(result_page, context={'request': request}, many=True)
            return paginator.get_paginated_response(serializer.data)
        except Exception as err:
            print(traceback.format_exc())
            return Response({"message": "Failed to get hotel financial statements list"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request):
        try:
            data = request.data
            statement_id = data.get('id', None)
            statement = HotelFinancialStatement.objects.get(id=statement_id)
            serializer = HotelFinancialStatementSerializer(statement, data=data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                message = f"Hotel financial statement updated successfully"
                return Response({"message": message}, status=status.HTTP_200_OK)
            else:
                return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            print(traceback.format_exc())
            return Response({"message": "Failed to update hotel financial statement"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request):
        try:
            statement_id = request.GET.get('id', None)
            statement = HotelFinancialStatement.objects.filter(id=statement_id).first()
            if not statement:
                return Response({"message": f"Hotel financial statement not found with id: {statement_id}"}, status=status.HTTP_404_NOT_FOUND)
            statement.delete()
            return Response({"message": "Successfully deleted the hotel financial statement"}, status=status.HTTP_200_OK)
        except Exception as err:
            print(traceback.format_exc())
            return Response({"message": "Failed to delete hotel financial statement"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

