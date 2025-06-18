import pysrt

# Load both subtitles
s1 = pysrt.open("Ben.10.S03E02.Midnight.Madness.1080p.WEB-DL.AAC2.0.H.264-SA89_track3_eng.srt")
s2 = pysrt.open("Ben.10.S03E02.Midnight.Madness.1080p.WEB-DL.AAC2.0.H.264-SA89_track3_eng-resync.srt")

# Take begin and end times (in milliseconds)
t1_orig = s1[0].start.ordinal
t2_orig = s1[-1].start.ordinal
t1_sync = s2[0].start.ordinal
t2_sync = s2[-1].start.ordinal

# Calculate factor of scaling
faktor = (t2_sync - t1_sync) / (t2_orig - t1_orig)
print(f"Factor of scaling: {faktor:.10f}")
