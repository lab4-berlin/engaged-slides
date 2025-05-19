from app import create_app
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

application = create_app()

@application.errorhandler(500)
def handle_500_error(error):
    logger.error(f"Internal error: {error}")
    return "Internal Server Error", 500

@application.route('/health')
def health_check():
    return "OK", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    application.run(host="0.0.0.0", port=port)