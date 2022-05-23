from dataclasses import field
from rest_framework import serializers
from .models import Warehouse, Inventory, City

class WarehouseSerializer(serializers.ModelSerializer):
	class Meta:
		model = Warehouse
		fields ='__all__'

class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = '__all__'


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'