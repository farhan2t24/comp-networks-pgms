import java.net.*;

class udpserver {
    public static void main(String[] args) throws Exception {
        DatagramSocket socket = new DatagramSocket(9876);
        byte[] buffer = new byte[1024];
        System.out.println("Server is Up");

        while (true) {
            DatagramPacket packet = new DatagramPacket(buffer, buffer.length);
            socket.receive(packet);
            String msg = new String(packet.getData(), 0, packet.getLength());
            System.out.println("RECEIVED: " + msg);

            byte[] sendData = msg.toUpperCase().getBytes();
            socket.send(new DatagramPacket(sendData, sendData.length, packet.getAddress(), packet.getPort()));
        }
    }
}
