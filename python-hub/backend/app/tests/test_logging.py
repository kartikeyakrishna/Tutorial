import os
import json

def test_log_file_exists(app):
    log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'logs')
    log_file = os.path.join(log_dir, 'app.log')
    assert os.path.exists(log_file)
    with open(log_file) as f:
        line = f.readline()
        assert line.strip() != ''
        log_entry = json.loads(line)
        assert 'levelname' in log_entry
        assert 'asctime' in log_entry 