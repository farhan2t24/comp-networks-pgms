import java.net.*; 
import java.io.*; 

class Udpclient {
    public static void main(String[] args) throws Exception {
        BufferedReader in = new BufferedReader(new InputStreamReader(System.in));
        DatagramSocket s = new DatagramSocket();
        InetAddress ip = InetAddress.getByName("localhost");

        System.out.print("Enter string to be converted to uppercase: ");
        byte[] send = in.readLine().getBytes();
        s.send(new DatagramPacket(send, send.length, ip, 9876));

        byte[] recv = new byte[1024];
        DatagramPacket p = new DatagramPacket(recv, recv.length);
        s.receive(p);

        System.out.println("FROM SERVER: " + new String(p.getData(), 0, p.getLength()));
        s.close();
    }
}
