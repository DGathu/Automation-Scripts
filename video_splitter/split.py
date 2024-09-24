import os
from moviepy.editor import VideoFileClip

def split_video(input_file, segment_length):
    # Load the video file
    try:
        video = VideoFileClip(input_file)
    except Exception as e:
        print(f"Error loading video file: {e}")
        return
    
    # Calculate total duration in minutes and number of segments
    total_duration = video.duration / 60
    num_segments = int(total_duration // segment_length) + (1 if total_duration % segment_length > 0 else 0)

    print(f"Total duration: {total_duration:.2f} minutes")
    print(f"Number of segments to be created: {num_segments}")

    # Split the video into segments
    for i in range(num_segments):
        start_time = i * segment_length * 60
        end_time = min((i + 1) * segment_length * 60, video.duration)

        # Define output file name
        output_file = f"{os.path.splitext(input_file)[0]}-segment-{i + 1}.mp4"

        # Create the subclip and write to file
        try:
            subclip = video.subclip(start_time, end_time)
            subclip.write_videofile(output_file, codec="libx264", audio_codec="aac")
            print(f"Segment {i + 1} saved as: {output_file}")
        except Exception as e:
            print(f"Error saving segment {i + 1}: {e}")
    
    # Close the video file
    video.close()

def main():
    # User input for the file path and the segment length
    input_file = input("Enter the input video file path: ")

    try:
        segment_length = float(input("Enter the desired segment length (in minutes): "))
        if segment_length <= 0:
            raise ValueError("Segment length must be greater than zero.")
    except ValueError as e:
        print(f"Invalid input for segment length: {e}")
        return

    split_video(input_file, segment_length)

if __name__ == "__main__":
    main()
    
