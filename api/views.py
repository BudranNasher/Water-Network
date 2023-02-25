from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
import pandas as pd
from geopy import Point
from geopy.distance import distance

from .models import Valve, Tree
from .serializers import *


@api_view(['POST', 'GET', 'DELETE'])
@parser_classes([MultiPartParser, FormParser])
def valve_handle(request):

    #read valves data from excel
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
        valves = []
        for _, row in df.iterrows():
            valves.append(Valve(lat = row['Latitude'], long = row['Longitude'],))

        # Bulk create the Tree objects in the database
        Valve.objects.bulk_create(valves)

        return Response({'message': f'{len(valves)} trees were successfully added.'}, status=status.HTTP_201_CREATED)
    
    #read all the valves    
    elif request.method == 'GET':
        snippet = Valve.objects.all()
        serializer = ValveSerializer(snippet, many = True)
        return Response({'data':serializer.data})
    
    #delete all the valves
    elif request.method == 'DELETE':
        Valve.objects.all().delete()


@api_view(['POST', 'GET', 'PUT', 'DELETE'])
@parser_classes([MultiPartParser, FormParser])
def valve_details(request, pk = None):

    #upload a single valve data
    if request.method == "POST":
        serializer = ValveSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':'success'})
        else:
            return Response({'data':'failed to upload data'})
        
    #get the data of a single valve
    elif request.method == 'GET':
        snippet = Valve.objects.get(id = pk)
        serializer = ValveSerializer(snippet, many = False)
        return Response({'data':serializer.data})
    
    #update the data of a single valve
    elif request.method == 'PUT':
        snippet = Valve.objects.get(id = pk)
        serializer = ValveSerializer(snippet, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data})
        else:
            return Response({"error":serializer.errors})
    #soft delete a single valve (to avoid database conflicts)
    elif request.method == 'DELETE':
        snippet = Valve.objects.get(id = pk)
        snippet.soft_delete = True
        snippet.save()
        return Response({'data':'successfully deleted'})


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


#get the trees for each valve
@api_view(['GET'])
def show_assigned(request):
    snippet = Valve.objects.all()
    serializer = ValveSerializer_2(snippet, many = True)
    return Response({'data':serializer.data})

#get the trees of a valve
@api_view(['GET'])
def get_valve_trees(request, pk):
    snippet = Valve.objects.get(pk = pk)
    serializer = ValveSerializer_2(snippet, many = False)
    return Response({'data':serializer.data})