import os
import sys
from moviepy.editor import VideoFileClip

def get_file_size(file_path):
    """Get the size of a file in MB."""
    size_in_bytes = os.path.getsize(file_path)
    return size_in_bytes / (1024 * 1024)

def compress_video(input_path, output_path, target_resolution=None, target_bitrate=None):
    """Compress the video using ffmpeg."""
    try:
        clip = VideoFileClip(input_path)
        
        # Adjust resolution if specified
        if target_resolution:
            clip = clip.resize(height=target_resolution)
        
        # Adjust bitrate if specified
        if target_bitrate:
            clip.write_videofile(output_path, bitrate=target_bitrate, codec='libx264')
        else:
            clip.write_videofile(output_path, codec='libx264')
        
        clip.close()
        return True
    except Exception as e:
        print(f"Error during compression: {e}")
        return False

def main():
    print("Welcome to the Video Compression Tool!")
    
    # Prompt user for input video file path
    input_path = input("Please enter the path to the video file you want to compress: ")
    
    # Check if the file exists
    if not os.path.exists(input_path):
        print("Error: The specified file does not exist.")
        sys.exit(1)
    
    # Display original file size
    original_size = get_file_size(input_path)
    print(f"Original video size: {original_size:.2f} MB")
    
    # Prompt user for output directory and file name
    output_dir = input("Enter the output directory (leave blank for current directory): ")
    if not output_dir:
        output_dir = os.path.dirname(input_path)
    
    output_name = input("Enter the output file name (with extension, e.g., output.mp4): ")
    output_path = os.path.join(output_dir, output_name)
    
    # Prompt user for compression settings
    target_resolution = input("Enter target resolution (e.g., 720 for 720p, leave blank for no change): ")
    target_bitrate = input("Enter target bitrate (e.g., 1000k for 1000 kbps, leave blank for default): ")
    
    if target_resolution:
        target_resolution = int(target_resolution)
    if target_bitrate:
        target_bitrate = target_bitrate
    
    # Confirm settings with the user
    print("\nCompression Settings:")
    print(f"Output Path: {output_path}")
    print(f"Target Resolution: {target_resolution if target_resolution else 'No change'}")
    print(f"Target Bitrate: {target_bitrate if target_bitrate else 'Default'}")
    
    confirm = input("Do you want to proceed with these settings? (y/n): ")
    if confirm.lower() != 'y':
        print("Compression cancelled.")
        sys.exit(0)
    
    # Compress the video
    if compress_video(input_path, output_path, target_resolution, target_bitrate):
        # Display new file size
        new_size = get_file_size(output_path)
        print(f"Compression successful! New video size: {new_size:.2f} MB")
    else:
        print("Compression failed.")

if __name__ == "__main__":
    main()