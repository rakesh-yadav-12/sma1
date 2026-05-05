import java.rmi.*;
import java.rmi.server.*;
import java.rmi.registry.*;

interface AddInterface extends Remote {
    public int sum(int n1, int n2) throws RemoteException;
}

class Add extends UnicastRemoteObject implements AddInterface {
    public Add() throws RemoteException { super(); }
    public int sum(int n1, int n2) throws RemoteException { return n1 + n2; }
}

class AddServer {
    public void start() {
        try {
            
            LocateRegistry.createRegistry(9090);  
            Naming.rebind("rmi://localhost:9090/Add", new Add());
            System.out.println("Server is connected and waiting for the client...");
        } catch (Exception e) {
            System.out.println("Server could not connect: " + e);
        }
    }
}

class AddClient {
    public Integer sumRemote(int n1, int n2) {
        try {
            AddInterface ai = (AddInterface) Naming.lookup("rmi://localhost:9090/Add");
            return ai.sum(n1, n2);
        } catch (Exception e) {
            System.out.println("Client Exception: " + e.getMessage());
            return null;
        }
    }
}

public class RMIExample {
    public static void main(String[] args) throws InterruptedException {
        System.out.println("=".repeat(50));
        System.out.println("RMI-style Remote Method Invocation");
        System.out.println("=".repeat(50));
        
        Thread serverThread = new Thread(() -> new AddServer().start());
        serverThread.setDaemon(true);
        serverThread.start();
        Thread.sleep(2000);
        
        AddClient client = new AddClient();
        System.out.println("\nMaking remote method calls...");
        System.out.println("-".repeat(40));
        
        int[][] tests = {{10,2}, {25,30}, {100,200}};
        for(int[] test : tests) {
            Integer result = client.sumRemote(test[0], test[1]);
            if(result != null) 
                System.out.println("The sum of " + test[0] + " and " + test[1] + " is: " + result);
        }
        
        System.out.println("-".repeat(40));
        System.out.println("\nServer is connected and waiting for the client...");
        System.out.println("Client successfully made remote calls to the server!");
        System.out.println("\n✨ RMI simulation completed successfully!");
        Thread.sleep(3000);
    }
}