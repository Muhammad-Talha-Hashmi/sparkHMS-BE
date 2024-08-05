from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status
import traceback
from .models import *
from .serializers import *


# Create your views here.

class ManageKitchenExpense(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            data = request.data
            expense_serializer = KitchenExpenseSerializer(data=data)
            if expense_serializer.is_valid():
                expense_serializer.save()
                message = f"Kitchen expense created successfully"
                return Response({"message": message}, status=status.HTTP_201_CREATED)
            else:
                return Response({"errors": expense_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            print(traceback.format_exc())
            return Response({"message": "Failed to create kitchen expense"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):
        try:
            all_expenses = KitchenExpense.objects.order_by('-date')
            paginator = PageNumberPagination()
            paginator.page_size = 10
            result_page = paginator.paginate_queryset(all_expenses, request)
            serializer = KitchenExpenseSerializer(result_page, context={'request': request}, many=True)
            return paginator.get_paginated_response(serializer.data)
        except Exception as err:
            print(traceback.format_exc())
            return Response({"message": "Failed to get kitchen expenses list"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request):
        try:
            data = request.data
            expense_id = data.get('id', None)
            expense = KitchenExpense.objects.get(id=expense_id)
            serializer = KitchenExpenseSerializer(expense, data=data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                message = f"Kitchen expense updated successfully"
                return Response({"message": message}, status=status.HTTP_200_OK)
            else:
                return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            print(traceback.format_exc())
            return Response({"message": "Failed to update kitchen expense"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request):
        try:
            expense_id = request.GET.get('id', None)
            expense = KitchenExpense.objects.filter(id=expense_id).first()
            if not expense:
                return Response({"message": f"Kitchen expense not found with id: {expense_id}"},
                                status=status.HTTP_404_NOT_FOUND)
            expense.delete()
            return Response({"message": "Successfully deleted the kitchen expense"}, status=status.HTTP_200_OK)
        except Exception as err:
            print(traceback.format_exc())
            return Response({"message": "Failed to delete kitchen expense"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ManageKitchenRevenue(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            data = request.data
            revenue_serializer = KitchenRevenueSerializer(data=data)
            if revenue_serializer.is_valid():
                revenue_serializer.save()
                message = f"Kitchen revenue created successfully"
                return Response({"message": message}, status=status.HTTP_201_CREATED)
            else:
                return Response({"errors": revenue_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            print(traceback.format_exc())
            return Response({"message": "Failed to create kitchen revenue"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):
        try:
            all_revenues = KitchenRevenue.objects.order_by('-date')
            paginator = PageNumberPagination()
            paginator.page_size = 10
            result_page = paginator.paginate_queryset(all_revenues, request)
            serializer = KitchenRevenueSerializer(result_page, context={'request': request}, many=True)
            return paginator.get_paginated_response(serializer.data)
        except Exception as err:
            print(traceback.format_exc())
            return Response({"message": "Failed to get kitchen revenues list"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request):
        try:
            data = request.data
            revenue_id = data.get('id', None)
            revenue = KitchenRevenue.objects.get(id=revenue_id)
            serializer = KitchenRevenueSerializer(revenue, data=data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                message = f"Kitchen revenue updated successfully"
                return Response({"message": message}, status=status.HTTP_200_OK)
            else:
                return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            print(traceback.format_exc())
            return Response({"message": "Failed to update kitchen revenue"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request):
        try:
            revenue_id = request.GET.get('id', None)
            revenue = KitchenRevenue.objects.filter(id=revenue_id).first()
            if not revenue:
                return Response({"message": f"Kitchen revenue not found with id: {revenue_id}"},
                                status=status.HTTP_404_NOT_FOUND)
            revenue.delete()
            return Response({"message": "Successfully deleted the kitchen revenue"}, status=status.HTTP_200_OK)
        except Exception as err:
            print(traceback.format_exc())
            return Response({"message": "Failed to delete kitchen revenue"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ManageKitchenFinancialStatement(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            data = request.data
            financial_statement_serializer = KitchenFinancialStatementSerializer(data=data)
            if financial_statement_serializer.is_valid():
                financial_statement_serializer.save()
                message = f"Kitchen financial statement created successfully"
                return Response({"message": message}, status=status.HTTP_201_CREATED)
            else:
                return Response({"errors": financial_statement_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            print(traceback.format_exc())
            return Response({"message": "Failed to create kitchen financial statement"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):
        try:
            all_statements = KitchenFinancialStatement.objects.order_by('-period_start')
            paginator = PageNumberPagination()
            paginator.page_size = 10
            result_page = paginator.paginate_queryset(all_statements, request)
            serializer = KitchenFinancialStatementSerializer(result_page, context={'request': request}, many=True)
            return paginator.get_paginated_response(serializer.data)
        except Exception as err:
            print(traceback.format_exc())
            return Response({"message": "Failed to get kitchen financial statements list"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request):
        try:
            data = request.data
            statement_id = data.get('id', None)
            statement = KitchenFinancialStatement.objects.get(id=statement_id)
            serializer = KitchenFinancialStatementSerializer(statement, data=data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                message = f"Kitchen financial statement updated successfully"
                return Response({"message": message}, status=status.HTTP_200_OK)
            else:
                return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            print(traceback.format_exc())
            return Response({"message": "Failed to update kitchen financial statement"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request):
        try:
            statement_id = request.GET.get('id', None)
            statement = KitchenFinancialStatement.objects.filter(id=statement_id).first()
            if not statement:
                return Response({"message": f"Kitchen financial statement not found with id: {statement_id}"},
                                status=status.HTTP_404_NOT_FOUND)
            statement.delete()
            return Response({"message": "Successfully deleted the kitchen financial statement"},
                            status=status.HTTP_200_OK)
        except Exception as err:
            print(traceback.format_exc())
            return Response({"message": "Failed to delete kitchen financial statement"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
