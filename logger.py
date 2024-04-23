import logging


def setup_logger():
    # Define Log to store the errors
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        filename="goldbar.log",
        filemode='a'
        )
    
    return logging.getLogger()
