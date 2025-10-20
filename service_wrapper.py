import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import sys
import os
import logging
from pathlib import Path

# Setup logging
log_path = Path(__file__).parent / "service_logs"
log_path.mkdir(exist_ok=True)
logging.basicConfig(
    filename=str(log_path / "messaging_service.log"),
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class MessagingService(win32serviceutil.ServiceFramework):
    _svc_name_ = "MessagingService"
    _svc_display_name_ = "Encrypted Messaging Service"
    _svc_description_ = "Runs the encrypted messaging web application continuously"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)
        self.stop_requested = False

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.stop_event)
        self.stop_requested = True

    def SvcDoRun(self):
        try:
            logging.info('Service is starting...')
            servicemanager.LogMsg(
                servicemanager.EVENTLOG_INFORMATION_TYPE,
                servicemanager.PYS_SERVICE_STARTED,
                (self._svc_name_, '')
            )
            
            # Add the app directory to Python path
            app_dir = os.path.dirname(os.path.abspath(__file__))
            sys.path.append(app_dir)
            
            # Import and run the Flask app
            from server import app
            import threading
            
            def run_app():
                app.run(host='0.0.0.0', port=5000, use_reloader=False)
            
            # Start Flask in a separate thread
            thread = threading.Thread(target=run_app)
            thread.daemon = True
            thread.start()
            
            logging.info('Service started successfully')
            
            # Keep the service running until stop is requested
            while not self.stop_requested:
                win32event.WaitForSingleObject(self.stop_event, 1000)
                
        except Exception as e:
            logging.error(f'Service error: {str(e)}', exc_info=True)
            raise

if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(MessagingService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(MessagingService)