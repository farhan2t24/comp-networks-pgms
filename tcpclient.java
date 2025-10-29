import java.net.*;
import java.io.*;

public class tcpclient {
    public static void main(String[] args) throws Exception {
        Socket s = new Socket("127.0.0.1", 4000);
        BufferedReader user = new BufferedReader(new InputStreamReader(System.in));
        System.out.print("Enter file name: ");
        PrintWriter out = new PrintWriter(s.getOutputStream(), true);
        out.println(user.readLine());

        BufferedReader in = new BufferedReader(new InputStreamReader(s.getInputStream()));
        String line;
        while ((line = in.readLine()) != null) System.out.println(line);

        user.close(); in.close(); out.close(); s.close();
    }
}
