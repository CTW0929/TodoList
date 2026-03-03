from app import app
import logging
import os

# 配置日志
if not os.path.exists('logs'):
    os.makedirs('logs')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
