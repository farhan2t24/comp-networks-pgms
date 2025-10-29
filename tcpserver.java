import java.net.*;
import java.io.*;

public class tcpserver {
    public static void main(String[] args) throws Exception {
        ServerSocket ss = new ServerSocket(4000);
        System.out.println("Server ready for connection...");
        Socket s = ss.accept();
        System.out.println("Client connected!");

        BufferedReader in = new BufferedReader(new InputStreamReader(s.getInputStream()));
        PrintWriter out = new PrintWriter(s.getOutputStream(), true);
        BufferedReader file = new BufferedReader(new FileReader(in.readLine()));

        String line;
        while ((line = file.readLine()) != null)out.println(line);

        file.close(); in.close(); out.close(); s.close(); ss.close();
    }
}
