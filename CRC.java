import java.util.Scanner;

public class CRC {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        System.out.print("Enter message bits: ");
        String msg = sc.nextLine().trim();
        System.out.print("Enter generator: ");
        String gen = sc.nextLine().trim();

        int m = msg.length(), n = gen.length();
        int[] data = new int[m + n - 1], div = new int[n];

        for (int i = 0; i < m; i++) data[i] = msg.charAt(i) - '0';
        for (int i = 0; i < n; i++) div[i] = gen.charAt(i) - '0';

        // CRC Division
        for (int i = 0; i < m; i++)
            if (data[i] == 1)
                for (int j = 0; j < n; j++)
                    data[i + j] ^= div[j];

        // Append checksum to message
        StringBuilder full = new StringBuilder(msg);
        for (int i = m; i < data.length; i++)
            full.append(data[i]);

        System.out.println("The checksum code is: " + full);

        // Validation
        System.out.print("Enter checksum code: ");
        String recv = sc.nextLine().trim();
        System.out.print("Enter generator: ");
        String g2 = sc.nextLine().trim();

        int[] val = new int[recv.length()], d2 = new int[g2.length()];
        for (int i = 0; i < recv.length(); i++) val[i] = recv.charAt(i) - '0';
        for (int i = 0; i < g2.length(); i++) d2[i] = g2.charAt(i) - '0';

        for (int i = 0; i <= val.length - d2.length; i++)
            if (val[i] == 1)
                for (int j = 0; j < d2.length; j++)
                    val[i + j] ^= d2[j];

        boolean valid = true;
        for (int i = val.length - (d2.length - 1); i < val.length; i++)
            if (val[i] != 0) valid = false;

        if (valid)
            System.out.println("Data stream is valid");
        else
            System.out.println("Data stream is invalid");

        sc.close();
    }
}
