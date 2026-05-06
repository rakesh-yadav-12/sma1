import java.rmi.Naming;

public class AddClient {
    public static void main(String[] args) {
        try {
            AddInterface ai = (AddInterface) Naming.lookup("rmi://localhost/Add");

            int result = ai.sum(10, 2);

            System.out.println("The sum of 2 numbers is: " + result);
        } catch (Exception e) {
            System.out.println("Client Exception: " + e);
        }
    }
}
