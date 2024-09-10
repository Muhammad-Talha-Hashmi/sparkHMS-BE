from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status
import traceback
from .models import *
from .serializers import *
from utils.responses import internal_server_error, bad_request, created, not_found, ok



# Create your views here.
class ManageKitchen(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            data = request.data
            serializer = KitchenSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                message = f"Kitchen created successfully"
                return created(message= message)
            else:
                return bad_request(message= serializer.errors)
        except Exception as err:
            print(traceback.format_exc())
            return internal_server_error(message= "Failed to create kitchen")

    def get(self, request, id=None):
        try:
            if id is not None:
                all_expenses = Kitchen.objects.filter(hotel=id).order_by('-created_datetime')
                paginator = PageNumberPagination()
                paginator.page_size = 10
                result_page = paginator.paginate_queryset(all_expenses, request)
                serializer = KitchenGetterSerializer(result_page, context={'request': request}, many=True)
                return paginator.get_paginated_response(serializer.data)
            else:
                return bad_request(message="Hotel id is missing")
        except Exception as err:
            print(traceback.format_exc())
            return Response({"message": "Failed to get kitchen expenses list"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request):
        try:
            data = request.data
            id = data.get('id', None)
            kitchenData = Kitchen.objects.filter(kitchen=id).get(id=id)
            serializer = KitchenSerializer(kitchenData, data=data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                message = f"Kitchen updated successfully"
                return ok(message="Successfully updated")
            else:
                return bad_request(message=serializer.errors)
        except Exception as err:
            print(traceback.format_exc())
            return internal_server_error(message= "Failed to update kitchen expense")

    def delete(self, request):
        try:
            id = request.GET.get('id', None)
            kitchen_intance = Kitchen.objects.filter(id=id).first()
            if not kitchen_intance:
                return bad_request(message= f"Kitchen not found with id: {id}")
            kitchen_intance.delete()
            return ok(message= "Successfully deleted the kitchen")
        except Exception as err:
            print(traceback.format_exc())
            return internal_server_error(message= "Failed to delete kitchen")

# Create your views here.
class ManageKitchenInventory(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            data = request.data
            serializer = KitchenInventorySerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                message = f"Kitchen created successfully"
                return created(message= message)
            else:
                return bad_request(message= serializer.errors)
        except Exception as err:
            print(traceback.format_exc())
            return internal_server_error(message= "Failed to create kitchen")

    def get(self, request, id=None):
        try:
            if id is not None:
                all_expenses = KitchenInventory.objects.order_by('-created_datetime')
                paginator = PageNumberPagination()
                paginator.page_size = 10
                result_page = paginator.paginate_queryset(all_expenses, request)
                serializer = KitchenInventoryGetterSerializer(result_page, context={'request': request}, many=True)
                return paginator.get_paginated_response(serializer.data)
            else:
                return bad_request(message="Kitchen id is missing")
        except Exception as err:
            print(traceback.format_exc())
            return Response({"message": "Failed to get kitchen expenses list"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request):
        try:
            data = request.data
            id = data.get('id', None)
            kitchen_inevtory = KitchenInventory.objects.get(id=id)
            serializer = KitchenInventorySerializer(kitchen_inevtory, data=data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                message = f"Kitchen updated successfully"
                return ok(message="Successfully updated")
            else:
                return bad_request(message=serializer.errors)
        except Exception as err:
            print(traceback.format_exc())
            return internal_server_error(message= "Failed to update kitchen expense")

    def delete(self, request):
        try:
            id = request.GET.get('id', None)
            kitchen_intance = KitchenInventory.objects.filter(id=id).first()
            if not kitchen_intance:
                return bad_request(message= f"Kitchen not found with id: {id}")
            kitchen_intance.delete()
            return ok(message= "Successfully deleted the kitchen")
        except Exception as err:
            print(traceback.format_exc())
            return internal_server_error(message= "Failed to delete kitchen")

class ManageKitchenRestock(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            data = request.data
            serializer = KitchenRestockSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                message = f"Restock Add successfully"
                return created(message= message)
            else:
                return bad_request(message= serializer.errors)
        except Exception as err:
            print(traceback.format_exc())
            return internal_server_error(message= "Failed to add restock")

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
                return created(message= message)
            else:
                return bad_request(message= serializer.errors)
        except Exception as err:
            print(traceback.format_exc())
            return internal_server_error(message= "Failed to add Expense")

    def get(self, request, id=None):
        try:
            if id is not None:
                all_expenses = KitchenExpense.objects.filter(kitchen=id).order_by('-date')
                paginator = PageNumberPagination()
                paginator.page_size = 10
                result_page = paginator.paginate_queryset(all_expenses, request)
                serializer = KitchenExpenseGetterSerializer(result_page, context={'request': request}, many=True)
                return paginator.get_paginated_response(serializer.data)
            else:
                return bad_request(message="Kitchen id is missing")
        except Exception as err:
            print(traceback.format_exc())
            return internal_server_error(message= "Failed to get Expense")

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
                return created(message= message)
            else:
                return bad_request(message=revenue_serializer.errors)
        except Exception as err:
            print(traceback.format_exc())
            return internal_server_error(message= "Failed to create kitchen revenue")

    def get(self, request, id=None):
        try:
            if id is not None:
                all_expenses = KitchenRevenue.objects.filter(kitchen=id).order_by('-date')
                paginator = PageNumberPagination()
                paginator.page_size = 10
                result_page = paginator.paginate_queryset(all_expenses, request)
                serializer = KitchenRevenueGetterSerializer(result_page, context={'request': request}, many=True)
                return paginator.get_paginated_response(serializer.data)
            else:
                return bad_request(message="Kitchen id is missing")
        except Exception as err:
            print(traceback.format_exc())
            return internal_server_error(message= "Failed to get kitchen revenue list")

    def patch(self, request):
        try:
            data = request.data
            revenue_id = data.get('id', None)
            revenue = KitchenRevenue.objects.get(id=revenue_id)
            serializer = KitchenRevenueSerializer(revenue, data=data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                message = f"Kitchen revenue updated successfully"
                return ok(message= message)
            else:
                return bad_request(message=serializer.errors)
        except Exception as err:
            print(traceback.format_exc())
            return internal_server_error(message= "Failed to update kitchen revenue")

    def delete(self, request):
        try:
            revenue_id = request.GET.get('id', None)
            revenue = KitchenRevenue.objects.filter(id=revenue_id).first()
            if not revenue:
                return bad_request(message= f"Kitchen revenue not found with id: {revenue_id}")
            revenue.delete()
            return ok(message= "Successfully deleted the kitchen revenue")
        except Exception as err:
            print(traceback.format_exc())
            return internal_server_error(message= "Failed to delete kitchen revenue")


class ManageKitchenFinancialStatement(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            data= request.data
            kitchen = data.get('kitchen')
            period_start_str = data.get('period_start')
            period_end_str = data.get('period_end')
            financial_statement_serializer = KitchenFinancialStatementSerializer(data=data)
            expenses = KitchenExpense.objects.filter(kitchen=kitchen, date__range=[period_start_str, period_end_str])
            revenues = KitchenRevenue.objects.filter(kitchen=kitchen, date__range=[period_start_str, period_end_str])
            total_expenses = sum(expense.amount for expense in expenses)
            total_revenues = sum(revenue.amount for revenue in revenues)
            net_profit = total_revenues - total_expenses
            data['total_expenses']=total_expenses
            data['total_revenues']=total_revenues
            data['net_profit']=net_profit
            if financial_statement_serializer.is_valid():
                financial_statement_serializer.save()
                message = f"Kitchen financial statement created successfully"
                return created(data=financial_statement_serializer.data, message=message)
            else:
                return bad_request(message=financial_statement_serializer.errors)
        except Exception as err:
            print(traceback.format_exc())
            return internal_server_error(message= "Failed to create kitchen financial statement")

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
