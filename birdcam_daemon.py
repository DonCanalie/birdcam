    #!/usr/bin/env python
    #
    # http://www.jejik.com/articles/2007/02/a_simple_unix_linux_daemon_in_python/
     
    import sys, time
    from birdcam_service import Birdcam_Service
     
    class Birdcam_Service(birdcam_service):
            def run(self):
                    while True:
                            time.sleep(1)
     
    if __name__ == "__main__":
            birdcam_service = Birdcam_Service('/var/run/birdcam.pid')
            if len(sys.argv) == 2:
                    if 'start' == sys.argv[1]:
                            birdcam_service.start()
                    elif 'stop' == sys.argv[1]:
                            birdcam_service.stop()
                    elif 'restart' == sys.argv[1]:
                            birdcam_service.restart()
                    else:
                            print "Unknown command"
                            sys.exit(2)
                    sys.exit(0)
            else:
                    print "usage: %s start|stop|restart" % sys.argv[0]
                    sys.exit(2)
