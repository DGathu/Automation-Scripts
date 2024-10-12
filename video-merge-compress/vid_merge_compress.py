import os
import cv2
import numpy as np
from tqdm import tqdm
import time

def merge_videos(video_directory, output_file, output_format, compression_level):
    """
    Merges videos from the specified directory into a single compressed output file.

    :param video_directory: Path to the directory containing the videos.
    :param output_file: Name of the output file.
    :param output_format: Desired output video format (e.g., 'mp4', 'avi').
    :param compression_level: Compression level ('low', 'medium', 'high').
    """
    # Define video codecs and compression levels
    codecs = {
        'mp4': cv2.VideoWriter_fourcc(*'mp4v'),
        'avi': cv2.VideoWriter_fourcc(*'XVID')
    }
    
    compression_factors = {
        'low': 1,
        'medium': 0.5,
        'high': 0.2
    }

    # Get the list of video files in the directory
    video_files = [f for f in os.listdir(video_directory) if f.endswith(('.mp4', '.avi', '.mov', '.mkv', '.AVI'))]
    
    if not video_files:
        print("No supported video files found in the directory.")
        return

    # Read the first video to get the frame size and FPS
    first_video_path = os.path.join(video_directory, video_files[0])
    cap = cv2.VideoCapture(first_video_path)
    if not cap.isOpened():
        print(f"Error: Could not open {first_video_path}")
        return
    
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    cap.release()

    # Create the output video writer
    out_path = f"{output_file}.{output_format}"
    out = cv2.VideoWriter(out_path, codecs[output_format], fps, (frame_width, frame_height))

    # Merge videos with progress bar
    total_frames = sum([int(cv2.VideoCapture(os.path.join(video_directory, f)).get(cv2.CAP_PROP_FRAME_COUNT)) for f in video_files])
    pbar = tqdm(total=total_frames, desc="Merging videos")
    
    for video_file in video_files:
        video_path = os.path.join(video_directory, video_file)
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(f"Error: Could not open {video_path}")
            continue
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            out.write(frame)
            pbar.update(1)
        
        cap.release()
    
    pbar.close()
    out.release()
    print(f"Merged video saved as {out_path}")

    # Compress the output video
    compress_video(out_path, compression_factors[compression_level])

def compress_video(video_path, compression_factor):
    """
    Compresses the video file using the specified compression factor.

    :param video_path: Path to the video file.
    :param compression_factor: Compression factor (0.2 for high, 0.5 for medium, 1 for low).
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Could not open {video_path}")
        return
    
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) * compression_factor)
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) * compression_factor)
    fps = cap.get(cv2.CAP_PROP_FPS)
    codec = int(cap.get(cv2.CAP_PROP_FOURCC))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.release()

    # Create a new video writer with the compressed dimensions
    out_path = f"{video_path.rsplit('.', 1)[0]}_compressed.{video_path.rsplit('.', 1)[1]}"
    out = cv2.VideoWriter(out_path, codec, fps, (frame_width, frame_height))

    cap = cv2.VideoCapture(video_path)
    pbar = tqdm(total=total_frames, desc="Compressing video")
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_resized = cv2.resize(frame, (frame_width, frame_height))
        out.write(frame_resized)
        pbar.update(1)
    
    pbar.close()
    cap.release()
    out.release()
    print(f"Compressed video saved as {out_path}")

def main():
    # Prompt for directory path
    video_directory = input("Enter the path to the directory containing the videos: ")
    
    # Validate the directory
    if not os.path.isdir(video_directory):
        print("Error: The specified path is not a valid directory.")
        return

    # Set the output parameters
    output_file = input("Enter the name of the output file (without extension): ")
    output_format = input("Enter the desired output video format (e.g., mp4, avi): ")
    compression_level = input("Enter the desired compression level (low, medium, high): ")

    # Start the merging process
    start_time = time.time()
    merge_videos(video_directory, output_file, output_format, compression_level)
    end_time = time.time()

    # Calculate elapsed time
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time:.2f} seconds")

if __name__ == "__main__":
    main()