
import tkinter as tk, os, threading, subprocess, pysrt, chardet, tempfile
from tkinter import filedialog, messagebox, ttk
import cv2

class SmartSoftSubtitleScaler:
    def __init__(self, root):
        root.title("🎬 Smart subtitle adder with scaling")
        root.geometry("520x580")
        root.resizable(False, False)

        # VIDEO
        tk.Label(root, text="🎥 Choose a video (.mp4):").pack(pady=(15, 3))
        tk.Button(root, text="Choose a video", command=self.pick_video).pack()
        self.lbl_video = tk.Label(root, fg="gray"); self.lbl_video.pack()
        self.video = ""

        # SRT
        tk.Label(root, text="📄 Choose a .srt file:").pack(pady=(10, 3))
        tk.Button(root, text="Choose a subtitle", command=self.pick_srt).pack()
        self.lbl_srt = tk.Label(root, fg="gray"); self.lbl_srt.pack()
        self.srt = ""

        # Predlog faktora
        self.btn_calc = tk.Button(root, text="📏 Recommend a scaling factor", command=self.auto_calc)
        self.btn_calc.pack(pady=(12, 3))
        self.lbl_calc = tk.Label(root, fg="blue"); self.lbl_calc.pack()

        # FAKTOR
        tk.Label(root, text="✏️ Custom factor (or keep recommended):").pack(pady=(8, 3))
        self.ent_factor = tk.Entry(root, width=15); self.ent_factor.insert(0, "0.9619388311"); self.ent_factor.pack()

        # IZLAZ
        tk.Label(root, text="💾 Modified video name (without .mp4):").pack(pady=(10, 3))
        self.ent_name = tk.Entry(root, width=30); self.ent_name.pack()

        tk.Button(root, text="Choose a folder to store the modified video", command=self.pick_folder).pack(pady=5)
        self.lbl_folder = tk.Label(root, fg="gray"); self.lbl_folder.pack()
        self.folder = ""

        # STATUS
        self.lbl_status = tk.Label(root, fg="blue"); self.lbl_status.pack(pady=10)
        self.bar = ttk.Progressbar(root, mode="indeterminate", length=300); self.bar.pack()

        tk.Button(root, text="➕ Add scaled subtitle (softcoded)", bg="green", fg="white",
                  font=("Arial",12,"bold"), command=lambda: threading.Thread(target=self.run).start()
                  ).pack(pady=20)

    def pick_video(self):
        self.video = filedialog.askopenfilename(filetypes=[("MP4 files", "*.mp4")])
        self.lbl_video.config(text=self.video)

    def pick_srt(self):
        self.srt = filedialog.askopenfilename(filetypes=[("SRT files", "*.srt")])
        self.lbl_srt.config(text=self.srt)

    def pick_folder(self):
        self.folder = filedialog.askdirectory()
        self.lbl_folder.config(text=self.folder)

    def auto_calc(self):
        if not self.video or not self.srt:
            messagebox.showerror("Error", "Choose a video and a subtitle before the calculation."); return
        try:
            video_duration = self.get_video_duration(self.video)
            srt_duration = self.get_srt_duration(self.srt)

            # Osnovni poznati faktor za video dužine 1323 sekunde (22:03)
            known_video_duration = 1323.0
            known_factor = 0.9619388311

            factor = round(known_factor * (video_duration / known_video_duration), 10)

            self.ent_factor.delete(0, tk.END)
            self.ent_factor.insert(0, str(factor))
            self.lbl_calc.config(text=f"📏 Recommended factor: {factor}")

        except Exception as e:
            self.lbl_calc.config(text="")
            messagebox.showerror("ERror", f"Not possible to calculate: {e}")

    def get_video_duration(self, path):
        cap = cv2.VideoCapture(path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        cap.release()
        return frame_count / fps if fps > 0 else 0

    def get_srt_duration(self, srt_path):
        enc = self.detect_encoding(srt_path)
        subs = pysrt.open(srt_path, encoding=enc)
        return subs[-1].end.ordinal / 1000.0

    def run(self):
        if not (self.video and self.srt and self.folder):
            messagebox.showerror("Error", "You have to choose a video, subtitle and folder"); return
        try: factor = float(self.ent_factor.get())
        except: messagebox.showerror("Error", "Factor must be a decimal number."); return

        name = self.ent_name.get().strip() or "Video_with_subtitle"
        output_path = os.path.join(self.folder, f"{name}.mp4")
        scaled_srt_path = tempfile.mktemp(suffix=".srt")

        self.scale_srt(self.srt, scaled_srt_path, factor)

        self.lbl_status.config(text="Adding subtitles…"); self.bar.start()
        cmd = ["ffmpeg", "-i", self.video, "-i", scaled_srt_path, "-c", "copy", "-c:s", "mov_text", output_path]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        self.bar.stop(); self.lbl_status.config(text="")

        os.unlink(scaled_srt_path)

        if result.returncode == 0:
            messagebox.showinfo("Success", f"✅ Video with scaled subtitles has been saved!:{output_path}")
        else:
            messagebox.showerror("Error", result.stderr[:1000])

    def scale_srt(self, src, dst, factor):
        enc = self.detect_encoding(src)
        subs = pysrt.open(src, encoding=enc)
        for sub in subs:
            sub.start.ordinal = int(sub.start.ordinal * factor)
            sub.end.ordinal   = int(sub.end.ordinal   * factor)
        subs.save(dst, encoding="utf-8")

    def detect_encoding(self, path):
        with open(path, 'rb') as f: raw = f.read()
        return chardet.detect(raw)['encoding'] or 'utf-8'

if __name__ == "__main__":
    root = tk.Tk()
    SmartSoftSubtitleScaler(root)
    root.mainloop()
