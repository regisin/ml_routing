def parse_trace_line(line):
    frame_index, frame_type, frame_time, frame_size = [x for x in line.rstrip("\n\r").split('\t') if x]
    return {
        'frame_index': int(frame_index),
        'frame_size': int(frame_size),
        'frame_type': frame_type,
        'frame_time': int(frame_time),
    }

def distance(a,b):
    return ( (a[0]-b[0])**2 + (a[1]-b[1])**2 + (a[2]-b[2])**2 )**0.5