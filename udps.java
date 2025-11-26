import java.net.*;

class udpserver {
    public static void main(String[] args) throws Exception {
        DatagramSocket =DS ;
        socket=s;
        DatagramPacket =DP;
        packet=p;

        DS s = new DS(9876);
        byte[] buffer = new byte[1024];
        System.out.println("Server is Up");

        while (true) {
            
            DP p = new DP(buffer, buffer.length);
            s.receive(p);
            String msg = new String(p.getData(), 0, p.getLength());
            System.out.println("RECEIVED: " + msg);

            byte[] sendData = msg.toUpperCase().getBytes();
            s.send(new DatagramPacket(sendData, sendData.length, p.getAddress(), p.getPort()));
        }
    }
}
