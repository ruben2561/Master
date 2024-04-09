from collections import defaultdict
import csv
from datetime import datetime, timedelta
from PIL import Image
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt

from process import scale_list


def generate_data_from_image(path, max_value):    
    # Load the image
    img = Image.open(path).convert('L')  # Convert to grayscale
    width, height = img.size
     
    # Calculate the width of each section
    section_width = 2 #width // number_of_points
    
    # Initialize an empty list to store bar heights
    bar_heights = []
    
    # Iterate through each section horizontally
    for i in range(int(width/2)):
        # Define the bounding box for the current section
        left = i * section_width
        upper = 0
        right = (i + 1) * section_width
        lower = height
        
        # Crop the section from the image
        section = img.crop((left, upper, right, lower))
        
        img_cv = np.array(section)
        
        edges = cv.Canny(img_cv,20,220)
        
        white_pixels_heights = np.where(edges == 255)[0]

        if len(white_pixels_heights) > 0:
            avg_height = np.mean(white_pixels_heights)
        else:
            avg_height = 0
            
        # Map the pixel intensity to the range [min_value, max_value]
        value = ((height-avg_height) / height) * max_value
        
        # print(avg_height)
        # print(height)
        # print(max_value)
        # print(value)
            
        # plt.subplot(121),plt.imshow(section,cmap = 'gray')
        # plt.title('Original Image'), plt.xticks([]), plt.yticks([])
        # plt.subplot(122),plt.imshow(edges)
        # plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
        # plt.show()
            
        # Append the calculated data (date, value) to the list
        bar_heights.append(round(value,3))
    
    return bar_heights

def scale_values_to_average(values, target_average):    
    # Calculate the current average of the values
    current_average = sum(values)
    print(current_average)
    
    # Calculate the scaling factor required to adjust the values
    scaling_factor = target_average / current_average
    
    # Scale the values using the scaling factor
    scaled_values = [value * scaling_factor for value in values]
    
    return scaled_values

def combine_and_scale_data(combined_data, average_month_values):
    # Separate the combined data into separate lists for each month
    month_data = defaultdict(list)
    
    for value, date in combined_data:
        month = date.month
        month_data[month].append(value)

    # Scale the values for each month based on the average_month values
    scaled_data = []
    for month, values in month_data.items():
        target_average = average_month_values[month - 1]  # Adjust for 0-based indexing
        scaled_values = scale_values_to_average(values, target_average)
        scaled_data.extend(scaled_values)

    return scaled_data

# Example usage:
path_summer = 'imagespowerdata/foto1.png'
path_spring = 'imagespowerdata/foto2.png'
path_winter = 'imagespowerdata/foto3.png'
max_value = 0.8
average_months = [130, 115, 120, 120, 115, 100, 48, 105, 110, 120, 120, 130]
number_of_points = 168 # 24 * 7
start_date_str = '2023-01-01 00:00:00'
start_date = datetime.strptime(start_date_str, '%Y-%m-%d %H:%M:%S')
hour_increment = 1

data1 = generate_data_from_image(path_summer, max_value)
data2 = generate_data_from_image(path_spring, max_value)
data3 = generate_data_from_image(path_winter, max_value) 
    
new_data_summer = scale_list(data1, number_of_points)
new_data_spring = scale_list(data2, number_of_points)
new_data_winter = scale_list(data3, number_of_points)

whole_year = new_data_winter * 13 + new_data_spring * 13 + new_data_summer * 13 + new_data_spring * 13 + new_data_spring[-24:]

whole_year_corrected = whole_year[312:] + whole_year[:312]

# Generate dates for the whole year
dates = [start_date + timedelta(hours=i * hour_increment) for i in range(len(whole_year_corrected))]

# Combine dates and values into a single list
combined_data = [(value, date) for value, date in zip(whole_year_corrected, dates)]

combined_data_scaled = combine_and_scale_data(combined_data, average_months)

data = [(value, date) for value, date in zip(combined_data_scaled, dates)]


# Write the combined data to a CSV file
csv_filename = 'combined_data.csv'
with open(csv_filename, 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['Date', 'Value'])  # Write header
    csv_writer.writerows(data)

print(f"CSV file '{csv_filename}' has been created successfully.")

plt.figure(figsize=(8,1))
plt.plot(new_data_winter)

plt.show()