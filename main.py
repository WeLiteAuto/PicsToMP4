import os
import logging
import cv2


# Setup basic configuration for logging
logging.basicConfig(filename='2mp4.log', filemode='a', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


  
def read_frames_in_files(directory: str, extension: str, frame_rate: int) -> None:

    videos = 0
    for root, dirs, files in os.walk(directory):
        files_processed = 0
        images = [img for img in files if img.endswith(extension)]
        images.sort()
        if len(images) == 0:
            continue
        
        output_video_file = root+".mp4"
        convert_images_to_video(root, images, frame_rate, output_video_file)
        videos += 1
        print(f"{output_video_file} is created")
    
    print(f"{videos} videos are created")



def convert_images_to_video(root: str, images: list, frame_rate: int, output_video_file: str) -> None:
    first_image_path = os.path.join(root, images[0])
    frame = cv2.imread(first_image_path)
    height, width, layers = frame.shape
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
      
    video = cv2.VideoWriter(output_video_file, fourcc, frame_rate, (width, height))
    for image in images:
        image_path = os.path.join(root, image)
        frame = cv2.imread(image_path)
        video.write(frame)  # Write the frame to the video

        # Release the video writer object
    video.release()
    print(f"Video saved as {output_video_file}")

def main() -> None:
    try:
        print("Welcome to the Pic2Mp4 Tool")
        directory: str = input("Please enter the directory path to process (Enter for Current Directory): ")
         # If the user did not enter anything, use the current directory
        if directory is None:
            raise TypeError("directory is None")
        if len(directory) == 0:
            directory = os.getcwd()

        if directory is None:
            raise TypeError("directory is None")
        if not os.path.isdir(directory):
            raise FileNotFoundError(f"directory {directory} is not a valid directory")

        extension = input("Please enter the pic format (Enter for jpg): ")  
        if extension is None:
           extension = "jpg"

        frame_rate = input("Please enter the frame rate (Enter for 24 pfs): ")
        if frame_rate is None:
           frame_rate = 24
        try:
            frame_rate = int(frame_rate)
        except ValueError as e:
            logging.error(f"Int format required: {str(e)}")
            frame_rate = 24

        read_frames_in_files(directory, extension, int(frame_rate))
    except TypeError as e:
        logging.error(f"Unhandled exception: {str(e)}")
    except UnicodeEncodeError as e:
        logging.error(f"Unable to encode directory: {str(e)}")


if __name__ == "__main__":
    main()