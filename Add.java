import java.rmi.RemoteException;
import java.rmi.server.UnicastRemoteObject;

public class Add extends UnicastRemoteObject implements AddInterface {

    public Add() throws RemoteException {
        super();
    }

    public int sum(int n1, int n2) throws RemoteException {
        return n1 + n2;
    }
}
