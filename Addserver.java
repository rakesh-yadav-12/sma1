import java.rmi.Naming;

public class AddServer {
    public static void main(String[] args) {
        try {
            Add obj = new Add();

            // Bind the remote object
            Naming.rebind("Add", obj);

            System.out.println("Server is connected and waiting for the client...");
        } catch (Exception e) {
            System.out.println("Server could not connect: " + e);
        }
    }
}
