from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
import pandas as pd
from geopy import Point
from geopy.distance import distance

from .models import Valve, Tree
from .serializers import *

@api_view(['GET'])
def show_all(request):
    valve = Valve.objects.all()
    point = Tree.objects.all()

    valve_ser = ValveSerializer(valve, many = True)
    point_ser = TreeSerializer(point, many = True)
    return Response({'valves': valve_ser.data, 'points': point_ser.data})


@api_view(['POST', 'GET', 'DELETE'])
@parser_classes([MultiPartParser, FormParser])
def tree_handle(request):

    #read new trees from an excel file (Latitude, Longitude)
    if request.method == 'POST':
        file = request.FILES.get('file')
        if not file:
            return Response({'error': 'No file was submitted'}, status=status.HTTP_400_BAD_REQUEST)

        # Load the Excel file into a pandas DataFrame
        try:
            df = pd.read_excel(file, usecols=['Latitude', 'Longitude'], dtype={'Long': float, 'Lat': float})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Create a list of Tree objects from the DataFrame
        trees = []
        for _, row in df.iterrows():
            trees.append(Tree(lat=row['Latitude'], long=row['Longitude'],))

        # Bulk create the Tree objects in the database
        Tree.objects.bulk_create(trees)

        return Response({'message': f'{len(trees)} trees were successfully added.'}, status=status.HTTP_201_CREATED)
    
    #get all the trees
    if request.method == 'GET':
        trees = Tree.objects.all()
        serializer = TreeSerializer(trees, many = True)
        return Response({'data':serializer.data})

    #delete all tree records
    if request.method == 'Delete':
        Tree.objects.all().delete
        return Response({"data":"successfully deleted all the records"})

    return Response({"data":'success'})


@api_view(['GET'])
def calculate_coordinates(request):
    valves = Valve.objects.all()
    print(valves)
    for valve in valves:
        
        #main point
        center = Point(valve.lat, valve.long)

        #offset value
        radius_m = 50

        # Calculate the distance in meters of latitude and longitude
        lat_m = distance(center, (center.latitude + 0.00005, center.longitude)).m
        long_m = distance(center, (center.latitude, center.longitude + 0.00005)).m

        # Calculate the offset in latitude and longitude for the given radius
        lat_offset = radius_m / lat_m
        long_offset = radius_m / long_m

        # Calculate the coordinates of the square area
        lat_offset = radius_m / lat_m
        long_offset = radius_m / long_m

        #define the offests for the long/lat
        max_lat = center.latitude + lat_offset
        min_lat = center.latitude - lat_offset
        max_long = center.longitude + long_offset
        min_long = center.longitude - long_offset

        #trees with no valve assigned
        no_distance_trees = Tree.objects.filter(lat__range = (min_lat, max_lat), long__range = (min_long, max_long), distance__isnull = True)
        for tree in no_distance_trees:
            tree_coor = Point(tree.lat, tree.long)
            tree.valve = valve
            tree.distance = distance(center, tree_coor).m
            print(tree.distance)
            tree.save()
            
        #trees with a distance to a valve assigned
        with_distance_trees = Tree.objects.filter(lat__range = (min_lat, max_lat), long__range = (min_long, max_long), distance__isnull = False)
        for tree in with_distance_trees:
            tree_coor = Point(tree.lat, tree.long)
            new_distance = distance(center, tree_coor).m
            if(new_distance < tree.distance):
                tree.distance = new_distance
                tree.valve = valve
                tree.save()

        return Response({"data":"assigning completed"})

@api_view(['GET'])
def get_valve_trees(request, pk):
    valve = Valve.objects.get(pk = pk)
    trees = Tree.objects.filter(valve = valve)
    serializer = TreeSerializer(trees, many = True)
    return Response({'data':serializer.data})