def read_log_file(file_path):
    with open(file_path, 'r') as file:
        return file.readlines()

def extract_log_info(log_lines):
    log_info = []
    for line in log_lines:
        # Assuming log lines are formatted as "timestamp - log level - message"
        parts = line.split(' - ')
        if len(parts) == 3:
            timestamp, level, message = parts
            log_info.append({
                'timestamp': timestamp.strip(),
                'level': level.strip(),
                'message': message.strip()
            })
    return log_info

def parse_log_file(file_path):
    log_lines = read_log_file(file_path)
    return extract_log_info(log_lines)