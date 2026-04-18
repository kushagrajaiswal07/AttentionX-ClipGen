from moviepy import VideoFileClip
import os
import cv2

cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
face_cascade = cv2.CascadeClassifier(cascade_path)

def get_face_center(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    height, width, _ = frame.shape
    if len(faces) > 0:
        x, y, w, h = faces[0]
        return x + (w // 2)
    return width // 2

def generate_clips(video_path, highlights):
    clips = []
    video = VideoFileClip(video_path)
    duration = video.duration

    # Notice we are now unpacking 'hook' too!
    for i, (start, end, hook) in enumerate(highlights):
        start = max(0, start)
        end = min(duration, end)

        if start >= end:
            continue

        output_path = os.path.join("outputs", f"clip_{i}.mp4")
        clip = video.subclipped(start, end)

        print(f"Tracking face for clip {i}...")
        mid_time = clip.duration / 2
        frame = clip.get_frame(mid_time)
        face_x_center = get_face_center(frame)
        
        target_h = clip.h
        target_w = int(target_h * (9 / 16))
        
        x1 = face_x_center - (target_w // 2)
        x2 = face_x_center + (target_w // 2)
        
        if x1 < 0:
            x1 = 0
            x2 = target_w
        elif x2 > clip.w:
            x2 = clip.w
            x1 = clip.w - target_w
            
        vertical_clip = clip.cropped(x1=x1, y1=0, x2=x2, y2=target_h)

        # --- DYNAMIC CAPTION (HOOK) LOGIC ---
        print(f"Adding catchy hook: '{hook}'...")
        def overlay_hook(img):
            # Create a copy so we can edit the pixels
            frame_copy = img.copy()
            h, w, _ = frame_copy.shape
            
            # 1. Draw a high-contrast black box at the top
            cv2.rectangle(frame_copy, (0, 0), (w, 120), (0, 0, 0), -1)
            
            # 2. Setup the font 
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = max(1, w / 400) # Auto-scale font based on video width
            thickness = 3
            
            # 3. Calculate exact center alignment for the text
            text_size = cv2.getTextSize(hook, font, font_scale, thickness)[0]
            text_x = (w - text_size[0]) // 2
            text_y = 80
            
            # 4. Draw the text in bright TikTok Yellow (BGR color format for OpenCV: Cyan, Magenta, Yellow)
            # Wait, MoviePy uses RGB! So Yellow is (255, 255, 0)
            cv2.putText(frame_copy, hook, (text_x, text_y), font, font_scale, (255, 255, 0), thickness, cv2.LINE_AA)
            return frame_copy

        # Apply the OpenCV drawing function to every frame of the clip!
        vertical_clip = vertical_clip.image_transform(overlay_hook)
        # -------------------------------------

        vertical_clip.write_videofile(
            output_path,
            codec="libx264",
            audio_codec="aac",
            logger=None
        )

        clips.append(output_path)

    video.close()
    return clips