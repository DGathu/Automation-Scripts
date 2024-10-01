# Import necessary libraries
from moviepy.editor import VideoFileClip
import os

# Function to convert framerate
def convert_framerate(video_file, target_framerate):
    # Check if the video file exists
    if not os.path.exists(video_file):
        print(f"Error: The file '{video_file}' does not exist.")
        return
    
    # Check if the target framerate is a positive number
    if target_framerate <= 0:
        print("Error: The framerate must be a positive number.")
        return
    
    # Load the video file
    try:
        video_clip = VideoFileClip(video_file)
    except Exception as e:
        print(f"Error: Unable to load the video file. {e}")
        return
    
    # Set the new framerate
    video_clip_resampled = video_clip.set_fps(target_framerate)
    
    # Define the output file name
    output_file = f"{os.path.splitext(video_file)[0]}_fps_{target_framerate}.mp4"
    
    # Write the output video file
    try:
        video_clip_resampled.write_videofile(output_file, codec='libx264')
        print(f"Framerate conversion successful. Output saved as '{output_file}'.")
    except Exception as e:
        print(f"Error: Unable to write the output video file. {e}")

# Main script execution
if __name__ == "__main__":
    # Prompt for video file input
    video_file = input("Enter the path to the video file: ")
    
    # Prompt for desired framerate input
    try:
        target_framerate = float(input("Enter the desired framerate (fps): "))
    except ValueError:
        print("Error: The framerate must be a number.")
        exit()
    
    # Call the conversion function
    convert_framerate(video_file, target_framerate)