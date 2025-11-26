import java.net.*; 
import java.io.*; 

class Udpclient {
    public static void main(String[] args) throws Exception {
        BufferedReader =BR;
        InputStreamReader=ISR;
        DatagramSocket =DS;
        InetAddress=IA;
        DatagramPacket=DP;
         
        BR in = new BR(new ISR(System.in));
        DS s = new DS();
        IA ip = IA.getByName("localhost");

        System.out.print("Enter string to be converted to uppercase: ");
        
        byte[] send = in.readLine().getBytes();
        s.send(new DP(send, send.length, ip, 9876));
        byte[] recv = new byte[1024];
        DP p = new DP(recv, recv.length);
        s.receive(p);

        System.out.println("FROM SERVER: " + new String(p.getData(), 0, p.getLength()));
        s.close();
    }
}