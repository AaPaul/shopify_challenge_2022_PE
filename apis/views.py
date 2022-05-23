import requests
from django.shortcuts import render

# Create your views here.
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import RestrictedError
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .serializers import InventorySerializer, WarehouseSerializer, CitySerializer

from .models import Inventory, Warehouse, City

# Create your views here.

@api_view(['GET'])
def apisOverview(request):
	api_urls = {
		'InventoryList':'/inventory-list',
		'Detail View':'/inventory-detail/<str:pk>/',
		'InventoryCreate':'/inventory-create',
		'InventoryUpdate':'/inventory-update/<str:pk>/',
		'InventoryDelete':'/inventory-delete/<str:pk>/',
		'WarehouseList':'/warehouse-list',
		'Detail View':'/warehouse-detail/<str:pk>/',
		'WarehouseCreate':'/warehouse-create',
		'WarehouseUpdate':'/warehouse-update/<str:pk>/',
		'WarehouseDelete':'/warehouse-delete/<str:pk>/',
		}

	return Response(api_urls)

# Get the list of inventories


@api_view(['GET'])
def inventoryList(request):
	try:
		inventorys = Inventory.objects.all().order_by('-id')
		url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid=cbc5f375163906d79a69b744feaa7b24&units=metric"
		serializer = InventorySerializer(inventorys, many=True)
		data = serializer.data
		for d in data:
			city_id = d['city']
			_city = City.objects.get(id=city_id)
			city_serializer = CitySerializer(_city, many=False)
			city_name = city_serializer.data['name']
			city_weather = requests.get(url.format(city_name)).json()
			d['city'] = city_name
			d['weather'] = {
				'main':city_weather['weather'][0]['main'],
				'Temperature/Celsius': city_weather['main']['temp'],
				'description':city_weather['weather'][0]['description']
			}
		status_code = status.HTTP_200_OK
		return Response(data=data, status=status_code)
	
	except ObjectDoesNotExist:
		status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
		resp = {
			'Message': "data does not exsited",
			'status': False
			}
		return Response(data=resp, status=status_code)

	except:
		status_code = status.HTTP_400_BAD_REQUEST
		resp = {
			'Message': "ERROR in retriving data",
			'status': False
			}
		return Response(data=resp, status=status_code)

# Show the detail information of the inventory with id=pk
@api_view(['GET'])
def inventoryDetail(request, pk):
	try:
		inventorys = Inventory.objects.get(id=pk)
		serializer = InventorySerializer(inventorys, many=False)
		url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid=cbc5f375163906d79a69b744feaa7b24&units=metric"
		d = serializer.data
		_city = City.objects.get(id=d['city'])
		city_serializer = CitySerializer(_city, many=False)
		city_name = city_serializer.data['name']
		city_weather = requests.get(url.format(city_name)).json()
		d['city'] = city_name
		d['weather'] = {
			'main':city_weather['weather'][0]['main'],
			'Temperature/Celsius': city_weather['main']['temp'],
			'description':city_weather['weather'][0]['description']
		}
		return Response(data=d, status=status.HTTP_200_OK)
	except ObjectDoesNotExist:
		status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
		resp = {
			'Message': "data does not exsited",
			'status': False
			}
		return Response(data=resp, status=status_code)
	except :
		status_code = status.HTTP_400_BAD_REQUEST
		resp = {
			'Message': "Error in retrieving data",
			'status': False
			}
		return Response(data=resp, status=status_code)

# Add a new inventory
@api_view(['POST'])
def inventoryCreate(request):
	"""
	Data: JSON
		{
			"name": "item name",
			"description": "information about the item" (could be null),
			"warehouse": "the id of the existed warehouse" 
			}

	Return: JSON
		{
			"message": message and status,
			"data": the inventory data you just created
			"status_code": status of the request
		}
	"""
	try:
		serializer = InventorySerializer(data=request.data)

		if serializer.is_valid():
			serializer.save()
			status_code = status.HTTP_200_OK

			resp = {
				'message': "Inventory created successfully",
				'data': serializer.data,
				'status': True}
		else:
			status_code = status.HTTP_400_BAD_REQUEST
			resp = {
				'message': "Inventory created failed",
				'status': False}
		return Response(data=resp, status=status_code)

	except:
		status_code = status.HTTP_400_BAD_REQUEST
		resp = {
			'message': "Inventory created failed",
			'status': False}
		return Response(data=resp, status=status_code)


# Edit the inventory with id=pk
@api_view(['GET', 'POST'])
def inventoryUpdate(request, pk):
	if request.method == "GET":
		try:
			inventory = Inventory.objects.get(id=pk)
			serializer = InventorySerializer(inventory, many=False)
			status_code = status.HTTP_200_OK
			return Response(data=serializer.data, status=status_code)

		except:
			status_code = status.HTTP_400_BAD_REQUEST
			resp = {
				'message':"Error in retriving record",
				'status':False
			}

			return Response(data=resp, status=status_code)

	else:
		try:
			inventory = Inventory.objects.get(id=pk)
			print(request.data)
			serializer = InventorySerializer(instance=inventory, data=request.data)

			if serializer.is_valid():
				serializer.save()
				status_code = status.HTTP_200_OK

				resp = {
					'message': "Inventory updated successfully",
					'Updated data': serializer.data,
					'status': True
				}
			else:
				status_code = status.HTTP_400_BAD_REQUEST
				resp = {
					'message': "Inventory updated failed",
					'status': False
				}
			return Response(data=resp, status=status_code)

		except ObjectDoesNotExist:
			status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
			resp = {
				'message': "Inventory instance does not existed",
				'status': False}
			return Response(data=resp, status=status_code)

		except:
			status_code = status.HTTP_400_BAD_REQUEST
			resp = {
				'message': "Inventory updated failed",
				'status': False}
			return Response(data=resp, status=status_code)

