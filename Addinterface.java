import java.rmi.Remote;
import java.rmi.RemoteException;

public interface AddInterface extends Remote {
    public int sum(int n1, int n2) throws RemoteException;
}
