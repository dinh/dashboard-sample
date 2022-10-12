from apps import application

DEBUG = application.config['DEBUG']

application.logger.info('DEBUG            = ' + str(DEBUG))
application.logger.info('Page Compression = ' + 'FALSE' if DEBUG else 'TRUE')
application.logger.info('ASSETS_ROOT      = ' + application.config['ASSETS_ROOT'])

if __name__ == "__main__":
    application.run()
