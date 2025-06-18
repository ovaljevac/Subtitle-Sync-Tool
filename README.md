# Subtitle Sync Tool 🎬

A smart Python desktop application for synchronizing subtitle files that drift out of sync over time — and embedding them directly into the video.

This tool solves a common subtitle issue: the subtitle is correctly synced at the start of the video, but progressively becomes delayed or early as the video plays. To fix this, the app calculates a **scaling factor** that proportionally adjusts all subtitle timestamps and then embeds the fixed subtitle (softcoded) into a new `.mp4` file.

---

## 🧠 How It Works

Instead of shifting subtitles by a fixed delay, this tool:

- Detects the **duration of the video** using OpenCV.
- Calculates the correct **scaling factor** using reference data (e.g., "Ben 10" subtitles that were manually corrected).
- Applies the factor to stretch or compress the `.srt` timings.
- Generates a **new video file** with the corrected subtitles embedded (softcoded using FFmpeg).

> ✅ Works best when subtitles are in sync at the beginning but become gradually worse over time.

---

## 🚀 Features

- 📏 Automatically calculates scaling factor based on video duration  
- ✍️ Option to manually input a custom factor  
- 🧠 Uses reference-based logic for high accuracy  
- 💬 Softcodes fixed subtitles into a new `.mp4` file  
- 📁 Lets you choose output folder and filename  
- 💡 Easy-to-use GUI (built with Tkinter)  

---

## ⚙️ How to Use

1. Launch the app.
2. Choose a video file (`.mp4`).
3. Choose the subtitle file (`.srt`).
4. Click **📏 Recommend a scaling factor** or enter your own.
5. Enter the name for the **output video** (without `.mp4`).
6. Choose the **output folder**.
7. Click **➕ Add scaled subtitle (softcoded)** to generate the fixed video.

The application will:

- Scale the subtitle timestamps
- Create a temporary `.srt` file
- Embed it into the video using FFmpeg
- Save the new `.mp4` with selectable subtitles in the chosen folder

---

## 📦 Requirements

- Python 3.x
- FFmpeg installed and added to system PATH
- Required Python packages:
  ```bash
  pip install pysrt opencv-python chardet

**---

## 📂 Output

- A new `.mp4` file with **softcoded subtitles** is saved in your selected folder.
- Subtitles are not hardcoded — they can be toggled on/off in media players like VLC.

---

## 🧪 Background

The scaling factor is based on manually corrected subtitles from a sample video  
("Ben 10", duration 1323 seconds) with a known factor:
known_factor = 0.9619388311
reference_duration = 1323.0 seconds


To adapt the correction to your video, the following formula is used:
scaling_factor = known_factor * (your_video_duration / reference_duration)

This approach ensures consistent correction across different video lengths.

**

## 📄 License

MIT License — feel free to use, modify, and contribute.
