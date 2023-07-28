import logging




def log_message(message):
	logging.basicConfig(filename='app.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
	logging.info(message)
	