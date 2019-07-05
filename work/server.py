import socketserver
import sys

class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        print('클라이언트 접속: {0}'.format(self.client_address[0]))
        sock = self.request

        rbuff = sock.recv(1024) # 데이터를 수신하고 그 결과를 rbuff에 저장 bytes 단위
        receive = str(rbuff, encoding='utf-8')
        print('수신: {0}'.format(receive))

        sock.send(rbuff)
        print('송신: {0}'.format(receive))
        sock.close()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('{0} <Bind IP>'.format(sys.argv[0]))
        sys.exit()

    bindIP = sys.argv[1]
    bindPort = 5425

    server = socketserver.TCPServer((bindIP, bindPort), MyTCPHandler)

    print('서버 시작..')

    server.serve_forever()  # 클라이언트로부터 접속 요청을 받아들일 준비