#Delete the inventory with id=pk
@api_view(['DELETE'])
def inventoryDelete(request, pk):
	try:
		inventory = Inventory.objects.get(id=pk)
		inventory.delete()

		status_code = status.HTTP_200_OK
		

		resp = {
			'message': "Inventory deleted succsesfully",
			'status': True}
		return Response(data=resp, status=status_code)


	except ObjectDoesNotExist:
		status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
		resp = {
			'message': "Inventory data does not existed",
			'status': False
		}

		return Response(data=resp, status=status_code)
	
	except:
		status_code = status.HTTP_400_BAD_REQUEST
		resp = {
			'message': "Error in the process of deleting",
			'status': False
		}

		return Response(data=resp, status=status_code)


# The list of all warehouses
@api_view(['GET'])
def warehouseList(request):
	try:
		warehouse = Warehouse.objects.all().order_by('-id')
		serializer = WarehouseSerializer(warehouse, many=True)
		status_code = status.HTTP_200_OK
		return Response(serializer.data, status=status_code)

	except ObjectDoesNotExist:
		status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
		resp = {
			'Message': "No data existed",
			'status': False
			}
		return Response(data=resp, status=status_code)

	except:
		status_code = status.HTTP_400_BAD_REQUEST
		resp = {
			'Message': "ERROR in retriving data",
			'status': False
			}
		return Response(data=resp, status=status_code)


# The infomation of the warehouse with id=pk
@api_view(['GET'])
def warehouseDetail(request, pk):
	try:
		warehouse = Warehouse.objects.get(id=pk)
		serializer = WarehouseSerializer(warehouse, many=False)
		return Response(serializer.data)
	
	except ObjectDoesNotExist:
		status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
		resp = {
			'Message': "Data does not existed",
			'status': False
			}
		return Response(data=resp, status=status_code)
	except :
		status_code = status.HTTP_400_BAD_REQUEST
		resp = {
			'Message': "ERROR in retriving data",
			'status': False
			}
		return Response(data=resp, status=status_code)

# Add a new warehouse
@api_view(['POST'])
def warehouseCreate(request):
	"""
		Data: JSON
			{
				"name": item name,
				"location": location of the warehouse,
				}

		Return: JSON
			{
				"message": message and status
				"data": the warehouse info which you just created
				"status_code": status of the request
			}
	"""
	try:
		serializer = WarehouseSerializer(data=request.data)

		if serializer.is_valid():
			serializer.save()
			status_code = status.HTTP_200_OK
			resp = {
				'message': "Warehouse created successfully",
				'data': serializer.data,
				'status': True}
		else:
			status_code = status.HTTP_400_BAD_REQUEST
			resp = {
				'message': "Warehouse created failed",
				'status': False}

		return Response(data=resp, status=status_code)

	except:
		status_code = status.HTTP_400_BAD_REQUEST
		resp = {
			'message': "Warehouse created failed",
			'status': False}
		return Response(data=resp, status=status_code)

# Edit the warehouse info with id=pk
@api_view(['GET', 'POST'])
def warehouseUpdate(request, pk):
	if request.method == "GET":
		try:
			warehouse = Warehouse.objects.get(id=pk)
			serializer = WarehouseSerializer(warehouse, many=False)
			status_code = status.HTTP_200_OK
			return Response(data=serializer.data, status=status_code)

		except ObjectDoesNotExist:
			status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
			resp = {
				'message':"No data existed",
				'status':False
			}

			return Response(data=resp, status=status_code)

		except:
			status_code = status.HTTP_400_BAD_REQUEST
			resp = {
				'message':"Error in retriving record",
				'status':False
			}

			return Response(data=resp, status=status_code)

	else:
		try:
			warehouse = Warehouse.objects.get(id=pk)
			serializer = WarehouseSerializer(instance=warehouse, data=request.data)

			if serializer.is_valid():
				serializer.save()
				status_code = status.HTTP_200_OK

				resp = {
					'message': "Warehouse updated successfully",
					'Updated data': serializer.data,
					'status': True}
			else:
				status_code = status.HTTP_400_BAD_REQUEST
				resp = {
					'message': "Warehouse updated failed",
					'status': False}
			return Response(data=resp, status=status_code)

		except ObjectDoesNotExist:
			status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
			resp = {
				'message': "Queried warehouse instance does not exsit",
				'status': False}
			return Response(data=resp, status=status_code)

		except:
			status_code = status.HTTP_400_BAD_REQUEST
			resp = {
				'message': "Warehouse created failed",
				'status': False}
			return Response(data=resp, status=status_code)

# Delete the warehouse with id=pk
@api_view(['DELETE'])
def warehouseDelete(request, pk):
	try:
		warehouse = Warehouse.objects.get(id=pk)
		warehouse.delete()

		status_code = status.HTTP_200_OK
		resp = {
			'message': "Warehouse deleted succsesfully",
			'status': True
		}
		return Response(data=resp, status=status_code)

	except RestrictedError:
		status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
		resp = {
			'message': "Instance of Warehouse deleted Faile as it is referenced through restricted foreign keys",
			'status': False
		}

		return Response(data=resp, status=status_code)
	except ObjectDoesNotExist:
		status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
		resp = {
			'message': "Warehouse data does not exist",
			'status': False
		}

		return Response(data=resp, status=status_code)
	except:
		status_code = status.HTTP_400_BAD_REQUEST
		resp = {
			'message': "Error in the process of deleting",
			'status': False
		}

		return Response(data=resp, status=status_code)

		