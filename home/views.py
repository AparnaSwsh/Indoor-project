from django.shortcuts import render
from django.http import JsonResponse
import cv2
import numpy as np
import networkx as nx
from . Utils import insert_nodes, find_shortest_path, generate_directions,draw_path
from . models import *
from django.core.files.base import ContentFile
import base64
import os
from django.conf import settings



# Create your views here.
def home(request):
    return render(request, 'home.html')



def get_route(request):
    # Your existing code to generate image and directions
    image_path = r'static\assets\image.jpeg'  
    node_coordinates = [(38, 302),
                    (154, 206),
                    (194, 208),
                    (359, 204),
                    (389, 168),
                    (420, 207),
                    (585, 206),
                    (624, 208),
                    (764, 248),
                    (762, 309),
                    (732, 353),
                    (628, 354),
                    (596, 354),
                    (552, 334),
                    (506, 334),
                    (311, 331),
                    (247, 333),
                    (206, 352),
                    (165, 352),
                    (62, 352),
                    (92, 272),  # X1
                    (176, 273),  # X2
                    (275, 269),  # X3
                    (361, 269),  # X4
                    (393, 208),  # X5
                    (426, 279),  # X6
                    (520, 265),  # X7
                    (606, 277),
                    (696, 282)]  
    node_names = ['Library','Smart Class', 'Boys common room', 'Gents Toilet', 'Lift1', 'First aid room',
              'Lab House keeping','Kitchen', 'Restaurant', 'Classroom', 'Stairs near restaurant', 'Tutorial room',
              'Staff room', 'Stationary store', 'Class 205', 'Mini hall', 'Professors room', 'Pantry', 'Tutorial room1',
              'Stairs near Library', 'Near smart class', 'Near to smart class', 'Near Professors room', 'Near to the turning towards lift', 
              'Near lift', 'Near to lift', 'Near stationary ', 'Near kitchen','Near restaruant']

    img = insert_nodes(image_path, node_coordinates, node_names)

    # Your existing code to find shortest path and generate directions
    start_node_name = request.GET.get('start_node_name')
    end_node_name = request.GET.get('end_node_name')
    print(start_node_name)
    print(end_node_name)
    shortest_path_indices = find_shortest_path(node_coordinates, str(start_node_name), str(end_node_name))
    directions = generate_directions(shortest_path_indices, node_coordinates, node_names)

    # Draw the path on the image
    draw_path(img, shortest_path_indices, node_coordinates)

    # Serialize the image data
    _, img_encoded = cv2.imencode('.jpg', img)
    img_base64 = base64.b64encode(img_encoded).decode('utf-8')

    # Save the image data to the static files directory
    image_filename = f'navigation_image_{start_node_name}_{end_node_name}.jpg'  # Unique filename
    image_path = os.path.join(r"static", 'navigation_images', image_filename)
    with open(image_path, 'wb') as f:
        f.write(img_encoded.tobytes())

    # Print directions
    for direction in directions:
        print(direction)
    response_data = {
        "directions": directions,
        "image_filename": image_filename  # Include the image filename in the response
    }

    # Return JSON response
    return JsonResponse(response_data)



def preview(request):
    if request.method == "GET":
        start_node_name = request.GET.get('start_node_name')
        end_node_name = request.GET.get('end_node_name')
        floor = request.GET.get("floor")
    image_path = r'static\assets\image.jpg' if floor == "1" else r"static\assets\floor0.jpg" 
    node_coordinates = [(38, 302),
                    (154, 206),
                    (194, 208),
                    (359, 204),
                    (389, 168),
                    (420, 207),
                    (585, 206),
                    (624, 208),
                    (764, 248),
                    (762, 309),
                    (732, 353),
                    (628, 354),
                    (596, 354),
                    (552, 334),
                    (506, 334),
                    (311, 331),
                    (247, 333),
                    (206, 352),
                    (165, 352),
                    (62, 352),
                    (92, 272),  # X1
                    (176, 273),  # X2
                    (275, 269),  # X3
                    (361, 269),  # X4
                    (393, 208),  # X5
                    (426, 279),  # X6
                    (520, 265),  # X7
                    (606, 277),
                    (696, 282)]  
    node_names = ['Library','Smart Class', 'Boys common room', 'Gents Toilet', 'Lift1', 'First aid room',
              'Lab House keeping','Kitchen', 'Restaurant', 'Classroom', 'Stairs near restaurant', 'Tutorial room',
              'Staff room', 'Stationary store', 'Class 205', 'Mini hall', 'Professors room', 'Pantry', 'Tutorial room1',
              'Stairs near Library', 'Near smart class', 'Near to smart class', 'Near Professors room', 'Near to the turning towards lift', 
              'Near lift', 'Near to lift', 'Near stationary ', 'Near kitchen','Near restaruant']


# result if condition floor ==1 else  else_result

    node_info = {name: coordinates for name, coordinates in zip(node_names, node_coordinates) if name.startswith('N')}
    
    img = insert_nodes(image_path, node_coordinates, node_names)

    # Your existing code to find shortest path and generate directions
    
    print(start_node_name)
    print(end_node_name)
    shortest_path_indices = find_shortest_path(node_info, str(start_node_name).upper(), str(end_node_name).upper())
    directions = generate_directions(shortest_path_indices, node_coordinates, node_names)

    # Draw the path on the image
    draw_path(img, shortest_path_indices, node_coordinates)

    # Serialize the image data
    _, img_encoded = cv2.imencode('.jpg', img)
    img_base64 = base64.b64encode(img_encoded).decode('utf-8')

    # Save the image data to the static files directory
    image_filename = f'navigation_image_{start_node_name}_{end_node_name}.jpg'  # Unique filename
    image_path = os.path.join(r"static", 'navigation_images', image_filename)
    with open(image_path, 'wb') as f:
        f.write(img_encoded.tobytes())

    # Print directions
    for direction in directions:
        print(direction)
    response_data = {
        "directions": directions,
        "image_filename": image_filename  # Include the image filename in the response
    }

    return render(request, "preview.html", response_data)